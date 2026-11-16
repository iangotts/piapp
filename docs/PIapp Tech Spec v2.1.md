# **PIapp — Technical Specification v2.1**

|  |  |
| ----- | ----- |
| Product | PIapp — Performance Intelligence app |
| Version | 2.1 (Draft) — 22 Oct 2026 |
| Status | For review. ADRs marked OPEN need a decision before the relevant phase starts |
| Companion specs | PIapp-Business-Spec-v2*1.md (BR-xx, CAP-xx), PIapp-UI-Spec-v2*1.md |
| Architecture reference | AquaBrain: Vercel web, Railway API, Postgres (Supabase) with pgvector, AWS backup, native Swift iOS |

PIapp is a standalone build (own codebase, database, deployment) that reuses AquaBrain's patterns: stack, job-worker pipeline, enrichment cycle, MCP deployment shape, contradiction handling (ADR-001).

---

## **1\. Architecture overview**

           ┌──────────────── Clients ────────────────┐  
            │ Web app (Next.js)   iOS (SwiftUI, P3)    │  
            │ app. admin. experts. coach.  Android (P4)│  
            │ User's AI client ── MCP (P2)             │  
            └───────┬───────────────────────┬──────────┘  
                    │ HTTPS/JSON            │ MCP Streamable HTTP  
         ┌──────────▼──────────┐    ┌───────▼─────────────┐  
 Vercel ►│ Next.js SSR \+ BFF   │    │ pi-mcp (Supabase    │  
         └──────────┬──────────┘    │ Edge Fn, Deno+Hono) │  
                    │               └───────┬─────────────┘  
         ┌──────────▼───────────────────────▼──────────┐  
Railway ►│ api.\*  Node.js / TypeScript (Hono)           │  
         │ REST · Agent · Job worker · YouTube sync     │  
         │ Credits · Q\&A · Scheduling · Stripe (+Connect)│  
         └───┬───────────┬───────────┬──────────────────┘  
             │           │           │  
   ┌─────────▼───┐ ┌─────▼──────┐ ┌──▼───────────────┐ ┌──────────────┐  
   │ Postgres 16 │ │ LLM        │ │ Video host (ADR-18)│ │ Calls/calendar│  
   │ pgvector RLS│ │ providers  │ │ coach answers      │ │ (ADR-019/020) │  
   │ Auth Storage│ └────────────┘ └────────────────────┘ └──────────────┘  
   └─────┬───────┘  
         │ nightly dump \+ PITR  
   ┌─────▼───────────────┐  
AWS►│ S3 versioned, Object Lock │

   └─────────────────────┘

## **2\. Technology stack**

| Layer | Choice | Notes |
| ----- | ----- | ----- |
| Web | Next.js (App Router), TypeScript, Tailwind, shadcn/ui | Vercel. One app, role-routed: `app.` users, `admin.` PI Admin/Client Admin/Sponsor, `experts.` SMEs, `coach.`coaches |
| API | Node.js 20, TypeScript, Hono | Railway |
| Database | Postgres 16 on Supabase, pgvector, pg\_trgm | RLS per client; graph in Postgres (ADR-003) |
| Auth | Supabase Auth: email/password, magic link, invite, join code; SAML later | JWT carries `client_id`, `role` |
| Storage | Supabase Storage | Backstory attachments, transcript uploads, photos |
| Jobs | Postgres jobs table, Railway worker | `jobs_claim_next()` with `FOR UPDATE SKIP LOCKED` |
| AI | LLM via provider abstraction; embeddings `text-embedding-3-small` | ADR-006; no training on PIapp data |
| MCP | Supabase Edge Function | As AquaBrain brain-mcp |
| Payments | Stripe Billing \+ Checkout (top-ups) \+ Connect Express (payouts) | Phase 4 |
| Answer video | Hosted video service with in-browser/in-app recording and signed playback (ADR-018) | Phase 3 |
| Calls and scheduling | External call links plus calendar integration in Phase 4 (ADR-019, ADR-020) |  |
| Email/push | Transactional email provider; APNs/FCM | Weekly briefing, inbox |
| iOS | Native Swift / SwiftUI (Phase 3\) |  |
| Android | Kotlin / Jetpack Compose (Phase 4\) | ADR-011 |
| Backup | AWS S3, versioned, Object Lock | Plus Supabase PITR |
| Observability | Sentry, Railway logs, PostHog |  |
| DNS/CDN | Cloudflare | `app.` `admin.experts.` `coach.` → Vercel; `api.` → Railway; `mcp.` → Supabase |

## **3\. Multi-tenancy and security**

* Tenant \= client. Every tenant-owned row carries `client_id`.  
* Roles in `memberships.role`: `pi_admin` (global), `client_admin`, `user` (one client), `coach` (global, `coach_id`), `sme` (global, `sme_id`). Sponsor is a flag (`memberships.is_sponsor`) granting read of client aggregate views only (BR-42).  
* RLS is enforcement. Helpers: `auth.current_client_id()`, `auth.is_pi_admin()`, `auth.is_client_admin()`, `auth.current_sme_id()`, `auth.current_coach_id()`.  
* Row classes:  
  * **Global content** (videos, SMEs, categories, insights, skills, coach profiles): readable when published and visible to the client; writable by `pi_admin` (coaches and SMEs edit own profile through approval tables).  
  * **Client-scoped** (backstory, glossary, credit allocations, aggregates): that client's admins and `pi_admin`.  
  * **User-private** (notes, library, conversations, memories, twin, briefings): `user_id = auth.uid()`. No admin, Sponsor or coach policy.  
  * **Question-scoped** (questions, coach answers, sessions): readable by the asker and the one allocated coach, only through the `question_view` that exposes the fields allowed by BR-71. No policy reaches other tables from a coach.  
  * **Coach/SME private** (earnings, statements, availability): own `coach_id`/`sme_id` only.  
* No RLS path from `coach` or `sme` to any user-private or client-scoped table.  
* Service role key only on Railway and Edge Functions.  
* Endpoints re-check role in middleware. Audit log for admin actions (user changes, publish, backstory change, credit adjustment, payouts).

## **4\. Content ingestion (Phase 1\)**

### **4.1 YouTube sync**

1. PI Admin connects the channel once via Google OAuth; tokens encrypted (Vault).  
2. Nightly and on-demand: `playlistItems.list` then `videos.list` (duration, thumbnails, date, description).  
3. New videos land as `draft`; `short` if duration ≤ 180 s.  
4. Captions via owner OAuth (`captions.download`); fallback manual VTT/SRT/TXT upload or ASR. Stored with timestamps.  
5. Quota default 10,000 units/day; caption download 200 units each, so backfill in batches.

### **4.2 Publishing**

`draft → in_review → published | rejected`. Publish requires SME, ≥ 1 category, summary, consent recorded (BR-03).

### **4.3 Playback**

YouTube IFrame Player API on web; `youtube-ios-player-helper` on iOS. Player events drive watch analytics. No download or caching of library videos (BR-04). Coach answer videos use the ADR-018 host.

## **5\. Search (Phase 1\)**

1. Glossary expansion of client terms (BR-11).  
2. Lexical: Postgres full-text plus `pg_trgm`.  
3. Semantic: pgvector over summary and transcript chunk embeddings.  
4. Fusion: Reciprocal Rank Fusion; filters (category, SME, format, duration, saved).  
5. Transcript hits return a timestamp.

Target p95 \< 400 ms for 5,000 videos.

## **6\. Data model**

snake\_case, UUID v7 keys, `created_at`/`updated_at` on all tables.

### **6.1 Tenancy and identity**

| Table | Key columns |
| ----- | ----- |
| `clients` | id, name, slug, status, settings jsonb (public*share*enabled, sso, coach*enabled, memory*enabled, user*topup*enabled, join*code*hash, support*resources), plan*id |
| `profiles` | id, full*name, avatar*url, job\_title, team, timezone |
| `memberships` | id, user*id, client*id (null for pi*admin, coach, sme), role, sme*id, coach*id, is*sponsor, status, invited\_by |
| `invitations` | id, client*id, email, role, token*hash, expires*at, accepted*at |
| `audit_log` | id, actor*id, client*id, action, entity, entity\_id, diff jsonb |

### **6.2 Content (global)**

`smes` (id, name, title, employer, bio, photo*url, links, published, extraction*consent, consent*date); `videos` (id, youtube*id, title, summary, key*takeaways, sme*id, interviewer, format, duration*s, status, access, summary*embedding vector(1536), …); `video_client_access`; `video_transcripts`; `transcript_chunks`; `categories`; `video_categories`; `tags`; `video_tags` — as v1.2.

### **6.3 Client context**

`backstories` (id, client*id, version, status draft/awaiting*sponsor/published, sections jsonb, approved*by, approved*at, approval*evidence*path, published*by); `backstory_documents`; `glossary_terms`; `client_categories` — as v1.2. **New:** `client_profiles`(user*id, client*id, team, function, chosen*terms uuid\[\], onboarding*completed*at) for the user's client-profile step.

### **6.4 User activity (private)**

`library_entries`, `notes`, `shares`, `watch_events`, `search_events` — as v1.2. Aggregate counters are materialised views refreshed every 15 minutes. **New:** `inbox_items` (id, recipient*user*id, kind question*update/session/briefing/share/system, ref*type, ref*id, read*at); `briefings` (id, user*id, week*start, status, generated*at, sent*at, opened*at) and `briefing_items` (briefing*id, kind video/insight/question/prompt, ref\_id, position, reason).

### **6.5 Wisdom graph (Phase 2\)**

`insights`, `concepts`, `graph_edges`, `insight_categories` — as v1.2; traversal by recursive CTE, depth ≤ 2\.

### **6.6 Agent (Phase 2–3)**

`skills`, `digital_twins` (now for users; coaches use `coach_profiles`), `conversations`, `messages`, `citation_events`, `user_memories` (P3), `client_learnings` (P3), `usage_ledger`, `mcp_tokens` — as v1.2.

### **6.7 Coaches, Q\&A and one-on-one (new)**

| Table | Key columns |
| ----- | ----- |
| `coaches` | id, name, title, bio, photo*url, status (invited/active/paused/removed), tier, languages, timezone, code*of*conduct*accepted*at, sme*id nullable (if also an SME) |
| `coach_profiles` | coach*id, specialties uuid, style, experience, free*text — the coach's "digital twin"; used for matching |
| `coach_availability` | coach*id, rrule or slots jsonb, max*open*questions, max*sessions*per*week, paused\_until |
| `questions` | id, user*id, client*id, body, shared*context jsonb (fields the user allowed, BR-71), requested*coach*id nullable, mode (chosen/auto), status (draft/submitted/allocated/answered/declined/expired/refunded), safety*flag, credits*reserved, due*at |
| `question_allocations` | id, question*id, coach*id, match*score, reason jsonb, state (offered/accepted/declined/expired), offered*at, responded\_at |
| `answers` | id, question*id, coach*id, video*asset*id, duration*s, transcript, status (recording/published/withdrawn), published*at, rating, helpful |
| `video_assets` | id, owner*type, owner*id, provider*asset*id, status, duration*s, retention*until |
| `sessions` | id, user*id, coach*id, client*id, scheduled*start, scheduled*end, call*url, status (requested/confirmed/completed/cancelled/no*show), credits*reserved, recording*consent*user, recording*consent*coach, notes*private*to\_coach |
| `session_requests` | id, user*id, coach*id nullable, proposed\_slots jsonb, status |
| `question_view` / `session_view` | Views exposing only BR-71 fields to the allocated coach |

### **6.8 Credits and billing**

| Table | Key columns |
| ----- | ----- |
| `credit_accounts` | id, owner*type (client/user/coach/sme), owner*id, balance (derived), currency\_unit credits |
| `credit_ledger` | id, account*id, entry*type (allocation/topup/reserve/release/spend/refund/earn/adjustment/payout), amount (signed), ref*type, ref*id, counter*entry*id, reason, actor, at. **Append-only**; balances are derived; every spend has a matching earn or platform entry |
| `credit_prices` | id, service (question/session*30/session*60/agent*overage), coach*tier nullable, credits, effective\_from |
| `plans`, `subscriptions`, `invoices` | Stripe mirror; seats, status, period\_end |
| `credit_packs`, `topups` | pack definitions; Stripe Checkout sessions and results |

Reservation flow: `reserve` entry at request; `spend` on delivery; `release`/`refund` on decline, expiry or cancellation — all in one transaction with the status change.

### **6.9 SME and coach earnings (Phase 3 ledger, Phase 4 payouts)**

| Table / view | Notes |
| ----- | ----- |
| `attribution_units` (P2) | month, sme*id, video*id, insight*id, client*id, kind (video*minute/citation/citation*opened/citation\_helpful), units. Nightly from `watch_events` and `citation_events`; watch minutes capped once per user per video per day; excluded accounts removed (BR-56); multi-SME split by `video_smes.share` |
| `video_smes` (P3) | video*id, sme*id, share |
| `sme_metrics_monthly`(P3, view) | Aggregates for the SME dashboard (video activity, credits earned); breakdown rows below 5 users or 5 clients suppressed |
| `sme_topic_themes`, `sme_profile_changes`, `insight_flags` (P3) | As v1.2; flagging an insight withdraws it in the same transaction (BR-54) |
| `coach_metrics_monthly`(P3, view) | Own sessions, answers, ratings, credits earned |
| `earnings_rates` / `rev_share_settings`(P4) | Versioned; pool percentage, SME unit weights, coach share of credits spent, payout threshold |
| `agreements` (P4) | party*type (sme/coach), party*id, version, accepted*at, withdrawn*at |
| `statements`, `statement_lines`, `statement_disputes`, `payouts`, `payout_accounts` (P4) | Stripe Connect account ids only; bank and tax data stay with Stripe |

Monthly run: lock period → recompute SME units from raw events → anomaly checks (spikes, single user \> 20% of units) → draft statements (SME units to credits; coach credits from ledger) → PI Admin approval → publish → quarterly payout batch via Stripe Connect.

## **7\. Insight extraction pipeline (Phase 2\)**

One job per video on the worker, as AquaBrain's enrichment cycle. **Blocked in code until `smes.extraction_consent = granted`.**Steps: `segment` → `extract_insights` (typed, verbatim support span) → `link_concepts` → `classify` → `contradictions` → `embed` → `review_queue` (confidence \< 0.75 or a contradiction goes to PI Admin; else sampled batch approval) → `report`. Re-running is idempotent. Withdrawing consent sets that SME's insights to `withdrawn` within 7 days.

## **8\. Agent (Phase 2\)**

### **8.1 Request flow**

Auth → safety pre-check (positive: fixed safe response, no coaching) → skill routing → context assembly (fixed system policy; backstory and glossary as data; user twin; P3 memories and client learnings; recent turns) → glossary-expanded hybrid retrieval over approved insights with graph expansion (depth ≤ 2\) and rerank (top 8–12) → generation (SSE) → citation post-check (uncited claims removed or regenerated; low confidence → "library doesn't cover this" and suggest videos or **Ask a coach**) → persist message, citations and usage.

### **8.2 Contradictions, injection controls, memory, models**

As v1.2: both positions presented for `CONTRADICTS` pairs; backstory and other content in delimited data blocks; Phase 3 memory extraction and client learnings only with ≥ 5 distinct users and PI review; per-task model selection; \< \$0.05 average model cost per agent turn target.

## **9\. Weekly briefing (Phase 2\)**

Weekly job per active user (in the user's timezone): 1\. Inputs: user twin (role, goals, challenges), chosen client terms, recent watch and search history (used only inside the job, never exposed), published videos not yet seen, approved insights for the user's goals, client backstory current priorities. 2\. Select 3–5 items by relevance, with a "why this for you" line; from Phase 3, include "questions coaches answered recently on your topics" only if the answering user and coach consent. 3\. Compose with the same grounding rules as the agent (every claim cited to an insight or video; no free-form advice). 4\. Deliver in-app and by email (opt-out); store in `briefings`; clicks feed `video_opened` events. Cost cap per briefing is part of the usage ledger.

## **10\. Q\&A and one-on-one services (Phase 3–4)**

### **10.1 Q\&A flow**

1. User drafts a question; the UI shows exactly what the coach will see (BR-71) and the credit price (BR-63); safety pre-check (Q-22).  
2. Mode `chosen`: allocate to the selected coach if they have capacity. Mode `auto`: score eligible coaches (specialty-to-topic embedding similarity, availability and load, language, tier, past helpful rate) and offer to the top coach; offer expires (proposed 24 h), then next.  
3. Credits reserved on submit. Coach receives an inbox item and email/push.  
4. Coach accepts or declines; declines re-match; no accept before `due_at` refunds.  
5. Coach records the answer in the browser or app (recording to ADR-018 host, max length proposed 5 minutes), may add a transcript; publishes.  
6. Spend entry and coach earn entry posted; user notified; user rates the answer.

### **10.2 One-on-one flow (Phase 4\)**

Shortlist by the same matching, user picks a coach, proposes or chooses slots from `coach_availability` (calendar sync, ADR-020); credits reserved; coach confirms; call link generated or attached (ADR-019); reminders; completion confirmed by both or by the provider's join data; spend and earn entries posted; cancellation window refunds; no-shows follow a stated rule.

### **10.3 Privacy controls**

Coach reads only through `question_view`/`session_view`; no join to `notes`, `conversations`, `user_memories` or other questions. Coach answer videos use signed, expiring URLs, visible to the asker unless shared in-client. Calls are not recorded by default (BR-76).

## **11\. MCP server (Phase 2\)**

`pi-mcp` Edge Function, Streamable HTTP, per-user token. Tools: `ask_coach` (agent answer), `search_insights`, `search_videos`, `list_categories`, `list_skills` / `get_skill`, `get_backstory_summary`, `save_note`, `get_my_notes`. From Phase 3: `my_credit_balance`. Questions to human coaches are not exposed through MCP in v2.1 (spending credits from outside the app needs separate controls).

## **12\. API surface (REST `/v1`)**

| Area | Examples |
| ----- | ----- |
| Auth/onboarding | `POST /invitations`, `POST /invitations/:token/accept`, `POST /join` (client join code), `PUT /me/client-profile` |
| Admin – content | `POST /admin/youtube/sync`, `PATCH /admin/videos/:id`, `POST /admin/videos/:id/publish`, CRUD `/admin/smes`, `/admin/categories`, `/admin/coaches` |
| Admin – clients | CRUD `/admin/clients`, `/users`, `/backstory`, `/glossary`, `/credits/allocate` |
| Client Admin (P3) | `/client/users`, `/client/backstory`, `/client/glossary`, `/client/credits`, `/client/join-code` |
| Search, library, notes, shares, stats | As v1.2 |
| Dashboard | `GET /me/dashboard` (credits spent, conversations, questions, past and future sessions) |
| Agent / twin / memory | As v1.2 |
| Briefing | `GET /me/briefings`, `GET /me/briefings/:week`, `PATCH /me/briefing-settings` |
| Credits | `GET /me/credits`, `POST /me/credits/topup` (Stripe Checkout, P4), `GET /me/credits/ledger` |
| Q\&A (user) | `POST /questions`, `GET /questions`, `GET /questions/:id`, `POST /questions/:id/rate`, `GET /coaches` (browse and match preview) |
| Coach portal | `GET /coach/inbox`, `POST /coach/questions/:id/accept` / `decline`, `POST /coach/questions/:id/answer`(upload or recording token), `GET/PUT /coach/profile`, `PUT /coach/availability`, `GET /coach/sessions`, `GET /coach/earnings` |
| One-on-one (P4) | `POST /session-requests`, `GET /sessions`, `POST /sessions/:id/cancel`, `POST /coach/sessions/:id/confirm` / `complete` |
| SME portal (P3–4) | `GET /sme/overview`, `/sme/videos`, `/sme/insights`, `POST /sme/insights/:id/flag`, `PATCH /sme/profile`, `POST /sme/consent/withdraw`, `GET /sme/earnings`, `/sme/statements` |
| Admin – earnings (P4) | `/admin/earnings/settings`, `/admin/earnings/periods/:period/run`/ `approve`, `/admin/payouts/batch`, `/admin/disputes` |
| Analytics | `GET /analytics/platform`, `/analytics/client` (client\_admin, sponsor; k ≥ 5), `/analytics/client/report.pdf?month=` |
| Webhooks | Stripe (billing, Connect), video host (asset ready), calendar/call provider |

## **13\. Analytics**

Events: watch, search, save, favourite, share, note, conversation, message, feedback, skill used, briefing opened, question submitted/answered, session booked/completed, credit spend. No event contains note, conversation, twin or question text. PI Admin sees by client, video, category, SME, coach, credits (spent, earned, utilisation), unanswered and zero-result searches. Client Admin and Sponsor: adoption, watch time, categories, de-identified themes and Q\&A volumes, credit use; aggregate only, k ≥ 5\.

## **14\. Non-functional requirements**

| Area | Requirement |
| ----- | ----- |
| Availability | 99.5% monthly in pilots; 99.9% from Phase 4 |
| Performance | TTI \< 2.5 s on 4G; search p95 \< 400 ms; agent first token \< 2.5 s; coach answer upload resumable; video playback start \< 3 s |
| Scale (design point) | 50 clients, 25,000 users, 5,000 videos, 250,000 insights, 200 coaches, 10,000 coach answers per month |
| Security | OWASP ASVS L2; TLS 1.2+; signed URLs for answer video; secrets in vaults; SOC 2 readiness by Phase 4; PCI via Stripe only |
| Privacy | GDPR/CCPA export and delete per user; DPA; no model training on customer data; retention limits for answer video and any call recording |
| Accessibility | WCAG 2.2 AA; captions on coach answers (auto-generated transcript); Dynamic Type and VoiceOver |
| Backup/DR | Supabase PITR (7 days); nightly `pg_dump` to S3 (versioned, Object Lock 35 days, cross-region); quarterly restore test; RPO 24 h; RTO 8 h. Answer video assets restored from the video host's own redundancy |
| Environments | local, staging, production; separate Supabase projects |
| CI/CD | GitHub Actions: lint, typecheck, unit, RLS tests (pgTAP including coach and SME isolation), e2e (Playwright); Vercel previews |

## **15\. Mobile**

iOS (Phase 3): everything in the user app including dashboard, briefing, Q\&A (with video answer playback), inbox, credits; coach app functions (record answer, inbox) are a candidate for a later release, since coaches can use the web portal on a phone. Calls via the provider's app (Phase 4). Android in Phase 4\.

## **16\. Migration from Inspiring Excellence (optional)**

Export `module`, SME `user` records and `tag` via the Bubble Data API into `videos`, `smes`, `categories`. User library data is not migrated.

## **17\. Architecture Decision Records**

| ADR | Title | Status | Decision |
| ----- | ----- | ----- | ----- |
| 001 | Standalone build, AquaBrain patterns | CLOSED | Own codebase, DB, deploy |
| 002 | Postgres host | CLOSED (proposed) | Supabase; Railway for API and workers |
| 003 | Graph store | OPEN | Postgres node/edge tables with recursive CTEs; the brief says "graph database", confirm acceptable |
| 004 | Tenancy | CLOSED | Client \= tenant; RLS |
| 005 | Web framework | CLOSED (proposed) | Next.js on Vercel, role-routed hosts |
| 006 | LLM provider | OPEN | Abstraction; Anthropic Claude for generation; confirm direct vs OpenRouter |
| 007 | Transcript source | OPEN | Owner OAuth captions first; upload fallback; ASR |
| 008 | Privacy boundary | CLOSED | No admin, Sponsor or coach RLS read on conversations, notes, twin |
| 009 | Client memory de-identification | OPEN | k ≥ 5 plus PI review |
| 010 | MCP auth | CLOSED (proposed) | PAT in Phase 2; OAuth 2.1 later |
| 011 | Android approach | OPEN | Native Kotlin vs Kotlin Multiplatform |
| 012 | Conversation persistence timing | CLOSED | Threads Phase 2; memory Phase 3 |
| 013 | SSO | OPEN | SAML via Supabase SSO if a pilot requires it |
| 014 | Shorts feed | CLOSED | Format filter only |
| 015 | SME attribution and earnings | OPEN | Units (capped minutes plus weighted citations) converted to credits; pool or fixed rate per Q-20; ledger from Phase 2 |
| 016 | Payouts | CLOSED (proposed) | Stripe Connect Express for SMEs and coaches |
| 017 | Portals hosting | CLOSED (proposed) | Same Next.js app on `experts.` and `coach.` hosts; web only |
| **018** | **Coach answer video hosting** | **OPEN** | Hosted video service (for example Mux or Cloudflare Stream) with browser recording, signed playback, auto-captions and retention controls; decide before Phase 3\. Rejected: YouTube (not private), Supabase Storage (no adaptive streaming) |
| **019** | **Call provider** | **OPEN** | Phase 4: generate Zoom/Google Meet/Teams links via OAuth, or embed a call SDK (for example Daily). Default: external links first (lowest cost); embed only if recording or quality control is required (Q-24) |
| **020** | **Scheduling and calendar** | **OPEN** | Own availability model with Google/Microsoft calendar sync (free/busy); coach controls slots |
| **021** | **Credit ledger design** | CLOSED (proposed) | Append-only double-entry ledger in Postgres, derived balances, idempotent keys on every write, reserve/spend/refund in one transaction |
| **022** | **Coach matching** | OPEN | Rules plus embedding similarity first; learn from ratings after enough data |
| **023** | **Weekly briefing delivery** | CLOSED (proposed) | Worker job per timezone; email provider; in-app copy; unsubscribe respected |

## **18\. Phase build checklist**

* **Phase 1:** repo and CI; schema 6.1–6.4 with RLS tests; auth, invitations, join code; YouTube sync and publishing; categories and SMEs admin; client onboarding, users, backstory, glossary; user registration with twin and client profile; search; library, notes, shares, stats; basic dashboard; basic analytics and client report PDF; S3 backup; staging with the real catalogue.  
* **Phase 2:** consent flags; transcripts backfill; extraction pipeline; insight review; skills admin; agent with safety pre-check; conversations; twin; MCP; `citation_events`, `attribution_units`; usage ledger; **weekly briefing job**.  
* **Phase 3:** iOS; Client Admin console; Sponsor views; memory and client learnings; SME role, RLS and portal; **coach role, profiles, availability, inbox; Q\&A flow with ADR-018 video; credit ledger with client allocation by PI Admin; dashboard credit panels; coach and SME earnings views**; pgTAP isolation tests for coach and SME.  
* **Phase 4:** Stripe billing, seats, credit packs, top-up; client billing; **one-on-one scheduling, calendar and calls**; statements and Stripe Connect payouts; Android.

## **19\. Change log**

| Version | Date | Change |
| ----- | ----- | ----- |
| 2.1 | 22 Oct 2026 | Merged v1.2 with the 16 Oct revised spec: coach role and tables, Q\&A and video hosting, one-on-one, credits ledger, weekly briefing, dashboard APIs, ADR-018..023 |
| 1.2 | 27 Sep 2026 | SME role, attribution ledger, revenue share |
| 1.1 | 27 Sep 2026 | Sponsor flag |
| 1.0 | 27 Sep 2026 | First issue |

