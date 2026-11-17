# **PIapp — UI Specification v3.0**

|  |  |
| ----- | ----- |
| Product | PIapp — Performance Intelligence app |
| Owner | Ian Gotts, for Jez Cartwright / Performance Intelligence |
| Version | 3.0 (Draft), 16 Nov 2026 |
| Status | DRAFT for review. Re-baselined to Business Specification v5.0. Items marked OPEN need a decision or a design review with PI |
| Companion specs | PIapp Biz Spec v5.0 (CAP-xx, BR-xx, D-xx, G-xx) and PIapp Tech Spec v3.0 |
| Supersedes | UI Specification v2.1 (22 Oct 2026) |
| Brand reference | performance-intelligence.com and youtube.com/@performance-intelligence (section 1.3) |

**How to read this version**

* **Business Spec v5.0 is the authority.** Where this spec and the Business Spec disagree, the Business Spec wins and this spec has a defect. Appendix B lists every place v2.1 disagreed with v5.0 and how it was resolved.
* **(BR-nn), (CAP-nn), (D-nn), (G-nn)** point into the Business Spec; **(T-nn)** into the technical gaps in Tech Spec 19.3.
* **\[P\]** marks a proposal that goes beyond what the Business Spec decides: not yet confirmed.
* Appendix A traces every capability to its screens.

**What changed from v2.1 in one paragraph.** The MVP is an **iPhone app for users and coaches**, plus a **PI Admin website** run as a concierge service (D-08). There is no user web app, no coach portal, no SME portal and no Android app. Credits, Ask a coach, one-on-one, the coach experience and the inbox are Phase 1. SMEs appear in videos only and are not stored (BR-57), so there are no SME pages or chips. A question never lapses (D-14), so the v2.1 copy "refunded if not answered within 5 working days" is gone. There is no coaching agent: the AI refines questions, suggests coaches and matches videos, and says so (BR-35). Weekly briefing, stats, ratings, memory, MCP and top-up are not in Phase 1.

---

## **1. Design intent**

### **1.1 Principles**

1. **Calm, not a feed.** No infinite scroll, streaks, badges or notification pressure.
2. **The coach is the product.** Coach faces and names lead on interviews, answers and sessions. The SME appears in the video only; the app never shows an SME profile (BR-57).
3. **Speak the client's language.** Search, categories and the AI question conversation use the client's terminology, with client terms overriding PI App terms (BR-11). The client logo sits alongside PI branding, never instead of it.
4. **The AI helps you ask; it does not coach.** Wherever AI appears it is labelled as AI, says what it does, and never answers the question (BR-35).
5. **Private by default.** Notes, twin and the question conversation are the user's own. Before a question goes to a coach, the user sees exactly what the coach will see (BR-71).
6. **Prices are never a surprise.** Any action that costs credits shows the cost, what is available, and what is returned if it is not delivered, before the user confirms (BR-62, BR-63, BR-69).
7. **A question stays open until answered or deleted.** The app never implies a deadline or an automatic refund (D-14).
8. **One design system, two surfaces.** The iPhone app and the PI Admin website share tokens and components.

### **1.2 Surfaces**

| Surface | Where | Who | Phase |
| ----- | ----- | ----- | ----- |
| iPhone app, user experience | App Store (TestFlight, then unlisted or custom) | User | 1 |
| iPhone app, coach experience | Same app; the role selects the experience | Coach | 1 |
| PI Admin website | `admin.` | PI Admin | 1 |
| Reschedule page | Web page opened from a link (ADR-025) | User, coach | 1 \[P\] |
| Client Admin console | `admin.` (client-scoped) | Client Admin | 3 |
| Sponsor dashboard | `admin.` (read-only) | Sponsor | 3 (Phase 1 and 2: PDF report sent by PI Admin) |
| Android, desktop and public share page | none | | Not scheduled (G-21, T-08) |

Client Admin and Sponsor have no sign-in in Phase 1; PI Admin performs their tasks on request (G-14).

### **1.3 Brand source**

On 22 Oct 2026 performance-intelligence.com returned only a "Coming soon" holding page, so no colours, type or layout could be taken from it. The visual language derives from the PI YouTube channel format, the PI logo and tagline, and the Inspiring Excellence Bubble app (palette, Krub type, dark default). **UI-OPEN-01:** a designer checks the tokens against the PI logo and the live site before Phase 1 build. Tokens make this a change, not a rework.

---

## **2. Design system**

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
| `accent.ai` | \#73539E | \#73539E | AI-assisted steps: question refinement, coach suggestions, "For you" matches. Renamed from `accent.agent`; there is no agent |
| `accent.coach` | \#1FA39A | \#137A73 | Human coach content: answers, sessions, the coach experience |
| `accent.credit` | \#E0B13A | \#8F6A00 | Credit amounts and balances (always with a text label) |
| `border` | \#1E335C | \#DFE6E9 | Dividers |
| `status.success` / `warning` / `danger` | \#2BB673 / \#F5A623 / \#E5534B | \#1E8E57 / \#B97700 / \#C0392B | Published, available; open for a long time, low credits; rejected, error |
| `client.brand` | from client | same | Logo area only |

All pairs meet WCAG 2.2 AA; verify `text.secondary` on `bg.raised` (dark) and `accent.credit` text on `bg.raised` first. `accent.coach` and `accent.credit` are new and need checking with PI (UI-OPEN-01).

### **2.2 Typography**

Krub for display and headings (32/40, 24/32, 20/28, 17/24, weight 600); Inter for body (16/24), small (14/20), caption (12/16); JetBrains Mono for timestamps and IDs in admin. The iPhone app uses Dynamic Type with a minimum body of 16 pt. Fonts are bundled in the app.

### **2.3 Spacing, shape, motion**

4-pt grid; radius 8, 12, 16, full. Dark elevation by surface colour, light one soft shadow. SF Symbols in the iPhone app; Material Symbols Rounded on the admin site. Library thumbnails are 16:9; coach answers are portrait 9:16. No stock photography. Motion 150 to 250 ms, no autoplay, reduced motion honoured. Admin max width 1440 px.

### **2.4 Layout**

* **iPhone app:** portrait, 375 to 430 pt wide. Bottom tab bar. Safe areas respected. No iPad-specific layout in the MVP; the app runs as an iPhone app on iPad (UI-OPEN-15).
* **PI Admin website:** desktop, 1024 px and wider, with a left sidebar. Below 1024 px a notice asks for a larger screen \[P\].

---

## **3. Components**

| Component | Description |
| ----- | ----- |
| VideoCard / VideoRow | Thumbnail, duration, title, interviewing coach, category chip, saved, favourite and progress overlays. No SME name field (BR-57) |
| CoachCard | Avatar, name, specialties, **AvailabilityBadge**; "Ask" and "Book" actions. In suggestions, a one-line "why suggested" (G-20). No rating and no price: prices are the same for every coach (G-29) and ratings are Phase 2 |
| AvailabilityBadge | Available or Unavailable. An unavailable coach cannot be chosen or booked (BR-80) |
| CategoryChip, SearchBar | Client-facing labels; a notice when client terminology expanded the search |
| Player | YouTube embedded player with PI chrome: "Add note at 12:34", save, favourite, share. No custom controls over the player; no download (BR-04) |
| NoteEditor / NoteCard, ShareSheet | Notes pinned to a timestamp; share to a colleague in the same client, chosen by name \[P\] |
| **CreditChip** | "N credits available" with the label, never colour alone. N is the smaller of the user's remaining allowance and the client's pool |
| **CreditMeter** | The user's allowance: "Used 4 of 12" |
| **CostConfirm** | Lists each charge, the total, what is available, and the refund conditions. Disables Submit when the credit check would fail (7.3 in Tech) |
| **CreditRequestSheet** | Ask for more credits: amount (default 12 \[P\]), optional note, send. Shows the state of an open request |
| **AIBubble / ConversationView** | The question-refinement conversation. Every AI message carries an "AI" label in `accent.ai` and the line "I help you word your question. I don't answer it." |
| **QuestionSplitReview** | One card per question the AI proposes. Each can be edited, kept or dropped. There is no merge (BR-67) |
| **CoachPicker** | Three suggestions with reasons, plus coach search. Select up to 3 \[P\] |
| **ShareContextPanel** | "What your coach will see." Always sent: the question, your first name and role, and a short summary of your organisation. Optional, with toggles: the twin fields you choose (BR-71) |
| **LengthPicker** | 20, 40 and 60 minutes with their credit price. A length the user cannot afford is disabled with the reason (BR-69) |
| **SlotPicker** | The coach's open slots in the user's time zone, with an explicit zone label |
| QuestionCard | A question with each coach's status and how long it has been open. "Open 4 days" |
| **AnswerPlayer** | Coach video answer, portrait, with captions, speed control and transcript. Share inside the client; report a problem. No rating and no follow-up (Phase 2 and G-09) |
| **VideoRecorder** | Coach: portrait capture with a 3:00 countdown, preview, trim handles, re-record, resumable upload progress |
| SessionCard | Time, coach or user, length, credits, status, meeting link |
| NotificationRow | Title, time, tap target. No private text |
| **SafetyCard** | Crisis resources and the client's own support resources; nothing is sent (BR-38) |
| ReportProblemSheet | A problem with an answer or a session; goes to PI Admin (Business 10) |
| **ReasonDialog** (admin) | Required before PI Admin opens a question or answer: reason code and note (BR-40) |
| **SettingsDiff** (admin) | Shows old and new values before saving a credit setting (BR-82) |
| **CSVImport** (admin) | Terminology upload with a preview of lines to be added and updated (G-30) |
| **InsightReviewCard** (admin) | Insight text, excerpt, start and end, jump to that moment, approve, reject, edit |
| **PublishChecklist** (admin) | Live status of the publish guards: coach, category, summary, 3 approved insights, release date |
| DataTable, StatusBadge, Toast, ConfirmDialog, EmptyState | As v2.1 |

---

## **4. Registration and onboarding**

### **4.1 User registration (CAP-04, CAP-24, CAP-14)**

1. **Invite code.** From the invite email a Universal Link opens the app with the code filled in; otherwise the user types the code. No open sign-up (BR-21). Client and PI logos shown.
2. **Create account.** Email and password, or Google. If the App Store requires an equivalent privacy-preserving option, add it (T-12).
3. **What PIapp is for.** One short screen: "PIapp is performance coaching. It is not therapy, medical, legal or HR-investigation advice" (Business 10). Continue to accept.
4. **Profile.** Headshot, bio. Skippable and editable later.
5. **Digital twin.** A short form \[P\] (G-19): your role, up to 3 goals, your preferred style. Each field has "why we ask". Skippable and editable later. Note: "Only you and the coaches you choose to share with can see this."
6. **Privacy.** See the copy in 9.2. Continue.
7. **Calendar.** Optional: "Connect your calendar so booked sessions appear in it" (CAP-33). Skippable.
8. **Home.**

### **4.2 Coach registration (CAP-26, CAP-30, BR-25)**

1. Invite code from PI Admin, then account (email and password, or Google).
2. **Code of conduct and boundaries** (Business 10): read and accept.
3. **Profile:** headshot, bio, digital twin (specialties, style, experience).
4. **Calendar:** connect Google or Microsoft calendar; set weekly availability windows; set a default meeting link \[P\] (G-11).
5. **Availability switch** (explained in 6.5).
6. A coach is **not visible to users until PI Admin makes them active** (BR-70). Until then the app shows "Your profile is being reviewed" with what is still needed (for example, interview videos published).

### **4.3 Sign-in and reset**

Email or Google, with password reset. Locked after 10 attempts. Client Admin and Sponsor accounts that try to sign in during Phase 1 see "This account doesn't have access to the app yet. PI will contact you" \[P\] (G-14).

## **5. User experience (iPhone)**

### **5.1 Navigation**

Bottom tabs: **Home, Videos, Ask, Sessions, Me.** A bell on Home opens Notifications (5.10). **Me** holds Library, Notes, Credits, Profile and twin, Settings and Help. Panels for features that are not live are hidden, not greyed.

### **5.2 Home (S-04)**

Greeting and a search bar. Sections in order: **Answers waiting** (new coach answers; only when there are some); **Continue watching**; **For you** (AI match on the user's twin, labelled "Matched to your profile", in `accent.ai`, CAP-05); **New from PI**; **Shared with you**; a **CreditChip**. There is no briefing, no agent card and no stats tiles (CAP-09 is Phase 2; CAP-12 and CAP-23 are unscheduled).

### **5.3 Videos: search and categories (S-05, S-06)**

* Search by text or by category. When the client's terminology expanded the query: "Showing results for *customer retention* and *churn*, in *Client*'s terms."
* Results are VideoRows with the matching approved insight and a tap-to-jump timestamp.
* Category page: global categories and the client's own.
* No results: "Nothing on that yet. Try a broader term, or ask a coach." with an Ask button.
* There is no SME page. The interviewing coach is shown instead; tapping them opens the coach profile.

### **5.4 Video detail (S-08)**

Player on top (YouTube embedded player; landscape interviews play full screen when the phone is turned). Tabs: **Notes | About | Insights.**

* **About:** summary, interviewing coach (CoachCard), categories.
* **Insights:** the approved insights for this video, each with its time; tapping seeks the player.
* Action row: Save for later, Favourite, Share (to a colleague in the same client), Add note at the current time.
* Watched at 80% or more; position saved every 15 seconds.
* There is no "Ask a coach about this video": a coach sees only the question, first name, role, shared twin fields and client summary (BR-71). A transcript tab is not shown (UI-OPEN-08).
* The iPhone has no Picture-in-Picture for the embedded player; offer "Keep watching on YouTube".

### **5.5 Library, notes, sharing (S-09, S-10, S-12)**

Under **Me.** Library: Saved, Favourites, Watched. Notes grouped by video; tap to jump to the moment; export as Markdown through the share sheet \[P\] (UI-OPEN-03). Sharing sends a video to a named colleague in the same client; **there are no public share links** in the app (T-08). A shared video appears under "Shared with you".

### **5.6 Credits (S-23, S-25; CAP-25, CAP-24)**

**Me, Credits.**

* **Available to you:** the CreditChip figure, and the allowance meter "Used 4 of 12."
* **History** in plain language: "Question to Alex Moreno: 1 credit reserved." "Answer received: 1 credit spent." "Question deleted: 1 credit returned." "Session cancelled: 3 credits returned."
* **Request more credits** at any time and automatically offered when an action is blocked. The CreditRequestSheet shows the state of an open request and the outcome of a decided one (T-04, G-13).
* **Two ways to be blocked** (T-04), each with its own message (9.2):
  * *Allowance reached:* the user has used their limit. Offer "Request more credits".
  * *Organisation out of credits:* the client's pool is empty (BR-83). The user cannot send new requests until PI adds credits; offer "Request more credits" too.
* The user never sees the client's pool figure or other users' use.
* There is no top-up and no payment screen (Phase 4, CAP-19).

### **5.7 Ask a coach (S-20, S-21; CAP-27, CAP-31, CAP-11)**

The user flow follows Business 1.2 and 5.5 step for step.

1. **Write the question.** A text box with the prompt "What would you like to ask a coach?"
2. **Refine with AI.** A conversation view (ConversationView). A banner: "I help you word your question. I don't answer it. A coach will." The AI asks clarifying questions and proposes final wording. The user can edit and reply, or **start over**, which discards the conversation (BR-36). A draft left for 24 hours is deleted \[P\]; until then "Continue your draft" appears on Ask.
3. **Review and split.** If the question contained several, QuestionSplitReview shows one card each. The user edits, keeps or drops each. **There is no merge** (BR-67). Each question will be charged separately; the screen says so.
4. **Safety check.** On Confirm the wording is screened. If flagged, a **SafetyCard** replaces the flow and nothing is sent (5.7.1).
5. **Choose coaches.** CoachPicker: three suggestions, each with "why suggested", plus coach search. Unavailable coaches are shown as Unavailable and cannot be selected (BR-80). Up to 3 coaches per question \[P\]. For several questions, the same coaches apply to all by default and can be changed per question \[P\].
6. **What your coach will see.** ShareContextPanel. The user confirms. "Your coach will see only what's shown here. Your notes stay private."
7. **Cost and credit check.** CostConfirm lists each question and coach and the total, for example "2 questions to 1 coach: 2 credits." Shows "Available to you: 4 credits." If the user has enough, **Submit** is active: "This will reserve 2 credits. They come back if a coach declines, or if you delete the question before it is answered." If not, **Submit is disabled**, the reason is shown (allowance reached, or organisation out of credits) and **Request more credits** is offered (BR-69).
8. **Sent.** A confirmation and the question appears under My questions.

#### **5.7.1 If the safety check flags the question**

SafetyCard: a calm message, crisis resources, and the client's own support resources (captured at onboarding, Business 10). The question is not sent and no credits are used. The card does not say "flagged by an administrator". Whether to tell the user that PI is notified is UI-OPEN-13 (G-34). Copy needs clinical and legal review before launch (9.2).

#### **5.7.2 My questions (S-21)**

Segments **Open** and **Answered.**

* **Open:** a QuestionCard per question showing each coach and "Open 3 days." Nothing says it will expire. Actions: **Delete** (the confirm says "This returns your reserved credits and the coach will no longer see it."). If a coach declined: "Alex couldn't answer. 1 credit returned. Choose another coach," which adds a new request and charges again after a credit check. Whether the user sees the coach's reason is UI-OPEN-14.
* **Answered:** each answer as an **AnswerPlayer**: captions on, speed control, transcript. Actions: Share inside your organisation, Report a problem, Delete (the confirm says "Credits for answered questions stay spent"). **No rating, no follow-up and no "add to library"** (CAP-34 is Phase 2, G-09, D-18). To follow up, ask a new question.
* Several coaches: each coach's answer is listed under the question as it arrives.

### **5.8 Notifications (S-22; CAP-29)**

A list from the bell on Home. Items: new videos; answers to your questions; session booked, cancelled and reminders; you are out of credits; the outcome of a credit request (Business 5.4). Push is opt-in; push and email carry titles only (Tech 11).

### **5.9 One-on-one (S-24; CAP-28, CAP-33, CAP-35)**

1. **Sessions** tab: Upcoming and Past, and a **Book a session** button.
2. **Find a coach.** The user can say what they want to talk about, in a short line or by category, which feeds the shortlist (BR-77) \[P\]. The app shows three suggestions with reasons, and search. Unavailable coaches are shown as Unavailable and cannot be booked.
3. **Coach profile.** Headshot, bio, specialties, availability.
4. **Length.** LengthPicker: 20, 40 or 60 minutes with 3, 5 or 8 credits (client prices). A length the user cannot afford is disabled with the reason. With 4 credits available, only 20 minutes can be chosen (BR-69).
5. **Slot.** SlotPicker with the time-zone label, from the coach's connected calendar.
6. **Note to coach** (optional) with the ShareContextPanel \[P\].
7. **Cost.** CostConfirm: "This will reserve 3 credits. They come back if you cancel." The user can request more credits if blocked.
8. **Booked.** Instant booking \[P\] (G-11): the session is confirmed at once, added to the user's calendar if connected (otherwise an invite is emailed), and the coach is notified.
9. **Session detail:** time, coach, length, credits, **meeting link** supplied by the coach, **Add to calendar**, **Reschedule** (opens the reschedule page, ADR-025), **Cancel** ("Cancel this session? 3 credits come back."). Past sessions: Report a problem.
10. **The call happens outside PIapp** on the client's conferencing app (Zoom, Teams, Slack). "Join" opens the link. PIapp does not record (BR-76). Reminders by push 24 hours and 15 minutes before \[P\].

### **5.10 Profile, twin and settings (S-13, S-15)**

Under **Me.** Headshot and bio; digital twin (role, goals, style) with a preview "How a coach will see you"; the default twin fields to share with coaches; calendar connection; notification settings; privacy notice; Help and Report a problem; Sign out. There is no memory page, MCP page or briefing setting.

---

## **6. Coach experience (iPhone)**

Coaches use the same app. The role selects tabs **Inbox, Sessions, Dashboard, Profile.** The accent is `accent.coach`. A coach sees only their own work: never another coach's questions or earnings (BR-72, BR-74).

### **6.1 Inbox (K-02; CAP-29)**

Requests for a video answer, oldest first, each with how long it has been open. Session bookings and cancellations. Notices from PI. Unread count on the tab. Notifications by push and email.

### **6.2 Question detail (K-03)**

Shows exactly what BR-71 allows: the question, the asker's first name and role, the twin fields they chose to share, and a short summary of their organisation. Nothing else; no history, notes or other questions. Buttons: **Record answer** and **Decline.** Decline requires a reason (BR-72) and says "The user's credit is returned and PI is told." A reminder of the boundaries (Business 10) and a link to the **named PI contact** for escalation and to **Report a problem** (G-17).

### **6.3 Record answer (K-03)**

1. **Record** in portrait. A countdown ring shows 3:00 and the recording stops at the limit. Guidance on light, sound and framing is shown first (R-07).
2. **Preview.** Play it back.
3. **Trim.** Drag start and end. **Trimming is the only editing** (D-06, G-22). Nothing else is offered.
4. **Re-record** any time before upload.
5. **Upload.** Progress bar; it resumes if the connection drops; the coach can leave the screen while it uploads.
6. **Captions.** Shown as "Captions are being added." The coach can mark the answer complete when captions are ready, or have failed and a transcript is provided \[P\] (G-22).
7. **Mark complete.** Confirms: "Send this answer? You'll earn 0.2 credits." The earning is shown in credits to two decimals (T-03).

### **6.4 Sessions (K-04)**

Upcoming and Past. Session detail: the user's first name and role, the length, the credits, the time, the meeting link (the coach's own), the note from the user if any. Actions: Join, **Mark complete** (after the session), **Mark no-show** \[P\], **Cancel** ("The user's credits are returned"), Reschedule. The coach sees the user's first name and role only.

### **6.5 Profile and availability (K-01)**

* Headshot, bio, digital twin (specialties, style, experience). Edits to what users see are reviewed by PI Admin \[P\].
* **Available / Unavailable switch** (vacation mode), prominent at the top. Beneath it: "While you are unavailable you won't be suggested, can't be chosen for new questions and can't be booked. Questions already sent to you stay open and sessions already booked stand" (BR-80).
* **Your share:** "You earn 20% of the credit value for each answer and session." Read only; only PI Admin can change it (BR-65).
* **Calendar:** connect Google or Microsoft; weekly availability windows; buffer; minimum notice.
* **Default meeting link** \[P\].
* Notification settings; code of conduct; the PI escalation contact.

### **6.6 Dashboard (K-05; CAP-26)**

**Credits earned** (this month and all time), **question and answer history**, **session history**, and **views of your interview videos** (Business 5.3). Earnings are in credits; payouts are manual outside the app until Phase 4 (G-05, CAP-22). No ratings (Phase 2).

## **7. PI Admin website (CAP-01 to CAP-03, CAP-18, CAP-30, CAP-32, CAP-38)**

The PI team runs PIapp for everyone in Phase 1. The site is for PI Admin only. Sidebar: **Dashboard, Clients, Users, Coaches, Videos, Categories, Terminology, Credits, Questions, Skills, Reports, Settings, Audit log, Backup.** Every save that changes money, access or content writes an audit entry.

* **Dashboard (A-01):** users, credit usage, questions, answers, sessions; notifications (a coach declined, a credit request, a client at 10, 5 or 0 credits, a safety flag, a takedown countdown). Per client: sign-ups and credit usage. Per coach: answers, sessions, credits earned.
* **Videos (A-02, CAP-01):** list and **import by YouTube URL**. The editor holds: interviewing coach, categories, summary, transcript upload (VTT, SRT, TXT), the **SME release date** (BR-57), status. A **PublishChecklist** shows the guards live: coach, category, summary, "3 approved insights (2 of 3)", release date. Publish is disabled until all pass (BR-02, BR-03). A warning, not a block, when a video is outside 10 to 20 minutes or not landscape (BR-09). Change history. There is **no SME record and no per-client visibility** (BR-05 retired).
* **Insights review (A-08, BR-06):** a queue of `generated` insights. Each InsightReviewCard shows the text, the transcript excerpt, start and end, and a jump to that moment in the video. Approve, reject, or edit then approve. Bulk approve is available for a selection the reviewer has read \[P\]. Withdrawn and rejected insights stay visible with the reason. A **takedown** countdown (5 working days to review, 7 days to remove) appears for any SME request (BR-54).
* **Categories (A-04, CAP-02):** two-level tree; global and client-specific; merge and archive.
* **Terminology (A-17, CAP-38, BR-11):** two tabs: PI App and Client. CSVImport with a preview of lines to add and update; each line editable; a client line overrides an app line with the same term (G-30).
* **Clients (A-05, CAP-03):** a workspace with tabs:
  * *Overview:* term dates, sponsor, status.
  * *Users (A-06):* invite by email or CSV; each person gets an **invite code** (BR-21); deactivate; no join code.
  * *Backstory:* sections and document upload; Draft, Send to Sponsor for approval, Published with approver and date and the written approval attached (BR-13).
  * *Terminology and Categories:* the client's own.
  * *Credits:* pool balance, allocate credits (no minimum, BR-61), adjust with a required reason (BR-64), credit requests queue, alerts at 10, 5, 0, a ledger search.
  * *Settings:* user credit limit (default 12), credits per question and per session length (defaults 1, 3, 5, 8), the client's staff-support resources shown by the safety card, public share links (off). Every change goes through **SettingsDiff** (BR-82).
  * *Reports.*
* **Credit requests (in A-16):** each request shows credits asked, the user's remaining allowance and the client's pool; the approver sees **counts only**, never what the credits bought (BR-66). Approve (default step of 12 \[P\]) or decline; a note to the user. If the pool is short, a link allocates credits to the client first (T-10).
* **Coaches (A-14, CAP-30, BR-70):** invite; a vetting pipeline *invited, approved, active* with a checklist (profile complete; interview videos published, 10 per coach \[P\] G-03; code of conduct accepted); coach percentage (default 20%, via SettingsDiff); suspend or remove; availability and open requests shown read only.
* **Questions (A-15):** open requests by age with **no question text**; declined requests with the coach's reason; safety flags (who, when, no text); problem reports; withdraw an answer (G-17). To read a question or answer, **ReasonDialog** is required: reason code (support, safety, dispute) and a note, and the access is logged (BR-40, G-16). PI Admin can never open a user's notes, twin or AI conversation.
* **Skills (A-09, CAP-11):** the playbooks the AI follows to refine questions, with a test panel. Skills are about question refinement only.
* **Reports (A-07, CAP-18):** platform and per-client dashboards using the Business 12 measures (G-24); **Sponsor report**: pick client and month, generate a branded PDF to send. Totals are always shown; breakdowns only for groups of 5 or more (BR-41, G-15 \[P\]).
* **Settings (A-18):** app defaults: credit value, default user limit, default prices, default coach percentage, the PI escalation contact, and the extraction clearance flag (Tech 4.4). Each change is audited.
* **Audit log (A-19, CAP-32):** every administrator action, filterable, including content-access entries with reason codes.
* **Backup and restore (A-20, CAP-32):** backup status and the last restore test; a "request restore" action that notifies engineering \[P\].
* **Phase 4:** Billing (A-11) and Payouts (A-13).

---

## **8. Client Admin console and Sponsor dashboard (Phase 3)**

Not designed in detail in this version: Phase 3 is scheduled after the MVP trial. What carries over from v2.1, re-baselined:

* **Same shell as PI Admin, client-scoped**, client logo in the header. Sidebar: **Overview, Users, Backstory, Terminology, Credits, Analytics.** Sign-in for Client Admin and Sponsor is switched on in Phase 3 (Tech 3.1).
* **Users:** invite codes, deactivate, make Client Admin. Banner: "You can manage accounts. You can't see anyone's activity, questions or notes."
* **Credits:** the client's pool and prices (read only; PI Admin changes them), usage by service, **credit requests** (G-14), and the balance alerts that PI Admin receives in Phase 1 (BR-83).
* **Analytics:** aggregate only, minimum group of 5, topics de-identified with counts and never quotes (BR-41, BR-43, BR-75).
* **Sponsor dashboard (C-03):** one page for a CxO: active users against seats, what people ask about (de-identified), credit use, backstory status. Banner: "You see organisation-wide patterns only. Individuals' activity is private" (BR-42). Sponsor as a user of the iPhone app is CAP-37.
* **Safety flags in Phase 3:** what a Client Admin sees about a flag is undecided (G-34).
* Removed from v2.1: the SME portal, agent and memory settings, and the user top-up setting until Phase 4.

---

## **9. States, voice, notifications, accessibility**

### **9.1 States**

Every screen defines loading, empty (one action), error (what happened and a retry), offline and permission-denied states. The recorder and the upload define their own states: recording, previewing, uploading, resumed after a drop, processing, captions pending, ready, failed.

### **9.2 Voice and copy**

Plain, warm, direct; no hype or emoji; client terms where terminology has them. The AI never claims to be a person or a coach. Credit copy always states the amount and what comes back.

| Situation | Copy |
| ----- | ----- |
| No search results | "Nothing on that yet. Try a broader term, or ask a coach." |
| AI role | "I help you word your question. I don't answer it. A coach will." |
| Before sending to a coach | "Your coach will see only what's shown here. Your notes stay private." |
| Reserving credits | "This will reserve 2 credits. They come back if a coach declines, or if you delete the question before it is answered." |
| Allowance reached | "You've used your allowance of 12 credits. You can ask for more." |
| Organisation out of credits | "Your organisation's credits have run out, so you can't send new requests right now. You can ask for more." |
| Delete an open question | "Delete this question? Your reserved credits come back and the coach won't see it." |
| Delete an answered question | "Delete this question? Credits for answered questions stay spent." |
| A coach declined | "Alex couldn't answer this one. 1 credit has been returned. Choose another coach if you'd like." |
| Question still open | "Open 3 days" (never "expires" or "overdue" to the user) |
| Cancel a session | "Cancel this session? 3 credits come back." |
| Coach unavailable | "Unavailable right now" |
| Coach: unavailable switch | "While you are unavailable you won't be suggested, can't be chosen for new questions and can't be booked. Questions already sent to you stay open and sessions already booked stand." |
| Scope | "PIapp is performance coaching. It is not therapy, medical, legal or HR-investigation advice." |
| Privacy \[P\] | "Your notes, twin and question conversations are yours. *Client* sees only anonymous totals. A coach sees only what you choose to send. PI can open a question or answer only for support, safety or a dispute, and every time is logged." |
| Safety card \[P\] | "We can't send this question. If you're struggling, these services can help now:" followed by crisis resources and the client's own support resources |

The privacy and safety copy needs legal and clinical review before launch (G-16, G-17, G-26, G-34).

### **9.3 Notifications**

In-app list and opt-in push; titles only, never question text, answer content or notes. **User:** new videos; answer ready; session booked, cancelled, reminder; out of credits; credit-request outcome. **Coach:** new question request; session booked; session cancelled; reminder to answer after 3 working days \[P\] (G-10). **PI Admin:** a coach declined (with reason); a credit request; a client at 10, 5 or 0 credits; a safety flag raised; takedown countdown; video awaiting review.

### **9.4 Accessibility**

WCAG 2.2 AA on the admin site; Dynamic Type, VoiceOver and Reduce Motion in the iPhone app. Touch targets at least 44 pt. Credit amounts always have a text label. **Captions are required on every coach answer** (not optional). The recorder works with VoiceOver: record, stop, preview, trim and upload are labelled controls; the countdown is announced at 30 and 10 seconds. Status is never colour alone.

### **9.5 Language**

English for v1; strings externalised; times shown with an explicit time zone; credits are unit amounts, not currency. UK or US spelling is UI-OPEN-19.

## **10. Analytics events (UI)**

`search_performed`, `search_zero_results`, `video_opened`, `video_progress`, `video_saved`, `video_favourited`, `video_shared`, `note_created`, `question_started`, `question_split_shown`, `question_submitted` (topic only), `answer_viewed`, `credit_blocked` (reason only), `credit_request_sent`, `session_requested`, `session_booked`, `session_cancelled`, `session_completed`, `coach_available_toggled`, `answer_recorded` (duration only), `safety_card_shown` (count only), `twin_updated`. **No event contains note, conversation, twin or question text.**

## **11. Screen inventory**

Screen IDs from v2.1 are kept where the screen continues, so earlier references still trace. New screens start at S-25, A-17 and K-01 onward.

### **11.1 iPhone app, user**

| \# | Screen | Phase |
| ----- | ----- | ----- |
| S-01 | Invite code and create account | 1 |
| S-02 | Sign in and reset password | 1 |
| S-03 | Onboarding: scope notice, profile, digital twin, privacy, calendar | 1 |
| S-04 | Home | 1 |
| S-05 | Search results | 1 |
| S-06 | Category page | 1 |
| S-08 | Video detail | 1 |
| S-09 | Library | 1 |
| S-10 | Notes | 1 |
| S-12 | Share to a colleague | 1 |
| S-13 | Profile and settings | 1 |
| S-15 | Digital twin | 1 (was 2) |
| S-20 | Ask a coach: write, refine, split, choose coaches, what the coach sees, cost | 1 (was 3) |
| S-21 | My questions and answers | 1 (was 3) |
| S-22 | Notifications | 1 (was 3) |
| S-23 | Credits | 1 (was 3); no top-up |
| S-24 | Find a coach, book, sessions | 1 (was 4) |
| S-25 | Request more credits | 1, new |
| S-26 | Reschedule page (web) | 1, new \[P\], ADR-025 |
| S-11 | Personal stats | 2 |

### **11.2 iPhone app, coach**

| \# | Screen | Phase |
| ----- | ----- | ----- |
| K-01 | Coach registration, profile, availability switch, calendar | 1 (was 3) |
| K-02 | Inbox | 1 (was 3) |
| K-03 | Question detail and record answer | 1 (was 3) |
| K-04 | Sessions | 1 (was 4) |
| K-05 | Dashboard and earnings (in credits) | 1; payouts 4 |

### **11.3 PI Admin website**

| \# | Screen | Phase |
| ----- | ----- | ----- |
| A-01 | Dashboard | 1 |
| A-02 | Videos: import, editor, transcript, publish checklist | 1 |
| A-04 | Categories | 1 |
| A-05 | Clients workspace | 1 |
| A-06 | Users | 1 |
| A-07 | Reports and analytics, sponsor report | 1 |
| A-08 | Insights review | 1 (was 2) |
| A-09 | Skills | 1 (was 2) |
| A-14 | Coaches | 1 (was 3) |
| A-15 | Questions queue, safety, problem reports, takedowns | 1 (was 3) |
| A-16 | Credits and credit requests | 1 (was 3) |
| A-17 | Terminology | 1, new |
| A-18 | App settings and defaults | 1, new |
| A-19 | Audit log and content access | 1, new |
| A-20 | Backup and restore | 1, new |
| A-10 | Coach quality (ratings) | 2 |
| A-11 | Billing | 4 |
| A-13 | Payouts | 4 |

### **11.4 Phase 3**

| \# | Screen | Phase |
| ----- | ----- | ----- |
| C-01 | Client Admin console | 3 |
| C-03 | Sponsor dashboard | 3 |
| C-02 | Client Admin billing | 4 |

### **11.5 Retired and unscheduled**

| \# | Screen | Status |
| ----- | ----- | ----- |
| S-07 | SME page | Retired: SMEs are not stored (BR-57) |
| A-03 | SMEs | Retired |
| A-12 | SME portal invites and approvals | Retired |
| E-01 to E-03 | SME portal | Retired |
| S-14 | Agent home and conversation | Unscheduled (CAP-12) |
| S-16 | MCP connections | Unscheduled (CAP-13) |
| S-17 | Memory | Unscheduled (CAP-17) |
| S-19 | Weekly briefing | Unscheduled (CAP-23) |
| S-18 | iOS app | Not a screen: the iPhone app is the product |
| M-01 | Android app | Unscheduled (CAP-20) |

## **12. Open UI questions**

| ID | Question | Recommendation |
| ----- | ----- | ----- |
| UI-OPEN-01 | Palette and type checked against the PI logo and the live site? Are the coach and credit accents acceptable? | Designer review before Phase 1 build |
| UI-OPEN-02 | Body font Inter or Krub? | Inter body, Krub headings |
| UI-OPEN-03 | Export notes? | Yes, Markdown through the share sheet |
| UI-OPEN-05 | Admin console light or dark? | Light, with a toggle |
| UI-OPEN-07 | Client co-branding depth | Logo and name only in v1 |
| UI-OPEN-08 | Transcript tab visible to users? | Not in the MVP; depends on the SME release scope (BR-57) |
| UI-OPEN-13 | When a question is flagged, do we tell the user that PI is notified? (G-34) | Yes, in the privacy notice and the SafetyCard, subject to legal review |
| UI-OPEN-14 | Does the user see the reason a coach declined? | No: PI Admin sees it; the user sees a neutral message and can choose another coach |
| UI-OPEN-15 | iPad layout? | None in the MVP; runs as an iPhone app |
| UI-OPEN-16 | Reschedule page: a web page opened from a link, or in-app only? (ADR-025) | Web page with a Universal Link into the app |
| UI-OPEN-17 | Should users see their allowance and the pool, or one "available" figure? (T-04) | One figure, with the reason shown only when blocked |
| UI-OPEN-18 | What does a coach card show without ratings or response time? | Specialties, availability and the suggestion reason |
| UI-OPEN-19 | UK or US spelling? The pilot client and data residency are US | Decide with Jez; strings are externalised |
| UI-OPEN-20 | How does a user pick a colleague to share a video with? | Search by name within the client |
| UI-OPEN-21 | Several questions: choose coaches once for all, or per question? | Once for all, editable per question |

Closed in v3.0: UI-OPEN-04 and UI-OPEN-06 (memory and graph, unscheduled), UI-OPEN-09 (SME portal retired), UI-OPEN-10 (answer length: portrait, under 3 minutes, D-06), UI-OPEN-11 (no agent), UI-OPEN-12 (the user chooses coaches, D-05).

## **13. Self-critique of this draft**

* **Brand not seen first-hand.** The site was a holding page on 22 Oct; tokens are inferred.
* **No wireframes.** The highest-value screens to wireframe first: S-04, S-20 (refine, choose coaches, cost), S-24 (book), K-03 (record), A-02 (video editor with checklist), A-05 (client workspace), A-16 (credits).
* **The recorder is the riskiest screen.** Portrait recording, trimming, resumable upload and captions on a phone need testing on real devices and networks early (R-07).
* **Several flows rest on \[P\] proposals** (instant booking, up to three coaches, reschedule page, step of 12 credits). Layouts will change if those answers change.
* **iPhone only.** Users and coaches without an iPhone have no app (G-21).
* **The admin site carries all client setup** in Phases 1 and 2. The client workspace is built so the Client Admin can reuse it in Phase 3.
* **Privacy and safety copy is a draft** and needs legal and clinical review.

## **14. Change log**

| Version | Date | Change |
| ----- | ----- | ----- |
| 3.0 | 16 Nov 2026 | Re-baselined to Business Spec v5.0. iPhone app for users and coaches plus PI Admin website (D-08); user and coach experiences in Phase 1; credit check, credit requests and per-client prices in the flows (BR-69); question never lapses, copy updated (D-14); AI question refinement with split and no merge (BR-35, BR-67); coach suggestions and availability switch (BR-77, BR-80); SME pages and portal removed (BR-57); no agent, briefing, memory, MCP, stats, ratings or top-up in Phase 1; PI Admin site rebuilt around Business 5.2; screen inventory re-numbered; open UI questions re-based; Appendix A traceability; Appendix B reconciliation log |
| 2.1 | 22 Oct 2026 | Merged v1.2 with the 16 Oct revised spec: registration flows, dashboards, weekly briefing, Ask a coach, one-on-one, credits and top-up, inbox, coach portal, new tokens and components, PI Admin coaches, Q&A and credits |
| 1.2 | 27 Sep 2026 | SME portal and revenue-share screens |
| 1.1 | 27 Sep 2026 | Sponsor surfaces |
| 1.0 | 27 Sep 2026 | First draft |

---

## **Appendix A. Traceability: Business Spec v5.0 to this spec**

### **A.1 Capabilities**

| ID | Capability | Phase | Screens and sections |
| ----- | ----- | ----- | ----- |
| CAP-01 | Asset management and insights | 1 | A-02, A-08; 7 |
| CAP-02 | Category management | 1 | A-04; 7 |
| CAP-38 | Terminology management | 1 | A-17; 7 |
| CAP-03 | Client onboarding | 1 | A-05, A-06; 7 |
| CAP-04 | Authentication | 1 | S-01, S-02, K-01; 4 |
| CAP-05 | Video search and AI match | 1 | S-04, S-05; 5.2, 5.3 |
| CAP-06 | Personal library | 1 | S-09; 5.5 |
| CAP-07 | Share inside the client | 1 | S-12; 5.5 |
| CAP-08 | Notes | 1 | S-08, S-10; 5.4, 5.5 |
| CAP-09 | Personal stats | 2 | S-11 (not designed) |
| CAP-10 | Insight graph | Unscheduled | No screen |
| CAP-11 | Skills | 1 | A-09, S-20 (refinement); 5.7, 7 |
| CAP-12 | Coach agent | Unscheduled | No screen (S-14 retired to unscheduled) |
| CAP-13 | MCP server | Unscheduled | No screen (S-16) |
| CAP-14 | Digital twin | 1 | S-03, S-15, K-01; 4, 5.10 |
| CAP-15 | iPhone app | 1 | All S- and K- screens; 1.2 |
| CAP-16 | Client Admin portal | 3 | C-01; 8 |
| CAP-17 | Conversation memory | Unscheduled | No screen (S-17) |
| CAP-18 | Analytics | 1, 3 | A-01, A-07, C-03; 7, 8 |
| CAP-19 | Billing | 4 | A-11, C-02 |
| CAP-20 | Android app | Unscheduled | M-01 |
| CAP-22 | Payouts | 4 | A-13, K-05 |
| CAP-23 | Weekly briefing | Unscheduled | No screen (S-19) |
| CAP-24 | Registration, profile, credit history | 1 | S-03, S-13, S-23; 4.1, 5.6 |
| CAP-25 | Credits | 1 | S-20, S-23, S-24, S-25, A-16, A-18; 5.6, 5.7, 7 |
| CAP-26 | Coach accounts | 1 | K-01 to K-05; 6 |
| CAP-27 | Q&A | 1 | S-20, S-21, K-02, K-03; 5.7, 6 |
| CAP-28 | One-on-one | 1 | S-24, K-04; 5.9, 6.4 |
| CAP-29 | Inbox and notifications | 1 | S-22, K-02, A-01; 5.8, 6.1, 9.3 |
| CAP-30 | Coach vetting | 1 | A-14; 7 |
| CAP-31 | Safety screen | 1 | S-20 (SafetyCard), A-15; 5.7.1, 7 |
| CAP-32 | Backup, restore, audit log | 1 | A-19, A-20; 7 |
| CAP-33 | Calendar connection | 1 | S-03, S-13, K-01; 4, 6.5 |
| CAP-34 | Ratings | 2 | A-10 (not designed) |
| CAP-35 | Call booking and calendar sync | 1 | S-24, S-26, K-04; 5.9 |
| CAP-36 | MVP feedback backlog | 2 | Not a screen |
| CAP-37 | Sponsor as user | 3 | The iPhone app with the sponsor role; no new screen |

### **A.2 Business rules**

Rules with a user-visible effect:

| ID | Where |
| ----- | ----- |
| BR-02, BR-03 | A-02 PublishChecklist; 7 |
| BR-04 | Player (3); 5.4 |
| BR-06, BR-07 | Insights tab 5.4; A-08; 7 |
| BR-08 | S-02; 4.3 |
| BR-09 | A-02 warning; 7 |
| BR-10 | Client summary in ShareContextPanel; 5.7, 6.2 |
| BR-11 | Terminology notice 5.3; A-17; 7 |
| BR-13 | A-05 Backstory; 7 |
| BR-21, BR-25 | S-01, K-01; 4; A-06, A-14 |
| BR-22 | A-06 deactivate; 7 |
| BR-23 | S-12; 5.5; public links off (A-05 Settings) |
| BR-35 | AIBubble label and banner; 3, 5.7 |
| BR-36 | Start over and draft retention 5.7 |
| BR-38 | SafetyCard; 5.7.1 |
| BR-40 | ReasonDialog; A-15; 7 |
| BR-41, BR-43, BR-75 | Reports; 7, 8 |
| BR-42 | Sponsor dashboard banner; 8 |
| BR-54 | Takedown countdown; A-08; 7 |
| BR-57 | No SME screens; 1.1, 5.3; release date A-02 |
| BR-60, BR-61, BR-68 | A-16 allocation; 7 |
| BR-62, BR-63 | CostConfirm; 9.2 copy; 5.7, 5.9 |
| BR-64 | Required reason on adjustment; A-16 |
| BR-65 | "Your share" 6.5; A-14 |
| BR-66, BR-69, BR-83 | CostConfirm, CreditRequestSheet, credit requests; 5.6, 5.7, 7; low-balance notices 9.3 |
| BR-67 | QuestionSplitReview; 5.7 |
| BR-70 | A-14 vetting; 4.2 |
| BR-71, BR-72, BR-73, BR-74 | ShareContextPanel, CoachPicker, AnswerPlayer; 5.7, 6.2 |
| BR-76 | No recording; 5.9 |
| BR-77, BR-78, BR-80 | 5.7, 5.9, 6.5; AvailabilityBadge |
| BR-81 | Delete confirms; 5.7.2, 9.2 |
| BR-82 | SettingsDiff; 7 |

Rules with **no user-visible effect** (backend only): BR-01, BR-12, BR-20, BR-24, BR-37.

Rules **retired** in Business v5.0, with nothing built: BR-05, BR-30, BR-31, BR-32, BR-33, BR-34, BR-50, BR-51, BR-52, BR-53, BR-55, BR-56, BR-79.

---

## **Appendix B. v2.1 reconciliation log**

Every place UI Specification v2.1 disagreed with Business Spec v5.0, and what v3.0 does.

| # | v2.1 said | Business v5.0 says | v3.0 |
| ----- | ----- | ----- | ----- |
| 1 | User web app first, iOS Phase 3, Android Phase 4 | iPhone app is the MVP (D-08, CAP-15); no user web app | iPhone app Phase 1; Android unscheduled (1.2) |
| 2 | Hosts `app.`, `experts.`, `coach.` | PI Admin website only | `admin.` only |
| 3 | Q&A Phase 3, one-on-one Phase 4, inbox Phase 3, coach portal Phase 3 | All Phase 1 | Phase 1 (11) |
| 4 | Coach portal on the web | Coaches use the iPhone app (D-08) | Coach experience in the app (6) |
| 5 | SME chip, SME page, SME portal, SME earnings | SME appears in videos only and is not stored (BR-57) | Removed; interviewing coach shown instead |
| 6 | Agent home, conversation, ChatThread, CitationCard, ContestedBanner, skills chips, "Ask the coach" cards | Agent unscheduled; the AI only refines questions (BR-35) | Removed; AI refinement conversation with a clear label (5.7) |
| 7 | Weekly briefing, BriefingCard, briefing settings | Unscheduled (CAP-23) | Removed |
| 8 | MCP connections page; memory page | Unscheduled | Removed |
| 9 | Home had briefing, agent card, "Short takes", "Featured experts" | No such capability | Home rebuilt (5.2) |
| 10 | Dashboard tiles: conversations, coaching questions, sessions, credits spent | No agent; stats are Phase 2 | Credits chip, lists (5.2, 5.6) |
| 11 | Stats tab | Personal stats Phase 2 (CAP-09) | Removed from Phase 1 |
| 12 | "Match me automatically" coach choice | Three AI suggestions or search; the user chooses (D-05) | CoachPicker (5.7) |
| 13 | CoachCard shows rating, response time and price | Ratings Phase 2; same prices for all coaches (G-29) | Specialties, availability, reason |
| 14 | Copy: "Refunded if not answered within 5 working days" | A question never lapses (D-14, BR-62) | Credits return only on decline, delete or cancel (9.2) |
| 15 | Question status Submitted, Matched, Answered with a due date; cancel before the coach accepts | Requested, answered, declined, deleted; no due date | QuestionCard shows age only (5.7.2) |
| 16 | "Ask a follow-up" as a paid linked question; rate helpful; "Request to add to library" | No threads (G-09); ratings Phase 2; answers never in the library (D-18) | Removed; ask a new question |
| 17 | "Ask a coach about this video" with the video attached | A coach sees only what BR-71 lists | Removed |
| 18 | Single-step cost confirmation with a spend preview | Credit check before submission; two blocked states; credit requests (BR-69) | CostConfirm and CreditRequestSheet (5.6, 5.7) |
| 19 | Top-up sheet and Stripe | Billing Phase 4 | Removed from Phase 1 |
| 20 | One-on-one lengths implied 30 and 60; request then coach confirms; recording consent | 20, 40, 60; calls outside PIapp; no recording (BR-76, BR-78) | LengthPicker 20, 40, 60; instant booking \[P\]; no recording |
| 21 | Cancellation window shown | A session can be cancelled at any time and is refunded (BR-78) | No window; cancel any time |
| 22 | Registration via invite or client join code, client profile step, SSO | Invite code only (BR-21); no client profile step in v5.0 | Invite code only (4.1) |
| 23 | Coach registration at the end of a web flow, with rate tier | Coach by invitation; vetted; same prices | 4.2; no tier |
| 24 | Coach availability weekly slots and pause until a date | Available / unavailable switch (BR-80); calendar connected | Switch plus windows (6.5) |
| 25 | Answer up to 5 minutes, either orientation, browser recorder | Portrait, under 3 minutes, crop only (D-06) | VideoRecorder 6.3 |
| 26 | Coach cannot read question content except where the user flags a problem | PI Admin may open content for support, safety or dispute with a reason code (BR-40) | ReasonDialog (7) |
| 27 | PI Admin Q&A queue with due dates and reallocation | No due dates; no reallocation | Open requests by age (7) |
| 28 | PI Admin Earnings and SME tabs | SMEs not paid; payouts Phase 4 | Payouts Phase 4 only |
| 29 | Admin Clients tab included join code, coach enabled, memory enabled, user top-up | Not in v5.0 | Replaced by credit limit, prices, support resources (7) |
| 30 | Copy: "Your conversations and notes stay private" before sending to a coach | Coach sees only BR-71 items | "Your notes stay private" (9.2) |

