UI V2

[https\://www\.appthetics.com/blog/onlyfans-app-ui-design-patterns](https://www.appthetics.com/blog/onlyfans-app-ui-design-patterns)

# **PIapp — UI Specification v2.1**

|  |  |
| ----- | ----- |
| Product | PIapp — Performance Intelligence app |
| Version | 2.1 (Draft) — 22 Oct 2026 |
| Status | For review. Items marked OPEN need a decision or design review with PI |
| Companion specs | PIapp-Business-Spec-v2*1.md (CAP-xx, BR-xx), PIapp-Technical-Spec-v2*1.md |
| Brand reference | performance-intelligence.com and youtube.com/@performance-intelligence (§1.3) |

---

## **1\. Design intent**

### **1.1 Principles**

1. **Calm, not a feed.** No infinite scroll, streaks, badges or notification pressure.  
2. **The expert is the product.** SME and coach faces, names and the interview or answer lead.  
3. **Speak the client's language.** Categories, suggestions and agent answers use the client glossary (BR-10..12). Client logo alongside PI branding, never instead of it.  
4. **Grounded and visible.** Agent answers show sources and disagreement (BR-30..32).  
5. **Private by default.** Notes, history, conversations and twin are visibly the user's own. Before a question goes to a coach, the user sees exactly what the coach will see (BR-71).  
6. **Prices are never a surprise.** Any action that spends credits shows the cost and balance first, and what is refunded if it isn't delivered (BR-62).  
7. **One design system, many surfaces.** User app (web, iOS, Android), admin consoles, SME portal and Coach portal share tokens and components.

### **1.2 Surfaces**

| Surface | Host | Who | Phase |
| ----- | ----- | ----- | ----- |
| User web app | `app.` | User | 1 (briefing 2, Q\&A 3, one-on-one 4\) |
| PI Admin console | `admin.` | PI Admin | 1 |
| Client Admin console | `admin.` (client-scoped) | Client Admin | 3 |
| Sponsor dashboard | `admin.` (read-only) | Sponsor | 3 (Phase 1–2: PDF report) |
| SME portal | `experts.` | SME | 3 |
| Coach portal | `coach.` | Coach | 3 (calls 4\) |
| iOS app | App Store | User | 3 |
| Android app | Play Store | User | 4 |
| Public share page | `app.` `/s/<token>` | Anyone with a link, if allowed (BR-23) | 1 |

### **1.3 Brand source**

On 22 Oct 2026 performance-intelligence.com returned only a "Coming soon" holding page (logo, tagline, contact details), so no colours, type or layout could be taken from it. The visual language derives from the PI YouTube channel format, the PI logo and tagline, and the Inspiring Excellence Bubble app (palette, Krub type, dark default). **UI-OPEN-01:** a designer checks tokens against the PI logo and the live site once it launches, before Phase 1 build. Tokens make this a change, not a rework.

---

## **2\. Design system**

### **2.1 Colour tokens (dark default; light supported)**

| Token | Dark | Light | Use |
| ----- | ----- | ----- | ----- |
| `bg.base` | \#071735 | \#FFFFFF | Page |
| `bg.raised` | \#0E2247 | \#F4F7F8 | Cards, panels |
| `bg.sunken` | \#050F24 | \#DFE6E9 | Inputs, player surround |
| `text.primary` | \#FFFFFF | \#071735 | Body, headings |
| `text.secondary` | \#B2BEC3 | \#636E72 | Meta, captions |
| `accent.primary` | \#01A3E3 | \#0676C5 | Buttons, links, focus |
| `accent.strong` | \#0676C5 | \#055A98 | Hover, pressed |
| `accent.agent` | \#73539E | \#73539E | Agent, insights, skills |
| `accent.coach` | \#1FA39A | \#137A73 | Human coach content: answers, sessions, coach UI |
| `accent.credit` | \#E0B13A | \#8F6A00 | Credit amounts and balances (always with a text label) |
| `border` | \#1E335C | \#DFE6E9 | Dividers |
| `status.success` / `warning` / `danger` | \#2BB673 / \#F5A623 / \#E5534B | \#1E8E57 / \#B97700 / \#C0392B | Published; in review or contested; rejected or error |
| `client.brand` | from client | same | Logo area only |

All pairs meet WCAG 2.2 AA; verify `text.secondary` on `bg.raised` (dark) and `accent.credit` text on `bg.raised` first. `accent.coach` and `accent.credit` are new and need checking with PI (UI-OPEN-01).

### **2.2 Typography**

Krub for display and headings (32/40, 24/32, 20/28, 17/24, weight 600); Inter for body (16/24), small (14/20), caption (12/16); JetBrains Mono for timestamps and IDs in admin. iOS uses Dynamic Type; minimum body 16 pt.

### **2.3 Spacing, shape, motion**

4-pt grid; radius 8, 12, 16, full. Dark elevation by surface colour, light one soft shadow. Max width 1200 px (user), 1440 px (admin). Material Symbols Rounded; SF Symbols on iOS; thumbnails 16:9; no stock photography. Motion 150–250 ms, no autoplay, honour reduced motion. Agent answers stream; citations appear on completion.

### **2.4 Breakpoints**

`sm` \< 640 (single column, bottom tab bar); `md` 640–1023; `lg` ≥ 1024 (left sidebar, side panel on video page). Responsive from 320 px; Phase 1 is web only so mobile web must be good.

---

## **3\. Components**

| Component | Description |
| ----- | ----- |
| VideoCard / VideoRow | Thumbnail, duration, title, SME, category chip, saved/favourite/progress overlays |
| SMEChip / SMECard, **CoachCard** | Avatar, name, credential; CoachCard adds specialties, response time, rating, price in credits, "Ask" and "Book" buttons |
| CategoryChip, SearchBar, FilterBar | Client-facing labels; glossary notice; Short ≤ 3 min / Standard |
| Player | YouTube IFrame with PI chrome: "Add note at 12:34", save, favourite, share. No custom controls over the player |
| **AnswerPlayer** | Coach video answer with captions, speed control, transcript, rate helpful, "Ask a follow-up" |
| **VideoRecorder** | Coach: record in browser or app, preview, re-record, add transcript edit, publish; shows max length |
| NoteEditor / NoteCard, ShareSheet, StatTile | As v1.2; no leaderboards |
| **CreditChip / CreditMeter** | Balance with label "credits"; spend preview "This will use 10 credits (balance 42)" |
| **CostConfirm** | Dialog before spend: price, balance after, refund conditions |
| **TopUpSheet** | Credit packs, Stripe Checkout, shown only where the client allows (P4) |
| **InboxItem / InboxList** | Actionable items with status; used by coaches and users |
| **BriefingCard** | One briefing item: thumbnail or insight, "why this for you" line, action |
| **ShareContextPanel** | "What your coach will see": question, first name, role, chosen twin fields, client summary; toggles per field |
| **SlotPicker** | Coach availability in the user's timezone with a clear time zone label (P4) |
| ChatThread, CitationCard, ContestedBanner, SkillChip, SafetyCard | As v1.2 |
| DataTable, StatusBadge, Toast, ConfirmDialog, EmptyState | As v1.2 |

---

## **4\. Registration and onboarding**

### **4.1 User registration (CAP-04, CAP-24)**

1. **Create account.** From an invitation link or a client join code: client and PI logos, name, email, password (or SSO). No open sign-up (BR-21).  
2. **Personal profile (digital twin).** Role, level, team size, tenure, up to 3 goals, challenges, preferred style, anything to avoid. Each field has "why we ask"; skippable, editable later. Note: "Only you and the coach use this. Your employer can't see it."  
3. **Client profile.** Confirm client, team and function; choose 3+ client terms or topics you care about. Seeds Home and the weekly briefing. The user does not edit the client's backstory.  
4. **Privacy.** "Your notes, history and conversations are yours — your employer sees only anonymous totals. A coach sees only what you choose to send."  
5. Land on the user dashboard (§5.1).

### **4.2 Other registration**

* **SME:** invitation from PI Admin → create account → set profile and consent (§9) → portal dashboard.  
* **Coach:** invitation from PI Admin → create account → accept code of conduct → personal profile (specialties, style, experience, languages, rate tier) → availability → coach dashboard (§10).  
* Sign in, reset password, locked after 10 attempts, as v1.2.

---

## **5\. User app (web) — Phase 1 onward**

### **5.1 Navigation and dashboard**

`lg` sidebar: **Home, Search, Library, Notes, Stats**; P2 **Coach (agent)**; P3 **Ask a coach, Inbox**; P4 **Sessions**. Profile menu: Profile, Digital twin, Client profile, Credits, Settings, Help, Sign out. `sm/md` bottom tabs: Home, Search, Coach, Library, Me.

**Dashboard (Home panel and Me page).** Tiles: **Credits spent** (this month, with balance and "Top up", P4), **Coaching conversations**(agent), **Coaching questions** (open and answered), **Past coaching sessions**, **Future coaching sessions** (P4). Panels for features not yet live are hidden, not greyed. Phase 1 shows videos watched, minutes, notes, saved.

### **5.2 Home**

Greeting and search; **This week's briefing** (P2); Continue watching; For your topics; New from PI; Short takes; Featured experts; Shared with you; **Answers waiting** (P3, new coach answers); P2 "Ask the coach" card with 3 prompts in client terms and SkillChips.

### **5.3 Search, category, SME pages**

As v1.2: result cards show why they matched with timestamp deep links; glossary expansion notice ("Showing results for *customer retention*, *churn* in *Client*'s terms"); SME and category strips; no results suggests categories, then agent (P2), then "Ask a coach" (P3).

### **5.4 Video detail**

Player left (\~65%), tabs **Notes \| About \| Transcript \| Insights (P2)**. Action row: Save for later, Favourite, Share, Add note. P3: "Ask a coach about this video" opens Ask with the video attached. Watched at ≥ 80%; position saved every 15 s.

### **5.5 Library, notes, stats, share, settings**

As v1.2 (Later/Favourites/History tabs; notes grouped by video with export; stats tiles and weekly chart; share to same-client colleagues, public link only if allowed). Settings add **Credits** (balance, ledger, top-up when allowed), **Notifications** (briefing, answers, sessions), **Client profile** and **Digital twin**.

### **5.6 Weekly briefing (CAP-23, Phase 2\)**

* A page and an email, each week at a time the user chooses (default Monday morning in their timezone).  
* 3–5 **BriefingCards**: videos and insights picked for the user's goals and topics, each with "why this for you", sources cited. A closing prompt to start the agent on the week's top theme.  
* Controls: change day, pause, unsubscribe; "Not relevant" on a card improves future picks.  
* Email carries no private content beyond titles.  
* Empty state (new user): "Complete your profile for a personal briefing", with a general briefing of new PI content.

### **5.7 Coach agent (Phase 2\)**

As v1.2: conversation list, composer with 3 prompts and SkillChips, answers with CitationCards and ContestedBanner, context chip, "I don't have expert material on that" state. **New:** when the agent can't help well or the topic is personal, it offers "Ask a coach" with the question prefilled (nothing is sent until the user confirms).

### **5.8 Ask a coach — Q\&A (CAP-27, Phase 3\)**

1. **Compose.** Question box, optional attachments from the library (video, note excerpts the user selects), topic.  
2. **Choose a coach.** Default "Match me automatically" (explains how: topics, availability, language); or browse CoachCards and choose one. Shows price in credits and typical response time.  
3. **What your coach will see.** ShareContextPanel with toggles (first name, role, goals, client summary). Cannot include agent conversations or notes unless the user pastes them.  
4. **Confirm.** CostConfirm: "10 credits, reserved now. Refunded if not answered within 5 working days or declined."  
5. **Status.** Question card: Submitted → Matched → Answered; shows the due date. Cancel before the coach accepts.  
6. **Answer.** Notification and inbox item; AnswerPlayer with transcript; rate helpful; "Ask a follow-up" (a new paid question linked to the first); save to library; share in-client (optional); "Request to add to library" if allowed (Q-21).  
7. **If declined or expired:** shows the refund, offers another coach. Safety: if the question suggests crisis, show SafetyCard and support resources before anything is sent (Q-22).

### **5.9 One-on-one (CAP-28, Phase 4\)**

**Find a coach** (shortlist from matching; filters for topic, language, price, time zone) → **Coach profile** (bio, specialties, ratings, availability) → **SlotPicker** with time zone label → note to the coach (same context controls as §5.8) → CostConfirm (price by length; cancellation window shown) → request sent; coach confirms; call link and calendar invite follow. **Sessions** page: Future (join, reschedule, cancel) and Past (notes only you can see, rate, book again). Reminders 24 h and 15 min before. No recording unless both parties agree on the session page (BR-76).

### **5.10 Inbox (CAP-29)**

One list: answers ready, session confirmations and reminders, shares, briefing. Unread count in the nav; actionable items first.

### **5.11 Credits and top-up**

Credits page: balance (client-allocated and personal), spend history by service, ledger. "Top up" appears only when the client allows (P4): packs, Stripe Checkout, receipt. If the client pool is empty: "Your organisation's credits have run out. Ask your admin, or top up yourself" (when allowed).

### **5.12 Digital twin, memory, MCP**

Twin and client profile editable at any time with preview "How the coach will see you". P3 memory page "What the coach remembers" with delete and pause. MCP connection page as v1.2.

---

## **6\. iOS and Android**

SwiftUI, iOS 17+; tabs Home, Search, Coach, Inbox, Me. Parity with web user features including dashboard, briefing, Q\&A with answer playback, credits, sessions (P4). No Picture-in-Picture for the YouTube IFrame, so offer "Keep watching on YouTube". Dynamic Type, VoiceOver, passkeys, offline lists, opt-in push (answer ready, session reminders, weekly briefing). Android (Phase 4\) mirrors iOS with Material 3\. Coaches use the web portal on mobile in v2.1; a coach mobile app is a later option.

---

## **7\. PI Admin console**

Sidebar **Dashboard, Videos, SMEs, Coaches, Categories, Clients, Users, Analytics**; P2 **Insights, Skills, Coach quality**; P3 **Q\&A, Credits**; P4 **Billing, Earnings**.

* **Dashboard:** videos in review, new uploads, active clients and users; P2 insights pending, flagged answers; P3 questions unanswered or near due, coach capacity.  
* **Videos (CAP-01):** list, YouTube import, editor with transcript, summary (50–150 words), takeaways, SME, categories, consent status, review workflow, change history; cannot publish without summary, category, SME, consent.  
* **SMEs:** profile, separate consent scopes (display, extraction, quotation), takedown with 7-day countdown; P3 portal invites and profile-change approvals; P4 agreement and payout status.  
* **Coaches (P3):** invite, vetting checklist, profile and specialty tags, tier, availability limits, status (active/paused/removed), code-of-conduct record, ratings and response-time stats, complaints; cannot read question content except where the user flags a problem (with the user's consent, BR-71).  
* **Q\&A (P3):** queue with status, age and due dates; unanswered and declined; reallocate manually; safety-flagged items (counts, no content unless the user flags); refunds and adjustments with a reason.  
* **Credits (P3):** per client: allocation, balance, usage by service; allocate or adjust with a reason; credit price table (service, coach tier); full ledger search.  
* **Categories (CAP-02):** two-level tree, merge and archive.  
* **Clients (CAP-03):** list and workspace with tabs Overview, Users (invite by email, CSV or join code), **Backstory** (sections, document upload with extraction assist P2, Draft → Send to Sponsor for approval → Published with approver and date, BR-13), **Glossary**, **Category labels**, **Credits** (P3), **Settings** (public links, SSO, coach enabled, memory enabled, user top-up allowed, join code, support resources), **Analytics**.  
* **Users (global):** support lookup, resend invite, reset password, deactivate. No private data.  
* **Analytics (CAP-18):** active users, videos, minutes, top videos, categories, searches and zero-result searches; P2 conversations, topics, helpful %, briefing opens; P3 Q\&A volumes, response times, helpful ratings, credit utilisation. Client-level cells \< 5 show "\< 5". **Export sponsor report** (Phase 1): per client and month, branded PDF.  
* **Phase 2 admin:** Insights review (queue, approve/edit/reject/merge, bulk approve, list before graph), Contradictions, Skills editor with test panel, Coach quality (flagged answers, uncited answers, safety counts).  
* **Earnings (P4):** settings (SME pool or rate, unit weights, coach share, threshold), monthly run with anomaly flags, approve and publish statements, quarterly payout batch, disputes queue.  
* **Billing (P4):** plan, seats, credit packs, invoices, credit adjustments.

---

## **8\. Client Admin console (Phase 3\) and Sponsor dashboard**

Same shell as PI Admin, client-scoped, client logo in header. Sidebar **Overview, Users, Backstory, Glossary, Credits, Analytics**; P4 **Billing**. \- **Users:** invite, CSV, join code on/off and regenerate, deactivate, make Client Admin; seats. Banner: "You can manage accounts; you can't see anyone's activity or questions." \- **Backstory and Glossary:** same editors; approval recorded here; changes logged. \- **Credits:** client balance and allocation, per-user caps (optional), usage by service and by team at k ≥ 5, request more credits (P3) or buy packs (P4). \- **Analytics:** as PI Admin for this client only, k ≥ 5, themes as de-identified topics with counts (BR-43), Q\&A and session volumes. \- **Billing (P4):** plan, seats, credit packs, invoices, payment method, whether users may top up. \- **Sponsor dashboard (C-03):**one page for a CxO in two minutes: active users vs seats, what people work on (de-identified topics, never quotes), most used content, gaps, credit use, backstory status (last approved, by whom), "Share with leadership team" PDF. Banner: "You see organisation-wide patterns only. Individuals' activity is private" (BR-42). \- Cannot see: video editor, other clients, any individual's notes, history, conversations, questions, twin, memory.

---

## **9\. SME portal (Phase 3; earnings Phase 4\)**

Sidebar **Dashboard, My videos, My insights, Profile, Consent**; P4 **Earnings**. Opens on a summary. \- **Dashboard (from the revised spec):** **Video activity** (minutes watched, views, completion, saves, shares, citations and opened clips, helpful rate; trend by month; reach as number of client organisations, sector only where ≥ 5\) and **Credits earned** (this month, all time, pending and paid). De-identified topics people ask when the SME's insights are cited, with counts. Banner: "You see totals across all clients. No individual user is ever shown." \- **My videos:** table with metrics and sparklines; retention curve if YouTube Analytics access allows (UI-OPEN-09). \- **My insights:** list with times cited, helpful rate, status; "Flag as inaccurate" withdraws the insight from the agent immediately and sends it to PI Admin (BR-54). \- **Profile and consent:** profile edits go to PI Admin for approval; consent scopes with **Withdraw** and a plain explanation of effects (insights removed within 7 days; future earnings stop; earned amounts still paid). \- **Earnings (P4):** accept agreement, payout setup (hosted by the payment provider), monthly statements (units by video and insight, credits earned, amount), PDF, raise a query within 60 days, payouts history, "How your earnings are calculated" with a worked example.

---

## **10\. Coach portal (Phase 3; sessions Phase 4\)**

Sidebar **Dashboard, Inbox, Questions, Sessions (P4), Availability, Profile, Earnings**. Own work only; never shows another coach's questions or earnings (BR-74). Uses `accent.coach`. \- **Dashboard (from the revised spec):** **Credits earned** (this month, all time, pending and paid), **Past coaching sessions** and **Future coaching sessions** (P4), plus open questions with due dates. \- **Inbox:**requests for a video answer (accept or decline, with a reason), session requests (confirm or propose another time), system notices. Badge count; email and push. \- **Question detail:** the question, the asker's first name and role, and only the context the user chose to share; price in credits; due date; safety note if flagged. Buttons: Accept, Decline, Record answer. Reminder that the coach must follow the boundaries and escalation route (Business §10). \- **Record answer:** VideoRecorder (browser camera and microphone, upload fallback), preview, re-record, auto transcript with edit, publish. Autosave of draft recordings; if the connection drops the upload resumes. \- **Sessions (P4):** list of upcoming and past; join link; notes visible only to the coach; mark complete; report a no-show. \- **Availability:** weekly slots, calendar sync (free/busy), maximum open questions and sessions per week, pause until a date. \- **Profile (personal profile / digital twin):** headshot, bio, specialties (categories), style, experience, languages; edits are approved by PI Admin before going live. \- **Earnings:**credits earned by answer and session, ratings, statements and payouts (P4).

---

## **11\. States, voice, notifications, accessibility**

* **States:** every screen defines loading, empty (one action), error (what happened and a retry), offline and permission denied.  
* **Voice:** plain, warm, direct; no hype or emoji; client terms where the glossary has them. The agent never claims to be a person or a named SME or coach. Credit copy always states the amount and the refund condition.

| Situation | Copy |
| ----- | ----- |
| No search results | "Nothing on that yet. Try a broader term, ask the coach, or ask a person." |
| Agent has no material | "I don't have expert material on that. Here's what PI's experts have said on related topics." |
| Contested | "Experts differ on this. Here are both views." |
| Before sending to a coach | "Your coach will see only what's shown here. Your conversations and notes stay private." |
| Spend | "This will use 10 credits. If it isn't answered in 5 working days, they come back." |
| Privacy | "Your notes, history and conversations are yours. *Client* sees only anonymous totals." |

* **Notifications:** in-app inbox and opt-in push: answer ready, session confirmed/reminder, shared with you, briefing; for coaches: new request, due soon; for PI Admin: video review needed, takedown countdown, unanswered questions. Email for invites, resets, answers, briefing (opt-out).  
* **Accessibility:** WCAG 2.2 AA; keyboard reachable; visible 2 px focus ring; captions and transcripts on coach answers (required, not optional); recorder usable by keyboard and with screen readers; credit amounts have text labels, not colour alone; touch targets ≥ 44 pt; streaming text announced on completion.  
* **Internationalisation:** English (UK spelling) for v1; strings externalised; times shown with explicit time zone; currency-free credit units.

## **12\. Analytics events (UI)**

`search_performed`, `search_zero_results`, `video_opened`, `video_progress`, `video_saved`, `video_favourited`, `video_shared`, `note_created`, `briefing_opened`, `briefing_item_clicked`, `coach_conversation_started`, `coach_answer_rated`, `citation_opened`, `skill_started/completed`, `question_started`, `question_submitted` (topic only), `question_answer_viewed`, `answer_rated`, `session_requested`, `session_completed`, `credit_spend_confirmed`, `topup_started`, `safety_card_shown`(count only), `twin_updated`, `memory_item_deleted`. No event contains note, conversation, twin or question text.

## **13\. Screen inventory**

| \# | Screen | Surface | Phase |
| ----- | ----- | ----- | ----- |
| S-01 | Accept invitation / join code, create account | User | 1 |
| S-02 | Sign in / Reset password | User | 1 |
| S-03 | Onboarding: personal profile (twin), client profile, privacy | User | 1 |
| S-04 | Home and dashboard | User | 1 (briefing 2, credits 3\) |
| S-05 | Search results | User | 1 |
| S-06 | Category page | User | 1 |
| S-07 | SME page | User | 1 |
| S-08 | Video detail | User | 1 |
| S-09 | Library | User | 1 |
| S-10 | Notes | User | 1 |
| S-11 | Stats | User | 1 |
| S-12 | Share sheet / public share page | User | 1 |
| S-13 | Profile and settings | User | 1 |
| S-14 | Agent home and conversation | User | 2 |
| S-15 | Digital twin | User | 2 |
| S-16 | MCP connections | User | 2 |
| S-19 | Weekly briefing | User | 2 |
| S-17 | Memory | User | 3 |
| S-20 | Ask a coach (compose, match, share context, confirm) | User | 3 |
| S-21 | Question status and coach answer | User | 3 |
| S-22 | Inbox | User | 3 |
| S-23 | Credits and top-up | User | 3 (top-up 4\) |
| S-24 | Find a coach, book, sessions | User | 4 |
| S-18 | iOS app | iOS | 3 |
| M-01 | Android app | Android | 4 |
| A-01..A-07 | PI Admin: dashboard, videos, SMEs, categories, clients, users, analytics (and sponsor report) | PI Admin | 1 |
| A-08..A-10 | Insights, Skills, Coach quality | PI Admin | 2 |
| A-14 | Coaches | PI Admin | 3 |
| A-15 | Q\&A queue | PI Admin | 3 |
| A-16 | Credits | PI Admin | 3 |
| A-12 | SME portal invites and approvals | PI Admin | 3 |
| A-11 | Billing | PI Admin | 4 |
| A-13 | Earnings: settings, monthly run, payouts, disputes | PI Admin | 4 |
| C-01 | Client Admin console | Client Admin | 3 |
| C-02 | Client Admin billing | Client Admin | 4 |
| C-03 | Sponsor dashboard | Sponsor | 3 |
| E-01..E-03 | SME portal: dashboard, videos and insights, profile and consent, earnings | SME | 3 (earnings 4\) |
| K-01 | Coach registration and profile | Coach | 3 |
| K-02 | Coach dashboard and inbox | Coach | 3 |
| K-03 | Question detail and record answer | Coach | 3 |
| K-04 | Availability and sessions | Coach | 3 (sessions 4\) |
| K-05 | Coach earnings | Coach | 3 (payouts 4\) |

## **14\. Open UI questions**

| ID | Question | Recommendation |
| ----- | ----- | ----- |
| UI-OPEN-01 | Palette and type checked against PI logo and the live site (holding page today)? Are the new coach and credit accents acceptable? | Designer review before Phase 1 build |
| UI-OPEN-02 | Body font Inter or Krub? | Inter body, Krub headings |
| UI-OPEN-03 | Export notes? | Yes, Markdown/PDF |
| UI-OPEN-04 | Wording for cross-user client learning | Agree with PI and privacy review |
| UI-OPEN-05 | Admin consoles light or dark? | Light, toggle |
| UI-OPEN-06 | Visual graph for insights? | List first |
| UI-OPEN-07 | Client co-branding depth | Logo and name only in v1 |
| UI-OPEN-08 | Transcript tab visible to users? | Depends on ADR-007 and consent scope |
| UI-OPEN-09 | Retention curves need YouTube Analytics access; available? | Request scope with captions |
| UI-OPEN-10 | Maximum coach answer length and format (portrait or landscape, 3 or 5 minutes)? | 5 minutes, either orientation |
| UI-OPEN-11 | How prominently should "Ask a coach" appear relative to the free agent, given it costs credits? | Offer it as the next step when the agent is unsure, plus a nav item; never the default |
| UI-OPEN-12 | Does the user see the coach's name before submitting an auto-matched question? | Yes, after matching, with a chance to choose another |

## **15\. Self-critique of this draft**

* **Brand not seen first-hand.** The site is a holding page; tokens are inferred.  
* **No wireframes.** The highest-value screens to wireframe first: S-04, S-05, S-08, S-14, S-20, K-03, A-02, A-05.  
* **Coach and Q\&A flows rest on assumptions** about phasing and credit economics (Business Q-16..Q-24). Layouts will change if those answers change.  
* **Coach UI is web-only** in this spec. Coaches recording on phones need a good mobile web recorder, which must be tested early.  
* **PI Admin carries all client setup** in Phases 1–2; the client workspace is built for reuse by the Client Admin in Phase 3\.

## **16\. Change log**

| Version | Date | Change |
| ----- | ----- | ----- |
| 2.1 | 22 Oct 2026 | Merged v1.2 with the 16 Oct revised spec: registration flows, user/SME/coach dashboards, weekly briefing, Ask a coach (Q\&A), one-on-one, credits and top-up, inbox, coach portal, new tokens and components, PI Admin coaches/Q\&A/credits |
| 1.2 | 27 Sep 2026 | SME portal and revenue-share screens |
| 1.1 | 27 Sep 2026 | Sponsor surfaces |
| 1.0 | 27 Sep 2026 | First draft |

