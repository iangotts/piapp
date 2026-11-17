# **PIapp — Technical Specification v3.0**

|  |  |
| ----- | ----- |
| Product | PIapp — Performance Intelligence app |
| Owner | Ian Gotts, for Jez Cartwright / Performance Intelligence |
| Version | 3.0 (Draft), 16 Nov 2026 |
| Status | DRAFT for review. Re-baselined to Business Specification v5.0. ADRs marked OPEN need a decision before the phase that depends on them |
| Companion specs | PIapp Biz Spec v5.0 (BR-xx, CAP-xx, D-xx, G-xx) and PIapp UI Spec v3.0 |
| Supersedes | Technical Specification v2.1 (22 Oct 2026) |
| Architecture reference | AquaBrain patterns: Supabase Postgres with pgvector, Railway API and job worker, Vercel web, native Swift iOS (ADR-001) |

**How to read this version**

* **Business Spec v5.0 is the authority.** Where this spec and the Business Spec disagree, the Business Spec wins and this spec has a defect. Appendix C lists every place v2.1 disagreed with v5.0 and how it was resolved; section 19 lists the open decisions and gaps.
* **(BR-nn), (CAP-nn), (D-nn), (G-nn)** point into the Business Spec. **(T-nn)** points to a new technical gap in section 19.
* **\[P\]** marks a proposal that goes beyond what the Business Spec decides. It follows the Business Spec's convention: not yet confirmed.
* Appendix A traces every Business Spec capability, rule and decision to the section of this spec that realises it, with how it is verified.

**What changed from v2.1 in one paragraph.** The MVP is an iPhone app for users and coaches plus a PI Admin website (D-08). There is no user web app, no coach portal, no SME portal and no Android app in Phase 1. Credits, coach accounts, Q&A and one-on-one move into Phase 1 (CAP-25 to CAP-29). SMEs are not stored in PIapp and are not paid (BR-57), so their tables, portal and earnings are removed. A question never lapses (D-14), so v2.1's due dates, expiry, auto-allocation and refund-on-timeout are removed. Calls are held outside PIapp (D-21, BR-76), so there is no call provider. The agent, MCP server, weekly briefing, memory and insight graph are unscheduled (CAP-10, 12, 13, 17, 23) and are parked in Appendix B. Insight generation moves into Phase 1 (CAP-01).

---

## **1. Architecture overview**

```
        ┌───────────────────── Clients ─────────────────────┐
        │  iPhone app (SwiftUI)          PI Admin website    │
        │  users and coaches             (Next.js, admin.)   │
        │  one app, role set at sign-in  PI team only        │
        └───────────────┬───────────────────────┬───────────┘
                        │ HTTPS/JSON            │ HTTPS/JSON
              ┌─────────▼───────────────────────▼─────────┐
   Railway ►  │  api.*  Node.js / TypeScript (Hono)        │
              │  REST · Credits · Q&A · Sessions ·         │
              │  Notifications · Job worker                │
              └──┬───────────┬────────────┬───────────┬───┘
                 │           │            │           │
        ┌────────▼───┐ ┌─────▼──────┐ ┌───▼────────┐ ┌▼───────────────┐
        │ Postgres 16│ │ LLM        │ │ Answer-    │ │ Calendar       │
        │ Supabase   │ │ provider   │ │ video host │ │ Google / MS    │
        │ pgvector   │ │ (ADR-006)  │ │ (ADR-018)  │ │ (ADR-020)      │
        │ RLS, Auth, │ └────────────┘ └────────────┘ └────────────────┘
        │ Storage    │   YouTube (library video, metadata) · APNs · email
        └────────────┘
```

* **Two clients only.** The iPhone app serves users and coaches (D-08, CAP-15). The PI Admin website serves the PI team, who run PIapp for every client in the concierge model (Business 5.1). Client Admin and Sponsor have no sign-in in Phase 1 (G-14).
* **One API.** The iPhone app and the admin website call the same REST API. There is no backend-for-frontend layer.
* **Everything runs in the US** (D-15, section 3.6).
* **Not in this version:** Stripe (Phase 4), MCP server, coaching agent, user web app, coach and SME portals, Android. See Appendix B.

## **2. Technology stack**

| Layer | Choice | Notes | Phase |
| ----- | ----- | ----- | ----- |
| iPhone app | Native Swift, SwiftUI, iOS 17+ | One binary; the role (user or coach) decides the experience. Recording with AVFoundation. Push with APNs | 1 |
| PI Admin website | Next.js (App Router), TypeScript, Tailwind, shadcn/ui on Vercel | Host `admin.` only. PI team only until the Client Admin portal in Phase 3 | 1 |
| API | Node.js 20, TypeScript, Hono on Railway | `api.` host. Runs the worker too | 1 |
| Database | Postgres 16 on Supabase (US region), pgvector, pg\_trgm | RLS per client. No graph tables (ADR-003 deferred) | 1 |
| Auth | Supabase Auth: email and password, Google, password reset | Invite-code sign-up only (BR-21, BR-24, BR-25). SAML undecided (ADR-013, G-32) | 1 |
| Storage | Supabase Storage | Backstory documents, transcript uploads, headshots | 1 |
| Jobs | Postgres `jobs` table and Railway worker | `jobs_claim_next()` with `FOR UPDATE SKIP LOCKED`, as AquaBrain | 1 |
| AI | LLM through a provider abstraction; embeddings | ADR-006 OPEN. No training on PIapp data (BR-37). US processing | 1 |
| Library video | YouTube IFrame Player embedded; YouTube Data API for metadata | `youtube-ios-player-helper` on iOS. Never downloaded or cached (BR-04) | 1 |
| Answer video | Hosted video service with signed playback, captions and resumable upload (ADR-018) | PIapp-hosted, US region | 1 |
| Calendar | Google and Microsoft calendar APIs, free/busy and booking events only (ADR-020) | Coaches and users | 1 |
| Email and push | Transactional email provider; APNs | Invites, resets, notifications. Push is opt-in | 1 |
| Payments | Stripe Billing, Checkout, Connect Express | Billing and payouts | 4 |
| Backup | Supabase PITR plus nightly `pg_dump` to S3 (versioned, Object Lock) | Admin "Backup and restore" (CAP-32) is operational, see 12.4 | 1 |
| Observability | Sentry, Railway logs, PostHog (no content in events) | | 1 |
| DNS and CDN | Cloudflare | `admin.` to Vercel; `api.` to Railway | 1 |

## **3. Multi-tenancy, roles and security**

### **3.1 Tenancy and roles**

* **Tenant = client.** Every tenant-owned row carries `client_id`.
* **Roles** (`memberships.role`): `pi_admin` (global), `client_admin` (one client), `sponsor` (one client), `user` (one client), `coach` (global, `coach_id`). There is **no `sme` role**: SMEs are not stored in PIapp (BR-20, BR-57).
* **Sign-in by role in Phase 1.** `pi_admin` signs in to the website. `user` and `coach` sign in to the iPhone app. `client_admin` and `sponsor` records exist but **cannot sign in** until Phase 3: the Auth sign-in hook rejects them while `app_settings.client_signin_enabled` is false (Business 4.2, G-14). PI Admin performs their tasks on request.
* **One account has one role.** A person who is both a coach and a user needs two accounts \[P\].

### **3.2 Enforcement**

* **RLS is the enforcement.** Helpers: `auth.current_client_id()`, `auth.current_coach_id()`, `auth.is_pi_admin()`. Endpoints re-check the role in middleware.
* **Service-role key** only on Railway (API and worker).
* **PI Admin sign-in uses MFA** \[P\] (G-24).

### **3.3 Row classes**

| Class | Examples | Who can read |
| ----- | ----- | ----- |
| Global content | Published videos, approved insights, categories (global), app terminology, active coach profiles | Any signed-in user; every published video is visible to every client (BR-05 retired). Writable by `pi_admin` |
| Client-scoped | Backstory, client terminology, client prices, credit settings, credit pool, client categories | `pi_admin`; that client's users see their own client's prices, limit and terminology (D-11). Client Admin from Phase 3 |
| User-private | Notes, library, digital twin, saved items, AI validation conversations (`question_drafts`) | The user only. **No policy for `pi_admin`, sponsor, client admin or coach** (BR-40) |
| Question-scoped | Questions, question requests, answers | The asker; a coach only through `coach_question_view` for requests addressed to them (BR-71, BR-72). PI Admin only through `admin_open_content()` (3.4) |
| Session-scoped | Sessions | The user and the coach on it. PI Admin sees metadata only (Business 11) |
| Coach-private | Earnings, calendar connection, availability | The coach. PI Admin sees earnings (Business 11) |
| Operational | Audit log, notifications, settings, jobs | `pi_admin`; recipients see their own notifications |

* **No RLS path** exists from `coach` to any user-private or client-scoped table, or to another coach's requests, answers or earnings (BR-72, BR-74).

### **3.4 PI Admin access to question and answer content (BR-40, G-16)**

PI Admin has **no direct SELECT** on question text, flagged text or answer video. Support, safety and dispute work goes through one `SECURITY DEFINER` function, `admin_open_content(ref_type, ref_id, reason_code, reason_text)`. It writes an `audit_log` row **before** returning content, and it refuses without a reason code. Reason codes: `support`, `safety`, `dispute`. PI Admin dashboards read status, age and counts from views that expose no text.

### **3.5 Audit log**

Every administrator action is logged with actor, time, entity, old and new values: user and coach changes, coach status changes, publish and unpublish, backstory changes, credit allocations and adjustments (with reason, BR-64), changes to credit settings and coach percentages (BR-82), insight approvals and withdrawals, answer withdrawal, and every call to `admin_open_content()` (CAP-32).

### **3.6 Data residency and sub-processors (D-15, BR-37)**

US only. Supabase project, Railway service, the answer-video host's storage region, and AI processing must all be in the US. Model providers must not train on PIapp data (BR-37): a contractual term, plus zero-retention endpoints where the provider offers them.

| Sub-processor | Used for | Listed in Business 11? |
| ----- | ----- | ----- |
| YouTube | Library video | Yes |
| Answer-video host | Coach answer videos | Yes ("video-hosting provider") |
| AI model provider | Question validation, suggestions, matching, insight generation | Yes |
| Apple push notifications | Push | Yes |
| Google sign-in and calendar; Microsoft calendar | Sign-in, calendar free/busy and events | Yes ("Google sign-in and calendar providers"); Microsoft is not named (T-01) |
| Supabase, Railway, Vercel, Cloudflare, AWS S3 | Hosting, database, storage, backup | **No** (T-01) |
| Email provider, Sentry, PostHog | Invites, resets, errors, product analytics | **No** (T-01) |

## **4. Content (CAP-01, CAP-02, CAP-38)**

### **4.1 Loading a video**

The PI team edits the interview, exports its transcript, and puts the video on the PI YouTube channel (Business 5.2). PI Admin then loads it into PIapp:

1. **Import by YouTube URL or ID.** PIapp reads title, duration, thumbnails and date with the YouTube Data API (API key; no channel OAuth). The channel must be in `approved_channels` (BR-01).
2. **PI Admin adds** the interviewing coach, one or more categories, a summary, and the date of the SME's signed release (BR-57).
3. **PI Admin attaches the transcript** (VTT, SRT or TXT, with timestamps). Stored as a new `video_transcripts` version.
4. **PIapp generates insights** from the transcript (4.4). The video cannot be published until at least 3 are approved.

v2.1's nightly channel sync, owner-OAuth caption download and ASR fallback are removed: the PI team supplies the transcript (ADR-007 closed). The SME is never stored; the cited speaker is identified by role only (BR-07, Business 5.7).

Import warns, and does not block, when a video is outside 10 to 20 minutes or not landscape (BR-09) \[P\].

### **4.2 Publishing (BR-02, BR-03)**

`draft → in_review → published | rejected`. The publish action is refused unless all of these hold:

* an interviewing coach is linked;
* at least one category is set;
* a summary is present;
* at least 3 insights are `approved` (BR-03);
* `sme_release_date` is set (BR-57, Business 9).

A published video is visible to every client. There is no per-client video access table.

### **4.3 Playback (BR-04, BR-08)**

YouTube IFrame Player API in the admin preview and `youtube-ios-player-helper` in the iPhone app. Library videos are only ever played in the embedded player. Player events drive watched state (watched at 80% or more; position saved every 15 seconds). Sign-in is required for all library access (BR-08). Coach answer videos are different content and use the answer-video host (8.8).

### **4.4 Insight generation and approval (CAP-01, BR-06, BR-07, Business 5.7)**

Insight generation is in Phase 1. One job per `(video_id, transcript_version)` on the worker, idempotent.

1. **Guards.** The job refuses unless `videos.sme_release_date` is set **and** `app_settings.extraction_cleared` is true. The second flag is the legal gate in Business 9: written clearance from PI as channel owner and the takedown process in place, before launch.
2. **Generate.** The transcript is split into timestamped chunks. The model returns structured JSON as in Business 5.7: `text`, `start_seconds`, `end_seconds`, `excerpt`, `speaker_role`.
3. **Validate** before saving: `text` at most 300 characters; `0 ≤ start_seconds < end_seconds ≤ duration`; `excerpt` is a substring of the transcript; `speaker_role` is `interviewer` or `guest`. Failures are dropped and counted.
4. **Store** as `generated`, with `generated_by` (model, version, date) and `transcript_version`.
5. **PI Admin review.** Approve or reject each insight. Editing an insight's text keeps it `generated` until re-approved \[P\]. Only `approved` insights are used for search, matching or summaries (BR-06).
6. **Replacing a transcript** withdraws the video's existing insights with reason `transcript replaced` and generates new ones.
7. **SME takedown (BR-54, Business 9).** An SME's request to correct or remove an insight or video is recorded in `takedown_requests`. The affected insights are withdrawn **at once** until PI Admin reviews them; review target is 5 working days, removal within 7 days. The admin dashboard shows the countdown.
8. **Rejected and withdrawn insights are kept**, never deleted, so history is auditable.

Citation is derived, not stored: video title, interviewing coach, and a link to `https://youtu.be/{youtube_id}?t={start_seconds}`.

## **5. Search, terminology and matching (CAP-05, CAP-11, CAP-38)**

### **5.1 Effective terminology (BR-11, D-13)**

Terminology lines are `(term, explanation)`. A client line overrides an app line with the same normalised term. CSV upload adds new terms and updates lines whose term already exists; it does not replace the list \[P\] (G-30). Matching ignores case and surrounding spaces \[P\]. The effective list for a user is app terminology overridden by their client's terminology. It is used in search expansion, in the AI question conversation, and in the coach's client summary \[P\] (G-30).

### **5.2 Video search**

1. **Expand** the query with effective terminology.
2. **Lexical:** Postgres full-text plus `pg_trgm` over video title, summary, category names and **approved** insight text.
3. **Semantic:** pgvector over approved insights and video summaries.
4. **Fuse** with Reciprocal Rank Fusion; filter by category.
5. **Return** videos, each with the best-matching insight's timestamp deep link.

Raw transcript chunks are **not** searched in the MVP, because BR-06 allows only approved insights to drive search \[P\]. Target: p95 under 400 ms. The pilot library is on the order of 100 videos.

### **5.3 AI match on profile (CAP-05)**

The user's digital twin (role, goals) is embedded at read time and compared with approved-insight and video-summary embeddings. Result: a "For you" list. Nothing is stored beyond the twin itself.

### **5.4 Coach suggestions (BR-72, BR-77, G-20)**

Input: the user's confirmed question text. Candidates are coaches with `status = active`, availability `available` (BR-80) and fewer open requests than the cap \[P\]. Score: similarity between the question embedding and the coach profile embedding (specialties, bio, twin), plus category overlap. Return the **top 3**, each with a one-line reason (G-20). Language is English in the MVP (G-21). All coaches carry the same prices (G-29), so price is not a factor. There is no learning from ratings in Phase 1 (ratings are Phase 2, CAP-34).

Users can also **search** coaches by name or specialty. Unavailable coaches appear as unavailable and cannot be chosen (BR-80).

The same rules shortlist coaches for one-on-one (BR-77), then filter by calendar availability (9.2).

### **5.5 Skills (CAP-11) \[P\]**

A skill is a playbook the AI follows to refine and clarify questions, held in `skills` (name, instructions, version, status) and maintained by PI Admin. Skills are about question refinement only, not coaching (Business 4.1). Each skill version is testable from the admin console against sample questions.

## **6. Data model**

snake\_case, UUID v7 keys, `created_at` and `updated_at` on every table. The tables below realise the entities in Business 5.6; entity names are noted in brackets. Entities with no Phase 1 table are listed at the end.

### **6.1 Tenancy and identity**

| Table | Key columns |
| ----- | ----- |
| `clients` [CLIENT] | id, name, slug, status, sponsor\_user\_id, contract\_start, contract\_end (the term, G-02), user\_credit\_limit (starts from the app default, 12), support\_resources jsonb (the client's staff-support contacts shown by the safety flow), settings jsonb (`public_share_enabled`, default false, BR-23) |
| `profiles` | id (= auth user id), full\_name, first\_name, job\_title (shown to coaches as "role"), headshot\_url, bio, timezone |
| `memberships` [USER, COACH link] | id, user\_id, client\_id (null for `pi_admin` and `coach`), role, coach\_id, status (invited, active, deactivated), credit\_limit (starts at the client's limit; approved credit requests add to it, BR-66) |
| `coaches` [COACH] | id, name, email, bio, headshot\_url, status (invited, approved, active, suspended, removed), available (the availability switch, BR-80), coach\_share\_pct (default 20, BR-65), default\_meeting\_url \[P\], profile\_embedding vector, code\_of\_conduct\_accepted\_at |
| `invites` [INVITE] | id, role, client\_id (users only), email, code\_hash, status (open, used, expired, revoked), expires\_at, used\_at, created\_by |
| `app_settings` | key, value jsonb. Keys: `credit_value_cents` (5000), `default_user_credit_limit` (12), `default_credit_prices` (question 1; 20 min 3; 40 min 5; 60 min 8), `default_coach_share_pct` (20), `coach_open_request_cap` \[P\], `extraction_cleared`, `client_signin_enabled` (false), `pi_escalation_contact`. Changes are audited (BR-82) |
| `audit_log` | id, actor\_id, client\_id, action, entity, entity\_id, old jsonb, new jsonb, reason\_code, reason\_text |

### **6.2 Content (global)**

| Table | Key columns |
| ----- | ----- |
| `approved_channels` | youtube\_channel\_id, name (BR-01) |
| `videos` [VIDEO] | id, youtube\_id, channel\_id, coach\_id (interviewer), title, summary, duration\_s, thumbnail\_url, status (draft, in\_review, published, rejected), sme\_release\_date (BR-57), transcript\_version, summary\_embedding vector, published\_at, published\_by. **No SME column and no client-access table** |
| `video_transcripts` | id, video\_id, version, format, body, uploaded\_by |
| `categories` [CATEGORY] | id, name, parent\_id (two-level tree), client\_id (null = global) |
| `video_categories` [VIDEO\_CATEGORY] | video\_id, category\_id |
| `insights` [INSIGHT] | id, video\_id, text (≤ 300), start\_seconds, end\_seconds, excerpt, speaker\_role (interviewer, guest), status (generated, approved, rejected, withdrawn), transcript\_version, generated\_by, reviewed\_by, reviewed\_at, withdrawn\_reason, embedding vector |
| `insight_categories` [INSIGHT\_CATEGORY] | insight\_id, category\_id |
| `takedown_requests` | id, video\_id, insight\_id nullable, received\_at, review\_due\_at (5 working days), removal\_due\_at (7 days), status, handled\_by |
| `skills` [Skill] | id, name, instructions, version, status |

### **6.3 Client context**

| Table | Key columns |
| ----- | ----- |
| `client_contexts` [CLIENT\_CONTEXT] | id, client\_id, version, status (draft, awaiting\_sponsor, published), sections jsonb, approved\_by (Sponsor or delegate), approved\_at, approval\_evidence\_path (BR-13), summary (the short client context shown to coaches, BR-71) \[P\], published\_by |
| `backstory_documents` | id, client\_id, storage\_path, uploaded\_by |
| `terminology` [TERMINOLOGY] | id, client\_id (null = PI App term), term, normalised\_term, explanation. Unique on (client\_id, normalised\_term) |
| `client_prices` [CLIENT\_PRICE] | id, client\_id, service (`question`, `session_20`, `session_40`, `session_60`), credits, effective\_from |

### **6.4 User activity (private)**

| Table | Key columns |
| ----- | ----- |
| `digital_twins` [DIGITAL\_TWIN] | id, person\_type (user, coach), person\_id, role, goals jsonb, style, share\_fields jsonb (the fields shared with a coach, BR-71) |
| `video_users` [VIDEO\_USER] | user\_id, video\_id, type (saved, favourite, watched), position\_s, at |
| `video_notes` [VIDEO\_NOTE] | id, user\_id, video\_id, timestamp\_s, text |
| `shares` | id, from\_user\_id, to\_user\_id (same client only), ref\_type (video, answer), ref\_id, revoked\_at |
| `question_drafts` | id, user\_id, client\_id, messages jsonb, status (open, sent, abandoned), last\_activity\_at. **The AI validation conversation (BR-36).** Deleted when the question is sent or abandoned, see 8.2 |
| `watch_events`, `search_events` | Analytics events. `search_events` stores `client_id` and the query text but **no `user_id`**, so zero-result reports cannot identify a person \[P\] |

### **6.5 Q&A**

| Table | Key columns |
| ----- | ----- |
| `questions` [QUESTION] | id, user\_id, client\_id, text, status (open, complete, deleted; derived from its requests), parent\_question\_id (when the AI split a message, BR-67) |
| `question_requests` [QUESTION\_REQUEST] | id, question\_id, coach\_id, status (requested, answered, declined, deleted), credits (the price in force when requested, BR-63), shared\_context jsonb (what the user allowed, BR-71), decline\_reason, declined\_at, answered\_at. **No due date and no expiry** (D-14) |
| `answers` [ANSWER] | id, request\_id (unique), video\_asset\_id, duration\_s, status (ready, withdrawn), completed\_at |
| `video_assets` | id, owner\_type, owner\_id, provider, provider\_asset\_id, status (uploading, processing, ready, failed), duration\_s, orientation, captions\_status, region, retention\_until |
| `safety_flags` | id, user\_id, client\_id, flagged\_text (readable only through `admin_open_content()`), source (question, conversation), notified\_at, reviewed\_by, reviewed\_at |
| `problem_reports` | id, reporter\_user\_id, ref\_type (answer, session), ref\_id, text, status. The "report a problem" route (Business 10) |
| `coach_question_view` | A view exposing to the addressed coach only: question text, asker first name, role, the shared twin fields, the client context summary (BR-71) |

### **6.6 Sessions and calendars**

| Table | Key columns |
| ----- | ----- |
| `sessions` [SESSION] | id, user\_id, coach\_id, client\_id, minutes (20, 40, 60), credits (price in force when booked), start\_at, end\_at (UTC), user\_timezone, meeting\_url, status (requested, booked, complete, cancelled, no\_show), cancelled\_by, cancelled\_at, reschedule\_token\_hash, calendar\_event\_ids jsonb, note\_to\_coach, shared\_context jsonb. Exclusion constraint prevents overlapping sessions for one coach |
| `coach_availability` | coach\_id, weekly\_windows jsonb, buffer\_minutes, min\_notice\_hours, max\_open\_requests \[P\] |
| `calendar_connections` | id, owner\_type (user, coach), owner\_id, provider (google, microsoft), account\_email, tokens (encrypted in Vault), scope (free/busy and booking events only, Business 11) |

### **6.7 Credits**

| Table | Key columns |
| ----- | ----- |
| `credit_txn` [CREDIT\_TXN] | id, client\_id, owner\_type (client, user, coach), owner\_id, reason (`purchase`, `reserve`, `spend`, `refund`, `earning`, `adjustment`), available\_delta, reserved\_delta (numeric, signed), ref\_type, ref\_id, spend\_ref\_id (for an `earning`), share\_pct (on an `earning`), credit\_value\_cents (on a `spend` and an `earning`), reason\_text (required for `adjustment`, BR-64), actor\_id, idempotency\_key (unique), created\_at. **Append-only** |
| `credit_requests` [CREDIT\_APPROVAL] | id, user\_id, client\_id, credits\_requested, status (open, approved, declined), credits\_granted, decided\_by, decided\_at |
| `client_balance_alerts` | client\_id, threshold (10, 5, 0), sent\_at. Cleared when credits are allocated |
| views | `client_pool` (available credits per client), `user_credit_position` (limit, used, reserved, remaining), `coach_earnings` |

`purchase` is the Business Spec's name for credits entering a client's pool. In Phase 1 a `purchase` entry is created by PI Admin allocation against an invoiced contract (BR-61, BR-68), not by a payment.

### **6.8 Notifications and jobs**

| Table | Key columns |
| ----- | ----- |
| `notifications` [NOTIFICATION] | id, recipient\_type (user, coach, pi\_admin), recipient\_id, type, ref\_type, ref\_id, payload (no private text), sent\_push\_at, sent\_email\_at, read\_at |
| `device_tokens` | user\_id or coach\_id, apns\_token, platform |
| `jobs` | As AquaBrain: id, type, payload, status, run\_at, attempts, locked\_by |

### **6.9 Not created in Phase 1**

* **RATING** (CAP-34): Phase 2.
* **Wisdom graph** (`insight_link`, CAP-10), **agent** (`conversations`, `messages`, `citation_events`), **memory** (CAP-17) and **weekly briefing** (CAP-23): unscheduled. See Appendix B.
* **SME tables** (`smes`, `video_smes`, attribution, earnings): removed with the SME record (BR-57).
* **Billing and payout tables** (`plans`, `invoices`, `credit_packs`, `topups`, `statements`, `payouts`): Phase 4.

### **6.10 Status lifecycles**

These follow Business 4.3 exactly.

| Object | Transitions |
| ----- | ----- |
| Coach availability | `available ↔ unavailable`, switched by the coach; independent of status |
| Coach | `invited → approved → active → suspended / removed`. `active` requires a complete profile and the published interviews (BR-70, G-03) |
| Video | `draft → in_review → published / rejected` |
| Question request | `requested → answered / declined / deleted`. Never lapses |
| Session | `requested → booked → complete / cancelled / no_show` |
| Credits on a request | `reserved → spent / refunded` |

## **7. Credits (CAP-25; BR-60 to BR-69, BR-82, BR-83)**

### **7.1 Settings and who sees them (D-03, D-11, BR-63, BR-65, BR-82)**

Defaults live in `app_settings`. Each client carries its own limit and prices, copied from the defaults at creation. Each coach carries their own percentage, copied from the default.

| Setting | Default | Held in | Who can change | Who can see |
| ----- | ----- | ----- | ----- | ----- |
| Credit value | \$50 | `app_settings` | PI Admin | PI Admin |
| User credit limit | 12 | `clients.user_credit_limit` | PI Admin | The client in its profile (Phase 3); each user sees their own remaining credits |
| Credits per question, per 20, 40 and 60 minute session | 1, 3, 5, 8 | `client_prices` | PI Admin only | Client in its profile; users see the price before confirming |
| Coach share | 20% | `coaches.coach_share_pct` | PI Admin only | The coach, read only |

Every change is audited with who, when, old and new value (BR-82). A request is charged at the price in force **when it was made** and stores it (`question_requests.credits`, `sessions.credits`, BR-63). A change to a limit affects the **next** credit check only. A coach's percentage in force **at the moment credits are spent** applies (BR-65); it is stored on the `earning` entry (G-31).

### **7.2 The ledger (ADR-021)**

`credit_txn` is append-only: no UPDATE or DELETE is granted to any role. Balances are calculated, never stored (BR-64). Every entry has an `idempotency_key`, so a retried request cannot post twice. A correction is a new `adjustment` entry with a mandatory reason and the admin as actor.

Each entry carries two signed amounts, `available_delta` and `reserved_delta`. The Business Spec's single signed `credits` column maps to `available_delta`; `reserved_delta` lets a reserve become a spend in one append.

| Reason | Owner | `available_delta` | `reserved_delta` | Meaning |
| ----- | ----- | ----- | ----- | ----- |
| `purchase` | client | +n | 0 | PI Admin allocates credits to the client (no minimum, BR-61) |
| `reserve` | user | −n | +n | A request was made |
| `spend` | user | 0 | −n | The coach delivered (answer marked complete; session marked complete) |
| `earning` | coach | +n × share | 0 | Posted with the `spend`. Carries `share_pct` and `spend_ref_id` |
| `refund` | user | +n | −n | Declined, deleted while unanswered, or cancelled |
| `adjustment` | any | ±x | ±y | Administrator correction, with a reason |

**Derived positions** (SQL views):

* **Client pool available** = sum of `available_delta` over rows with that `client_id` whose owner is the client or one of its users. Coach `earning` rows are excluded.
* **User position:** `used` = −(sum of the user's `available_delta`); `reserved` = sum of the user's `reserved_delta`; `spent` = `used` − `reserved`; `remaining` = `credit_limit` − `used`. Counting only entries since `contract_start` makes the limit period the contract term \[P\] (G-02).
* **Coach earned** = sum of the coach's `available_delta`, in credits (BR-74). Conversion to dollars is Phase 4 (Q-12); each `spend` and `earning` stores `credit_value_cents` so later payouts use the value in force.

**Credits are fractional.** At the default 20% a question answered pays the coach 0.2 of a credit. The ledger uses `numeric(12,4)` (ADR-027, T-03).

### **7.3 Credit check (BR-69, D-03)**

Run on the server inside the same transaction that creates the request. The app also pre-checks to show affordability, but the server decides.

1. Take advisory locks on the client, then the user (fixed order, so no deadlock).
2. **Required** = for Q&A, the sum of the per-question price for every (question, coach) pair; for a session, the price of the chosen length.
3. Read the user's `remaining` and the client's `pool available`.
4. If `required` > `remaining`: reject with `user_limit_reached`. If `required` > `pool available`: reject with `client_pool_exhausted`. Both responses list what **would** be affordable, so the app can offer only affordable session lengths (BR-69) and a credit request.
5. Otherwise insert the request rows and one `reserve` entry per request, then commit.

A used-up client blocks every request that costs credits (BR-83).

### **7.4 Reserve, spend and refund (BR-62)**

| Event | Entries |
| ----- | ----- |
| User submits a question to a coach | `reserve` of the per-question price |
| Coach marks the answer complete | `spend`, plus `earning` for the coach at their percentage |
| Coach declines a request | `refund` (reason required; PI Admin notified, BR-72) |
| User deletes an unanswered question | `refund` for each open request (BR-81) |
| User deletes an **answered** question | No entry: credits stay spent (BR-81) |
| User books a session | `reserve` of the length's price |
| Coach marks a session complete | `spend`, plus `earning` |
| User or coach cancels a session, at any time including after a no-show | `refund` (BR-62, BR-78) |
| Session marked `no_show` | No entry: credits stay reserved until the session is cancelled or completed (T-05) |

Because a question never lapses (D-14), a reserve is released only by an answer, a decline, a deletion or a cancellation. There is no timeout job.

### **7.5 Credit requests (BR-66, BR-69, G-13)**

1. The user sends a **credit request** (from the blocked-action prompt or at any time). It is a `credit_requests` row and a notification to PI Admin (Client Admin from Phase 3).
2. PI Admin approves or declines. The approver sees counts only, never what credits were spent on (BR-66, BR-42). Approval is recorded with approver, date and amount. Approving in steps of 12 is a proposal \[P\].
3. **Approval adds credits to that user's limit** (`memberships.credit_limit`). If the client's pool is also short, PI Admin allocates credits to the client as a separate `purchase` entry (BR-69, BR-68).
4. The user is notified of the outcome (Business 5.4).

### **7.6 Low-balance alerts (BR-83)**

After any entry that lowers a client's pool, if the pool is at or below 10, 5 or 0 and no `client_balance_alerts` row exists for that threshold, insert one and notify PI Admin (Client Admin from Phase 3). A new `purchase` clears alerts for thresholds the pool now exceeds.

### **7.7 Integrity**

* A nightly reconciliation job checks: every `spend` has one matching `earning`; no pool is negative; no user `remaining` is negative; every reserve is resolved or still open. A failure pages the team.
* Property tests (section 18.4) generate random sequences of reserve, spend, refund and cancel and assert the invariants.

## **8. Q&A service (CAP-27; BR-35 to BR-38, BR-67, BR-71 to BR-73, BR-81)**

### **8.1 Flow**

| Step | Server action | Credit entry |
| ----- | ----- | ----- |
| 1. Ask | User types a question; the AI conversation validates and refines it (8.2); the safety screen runs on the confirmed wording (8.4) | none |
| 2. Split | If the user packed several questions in, the AI proposes separate questions; the user keeps or drops each (8.3) | none |
| 3. Choose | User picks one or more coaches: three AI suggestions or search (5.4). Up to 3 coaches per question \[P\] (G-09). The app shows each cost and the total | none |
| 4. Check and submit | Credit check (7.3); one `questions` row per question, one `question_requests` row per coach; notify coaches | `reserve` per request |
| 5. Answer | Coach records and uploads a video answer and marks it complete (8.8) | `spend` and `earning` |
| 6. Otherwise | Coach declines, or the user deletes the question. The request stays open until one of these happens | `refund` |

### **8.2 AI validation conversation (BR-35, BR-36, CAP-11)**

* The conversation is held in `question_drafts` and proxied by the API; the client app never calls the model provider.
* The model **clarifies and refines; it does not answer** (Business 1.2). Its response must be one of two typed outputs: a clarifying message, or a list of proposed questions. A response that is neither (for example coaching advice) is discarded and regenerated. This is enforced by output schema and tested with a fixed set of advice-seeking prompts.
* Skills (5.5) and effective terminology (5.1) are supplied as delimited data blocks, not instructions.
* **Retention (BR-36):** on send, the draft is deleted immediately. A draft with no activity for 24 hours is `abandoned` and deleted by a job \[P\]. The user cannot choose to keep it. The final confirmed question text persists in `questions`.
* No policy lets PI Admin, a coach or anyone else read `question_drafts` (BR-40).

### **8.3 Splitting (BR-67)**

Each proposed question is separate and charged separately. The app shows each question and the total cost, and the user may send or drop each one. **Merging is not offered.** Each kept question becomes its own `questions` row, with `parent_question_id` pointing to the first.

### **8.4 Safety screen (CAP-31, BR-38, D-23, Business 10)**

* A classifier runs on each question's **confirmed wording** before anything is sent. It covers typed questions only; video answers and calls cannot be screened in advance (G-17). The classifier also runs on each user turn in the validation conversation, because a user may disclose a crisis to the AI \[P\] (G-17).
* **If flagged:** nothing is sent to any coach and no credits are reserved. The app shows crisis resources and the client's own support resources (`clients.support_resources`). A `safety_flags` row is written and PI Admin (Client Admin from Phase 3) is notified that **a flag was raised and for whom**, not what was said (BR-38). PI Admin can read the flagged text only through `admin_open_content()` with reason `safety` (BR-40, G-34).
* The classifier approach is ADR-026 (OPEN).
* The flagged text is retained so it can be reviewed; its retention follows G-33 and is open (T-09).

### **8.5 Submit**

One database transaction: credit check, rows, `reserve` entries, notifications queued. If any step fails, nothing is written. An availability re-check rejects a coach who has switched to unavailable since selection (BR-80).

### **8.6 A question never lapses (D-14, BR-72, G-10)**

`question_requests` has no due date and no expiry. A request stays open until the coach answers or declines it or the asker deletes the question. Operational controls instead of expiry:

* a PI Admin report of open requests by age;
* a reminder notification to the coach after 3 working days \[P\];
* the asker can delete the question and ask again;
* a coach cap on open requests \[P\] (G-20).

### **8.7 Declines, deletion and coach visibility**

* **Decline (BR-72):** the coach must give a reason. The request becomes `declined`, the credit is refunded, PI Admin is notified with the reason, and the user is told and may choose another coach. Choosing another coach adds a new request and a new `reserve`.
* **Delete (BR-81):** only the asker can delete. An unanswered question is refunded and disappears from the coach's inbox. An answered question can be deleted; credits stay spent and the coach's earning stands. The answer video is retained, because PIapp owns it (D-19); whether deletion removes it is open (T-07, G-33).
* **What a coach sees (BR-71):** only `coach_question_view`: question text, the asker's first name and role, the twin fields the user chose to share, and the short client context summary. The user sees this list on the confirm screen before sending. Coaches cannot see questions not sent to them (BR-72).

### **8.8 Answer video (D-06, BR-73, ADR-018)**

1. **Record on the iPhone** in portrait, under 3 minutes, with a visible countdown. **Cropping only** means trim (set start and end); there is no other editing (D-06, G-22).
2. **Preview and re-record** before upload.
3. **Upload** directly to the host with a resumable protocol, so a dropped connection resumes. The API issues a short-lived upload URL.
4. **Host webhook** reports `asset ready` with duration, orientation and caption status. The server rejects an asset of 3 minutes or longer, or not portrait.
5. **Captions** are auto-generated and are required for accessibility. The coach can mark the answer complete only when captions are `ready` or have `failed` and a fallback transcript exists \[P\] (G-22).
6. **Mark complete** creates the `answers` row, sets the request `answered`, posts `spend` and `earning`, and notifies the user.
7. **Playback** is by signed, expiring URL. The answer is visible only to the asker and the coach who recorded it, unless the asker shares it inside the client (`shares`, BR-23, BR-73). **Answers are never added to the library** (D-18).
8. **Withdrawal:** PI Admin can withdraw an answer (`answers.status = withdrawn`) as a control for content that cannot be screened in advance (G-17). Whether the credit is refunded is not decided (T-06).
9. **Report a problem:** every answer and session has a route to `problem_reports` (Business 10).

## **9. One-on-one (CAP-28, CAP-33, CAP-35; BR-76 to BR-78)**

### **9.1 Flow**

| Step | What happens | Credit entry |
| ----- | ----- | ----- |
| 1. Match | User searches for a coach or takes a shortlist (5.4); sees availability | none |
| 2. Check and book | User picks 20, 40 or 60 minutes and a slot. Only affordable lengths are offered (7.3). Booking creates the session and calendar events and notifies the coach | `reserve` |
| 3. Run | Coach and user hold the call **outside PIapp** on their own conferencing app. PIapp does not record calls (D-21, BR-76) | none |
| 4. Close | Coach marks the session complete in the app | `spend`, `earning` |
| 5. Otherwise | Either party cancels (at any time), or the session is rescheduled through the reschedule link | `refund` on cancellation |

### **9.2 Availability and slots (BR-77, BR-80)**

A coach connects a Google or Microsoft calendar (`calendar_connections`, free/busy and booking events only) and sets weekly windows, a buffer, and minimum notice (`coach_availability`). Offered slots are: weekly windows, minus calendar busy time, minus booked sessions, minus buffer, in 20, 40 and 60 minute lengths, shown in the user's time zone with an explicit zone label. A coach who has switched to unavailable is not suggested and cannot be booked (BR-80); sessions already booked stand.

### **9.3 Booking (G-11)**

Instant booking against the coach's calendar \[P\]: the session goes straight to `booked`; no coach acceptance step. The `requested` status remains in the schema if coach acceptance is chosen instead (G-11). An exclusion constraint on `(coach_id, tstzrange)` prevents double-booking. The booking creates a calendar event on each party's connected calendar; if the user has no connected calendar, an `.ics` invite is emailed \[P\] (CAP-33).

### **9.4 Meeting link (G-11)**

PIapp does not create meetings. The coach supplies a meeting link, as a default on their profile and optionally per session \[P\]. It is in the calendar event and the session detail. Call providers and call SDKs are out of scope (ADR-019 closed).

### **9.5 Cancel and reschedule (BR-78)**

* **Cancel** by user or coach at any time, including after a no-show: status `cancelled`, `refund` posted, calendar events removed, both notified.
* **Reschedule through a link, as in Calendly:** each session has a signed single-purpose token. The link opens a page where the user (or coach) picks a new slot; the same session moves and credits are unchanged. The link works until the session starts \[P\]. Where the page lives is ADR-025 (OPEN).

### **9.6 No-show and completion (G-11)**

The coach marks a no-show \[P\]. Credits stay reserved; the session can then be cancelled (refund) or completed (spend). Reminders by push at 24 hours and 15 minutes before \[P\].

## **10. AI use (BR-35, BR-37)**

In the MVP, AI is used only for the four tasks below. It gives no coaching advice (BR-35). Categories are added by the PI team, not by AI.

| Task | Input | Output stored | Notes |
| ----- | ----- | ----- | ----- |
| (a) Validate, refine and split a question | The user's text, effective terminology, skills | Conversation in `question_drafts`, deleted on send or abandon (BR-36) | 8.2 |
| (b) Suggest coaches | Confirmed question text, coach profiles | Nothing | 5.4 |
| (c) Match videos to a profile | The user's twin | Nothing | 5.3 |
| (d) Generate insights from a transcript | Transcript chunks | `insights` rows, status `generated` | 4.4; blocked until release date and clearance |

**Controls.**

* A provider abstraction in the API; the app never calls a provider. ADR-006 (provider choice) is OPEN and **now blocks Phase 1**: criteria are US processing, no training on PIapp data (BR-37), structured output, and zero retention.
* Backstory, terminology and user text are passed as delimited data, never as instructions; output is schema-validated.
* Embeddings come from the same provider decision. If a separate embedding provider is used it is a separate sub-processor (3.6).
* A cost cap per validation conversation \[P\].
* The agent's controls (citation post-check, contradiction handling, memory) are parked with the agent (Appendix B).

## **11. Notifications (CAP-29)**

In-app list plus opt-in push (APNs); email for invites, resets and as a fallback where push is off (G-21). Push and email carry titles only, never question text, answer content or notes.

| Event | Recipient | Source |
| ----- | ----- | ----- |
| New question request | Coach | Business 5.3 |
| Session requested or booked | Coach | 5.3 |
| Answer ready | User | 5.4 |
| Session scheduled, cancelled, reminder | User and coach | 5.4, 5.3 |
| New videos | User | 5.4 |
| Out of credits; outcome of a credit request | User | 5.4 |
| Coach declines a question (with reason) | PI Admin | 5.2, BR-72 |
| User requests credits | PI Admin | 5.2, BR-69 |
| Client pool reaches 10, 5, 0 | PI Admin | BR-83 |
| Safety flag raised | PI Admin | BR-38 |
| Takedown request countdown; video in review; open requests by age | PI Admin | BR-54, G-10 |

From Phase 3 the Client Admin receives the credit, balance and safety notifications that PI Admin receives in Phase 1.

## **12. PI Admin website (CAP-01 to CAP-03, CAP-18, CAP-30, CAP-32, CAP-38)**

The PI team runs PIapp for everyone in Phase 1 (concierge model, Business 5.1). Every action below writes an audit entry (3.5).

### **12.1 Client management**

* Create the client: name, term (`contract_start`, `contract_end`), backstory, client terminology (CSV upload, each line editable), client categories, and the client's staff-support resources shown by the safety flow.
* Add users and send each an **invite code** (BR-21). Invites expire and can be revoked.
* **Deactivate a user** (BR-22): access is removed immediately; personal data is kept (G-33); unspent credits stay in the client's pool; requests already reserved are completed or refunded as normal.
* **Reallocate credits** (D-17): within a client, by changing user limits; between clients, by a pair of `adjustment` entries with a reason \[P\].
* Manage credits: allocate credits to the client (`purchase` entry, no minimum), approve or decline credit requests, adjust with a reason (7.5).
* Maintain the client's credit limit and prices (7.1), with the old and new values shown before saving (BR-82).
* Dashboard: sign-ups; user credit usage.

### **12.2 Coach management (CAP-30, BR-25, BR-70)**

* Invite a coach and send an invite code.
* Record vetting: `invited → approved → active` (4.3 in Business). **A coach can be made `active` only when** the profile is complete and the required interview videos are published \[P\] (G-03, ten per coach is the proposed reading).
* Set each coach's percentage (default 20%). The coach sees it read-only.
* Suspend or remove a coach. Withdraw an answer.
* Dashboard: answers, sessions, credits earned; open requests by age.

### **12.3 Content management (CAP-01, CAP-02, CAP-38)**

Video import, categories, transcript, insight review, publish and takedown as in section 4. Categories are global or client-specific. PI App terminology is maintained here; client terminology overrides it (BR-11). Skills are edited with a test panel (5.5).

### **12.4 App management**

* **Notifications** to PI Admin (section 11).
* **Defaults:** credit limit, credit prices, coach percentage, credit value (7.1).
* **Dashboard:** users, credit usage, questions, answers, sessions.
* **Audit log** viewer, including content-access entries with reason codes.
* **Backup and restore (CAP-32).** The page shows backup status (last PITR window, last nightly dump, last restore test) and lets PI Admin raise a restore request that notifies engineering \[P\]. A restore is performed by engineering, not by a button. Quarterly restore tests are recorded here (section 16).
* **Open question content** only through the reason-code dialog (3.4).

### **12.5 Reports (G-15, G-24)**

* **Sponsor report, monthly, per client** (Business 4.2): a branded PDF generated for PI Admin to send. Totals are always shown; breakdowns are shown only for groups of 5 or more users (k ≥ 5, BR-41), so a 50-user client still gets useful totals \[P\] (G-15).
* **Cross-client reporting** for PI Admin (CAP-18, basic).
* The metric list is Business 12; see 14.2 (G-24).

## **13. API surface (REST /v1)**

| Area | Examples |
| ----- | ----- |
| Auth and invites | `POST /invites/redeem` (code, then account), `POST /auth/*` through Supabase Auth, `GET /me` |
| Profile and twin | `GET/PUT /me/profile`, `GET/PUT /me/twin`, `PUT /me/twin/share-fields`, `POST /me/calendar/connect`, `DELETE /me/calendar` |
| Content | `GET /videos`, `GET /videos/:id`, `GET /search?q=&category=`, `GET /me/for-you`, `GET /categories` |
| Library, notes, shares | `PUT/DELETE /me/library/:videoId`, `GET /me/library`, CRUD `/me/notes`, `POST /me/shares`, `DELETE /me/shares/:id` |
| Credits | `GET /me/credits` (limit, used, reserved, remaining, pool available), `GET /me/credits/history`, `POST /me/credit-requests`, `GET /me/credit-requests`, `POST /me/credit-check` (dry run) |
| Q&A (user) | `POST /me/question-drafts`, `POST /me/question-drafts/:id/messages`, `POST /me/question-drafts/:id/confirm` (safety screen), `GET /me/coach-suggestions`, `GET /coaches?q=`, `POST /questions` (submit), `GET /questions`, `GET /questions/:id`, `DELETE /questions/:id`, `POST /questions/:id/coaches` (add another coach), `GET /answers/:id/playback` |
| Sessions (user) | `GET /coaches/:id/slots?minutes=`, `POST /sessions`, `GET /sessions`, `POST /sessions/:id/cancel`, `POST /sessions/reschedule` (token) |
| Coach | `GET/PUT /coach/profile`, `PUT /coach/available`, `PUT /coach/availability`, `POST /coach/calendar/connect`, `GET /coach/inbox`, `POST /coach/requests/:id/decline`, `POST /coach/requests/:id/upload-url`, `POST /coach/requests/:id/complete`, `GET /coach/sessions`, `POST /coach/sessions/:id/complete`, `POST /coach/sessions/:id/no-show`, `POST /coach/sessions/:id/cancel`, `GET /coach/earnings` |
| Notifications | `GET /me/notifications`, `POST /me/notifications/:id/read`, `PUT /me/devices` |
| Reports | `POST /problem-reports` |
| Admin: clients and users | CRUD `/admin/clients`, `/admin/clients/:id/users`, `/admin/invites`, `/admin/clients/:id/context`, `/admin/clients/:id/prices`, `/admin/clients/:id/limit` |
| Admin: credits | `POST /admin/credits/allocate`, `POST /admin/credits/adjust` (reason), `GET /admin/credit-requests`, `POST /admin/credit-requests/:id/decide` |
| Admin: coaches | CRUD `/admin/coaches`, `PUT /admin/coaches/:id/status`, `PUT /admin/coaches/:id/share`, `POST /admin/answers/:id/withdraw` |
| Admin: content | `POST /admin/videos/import`, `PATCH /admin/videos/:id`, `PUT /admin/videos/:id/transcript`, `POST /admin/videos/:id/publish`, `/admin/insights/*` (approve, reject, withdraw), `/admin/categories`, `/admin/terminology` (CSV upload and line edit), `/admin/skills`, `/admin/takedowns` |
| Admin: operations | `GET /admin/questions/open` (no text), `GET /admin/safety-flags`, `POST /admin/content/open` (reason code, audited), `GET/PUT /admin/settings`, `GET /admin/audit`, `GET /admin/backup/status`, `POST /admin/backup/restore-request`, `GET /admin/reports/sponsor?client=&month=` |
| Analytics | `GET /admin/analytics/platform`, `GET /admin/analytics/client/:id` |
| Webhooks | Answer-video host (asset ready, captions), calendar providers (change notifications) |

Every endpoint re-checks the role in middleware in addition to RLS. Error bodies use a typed envelope with stable codes (`user_limit_reached`, `client_pool_exhausted`, `coach_unavailable`, and so on).

## **14. Analytics and reporting (CAP-18)**

### **14.1 Events**

Events: video opened, progress, saved, favourited, shared, note created; search performed and zero results; question started, submitted (topic only), answer viewed; session requested, booked, completed, cancelled; credit spend confirmed; credit request sent; safety card shown (count only). **No event contains note, conversation, twin or question text.** Product analytics (PostHog) receives pseudonymous IDs and event names only.

### **14.2 Success measures (Business 12, G-24 \[P\])**

Targets are deferred until after the MVP (D-22). The measures are tracked from launch. Each is computed from the tables shown.

| Measure | Source |
| ----- | ----- |
| Seats activated | `memberships`, `profiles` (profile completed within 30 days of invite) |
| Monthly active users | `watch_events`, `questions`, `sessions` |
| Videos watched per active user per month | `video_users` |
| Notes per active user per month | `video_notes` |
| Questions asked per active user per month | `questions` |
| Sessions completed | `sessions` |
| Open questions, age, median time to answer | `question_requests` |
| Credit utilisation | `credit_txn`: spent ÷ purchased |
| Credit requests and outcome | `credit_requests` |
| Active coaches and response | `coaches`, `question_requests` |
| Library coverage | `videos`, `video_categories` |
| Client renewal | Recorded outside PIapp |
| Answers and sessions rated helpful | **Not available**: ratings are Phase 2 (CAP-34, G-25) |
| Statement disputes | Phase 4 |

### **14.3 Aggregation rules**

PI Admin sees platform and per-client aggregates. Sponsor and Client Admin views (Phase 3) and the Phase 1 sponsor report use a minimum group size of 5 for breakdowns (BR-41, BR-75). Themes are de-identified topics with counts, never quotes (BR-43). Nobody sees an individual's notes, twin or AI conversations (BR-40).

## **15. iPhone app (CAP-15)**

* **One binary, two experiences.** The role returned at sign-in selects the user tabs or the coach tabs. Details are in UI Spec 3.0.
* **Stack.** SwiftUI, iOS 17+, async/await, Keychain for tokens, Universal Links for invite and reschedule links.
* **Recorder.** AVFoundation capture in portrait; trim only; resumable upload (8.8).
* **Library playback.** YouTube embedded player. There is no Picture-in-Picture for the IFrame (UI 6).
* **Push.** APNs, opt-in, titles only (section 11).
* **Distribution (ADR-024, G-21, R-13).** Pilot through TestFlight, then unlisted or custom App Store distribution. App Store rules for a B2B credits app and for third-party sign-in must be checked before build; the findings feed back to G-21 and T-12.
* **No Android, iPad-specific or desktop app in the MVP** (G-21, CAP-20 unscheduled). An email fallback covers users without an iPhone \[P\].
* **Accessibility.** Dynamic Type, VoiceOver, 44 pt targets, captions on every coach answer.

## **16. Non-functional requirements**

| Area | Requirement |
| ----- | ----- |
| Availability | 99.5% monthly during the pilot; 99.9% from Phase 4 |
| Performance | App cold start to interactive under 2.5 s on 4G; search p95 under 400 ms; library playback start under 3 s; answer upload resumable; credit check under 300 ms server time |
| Scale | Pilot: 1 client, 50 users, 10 coaches, about 100 library videos. Design point carried from v2.1, not binding: 50 clients, 25,000 users, 5,000 videos, 200 coaches \[P\] |
| Security | OWASP ASVS L2; TLS 1.2+; signed URLs for answer video; secrets in a vault; PI Admin MFA \[P\]; PCI through Stripe only (Phase 4) |
| Privacy | DPA before the first pilot (Business 11). No model training on PIapp data (BR-37). Personal data is kept indefinitely (BR-22, G-33); export and delete tooling is built so that legal can decide the policy (T-02) |
| Data residency | US only (D-15) |
| Accessibility | WCAG 2.2 AA on the admin site; iOS Dynamic Type and VoiceOver; captions required on coach answers |
| Backup and DR | Supabase PITR (7 days); nightly `pg_dump` to S3 (versioned, Object Lock, cross-region); quarterly restore test; RPO 24 h; RTO 8 h. Answer assets rely on the video host's redundancy |
| Environments | local, staging, production; separate Supabase projects; staging loaded with the real catalogue |
| Observability | Sentry, Railway logs; alerts on ledger reconciliation failures and webhook failures |

## **17. Architecture Decision Records**

| ADR | Title | Status | Decision |
| ----- | ----- | ----- | ----- |
| 001 | Standalone build, AquaBrain patterns | CLOSED | Own codebase, database and deployment |
| 002 | Postgres host | CLOSED (proposed) | Supabase US region; Railway US for API and worker |
| 003 | Graph store | DEFERRED | The insight graph (CAP-10) is unscheduled. Insights are a list per video |
| 004 | Tenancy | CLOSED | Client = tenant; RLS |
| 005 | Web framework | CLOSED (proposed) | Next.js on Vercel for the PI Admin site only |
| 006 | LLM and embedding provider | OPEN, **blocks Phase 1** | Provider abstraction. Criteria: US processing, no training (BR-37), structured output, zero retention. Direct provider or a router to be confirmed |
| 007 | Transcript source | CLOSED | PI team exports and PI Admin uploads the transcript (Business 5.2). No ASR or caption download |
| 008 | Privacy boundary | CLOSED (extended) | No admin, sponsor, client admin or coach policy on notes, twin or AI conversations. Question and answer content only through `coach_question_view` or audited `admin_open_content()` |
| 009 | Client memory de-identification | DEFERRED | Memory (CAP-17) is unscheduled |
| 010 | MCP auth | DEFERRED | MCP (CAP-13) is unscheduled |
| 011 | Android approach | DEFERRED | Android (CAP-20) is unscheduled |
| 012 | Conversation persistence | REVISED | The validation conversation is deleted on send or abandon (BR-36). Persistent threads and memory are dropped |
| 013 | SSO | OPEN, **decide before build** | SAML through Supabase SSO if the first client requires it (G-32) |
| 014 | Shorts feed | RETIRED | Interview videos are 10 to 20 minutes (BR-09) |
| 015 | SME attribution and earnings | RETIRED | SMEs are not stored or paid (BR-57) |
| 016 | Payouts | CLOSED (proposed) | Stripe Connect Express for coaches, Phase 4. SMEs removed |
| 017 | Portals hosting | RETIRED | No SME, coach or user web portals in the MVP |
| 018 | Answer-video hosting | OPEN, **decide before build** | Hosted video service (for example Mux or Cloudflare Stream). Must have: US storage region, portrait upload, 3-minute limit check, resumable direct upload, signed playback, auto captions, indefinite retention. Rejected: YouTube (not private), Supabase Storage (no adaptive streaming) |
| 019 | Call provider | CLOSED | No provider. Calls are held outside PIapp (D-21, BR-76) |
| 020 | Scheduling and calendar | OPEN (revised) | Own availability windows plus Google and Microsoft free/busy and event creation; the coach controls windows and the available switch. Needed before build |
| 021 | Credit ledger | CLOSED (proposed, revised) | Append-only ledger with `available_delta` and `reserved_delta`; derived balances; idempotency keys; reserve, spend and refund in one transaction (section 7) |
| 022 | Coach matching | CLOSED (proposed, revised) | Rules plus embedding similarity; top three; no rating-based learning in Phase 1 |
| 023 | Weekly briefing delivery | DEFERRED | Briefing (CAP-23) is unscheduled |
| 024 | iPhone distribution and sign-in | OPEN | TestFlight then unlisted or custom distribution; App Store rules for credits and third-party sign-in to be verified (G-21) |
| 025 | Reschedule link and public pages | OPEN | A small public web page (and Universal Link) for the reschedule link, hosted with the admin site or separately. Also decides whether the per-client public share link (BR-23) exists in the MVP (T-08) |
| 026 | Safety classifier | OPEN | A model-based classifier with a fixed rubric versus a moderation API; required behaviour in 8.4 |
| 027 | Credit amounts | CLOSED (proposed) | `numeric(12,4)` credits; coach earnings are fractional at the default share (T-03) |

## **18. Phase build checklist and test strategy**

### **18.1 Phase build checklist**

**Phase 1: MVP launch (D-08, D-09).** Repository and CI; schema 6.1 to 6.8 with RLS tests; invite-code sign-up and role-aware sign-in; app settings; client onboarding, users, backstory, terminology, categories, support resources (CAP-03, CAP-38, CAP-02); video import, transcript, insight generation and review, publish, takedown (CAP-01); search and AI match (CAP-05); library, share, notes (CAP-06 to CAP-08); digital twin and profiles (CAP-14, CAP-24); credit ledger, credit check, credit requests, alerts (CAP-25); coach accounts, vetting, availability switch, calendar connection (CAP-26, CAP-30, CAP-33); Q&A with AI validation, split, suggestions, safety screen, answer video (CAP-27, CAP-31, CAP-11); one-on-one booking, cancel, reschedule (CAP-28, CAP-35); inbox and notifications (CAP-29); admin dashboards, reports, audit log, backup status (CAP-18, CAP-32); iPhone app (CAP-15); staging with the real catalogue.

**Phase 2: incorporate trial feedback (CAP-36).** The feedback backlog; ratings (CAP-34); personal stats (CAP-09).

**Phase 3: Client Admin portal (CAP-16).** Client Admin console and Sponsor views at k ≥ 5 (CAP-18 full); enable Client Admin and Sponsor sign-in; Sponsor as user (CAP-37).

**Phase 4: billing (CAP-19, CAP-22).** Stripe billing and credit packs; user top-up where the client allows; coach payouts through Stripe Connect.

**Unscheduled.** Agent, MCP, memory, weekly briefing, insight graph, Android (CAP-12, 13, 17, 23, 10, 20). See Appendix B.

### **18.2 Test layers and CI**

| Layer | What it covers |
| ----- | ----- |
| Database (pgTAP) | RLS isolation (client to client; coach to coach; coach to user-private; PI Admin to question text, notes, twin and drafts); ledger append-only; constraints |
| API unit and integration | Role middleware; credit check; Q&A and session state machines; webhooks, against fakes for the model provider, video host and calendar |
| Ledger properties | Random sequences of reserve, spend, refund, cancel and adjust; assert the invariants in 7.7 |
| AI behaviour | A fixed set of advice-seeking prompts must never produce advice (8.2); a fixed set of crisis prompts must be flagged (8.4) |
| iOS | Unit tests; UI tests for the question, credit-blocked and booking flows; recorder limits |
| End to end smoke | The deployed staging API through a full question and a full session |
| Manual | Answer recording on real devices and networks; calendar sync on real accounts; accessibility (VoiceOver) |

CI (GitHub Actions) runs lint, typecheck, unit, pgTAP and API tests on every pull request, and the smoke test on staging deploys. Vercel previews cover the admin site.

### **18.3 Requirement traceability check**

Appendix A maps every capability and rule to a section and to a verification type. A script reads the Business Spec's IDs and fails CI when an active BR or CAP has no row in Appendix A, or an Appendix A row points at an ID the Business Spec no longer has \[P\]. This keeps the three specs from drifting apart again.

### **18.4 Behaviours that must have an automated test before launch**

The credit check (BR-69) including both rejection codes; reserve, spend and refund for every event in 7.4; question never lapses (no job can close a request, D-14); coach sees only `coach_question_view` (BR-71, BR-72); PI Admin cannot read question text, notes, twin or drafts except through `admin_open_content()` (BR-40); a flagged question is never sent (BR-38, D-23); validation conversation deletion (BR-36); publish guards (BR-03, BR-57); unavailable coach cannot be chosen or booked (BR-80); settings changes are audited with old and new values (BR-82).

## **19. Open decisions and gaps**

### **19.1 Decisions needed before build starts**

These are the items that would change the design most. Items from the Business Spec's gap register marked priority A are included.

| Decision | Why it blocks | Owner | Source |
| ----- | ----- | ----- | ----- |
| LLM and embedding provider (ADR-006) | Question validation, suggestions, matching and insight generation all depend on it; US processing and no-training terms must be in place | Ian | ADR-006 |
| Answer-video host (ADR-018) | Recording, upload, captions, playback and retention depend on it; must be US region | Ian | ADR-018, G-22 |
| SAML single sign-on (ADR-013) | The first client's identity provider decides it | Ian, first client | G-32 (A) |
| iPhone-only reach and distribution (ADR-024) | App Store rules for a B2B credits app and for third-party sign-in; client device mix | Ian | G-21 (A) |
| Calendar and meeting links (ADR-020, G-11) | Instant booking versus coach acceptance; who supplies the link; who marks a no-show | Jez, Ian | G-11 (A) |
| Retention and deletion policy | The tooling is built either way; the policy changes what is deleted and when | Jez, Legal | G-33 (A) |
| Safety flag handling | What the notified person sees and does; whether flagged text is kept and for how long | Jez, Legal | G-34 (A), T-09 |
| Legal clearance for insight extraction | `app_settings.extraction_cleared` must be set before the first insight job can run | Jez, Legal | Business 9 |

### **19.2 Business gaps and what this spec assumes**

Every gap in Business Appendix A, with the technical position.

| Gap | Priority | What v3.0 assumes | If decided differently |
| ----- | ----- | ----- | ----- |
| G-01 | Done | Planning figure \$25,000 (500 credits) | None |
| G-02 | B | The limit period is the contract term: usage counts entries since `contract_start` (7.2) | A per-year or lifetime period changes one view and the `clients` term columns |
| G-03 | A | Ten interviews **per coach**; a coach becomes `active` only when they are published (12.2) | A different count changes one guard |
| G-04 | A | Coach percentage is a per-coach setting; no rule for when it differs | No schema change |
| G-05 | B | Manual monthly payout from the `coach_earnings` view and an export, in US dollars | Phase 4 replaces it |
| G-06 | Done | Invite code is the single term | None |
| G-07 | A | The agent is unscheduled and parked (Appendix B) | If scheduled, un-park Appendix B and re-plan Phase 2 |
| G-08 | B | Notes are in the MVP (6.4) | Removing them drops `video_notes` |
| G-09 | B | No threads; a follow-up is a new question; at most 3 coaches per question (8.1) | A thread model adds a table and changes 8.7 |
| G-10 | B | Open-requests-by-age report; coach reminder after 3 working days; user can delete (8.6) | A re-route rule would need a job |
| G-11 | A | Instant booking; coach supplies the link; coach marks a no-show; credits stay reserved after a no-show (9.3 to 9.6) | Coach acceptance uses the existing `requested` status |
| G-12 | C | No minimum purchase (7.1) | A minimum returns with Phase 4 billing |
| G-13 | B | Approval in steps of 12; approver sees counts only (7.5) | A setting, not a schema change |
| G-14 | B | PI Admin acts for Client Admin and Sponsor; they cannot sign in (3.1) | None until Phase 3 |
| G-15 | B | Monthly PDF report; k ≥ 5 on breakdowns, not totals (12.5) | A template change |
| G-16 | A | Logged access with reason code through `admin_open_content()` (3.4) | Fewer or more reason codes |
| G-17 | A | Classifier on typed questions and conversation turns; report route; withdraw an answer; PI contact in settings (8.4, 8.8) | A different escalation route changes notifications |
| G-18 | Done | Data model includes twin, notes, categories link, approvals, invites, notifications, parent question, no-show (6) | None |
| G-19 | B | Short twin form (role, goals, style); user picks fields to share (6.4) | A UI and `share_fields` change |
| G-20 | B | Top three by similarity; cap on open requests per coach; coach pause switch (5.4) | Scoring weights only |
| G-21 | A | iPhone only; unlisted distribution; push with email fallback; English only (15) | Android or web adds a client; the API does not change |
| G-22 | B | Trim only; auto captions required; provider chosen in ADR-018 (8.8) | Caption policy |
| G-23 | B | Admin workflow for categories and terminology (12.3); hours per video estimated in the pilot | None |
| G-24 | B | Success measures are the dashboard list (14.2); admin operations in 12.2 and 12.4 | None |
| G-25 | B | Ratings absent; the two "rated helpful" measures start in Phase 2 (14.2) | None |
| G-26 | A | Legal agreements. No technical effect; the extraction gate depends on them (4.4) | None |
| G-27 | A | Pilot plan. No technical effect | None |
| G-28 | B | Outside PIapp. No technical effect | None |
| G-29 | C | Same prices for every coach (7.1) | A coach-tier column on `client_prices` |
| G-30 | B | Two-column CSV; adds and updates, never replaces; case-insensitive match; used in search, AI conversation and coach summary (5.1) | Parsing rules |
| G-31 | B | Price in force at request; limit at next check; percentage at spend; every change audited (7.1) | None |
| G-32 | A | Email and Google only; SAML undecided (ADR-013) | SAML adds Supabase SSO configuration |
| G-33 | A | Data kept indefinitely; export and delete tooling built (16) | Retention jobs added |
| G-34 | A | PI Admin is the notified person; reads text under `admin_open_content()` (8.4) | Phase 3 Client Admin visibility is a policy change |

### **19.3 New technical gaps found while re-baselining**

| ID | Gap | Proposed resolution | Owner | Priority |
| ----- | ----- | ----- | ----- | ----- |
| T-01 | Business 11 lists sub-processors but omits hosting, database, storage, backup, email, error-tracking and product-analytics providers, and does not name Microsoft for calendar | Add them to the DPA list (3.6) | Ian, Legal | A |
| T-02 | v2.1 required GDPR and CCPA export and delete per user. Business keeps personal data indefinitely (BR-22, G-33). The two conflict | Build export and delete tooling; legal sets the policy (G-33) | Jez, Legal | A |
| T-03 | At the default 20% a coach earns 0.2 of a credit for one answered question, so credits cannot be whole numbers | `numeric(12,4)` credits; the app shows earnings in credits to two decimals (ADR-027) | Ian | B |
| T-04 | A user has two limits: their own remaining limit and the client's pool. Business 1.4 treats "not enough credits" as one case. They need different prompts: "request more credits" versus "your organisation's credits have run out" | The API returns both and a specific error code; UI Spec 3.0 shows each (7.3) | Ian | B |
| T-05 | A session marked no-show keeps its credits reserved until cancelled or completed. Business is silent on whether a no-show refunds or spends | Leave reserved and report; decide in G-11 | Jez | B |
| T-06 | A withdrawn answer has no stated credit effect | Decide: refund, or keep spent | Jez | B |
| T-07 | When a user deletes an **answered** question, what happens to the answer video is not stated. PIapp owns it (D-19), but the user expects it gone from their view | Hide from the user, retain in storage, align with G-33 | Jez, Legal | B |
| T-08 | BR-23 allows a per-client public share link, but the MVP has no user web app to serve it | Keep the setting (off); do not build the public page in Phase 1 unless a client asks (ADR-025) | Ian | B |
| T-09 | A flagged question's text must be kept for PI Admin review, but BR-36 deletes conversations and G-33 retains personal data indefinitely | Keep only the final flagged text, access by `admin_open_content()`; retention per G-33 | Jez, Legal | A |
| T-10 | Approving a credit request adds to the user's limit (BR-66), but if the client's pool is empty the user is still blocked | PI Admin allocates credits to the client as a separate step (7.5); show both in the approval screen | Ian | C |
| T-11 | A question sent to several coaches has several requests; Business defines a status for the question but not how it derives | `open` while any request is open; `complete` when all are answered or declined; `deleted` by the asker (6.5) | Ian | C |
| T-12 | App Store review for a B2B app that sells services in credits, and the rule requiring an equivalent option when third-party sign-in is offered, have not been checked | Verify before build; record the finding under G-21 | Ian | A |

## **20. Change log**

| Version | Date | Change |
| ----- | ----- | ----- |
| 3.0 | 16 Nov 2026 | Re-baselined to Business Spec v5.0. iPhone app for users and coaches plus PI Admin website (D-08); credits, coach accounts, Q&A and one-on-one in Phase 1; credit check and credit requests (BR-69); per-client prices and limits, per-coach percentage; SME removed as a record (BR-57); questions never lapse (D-14); calls outside PIapp (D-21); insight generation in Phase 1; privacy boundary extended to audited content access (BR-40); agent, MCP, memory, briefing, graph and Android parked (Appendix B); ADRs reviewed (section 17); new ADR-024 to 027; Appendix A traceability; technical gap register T-01 to T-12. Appendix C records every v2.1 conflict; section 19 lists open decisions and gaps |
| 2.1 | 22 Oct 2026 | Merged v1.2 with the 16 Oct revised spec: coach role and tables, Q&A and video hosting, one-on-one, credits ledger, weekly briefing, dashboard APIs, ADR-018 to 023 |
| 1.2 | 27 Sep 2026 | SME role, attribution ledger, revenue share |
| 1.1 | 27 Sep 2026 | Sponsor flag |
| 1.0 | 27 Sep 2026 | First issue |

---

## **Appendix A. Traceability: Business Spec v5.0 to this spec**

**Verified by:** **DB** = pgTAP / constraint test; **API** = API unit or integration test; **LEDGER** = ledger property or reconciliation test; **AI** = AI behaviour test set; **iOS** = iOS unit or UI test; **E2E** = staging smoke test; **MANUAL** = manual test on devices or accounts; **REVIEW** = document or legal review; **n/a** = not built in the phase or retired.

### **A.1 Capabilities**

| ID | Capability | Phase | Where | Verified by |
| ----- | ----- | ----- | ----- | ----- |
| CAP-01 | Asset management, insights, approval before publish | 1 | 4.1 to 4.4, 12.3 | API, AI |
| CAP-02 | Category management, global and client | 1 | 6.2, 12.3 | API |
| CAP-38 | Terminology management | 1 | 5.1, 6.3, 12.3 | API |
| CAP-03 | Client onboarding (concierge) | 1 | 12.1, 6.1, 6.3 | API |
| CAP-04 | Authentication, invite code | 1 | 3.1, 6.1, 13 | API, DB |
| CAP-05 | Video search and AI match | 1 | 5.2, 5.3 | API |
| CAP-06 | Personal library | 1 | 6.4, 13 | API |
| CAP-07 | Share a video inside the client | 1 | 6.4, 3.3 | API, DB |
| CAP-08 | Notes pinned to a timestamp | 1 | 6.4 | API |
| CAP-09 | Personal stats dashboard | 2 | 18.1 | n/a |
| CAP-10 | Insight graph | Unscheduled | Appendix B | n/a |
| CAP-11 | Skills for question refinement | 1 | 5.5, 8.2 | API, AI |
| CAP-12 | Coach agent | Unscheduled | Appendix B | n/a |
| CAP-13 | MCP server | Unscheduled | Appendix B | n/a |
| CAP-14 | Digital twin | 1 | 6.4, 5.3 | API, DB |
| CAP-15 | iPhone app | 1 | 1, 15 | iOS, E2E |
| CAP-16 | Client Admin portal | 3 | 18.1 | n/a |
| CAP-17 | Conversation memory | Unscheduled | Appendix B | n/a |
| CAP-18 | Analytics (basic 1, full 3) | 1, 3 | 12.5, 14 | API |
| CAP-19 | Billing | 4 | 2, 18.1 | n/a |
| CAP-20 | Android app | Unscheduled | Appendix B | n/a |
| CAP-22 | Payouts | 4 | 2, 17 (ADR-016) | n/a |
| CAP-23 | Weekly briefing | Unscheduled | Appendix B | n/a |
| CAP-24 | Registration, profile, credit history | 1 | 6.1, 6.4, 7 | API |
| CAP-25 | Credits | 1 | 7 | LEDGER, API |
| CAP-26 | Coach accounts | 1 | 6.1, 6.6, 9.2, 12.2 | API, DB |
| CAP-27 | Q&A | 1 | 8 | API, AI, E2E |
| CAP-28 | One-on-one | 1 | 9 | API, E2E |
| CAP-29 | Inbox and notifications | 1 | 11 | API |
| CAP-30 | Coach vetting and qualification | 1 | 12.2, 6.10 | API |
| CAP-31 | Safety screen | 1 | 8.4 | AI, API |
| CAP-32 | Backup, restore, audit log | 1 | 3.5, 12.4 | API, MANUAL |
| CAP-33 | Calendar connection | 1 | 6.6, 9.2, 9.3 | MANUAL |
| CAP-34 | Ratings | 2 | 6.9 | n/a |
| CAP-35 | Call booking and calendar sync | 1 | 9 | API, E2E |
| CAP-36 | MVP feedback backlog | 2 | 18.1 | n/a |
| CAP-37 | Sponsor as user | 3 | 18.1 | n/a |

### **A.2 Business rules**

| ID | Where | Verified by |
| ----- | ----- | ----- |
| BR-01 | 4.1, 6.2 (`approved_channels`) | API |
| BR-02 | 4.2 | API |
| BR-03 | 4.2 | API |
| BR-04 | 4.3 | iOS, REVIEW |
| BR-05 | Retired: no per-client video access (4.2) | n/a |
| BR-06 | 4.4, 5.2 | API |
| BR-07 | 4.4 (citation) | API |
| BR-08 | 3.1, 4.3 | API, DB |
| BR-09 | 4.1 | API |
| BR-10 | 5.1, 6.3 | API |
| BR-11 | 5.1, 6.3 | API |
| BR-12 | 3.3 | DB |
| BR-13 | 6.3 (`approval_evidence_path`) | API, REVIEW |
| BR-20 | 3.1, 6.1 | DB |
| BR-21 | 6.1 (`invites`), 12.1 | API |
| BR-22 | 12.1 (deactivation), 16 | API |
| BR-23 | 3.3, 6.4, ADR-025 | DB |
| BR-24 | 2, ADR-013 | API |
| BR-25 | 6.1, 12.2 | API |
| BR-30 to BR-34 | Retired with the agent (Appendix B) | n/a |
| BR-35 | 10 | AI |
| BR-36 | 8.2 | API |
| BR-37 | 3.6, 10 | REVIEW |
| BR-38 | 8.4 | AI, API |
| BR-40 | 3.3, 3.4 | DB |
| BR-41 | 14.3 | API |
| BR-42 | 3.3, 7.5, 14.3 | DB |
| BR-43 | 14.3 | API |
| BR-50 to BR-53 | Retired with the SME portal | n/a |
| BR-54 | 4.4 | API |
| BR-55, BR-56 | Retired with SME attribution | n/a |
| BR-57 | 4.1, 4.2 | API |
| BR-60 | 7 | LEDGER |
| BR-61 | 7.1, 7.2 | LEDGER |
| BR-62 | 7.4 | LEDGER |
| BR-63 | 7.1 | LEDGER |
| BR-64 | 7.2 | LEDGER, DB |
| BR-65 | 7.1, 7.2 | LEDGER |
| BR-66 | 7.2, 7.5 | LEDGER |
| BR-67 | 8.3 | API |
| BR-68 | 7.1, 12.1 | API |
| BR-69 | 7.3 | LEDGER, API |
| BR-70 | 12.2, 6.10 | API |
| BR-71 | 8.7, 6.5 (`coach_question_view`) | DB |
| BR-72 | 5.4, 8.6, 8.7 | API, DB |
| BR-73 | 8.8 | DB, API |
| BR-74 | 3.3 | DB |
| BR-75 | 14.3 | API |
| BR-76 | 9.1, 9.4 | REVIEW |
| BR-77 | 5.4, 9.2 | API |
| BR-78 | 9.5 | API |
| BR-79 | Retired: off-platform solicitation is in the coach agreement | n/a |
| BR-80 | 5.4, 8.5, 9.2 | API |
| BR-81 | 8.7, 7.4 | API, LEDGER |
| BR-82 | 7.1, 3.5 | API |
| BR-83 | 7.6 | LEDGER, API |

### **A.3 Decisions**

| ID | Where |
| ----- | ----- |
| D-01 | 1 |
| D-02 | 4, 8, 9 |
| D-03 | 7.1 to 7.3 |
| D-04 | 7.1 |
| D-05 | 5.4 |
| D-06 | 8.8 |
| D-07 | 12.2 |
| D-08 | 1, 15 |
| D-09 | 18.1 |
| D-10 | 4, 5.1 |
| D-11 | 7.1 |
| D-12 | 6.1 (`coaches.available`), 9.2 |
| D-13 | 5.1 |
| D-14 | 8.6 |
| D-15 | 3.6 |
| D-16 | 7.2 (`credit_value_cents`; conversion in Phase 4) |
| D-17 | 12.1 (reallocation) |
| D-18 | 8.8 |
| D-19 | 8.7 |
| D-20 | No technical effect (commercial) |
| D-21 | 9 |
| D-22 | 14.2 |
| D-23 | 8.4 |

---

## **Appendix B. Parked designs (unscheduled in Business v5.0)**

These capabilities are kept, unscheduled, until Jez and Ian decide (G-07). Their v2.1 designs are not repeated here; they remain in v2.1 (git history) and need re-baselining before use.

| Capability | v2.1 section | What Phase 1 already does to keep the door open | Re-plan needed if scheduled |
| ----- | ----- | ----- | ----- |
| Coach agent (CAP-12) | 8, 9 | Provider abstraction (10); approved insights with timestamps and citations (4.4); embeddings and retrieval (5.2) | Conversation tables, citation post-check, contradiction handling, per-turn cost control |
| MCP server (CAP-13) | 11 | The REST API is the only surface; the same service layer can back a tool server | Token model (ADR-010), tool list, credit-spending controls |
| Conversation memory and client learning (CAP-17) | 6.6, 8.2 | `digital_twins`, privacy boundary (ADR-008) | De-identification (ADR-009), consent, deletion |
| Weekly briefing (CAP-23) | 9 | Notifications and email infrastructure (11); embeddings (5.3) | Job per time zone, content selection, opt-out |
| Insight graph (CAP-10) | 6.5, 7 | Insights are first-class rows (6.2). The graph is one added table, `insight_link` (Business 5.7) | Link generation, review queue, traversal |
| Android (CAP-20) | 15 | One REST API; no iPhone-only server behaviour | Native Kotlin or Kotlin Multiplatform (ADR-011) |

**Not parked, retired.** The SME portal, SME accounts, SME attribution and SME earnings (BR-50 to BR-53, BR-55, BR-56) are retired in Business v5.0, not unscheduled. Nothing is kept for them.

---

## **Appendix C. v2.1 reconciliation log**

Every place Technical Spec v2.1 disagreed with Business Spec v5.0, and what v3.0 does.

| # | v2.1 said | Business v5.0 says | v3.0 |
| ----- | ----- | ----- | ----- |
| 1 | Web user app first; iOS in Phase 3 | iPhone app is the MVP; no user web app (D-08, CAP-15) | iPhone app Phase 1; admin site only (1, 15) |
| 2 | Q&A in Phase 3; one-on-one in Phase 4; credit ledger in Phase 3 | All Phase 1 (CAP-25, 27, 28) | Phase 1 (18.1) |
| 3 | Hosts `app.`, `admin.`, `experts.`, `coach.`, `mcp.` | PI Admin website only; no portals | `admin.` and `api.` only (2) |
| 4 | `sme` role; SME accounts and portal | SME appears in videos only, not stored (BR-57) | No SME role or tables (3.1, 6.9) |
| 5 | `smes` table with extraction consent; publish needs an SME | Release date on the VIDEO; publish needs coach, category, summary and 3 approved insights | `videos.sme_release_date`; guards in 4.2 |
| 6 | `video_client_access` | BR-05 retired | Removed (4.2) |
| 7 | YouTube channel sync and caption download by OAuth; ASR | PI team exports and attaches the transcript | Manual upload (4.1, ADR-007) |
| 8 | Insight pipeline in Phase 2, with graph, concepts, contradictions | Insights in Phase 1; graph unscheduled | Phase 1 generation and review (4.4); graph parked |
| 9 | Agent, weekly briefing, MCP, memory | Unscheduled | Parked (Appendix B) |
| 10 | Question statuses include `expired`, `refunded`; `due_at`; allocation offers; auto mode | A question never lapses (D-14); user chooses coaches (D-05) | `question_requests` with four statuses and no expiry (6.5, 8.6) |
| 11 | "No accept before `due_at` refunds"; UI copy "refunded if not answered in 5 working days" | Credit returns only on decline, deletion or cancellation (BR-62) | Removed; see UI Spec 3.0 |
| 12 | Answer length "proposed 5 minutes"; browser recording | Portrait, under 3 minutes, crop only, recorded on the phone (D-06) | 8.8 |
| 13 | Session lengths 30 and 60 | 20, 40, 60 (BR-78) | 6.6, 7.1 |
| 14 | Prices by coach tier; global `credit_prices` | Prices per client; same for every coach (G-29) | `client_prices` (6.3) |
| 15 | `credit_accounts`, SME accounts, `earn` entries for SMEs | Coaches earn a percentage in credits; SMEs are not paid | `credit_txn` with coach `earning` entries (7.2) |
| 16 | Stripe packs and top-up in the credits design | Billing is Phase 4 | Phase 4 only (18.1) |
| 17 | Call provider decision (ADR-019), recording consent columns | Calls outside PIapp; no recording (BR-76) | ADR-019 closed; no recording fields |
| 18 | `answers.rating`, `helpful` | Ratings are Phase 2 | Not created (6.9) |
| 19 | `glossary_terms` | Terminology at app and client level (D-13) | `terminology` (6.3) |
| 20 | Client join code | Invite code only; no open self-registration (BR-21, G-06) | `invites` only (6.1) |
| 21 | `client_profiles` for chosen terms; `briefings`; `inbox_items` | Not in v5.0 | Removed; `notifications` replaces `inbox_items` (6.8) |
| 22 | Coach mobile app "a later release"; coaches use a web portal | Coaches use the iPhone app in Phase 1 (D-08) | One app, two roles (15) |
| 23 | SAML "later" | Open and priority A (G-32) | ADR-013 OPEN |
| 24 | GDPR and CCPA export and delete per user | Data kept indefinitely (BR-22, G-33) | Tooling built, policy open (T-02) |
| 25 | `GET /me/dashboard` with conversations and briefings | No agent or briefing | `GET /me/credits` and lists (13) |
| 26 | Coaches "tier" and rate tier | Same prices for all coaches in the MVP (G-29) | No tier |
| 27 | Matching "auto" mode with offer expiry | Three AI suggestions; the user chooses (D-05) | 5.4 |
| 28 | Follow-up as a paid question linked to the first | No threads; a follow-up is a new question (G-09 \[P\]) | 8.1 |
| 29 | Question "request to add to library" | Answers are never added to the library (D-18) | Removed (8.8) |
| 30 | Backup: S3 and PITR only | Admin "Backup and restore" and audit log (CAP-32) | 12.4 added |

