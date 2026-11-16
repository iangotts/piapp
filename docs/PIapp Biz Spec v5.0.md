# **PIapp — Business Specification v5.0**

|  |  |
| ----- | ----- |
| Product | PIapp — Performance Intelligence app |
| Owner | Ian Gotts, for Jez Cartwright / Performance Intelligence |
| Version | 5.0, 13 Nov 2026 |
| Status | DRAFT for review. §1–5 carry the content validated by Jez and Ian in v3.0, with fuller detail and clearer wording. §6–15 are rewritten to follow §1–5. Appendix A is the gap register |
| Companion specs | PIapp-UI-Spec-v2.1.md and PIapp-Technical-Spec-v2.1.md. Both pre-date this version and need re-baselining to it (see §15) |
| Supersedes | v4.0 (12 Nov), v3.0 (28 Oct) and v2.1 (22 Oct) |

**How to read this version**

* Every decision validated in v3.0 §1–5 is kept. Where wording is expanded, the meaning is unchanged.  
* **\[P\]** marks a proposal that is not yet confirmed. Detail that Jez and Ian confirmed in review has had the marker removed.  
* **(G-nn)** points to a gap in Appendix A: an error, inconsistency or undecided item.  
* **Numbering fix.** v3.0 had no §5, and "Functionality" was numbered 6\. Functionality is now §5 and Capabilities is §6. Cross-references in other documents to "§6.x Functionality" now point to §5.x.

---

## **1\. Executive summary**

### **1.1 What PIapp is**

Jez Cartwright's Performance Intelligence (PI) coaching is high-touch, one-to-one work with CxOs at large corporations. It does not scale down the organisation, and that is where the need has grown. AI-driven flattening is removing the middle managers who used to coach junior staff and translate the business for them. Those staff now turn to general-purpose AI, which gives generic, context-free and often wrong advice.

PIapp packages Performance Intelligence for every level of a client organisation. It is a **two-sided marketplace**:

* **Coaches** get access to client work with very little friction.  
* **Clients** can offer their employees cost-effective coaching.

It is a **B2B product**. The buyer is usually a CxO whom Jez already coaches (the **Sponsor**). The organisation is the **Client**. Its employees are the **Users**. Coaches are vetted PI coaches who serve users from any client.

### **1.2 The three services**

PIapp offers three services. Services 2 and 3 are paid for with a common currency, **credits** (§1.4). Service 1 is free.

**Service 1: Content.** Users search the PI **expert-interview video** library, hosted on YouTube, using the client's own categories and terminology. They can save, favourite, share and add notes to videos. Users must be logged in. There is no credit cost.

**Service 2: Q\&A (video answers from a coach).**

1. The user types a question in the app.  
2. An AI conversation validates the question. It checks that the question is not ambiguous. If the user has packed several questions into one, it splits them into separate questions. The AI clarifies and refines; it does not answer. The user confirms the final wording, sees the credit cost, and the question passes the safety screen in §10 before anything is sent.  
3. The user chooses one or more coaches, either by searching for them or by accepting AI suggestions. The AI suggests three coaches who match the question; the user may select one or more of the three, or search for others.  
4. Each chosen coach is notified. The question stays **open until a coach answers it, or until the user who submitted it deletes it**. It never lapses.  
5. Each coach records a **video answer** on their phone: portrait orientation, under 3 minutes, cropping only (no editing). The coach uploads it in the app and marks the question complete.  
6. The user is notified and watches the answer in the app.

**Service 3: One-on-one.** The user is matched with a coach (by search or AI suggestion), sets up a call and books it. The coach is notified of the call. The call is held outside PIapp on the corporate video-conferencing or meeting app (for example Zoom, Teams or Slack). The coach conducts the call and closes it in the app when it is complete. Calls are 20, 40 or 60 minutes.

### **1.3 Who does what**

| Who | In one line |
| ----- | ----- |
| Sponsor | The CxO who buys PIapp credits for the client, agrees to promote PIapp to its users, and owns it executively |
| Client | The customer organisation; holds the credit pool, backstory and terminology |
| User | An employee of the client who uses PIapp for their own development |
| Coach | A vetted PI coach who answers questions by video and runs one-on-one calls |
| SME | A subject-matter expert interviewed in a library video. Appears in the video only: not a user, no account, no portal, not compensated, and **not stored in PIapp** |
| PI Admin | The PI team, who run PIapp for everyone in Phase 1 (the "concierge" model, §5.1) |

### **1.4 Credits and payment**

| Item | Rule |
| ----- | ----- |
| Credit value | A credit costs **\$50** |
| Client credits | The client has a **pool of credits** that its users draw on. **MVP: no minimum purchase; PI Admin allocates the credits.** (v3.0's \$10,000 / 200-credit minimum is not applied in the MVP; whether it returns with billing in Phase 4 is G-12) |
| User allowance | A user may spend up to **12 credits** (the default) before approval is needed to spend more. The default can be overridden for each client |
| Credit check | Every action that costs credits is checked **before it can be submitted**. If the user does not have enough credits for its full cost, the request cannot be submitted. The user can instead **request more credits**, which notifies the Client Admin (in the MVP, PI Admin) |
| Coach share | The coach receives **20%** (the default) of the credit value for each question answered and each session conducted. The default can be overridden for each coach |
| Content | Free (login required) |
| Q\&A | **1 credit** (default) per question answered by one coach. The same question sent to two coaches costs 2 credits |
| One-on-one | **20-minute call: 3 credits. 40-minute: 5 credits. 60-minute: 8 credits** (defaults) |

**Example.** A user with 4 credits left can ask up to 4 questions, or request a 20-minute call (3 credits), but cannot request a 40-minute call (5) or a 60-minute call (8). They can request more credits.

Derived price list at the default prices and the default 20% coach share, to make the economics visible:

| Service | Credits | Client pays | Coach earns (20%) |
| ----- | ----- | ----- | ----- |
| Q\&A, one coach | 1 | \$50 | \$10 |
| 20-minute call | 3 | \$150 | \$30 |
| 40-minute call | 5 | \$250 | \$50 |
| 60-minute call | 8 | \$400 | \$80 |

At the default of 12 credits, the allowance is worth \$600 per user. It covers, for example, 12 questions, or four 20-minute calls, or one 60-minute call plus four questions.

**Defaults, overrides and who maintains them \[P for the "who sees" column\]**

| Setting | Default | Held at | Who can update | Who can see |
| ----- | ----- | ----- | ----- | ----- |
| User credit limit | 12 credits | Client | PI Admin | Client (in its profile); each user sees their own credits remaining |
| Credits per question, and per 20, 40 and 60-minute session | 1, 3, 5 and 8 | Client | PI Admin only | Client sees them in its profile; users see the price before confirming |
| Coach share of credit value | 20% | Coach | PI Admin only | The coach sees their percentage in their profile |
| Credit value | \$50 | App | PI Admin | PI Admin |

The defaults are held at app level. Each client carries its own limit and prices, starting from the defaults. Each coach carries their own percentage, starting from the default.

**Phase 1 sizing.** The first client has a team of 50 users and a credit allocation worth **\$25,000**. At \$50 per credit that is 500 credits, about 10 credits per user per year. (v3.0 also assumed 20 credits per user per year, which would be \$50,000; the \$25,000 figure is the one to plan with: G-01.) At about 10 credits per user per year, the default 12-credit limit is above the planned average, so approvals above the limit should be exceptional.

### **1.5 Coach qualification**

* Coaches are vetted and approved by the Performance Intelligence team. For the MVP, Jez is the vetting authority.  
* Each coach must record **10 video expert-interviews**. Each is 10 to 20 minutes, landscape, with the coach interviewing an SME. The PI team edits them. (Whether the 10 is per coach or in total needs confirming: G-03.)  
* To launch the MVP, **10 coaches** must be qualified.

### **1.6 Phasing**

**Phase 1: MVP launch**

* First client with a block of credits for a team of 50 users.  
* 10 vetted coaches.  
* iPhone app, the primary interface for users and coaches.  
* PI Admin website for concierge activities:  
  * Set up the client and its users.  
  * Manage coaches and their videos.  
  * Load credits.  
  * Allow a user access to more than the credit limit (12 by default).  
  * Set each client's credit limit and prices, and each coach's percentage.  
  * Report across all of PIapp, and for each client.

**Phase 2: Incorporate feedback from the MVP trial.**

**Phase 3: Client Admin portal.**

**Phase 4: Billing.** Collecting money for credits and distributing money to those who earn it.

Section 6 assigns every capability to a phase.

---

## **2\. Problem and opportunity**

### **2.1 The problem**

* **Coaching scarcity.** One coach can serve only a handful of CxOs. High-touch coaching does not reach the rest of the organisation.  
* **Coaching gap.** The middle-management coaching layer is disappearing as AI-driven flattening removes the managers who coached and translated the business for junior staff.  
* **Bad substitute.** General AI has no knowledge of the company and no proven coaching method. Its advice is generic, context-free and often wrong.

### **2.2 Assets PI already has**

* The **PI YouTube channel**: long-form expert interviews by top performance coaches.  
* A **network of coaches** who can answer questions and coach one-to-one.  
* **Jez's method** and relationships with CxOs, who are the buyers.  
* **Precedent.** Ian's Inspiring Excellence app (Bubble, 2021\) proved the video model.

### **2.3 How PIapp responds**

| Problem | PIapp response |
| ----- | ----- |
| Scarcity | A network of coaches, paid per use in credits, so one request reaches the right coach without a long-term engagement |
| Gap | Content for self-serve learning, plus a named human coach by video or call when content is not enough |
| Bad substitute | Vetted expert content and real coaches, framed in the client's own categories and terminology |
| Cost | Content is free; the client buys one block of credits, and users draw it down only when they need a human coach |

### **2.4 Opportunity**

Sell Jez's method as an **organisational capability**: scalable, self-serve content (and, later, an AI agent) at the base, with human coaches, paid per use, on top.

---

## **3\. Vision and positioning**

**Vision.** Every person in a client organisation has coaching that knows their company, from the agent at 2am to a video answer from a named coach to a one-to-one call.

**Positioning.** "Jez Cartwright's Performance Intelligence: the coaching your CxOs get, for everyone else, in your company's language."

**Versus generic AI.** PIapp is:

* **Grounded**: vetted expert insights, cited to the video and the moment in it.  
* **Contextual**: it uses the client's backstory and terminology.  
* **Methodical**: it applies PI's method (awareness, discerning reality, effective choices, grounded confidence, "the elephant in the room").  
* **Remembering**: per user, and across the client.  
* **Human on demand**: real coaches when AI is not enough.

**How the MVP delivers each promise \[P\].** The vision describes the end state. The phased scope in §1.6 delivers part of it first:

| Promise | In the MVP (Phase 1\) | Not yet scheduled |
| ----- | ----- | ----- |
| Grounded | Library of vetted expert interviews; coach answers from named, vetted coaches | Citations to the exact video moment in agent answers |
| Contextual | Client categories and terminology drive search; coaches see a short client context summary (BR-71) | Backstory-aware agent |
| Methodical | PI method carried by coach vetting and the interview library | Skills the agent follows |
| Remembering | None | Per-user and client memory |
| Human on demand | Q\&A by video; one-on-one calls | n/a |
| Agent "at 2am" | None. The MVP's AI validates questions and suggests coaches or videos; it does not coach | Coach agent (G-07) |

---

## **4\. Terminology and roles**

### **4.1 Entities**

**People and organisations**

| Entity | Definition |
| ----- | ----- |
| Client | A customer organisation (the tenant). It holds the backstory, terminology, users, credit balance, billing and analytics. One contract per client |
| Sponsor | The CxO who buys PIapp credits for the client and agrees to promote PIapp to its users. Budget holder and executive owner. Recorded as a user of the client with the sponsor role |
| Client Admin | A person the Sponsor nominates to run PIapp day to day: users, backstory, credits. Until the Phase 3 portal exists, PI Admin does this work on the client's behalf (§5.1) |
| User | A person inside a client who uses PIapp for their own coaching |
| Coach | A vetted PI coach who answers questions by video and runs one-on-one calls. Network-wide: not tied to one client |
| SME (Expert) | A person interviewed in an expert-interview video. An SME simply appears in the video. **Not stored in PIapp:** no record, no account or portal, no compensation. Not necessarily a coach. The date of PI's signed release is held on the video record (BR-57) |
| PI Admin | A member of the PI team who runs PIapp across all clients |

**Content and context**

| Entity | Definition |
| ----- | ----- |
| Video (expert-interview video) | A video on the PI YouTube channel, with PI metadata: interviewing coach, categories, summary and transcript. Played only in YouTube's embedded player |
| Answer video | A coach's recorded response to a question. Hosted by PIapp, not YouTube, and private to the asker. Not part of the library |
| Insight | An atomic, citable idea extracted from a video transcript, tied to the video and a timestamp. PI Admin approves it before use |
| Category | A PI-managed classification for videos and insights. Categories exist globally (PIapp level) and per client |
| Backstory | The client's corporate background, used as context to frame searches and to give coaches a short client summary. Versioned; approved by the Sponsor |
| Terminology | A list of terms, each with an explanation (two fields: term, explanation). **PI App terminology** is held at app level. **Client terminology** is held at client level and overrides PI App terminology for that client. Both are loaded from CSV and each line can be edited. Example: term CPQ, explanation "Configure Price Quote. System to control products and pricing" |
| Digital twin | A person's own profile: role, goals, style. Users and coaches each have one. Used for matching and, selectively, shared with a coach |
| Skill | A playbook the AI follows to help a user refine and clarify a question. It is about question refinement, not coaching |

**Services and commerce**

| Entity | Definition |
| ----- | ----- |
| Question | A user's request for a coach's video answer, after the AI conversation has validated it |
| Question request | One question sent to one coach. It carries the status and the credit charge. A question sent to two coaches creates two requests |
| Answer | A coach's video answer to one question request |
| Session | A booked one-on-one call between one user and one coach |
| Credit | The unit that users spend on coach services and that coaches earn against. \$50 per credit |
| Credit block | A quantity of credits allocated to a client by PI Admin (no minimum in the MVP). The client's credit pool |
| Credit limit | The number of credits a user may spend before approval is needed. Default 12; can be overridden for each client |
| Credit request | A user's request for more credits when they do not have enough for an action. Goes to the Client Admin; in the MVP, to PI Admin |
| Availability | A coach's available / unavailable switch (vacation mode), maintained by the coach |
| Invite code | A code, sent by PI Admin, that lets a user or coach create their account |
| Inbox | A coach's (and a user's) queue of requests and notifications |
| Notification | A message to a user, coach or PI Admin: a new question or booking, an answer, a credit request, a decline, a low client balance, a safety flag |
| Minimum group size (k ≥ 5\) | A report or breakdown is shown to a Sponsor or Client Admin only when it covers at least 5 users, so that no individual can be identified. Smaller groups are shown only as part of a larger total |

### **4.2 Roles**

| Role | Scope | Can | Cannot | In Phase 1 |
| ----- | ----- | ----- | ----- | ----- |
| PI Admin | All clients | Load and manage YouTube assets; manage categories, coaches and skills; approve insights; create clients and users; maintain any backstory; allocate credits to clients and approve credit requests; see analytics across all clients; control billing and credits | Read an individual user's private conversations, notes, twin or memory (BR-40) | Web site. Performs the Client Admin's tasks as concierge |
| Sponsor (CxO) | One client | Nominate Client Admins; approve the backstory; see client aggregate analytics and themes (k ≥ 5); receive the sponsor report; use PIapp as a user (Phase 3\) | See any individual's activity, notes, conversations, questions, twin or memory, including direct reports | No sign-in. Receives the sponsor report from PI Admin; approves backstory in writing (BR-13) |
| Client Admin | One client | Maintain backstory and client terminology; invite, deactivate and manage users; see client and user analytics; allocate and top up client credits and manage billing (Phase 3\) | See other clients; edit videos, categories or insights; read individuals' private data or question content | No sign-in. Performed by PI Admin for the MVP |
| User | Self, one client | Search and watch videos; save, favourite, share; add notes; see own credit history; manage own twin; ask coaches questions; book one-on-ones; spend credits within the limit | See other users' data; change the backstory | iPhone app |
| Coach | Network-wide, own work only | Maintain own profile and twin; connect a calendar; switch themselves available or unavailable; see their own earnings percentage (read only); receive requests in an inbox; record video answers; run one-on-one sessions; see own earnings, questions and sessions | Answer or see questions not sent to them (BR-72); see a user's conversations, notes or memory; see other coaches' questions or earnings | iPhone app |

Three points that v3.0 left implicit:

* SMEs are not a role and are not stored in PIapp. They have no account, portal or access, and are not compensated (BR-57).  
* The Client Admin and Sponsor have no sign-in until Phase 3\. Everything the roles table gives them in Phase 1 is delivered by PI Admin on request.  
* PI Admin's access to the content of a question or answer is not stated in v3.0. It is allowed only for support, safety or dispute reasons, with a reason code and an audit entry (BR-40, G-16).

### **4.3 Status lifecycles**

| Object | Statuses |
| ----- | ----- |
| Coach availability | available ↔ unavailable (switched by the coach; independent of the status below) |
| Coach | invited → approved (vetted by PI) → active (visible to users: profile complete, interviews published) → suspended / removed |
| Video | draft → in review → published / rejected |
| Question request | requested → answered / declined / deleted by the asker. It never lapses: it stays open until one of these happens |
| Session | requested → booked → complete / cancelled / no-show |
| Credits on a request | reserved → spent (coach delivered) / refunded |

---

## **5\. Functionality (MVP)**

### **5.1 Platforms and operating model**

* **iPhone app**: the primary interface for users and coaches. No Android or desktop app in the MVP (G-21).  
* **PI Admin website**: for the PI team. It is the only web interface in Phase 1\.  
* **Concierge model.** In Phase 1 the PI team sets up clients, users, coaches, categories and credits by hand, and answers client requests such as approving credit above the limit. The Client Admin portal in Phase 3 hands these tasks to the client.  
* **Payments.** No payment collection or payout in the app until Phase 4\. Credits are loaded by PI Admin against a contract invoiced manually.

### **5.2 PI Admin experience (web)**

**Client management**

* Set up the client profile: name, backstory, client terminology (uploaded from CSV; each line editable) and categories (global and client-specific). Also the client's staff-support resources, which the safety flow shows to users (§10).  
* Add users and send each an invite code.  
* Manage credits: allocate credits to the client (no minimum) and top up. Receive users' credit requests as notifications and approve or decline them. Approvals are recorded with the approver, date and amount.  
* Maintain the client's credit settings: user credit limit (default 12\) and credits per question and per session length (defaults 1, 3, 5, 8). The client can see these in its profile; only PI Admin can change them.  
* Dashboard: user sign-ups; user credit usage.

**Coach management**

* Set up a coach and send an invite code. (v3.0 said "set up user"; it meant coach.)  
* Record vetting: invited → approved → active (§4.3).  
* Maintain each coach's percentage of credit value (default 20%). The coach sees it in their profile; only PI Admin can change it.  
* Dashboard: answers, sessions, credits earned.

**Content management (expert-interview videos)**

1. The PI team edits the interview video and exports its transcript.  
2. The video goes on the PI YouTube channel.  
3. When loading the video into PIapp, PI Admin adds its categories, links its interviewing coach, attaches the transcript, and records the date of the SME's signed release on the video. The SME is not recorded in PIapp.  
4. PIapp reads the transcript, generates AI insights and stores them. An insight is not used until PI Admin has approved it (BR-06). A video can be published only when it has at least 3 approved insights (BR-03).

**App management**

* Receive notifications: a coach declines a question (with the reason); a user requests credits; a client's remaining credits reach 10, 5 and 0 (BR-83); the safety check flags a question (BR-38).  
* Maintain **PI App terminology** (term, explanation): upload from CSV; each line editable. Client terminology overrides it.  
* Maintain the default credit limit, credit prices and coach percentage.  
* Dashboard: users, credit usage, questions, answers, sessions.  
* Backup and restore.  
* Audit log of administrator actions, including credit adjustments (with a reason) and any access to question or answer content.

### **5.3 Coach experience (mobile)**

* **Sign-in.** From the invite email; thereafter by email or Google, with password reset.  
* **Profile.** Headshot, bio and digital twin. An **available / unavailable switch** (vacation mode) that the coach maintains. While unavailable the coach cannot be chosen for new questions or bookings (BR-80). The coach also sees their percentage of credit value, read only; only PI Admin can change it.  
* **Availability.** Connect a calendar so that session availability is shown to users.  
* **Inbox.** Questions and session bookings.  
* **Answering a question.** Record a video answer on the phone: portrait, under 3 minutes, cropping only. Upload it and mark the question complete. The coach can preview and re-record before uploading, and can decline a request, giving a reason (BR-72).  
* **Sessions.** Run the session on the client's own video-conferencing app (outside PIapp) and mark it complete in PIapp.  
* **Dashboard.** Views of videos; question and answer history; session history. Earnings in credits.  
* **Notifications.** Question request; session request; session scheduled.

### **5.4 User experience (mobile)**

* **Sign-in.** From the invite email; thereafter by email or Google, with password reset.  
* **Profile.** Headshot, bio and digital twin. Connect a calendar so booked sessions sync to it.  
* **Videos.** Search by category, or an AI match against the user's profile. Watch, favourite, save and share. Lists of saved, favourite and watched videos. Notes pinned to a video timestamp (v3.0 §1 lists notes; §5 did not; G-08).  
* **Questions.**  
  1. Create a question.  
  2. The AI validates and refines it, and splits it if it contains more than one question.  
  3. The user edits and confirms.  
  4. The user chooses coaches (search, or three AI suggestions) and sees the credit cost.  
  5. The app checks the user has enough credits for the full cost. If not, Submit is unavailable and the user is offered "Request more credits".  
  6. Submit.  
  7. A list of answers to the user's questions, and of questions still open. The user can delete an open question; its reserved credits are refunded.  
* **Sessions.** Request a session (search for a coach, or AI recommends). Only lengths the user has enough credits for can be requested (for example, with 4 credits left, 20 minutes only). Choose date and time and book. See past and upcoming sessions. Cancel, or reschedule through a reschedule link (as in Calendly). Sync to the calendar. The call itself is held outside PIapp on the corporate conferencing app (Zoom, Teams, Slack). Coaches who are unavailable are shown as unavailable and cannot be booked.  
* **Notifications.** New videos; answers to submitted questions; session scheduled; out of credits; outcome of a credit request.  
* **Credits.** History of usage. Credits remaining. **Request more credits** at any time, and automatically offered when an action is blocked for lack of credits. The request notifies PI Admin in the MVP (Client Admin from Phase 3).

### **5.5 Key flows and credit movements**

**Q\&A**

| Step | What happens | Credits |
| ----- | ----- | ----- |
| 1\. Ask | User writes a question; AI validates, refines and splits; safety screen runs | None |
| 2\. Choose | User picks one or more coaches; app shows the total cost | None |
| 3\. Check and submit | The app checks the user has enough credits for the total (1 per coach), within their limit and the client's pool. If not, Submit is blocked and the user can request more credits. If yes, one question request per coach is created | 1 credit **reserved** per request |
| 4\. Answer | Coach is notified, records and uploads a video answer, and marks it complete | 1 credit **spent**; coach earns 20% of its value |
| 5\. Otherwise | Coach declines, or the user deletes the question before it is answered. A question never lapses; until one of these happens it stays open and its credit stays reserved | 1 credit **refunded** |

**One-on-one**

| Step | What happens | Credits |
| ----- | ----- | ----- |
| 1\. Match | User searches for a coach or takes an AI recommendation; sees the coach's availability | None |
| 2\. Check and book | User picks a length (20, 40 or 60 minutes) and a slot, and sees the cost. Only lengths the user has enough credits for can be booked; otherwise the user can request more credits. Coach is notified and the session is added to both calendars | 3, 5 or 8 credits **reserved** |
| 3\. Run | Coach and user hold the call outside PIapp, on the corporate video-conferencing or meeting app (for example Zoom, Teams or Slack) | None |
| 4\. Close | Coach marks the session complete | Credits **spent**; coach earns 20% of their value |
| 5\. Otherwise | The user or the coach cancels the session (at any time, including after a no-show), or it is rescheduled through the reschedule link | Credits **refunded** on cancellation |

### **5.6 Data model**

The diagram below is the v5.0 view; the v3.0 picture is withdrawn because it lacks the new entities.

```
erDiagram
  CLIENT ||--|| CLIENT_CONTEXT : has
  CLIENT ||--o{ TERMINOLOGY : "overrides app terms with"
  CLIENT ||--o{ CLIENT_PRICE : "sets credits per service"
  CLIENT ||--o{ USER : employs
  CLIENT ||--o{ CATEGORY : "owns client-specific"
  CLIENT ||--o{ CREDIT_TXN : "pool entries"
  USER ||--o{ CREDIT_TXN : "spend entries"
  COACH ||--o{ CREDIT_TXN : "earning entries"
  USER ||--o| DIGITAL_TWIN : has
  COACH ||--o| DIGITAL_TWIN : has
  USER ||--o{ QUESTION : asks
  QUESTION ||--o{ QUESTION_REQUEST : "sent as"
  COACH ||--o{ QUESTION_REQUEST : receives
  QUESTION_REQUEST ||--o| ANSWER : "answered by"
  USER ||--o{ SESSION : books
  COACH ||--o{ SESSION : runs
  USER ||--o{ VIDEO_USER : "saves, favourites, watches"
  VIDEO ||--o{ VIDEO_USER : "is acted on in"
  USER ||--o{ VIDEO_NOTE : writes
  VIDEO ||--o{ VIDEO_NOTE : "pinned to"
  COACH ||--o{ VIDEO : interviews
  VIDEO ||--o{ INSIGHT : yields
  INSIGHT ||--o{ INSIGHT_CATEGORY : "may have"
  CATEGORY ||--o{ INSIGHT_CATEGORY : tags
  CATEGORY ||--o{ VIDEO_CATEGORY : classifies
  VIDEO ||--o{ VIDEO_CATEGORY : "is classified by"
  USER ||--o{ CREDIT_APPROVAL : "needs"
```

| Entity | Purpose | Key attributes |
| ----- | ----- | ----- |
| CLIENT | Customer organisation (tenant) | name, status, sponsor (a USER), support resources (the client's staff-support contacts, shown by the safety flow), contract start and term, default user credit limit (default 12\) |
| CLIENT\_CONTEXT | Backstory used to frame searches and give coaches context. One per client. Terminology is held in TERMINOLOGY | backstory (versioned) |
| USER | Employee of a client | client, name, email, role (user, client admin, sponsor), credit\_limit (starts at the client's limit; approved credit requests add to it) |
| COACH | Vetted PI coach. Network-wide | name, email, bio, headshot, status (invited, approved, active), calendar availability, availability switch (available, unavailable), coach share % (default 20\) |
| VIDEO | PI expert-interview video on YouTube | coach (interviewer), youtube\_id, title, status, summary, transcript, SME release date (set by PI Admin), categories (through VIDEO\_CATEGORY), insights (through INSIGHT) |
| INSIGHT | Atomic, citable idea generated by AI from a video transcript and stored (§5.7) | video, text, start and end seconds, excerpt, status (generated, approved, rejected, withdrawn), transcript version, reviewed by and date |
| INSIGHT\_CATEGORY | Optional categories on an insight; without any, the insight uses its video's categories | insight, category |
| CATEGORY | PI-managed classification. Global, or client-specific when client is set | name, client (nullable) |
| VIDEO\_USER | A user's interaction with a video | user, video, type (saved, favourite, watched), date |
| QUESTION | A user's validated question after the AI refinement conversation | user, text, status, parent question (when split) |
| QUESTION\_REQUEST | One question sent to one coach. Carries the status and the credit charge | question, coach, status (requested, answered, declined, deleted), credits (from the client's price) |
| ANSWER | Coach's video answer to a request | request, video file, duration, date |
| SESSION | Booked one-on-one call | user, coach, minutes (20, 40, 60), credits, scheduled time, status (requested, booked, complete, cancelled, no-show) |
| CREDIT\_TXN | Ledger of every credit movement. Balances are calculated from it | owner\_type (client, user, coach), owner, credits (+/-), reason (purchase, reserve, spend, refund, earning, adjustment), reference |
| TERMINOLOGY | One line of terminology. Client is empty for PI App terms and set for client terms; a client term overrides the app term with the same term | client (nullable), term, explanation |
| CLIENT\_PRICE | Credits a client is charged for each service | client, service (question, 20, 40, 60 minutes), credits |
| DIGITAL\_TWIN | A user's or coach's profile | person, role, goals, style, fields shared with coaches |
| VIDEO\_NOTE | A user's note pinned to a video | user, video, timestamp, text |
| VIDEO\_CATEGORY | Links videos to categories (many to many) | video, category |
| CREDIT\_APPROVAL | A user's request to exceed the credit limit, and its outcome | user, credits requested, approved by, status, date |
| INVITE | An invite code | role, client (users only), email, code, status, expiry |
| NOTIFICATION | A message to a user, coach or PI Admin | recipient, type, reference, sent, read |
| RATING | **Not in the MVP (Phase 2).** A user's helpfulness rating of an answer or session | request or session, user, score, date |

### **5.7 Insight schema (draft for review) \[P\]**

An insight is one idea, taken from a video transcript, that stands on its own and can be cited back to a moment in the video. PIapp generates insights when a video is loaded (§5.2) and uses approved ones for search and for AI matching of videos to a user's profile. The SME is not recorded: the cited speaker is identified only by role.

**INSIGHT**

| Field | Type | Rule |
| ----- | ----- | ----- |
| id | identifier | Generated by PIapp |
| video\_id | link to VIDEO | Required |
| text | text, up to 300 characters | One idea, understandable without watching the video, in plain language |
| start\_seconds | whole number | Where the idea starts in the video. Required |
| end\_seconds | whole number | Where it ends. Greater than start, and within the video's length |
| excerpt | text | The transcript passage the idea came from. Lets PI Admin check it quickly |
| speaker\_role | interviewer or guest | Who said it. The guest is not stored as a record |
| status | generated, approved, rejected, withdrawn | New insights are "generated". Only "approved" insights are used (BR-06) |
| transcript\_version | whole number | Which transcript produced it |
| generated\_by | text | The AI model and version, and the date |
| reviewed\_by, reviewed\_at | PI Admin user, date | Set when PI Admin approves or rejects |
| withdrawn\_reason | text | Required when withdrawn: for example SME request (BR-54), inaccurate, transcript replaced |

**INSIGHT\_CATEGORY** (optional): insight, category. An insight with none uses its video's categories.

**Citation.** Derived, not stored: the video title, the interviewing coach, and a link to the YouTube video at start\_seconds (for example, https\://youtu.be/{youtube\_id}?t={start\_seconds}).

**Rules**

1. When a transcript is attached, PIapp reads it once and stores a list of insights, each "generated".  
2. PI Admin approves or rejects each one. A video can be published only with at least 3 approved insights (BR-03).  
3. Search and AI matching use only approved insights (BR-06).  
4. If the transcript is replaced, the video's existing insights are withdrawn with the reason "transcript replaced", and new ones are generated.  
5. If an SME asks for removal, the affected insights are withdrawn within 7 days (BR-54, §9).  
6. Withdrawn and rejected insights are kept, not deleted, so the history is auditable.

**What the AI returns for each video (example)**

```json
{
  "video_id": "…",
  "transcript_version": 1,
  "insights": [
    {
      "text": "Name the thing nobody is saying in the room before trying to solve the problem.",
      "start_seconds": 312,
      "end_seconds": 355,
      "excerpt": "…",
      "speaker_role": "guest"
    }
  ]
}
```

**Graph extension (CAP-10, unscheduled).** To link insights across videos, add one table, INSIGHT\_LINK: from\_insight, to\_insight, link\_type (supports, contradicts, elaborates, duplicates), created\_by (AI or PI Admin), status. Both insights must be approved. The graph is then: VIDEO has INSIGHT; INSIGHT is tagged with CATEGORY; INSIGHT links to INSIGHT; VIDEO is interviewed by COACH. Nothing in the MVP depends on it.

---

## **6\. Capabilities**

Capability IDs from v2.1 are kept where the capability continues, so the UI and Technical specs can trace them. New capabilities start at CAP-30. The last column shows what moved against v2.1.

### **6.1 Phase 1: MVP launch**

| ID | Capability | Change vs v2.1 |
| ----- | ----- | ----- |
| CAP-01 | Asset management: load YouTube expert-interview videos, link interviewing coach, categories added by PI team, transcript, AI-generated insights, approval before publish | Adds AI insight generation and coach link |
| CAP-02 | Category management: global and client-specific | Unchanged |
| CAP-38 | Terminology management: PI App terminology and client terminology (term, explanation), CSV upload, line editing, client overrides app | New (replaces the v2.1 glossary) |
| CAP-03 | Client onboarding (concierge): create client, users, backstory, client terminology, credit settings, support resources, invite codes | Adds invite codes and support resources |
| CAP-04 | Authentication: invite-code sign-up, email or Google sign-in, password reset | Unchanged; coaches included |
| CAP-05 | Video search by category and AI match on profile, in the client's terminology | Adds AI match |
| CAP-06 | Personal library: save, favourite, watched lists | Unchanged |
| CAP-07 | Share a video inside the client (BR-23) | Unchanged |
| CAP-08 | Notes pinned to a video timestamp, and a notes view | Unchanged (G-08) |
| CAP-14 | Digital twin: profile for users and coaches | Was users only, Phase 2 |
| CAP-15 | iPhone app for users and coaches | Was "iOS with web parity", Phase 3\. No user web app |
| CAP-18 | Analytics, basic: PI Admin dashboards across clients and per client | Unchanged (1 basic) |
| CAP-24 | User registration and profile (headshot, bio, twin); credit history | Credit history added |
| CAP-25 | Credits: allocation by PI Admin (no minimum), internal ledger, credit check before any request, user limit and prices set per client, coach percentage set per coach, credit requests and approval, reserve, spend and refund, coach earnings | Was Phase 3; moved to 1 |
| CAP-26 | Coach accounts: profile and twin, calendar availability, available / unavailable switch, inbox, earnings, sessions | Was Phase 3; moved to 1 |
| CAP-27 | Q\&A: AI-validated question, coach selection by search or three AI suggestions, video answer recorded in app | Was Phase 3; moved to 1\. Selection replaces auto-match |
| CAP-28 | One-on-one: match, schedule, book, run, close, spend credits | Was Phase 4; moved to 1 |
| CAP-29 | Inbox and notifications for users, coaches and PI Admin (requests, declines, low client balance) | Was Phase 3; moved to 1 |
| CAP-30 | Coach vetting and qualification: invite, approval, interview requirement, activation | New |
| CAP-31 | Safety screen on questions before sending; a flagged question is not sent and the Client Admin (PI Admin in the MVP) is notified (§10) | New in this form; was in §10 only |
| CAP-32 | Backup and restore; administrator audit log | Backup/restore from v3.0; audit log new |
| CAP-33 | Calendar connection for coaches and users | New (from v3.0 §5) |
| CAP-11 | Skills: the playbooks the AI follows to refine and clarify questions (not coaching), maintained by PI Admin **\[P\]** | Was Phase 2 and agent-wide; now limited to question refinement |
| CAP-35 | Call booking and calendar sync. Sessions are hosted outside PIapp on the corporate conferencing app (Zoom, Teams, Slack); PIapp books, notifies and syncs calendars | New |

### **6.2 Later phases**

| ID | Capability | Phase | Change vs v2.1 |
| ----- | ----- | ----- | ----- |
| CAP-36 | MVP feedback backlog: items agreed after the trial **\[P\]** | 2 | New |
| CAP-09 | Personal stats dashboard (v3.0 MVP scope shows lists and credit history only) | 2 **\[P\]** | Was 1 |
| CAP-34 | Ratings: helpfulness of answers and sessions | 2 | New; not in the MVP |
| CAP-16 | Client Admin portal: users, backstory, terminology, credit allocation and top-up requests | 3 | Unchanged |
| CAP-18 | Analytics, full: Sponsor and Client Admin aggregate views at k ≥ 5 | 3 | Unchanged (3 full) |
| CAP-37 | Sponsor as user: Sponsor uses PIapp like any user **\[P\]** | 3 | New (from v3.0 roles) |
| CAP-19 | Billing: collect money for credits; credit packs; subscriptions; user top-up where the client allows | 4 | Unchanged |
| CAP-22 | Payouts: coach earnings converted to money, monthly statements | 4 | Unchanged |

### **6.3 Not yet scheduled**

The v3.0 services and phasing do not include these. They are kept, unscheduled, until Jez and Ian decide (G-07).

| ID | Capability | Was |
| ----- | ----- | ----- |
| CAP-10 | Insight graph: links insights to one another across videos (for example, supports or contradicts). The MVP stores insights as a list on each video (INSIGHT) | Phase 2 |
| CAP-12 | Coach agent (grounded, cited, backstory-aware) | Phase 2 |
| CAP-13 | MCP server | Phase 2 |
| CAP-17 | Conversation memory and client-level learning | Phase 3 |
| CAP-23 | Weekly briefing curated from profile | Phase 2 |
| CAP-20 | Android app | Phase 4 |

---

## **7\. Business rules**

Rule IDs from v2.1 are kept. "Change" says whether the rule is retained, revised, new or deferred. Rules marked **\[P\]** go beyond the validated §1–5 text.

### **7.1 Content and curation**

BR-05 (restricting a video to specific clients) is retired: every published video is visible to every client.

| ID | Rule | Change |
| ----- | ----- | ----- |
| BR-01 | Only videos from the PI YouTube channel, or channels PI Admin approves, are loaded | Retained |
| BR-02 | A video is not visible until a PI Admin publishes it (draft → in review → published or rejected) | Retained |
| BR-03 | Every published video has its interviewing coach, at least one category, a summary and at least 3 approved insights. The SME is not recorded in PIapp | Revised |
| BR-04 | Library videos play only in YouTube's embedded player; never downloaded, re-hosted or cached. (Coach answer videos are different content: BR-73) | Retained |
| BR-06 | An insight is not used for search, matching or summaries until PI Admin approves it | Revised |
| BR-07 | Every insight carries attribution: video (and so its interviewing coach) and timestamp. No SME record is kept | Revised |
| BR-08 | Library content is free but requires sign-in. There is no anonymous access | New |
| BR-09 | Interview videos are landscape, 10 to 20 minutes, and edited by the PI team before publication | New |

### **7.2 Client context**

| ID | Rule | Change |
| ----- | ----- | ----- |
| BR-10 | Each client has one versioned backstory. The current published version frames searches and produces the client summary coaches see (BR-71) | Revised |
| BR-11 | Terminology is a list of term and explanation. PI App terminology is held at app level; client terminology is held at client level and overrides PI App terminology for that client's users. Both are uploaded from CSV and each line is editable. PI Admin maintains both in the MVP; the Client Admin maintains client terminology from Phase 3 | Revised |
| BR-12 | Backstory content is confidential to the client and PI, and is never used for another client's users | Retained |
| BR-13 | The backstory is built only from material the client provides and the Sponsor (or Client Admin delegate) approves in writing. Nothing learned in confidential one-to-one coaching enters a backstory | Revised |

### **7.3 Users and access**

| ID | Rule | Change |
| ----- | ----- | ----- |
| BR-20 | A user belongs to exactly one client. Coaches are network-wide accounts with no client. SMEs are not stored in PIapp | Retained |
| BR-21 | Users join by invite code. In Phase 1 PI Admin issues codes on the client's request; from Phase 3 the Client Admin controls them. There is no open self-registration | Revised |
| BR-22 | Deactivation removes access immediately. Personal data is kept indefinitely (G-33). The user's unspent credits stay in the client's pool and can be reallocated, and any request already reserved is completed or refunded | Revised |
| BR-23 | Sharing is within the client by default. Public share links are a per-client PI Admin setting, off by default | Retained |
| BR-24 | Sign-in is by email or Google, with password reset. SAML-based sign-in may be added, depending on the first client's needs (G-32) | New |
| BR-25 | Coach accounts are created by PI Admin invitation only | New |

### **7.4 Credits**

| ID | Rule | Change |
| ----- | ----- | ----- |
| BR-60 | Credits are the single unit for paid interactions: coach Q\&A and one-on-one sessions. Content is free | Revised |
| BR-61 | A credit is worth \$50. Credits are held in a client pool that users draw on. In the MVP there is no minimum purchase and PI Admin allocates the credits to the client (v3.0's \$10,000 / 200-credit minimum is not applied; G-12). Unspent credits stay at client level and can be reallocated. User top-up is Phase 4 and only where the client enables it | Revised |
| BR-62 | Credits are reserved when a request is made and spent when the coach delivers (answer marked complete; session marked complete). A question request never lapses: it stays open, with its credit reserved, until it is answered or the user who submitted it deletes it. Credits are refunded if the coach declines, if the user deletes an unanswered question, or if a session is cancelled by the user or the coach (at any time, including after a no-show) | Revised |
| BR-63 | Credits per service are set per client and shown to the user before they confirm. Defaults, held at app level: Q\&A 1 credit per coach per question; one-on-one 3 credits (20 min), 5 (40 min), 8 (60 min). The client can see its prices in its profile; only PI Admin can change them. A request is charged at the price in force when it was made | Revised |
| BR-64 | The credit ledger is append-only. Every spend, refund and earning has a matching entry. Balances are calculated from it. Administrator adjustments need a reason | Revised |
| BR-65 | A coach earns a percentage of the credit value for each question answered and each session conducted. The default is 20%; it is held per coach. The coach can see their percentage in their profile; only PI Admin can change it. The percentage in force when credits are spent applies. Earnings are shown to the coach in credits. Earnings are recorded when credits are spent and never on refunded credits. Conversion to money is Phase 4 (Q-12). SMEs are not compensated | Revised |
| BR-66 | A user may spend up to the client's credit limit before approval is needed. The default is 12; PI Admin can set a different limit for a client. A user who needs more can send a credit request (BR-69); an approval adds credits to that user's limit. The approver sees credit counts only, never what they were spent on. Period of the limit: G-02 | Revised |
| BR-67 | When the AI splits a message into several questions, each is a separate question and is charged separately. The user sees each question and the total cost, and may send or drop each one. They cannot merge them: each is sent as its own single question | New |
| BR-68 | Credit allocation (the amount, the term, and any expiry or reallocation) is handled outside PIapp for the MVP. PI Admin records the resulting allocation in PIapp | New |
| BR-69 | **Credit check.** Before any request that costs credits can be submitted, the app checks that the user has enough credits for its full cost: the total of the question requests, or the price of the chosen session length. "Enough" means within the user's remaining limit (BR-66) and the client's remaining pool. If not, the request cannot be submitted. The app offers only the session lengths the user can afford (for example, with 4 credits left: 20 minutes only). The user may instead send a **credit request**, which notifies the Client Admin; in the MVP it goes to PI Admin, who approves or declines it and allocates the credits. The user is told the outcome | New |
| BR-82 | Credit settings are maintained by PI Admin only: each client's credit limit and prices, and each coach's percentage. Clients and coaches can see their own settings. Every change is logged with who, when and the old and new values | New |
| BR-83 | When a client's credits are used up, its users cannot submit requests that cost credits (BR-69). The Client Admin is notified when the client's remaining credits reach 10, 5 and 0; in the MVP the notification goes to PI Admin | New |

### **7.5 Q\&A and one-on-one**

v2.1's rule that coaches may not solicit users off-platform (BR-79) is outside PIapp's scope and is covered in the coach agreement (§9).

| ID | Rule | Change |
| ----- | ----- | ----- |
| BR-70 | Coaches are vetted and invited by PI Admin (initially Jez, who is a user with PI Admin status), accept a code of conduct, and are bound by the boundaries in §10. A coach becomes active only after the interview videos required in §1.5 are published | Revised |
| BR-71 | A coach sees only: the question text, the asker's first name and role, the twin fields the user chooses to share, and a short client context summary. Never the user's notes, memory or other questions. The user sees this list before sending | Retained |
| BR-72 | A user sends a question to one or more coaches of their choice, found by search or from three AI suggestions. Each coach gets a separate request and each costs the client's per-question price (1 credit by default). A question stays open until a coach answers it or the user deletes it; it does not lapse. A coach may decline, and must give a reason. The credit is refunded, PI Admin is notified, and the user may choose another coach. Coaches cannot see questions not sent to them | Revised |
| BR-73 | A coach's video answer is recorded in the app (portrait, under 3 minutes, cropping only), hosted by PIapp (not YouTube), and visible only to the asker and the coach who recorded it, unless the user shares it inside the client (BR-23). PIapp owns it (§9). Answers are never added to the library | Revised |
| BR-74 | Coaches see their own earnings only, in credits | Revised |
| BR-75 | Sponsor and Client Admin see Q\&A and session volumes and de-identified topics at k ≥ 5 (see Minimum group size, §4.1); never the question, the answer video or who asked | Retained |
| BR-76 | PIapp does not record calls. Calls are held outside PIapp on the client's own conferencing app | Revised |
| BR-77 | For one-on-one, the user searches for a coach or takes an AI shortlist, chooses a coach and then a slot from that coach's connected calendar. Matching uses topic fit, coach skills, availability and language. Coaches who have switched themselves unavailable are not suggested | Revised |
| BR-78 | Session lengths are 20, 40 and 60 minutes. A user or coach may cancel at any time, including after a no-show, and the credits are refunded. A session can be rescheduled through a reschedule link, as in Calendly. Sessions are hosted outside PIapp | New |
| BR-80 | A coach can switch themselves available or unavailable (vacation mode) at any time. While unavailable, the coach is not suggested, cannot be chosen for new questions and cannot be booked for new sessions. Questions already sent to them stay open and sessions already booked stand | New |
| BR-81 | Deleting a question: only the user who submitted it can delete it. If unanswered, its reserved credits are refunded and the coach no longer sees it. If already answered, the credits stay spent | New |

### **7.6 AI use**

| ID | Rule | Change |
| ----- | ----- | ----- |
| BR-35 | In the MVP, AI is used only to: (a) validate, refine and split a question, following the PI skills; (b) suggest coaches; (c) match videos to a user's profile; (d) read a transcript and generate insights. (Categories are added by the PI team, not AI.) It does not give coaching advice | New |
| BR-36 | The question-validation conversation is kept only until the question is sent or abandoned, then deleted. The user cannot choose to keep it | New |
| BR-37 | Model providers must not train on PIapp data | Moved from §11 |
| BR-38 | **\[P\]** When the safety check flags a question (signs of crisis or risk of harm), the question is not sent to any coach. The user is shown crisis resources and the client's support resources. The Client Admin is notified (PI Admin in the MVP). The notification says that a safety flag was raised and for whom; PI Admin may open the question under BR-40 (G-34) | New |

v2.1's agent rules BR-30 to BR-34 are removed.

### **7.7 Privacy**

| ID | Rule | Change |
| ----- | ----- | ----- |
| BR-40 | No admin role, Sponsor or coach can read an individual's notes, twin or AI conversations. Admins see aggregates only. A coach sees only what a user sends them (BR-71). PI Admin may open a question or answer only for support, safety or dispute reasons, with a reason code and an audit entry | Revised |
| BR-41 | Analytics for the Sponsor and Client Admin use a minimum group size of 5 users | Retained |
| BR-42 | The Sponsor has no extra visibility of individuals. This is stated in the client contract and the user privacy notice. Credit approvals (BR-66) show counts only | Retained |
| BR-43 | Themes (what people ask about, including Q\&A topics) are reported as de-identified topics with counts, never quotes | Retained |

### **7.8 SMEs (appear in videos only)**

SMEs are not users, are not stored in PIapp, have no account or portal and are not compensated. v2.1 rules BR-50, 51, 52, 53, 55 and 56 (SME portal, SME accounts, SME earnings and attribution) are retired.

| ID | Rule | Change |
| ----- | ----- | ----- |
| BR-54 | An SME who asks PI Admin to correct or remove an insight or video is heard: the insight is withdrawn until PI Admin reviews it (target 5 working days) | Revised |
| BR-57 | Before an interview is published, PI holds the SME's signed release to be interviewed, published and (for insights) extracted. The date of the release is held on the VIDEO record and maintained by PI Admin | New |

---

## **8\. Commercial model**

* **Buyer.** The Sponsor, usually an existing Jez coaching client. One contract per client. Route to market is Jez's CxO relationships, then referrals. There is no self-serve client sign-up.  
* **No bundling.** PIapp is sold separately from the one-to-one coaching of the CxO.  
* **Pricing.** A credit is \$50. In the MVP there is no minimum purchase and PI Admin allocates credits to the client; further credits are allocated on request at the same price **\[P\]**. Credits per service are set per client (defaults 1, 3, 5 and 8\) and the client sees them in its profile; only PI Admin changes them. A minimum may return with billing in Phase 4 (G-12). Users may top up themselves only where the client allows, from Phase 4\.  
* **Revenue split.** The coach receives a percentage of the credit value, 20% by default, held per coach. The coach sees it in their profile; only PI Admin changes it. At 20%, the coach receives 20% of the credit value for each question answered and each session conducted. The remainder (80% at the default) is PI's revenue, out of which PI pays platform costs (hosting, AI, tooling) (G-04). SMEs are not compensated. Coaches are paid in US dollars (D-16).  
* **Billing.** Phases 1–3: contracts are invoiced manually and coaches are paid manually outside the app from the ledger (G-05). Phase 4 builds billing and payouts (Stripe).

**Unit economics at default prices and the default 20% share**

| Service | Client pays | Coach earns | PI keeps |
| ----- | ----- | ----- | ----- |
| Q\&A, one coach | \$50 | \$10 | \$40 |
| 20-minute call | \$150 | \$30 | \$120 |
| 40-minute call | \$250 | \$50 | \$200 |
| 60-minute call | \$400 | \$80 | \$320 |

**Phase 1 client, at default prices and 20%**

| Item | Value |
| ----- | ----- |
| Users | 50 |
| Credit allocation | \$25,000 |
| Credits (at \$50) | 500 |
| Credits per user per year | about 10 |
| Coach pool at 20% | \$5,000 |
| PI keeps before costs | \$20,000 |

\$25,000 is the planning figure (G-01). v3.0's other assumption of 20 credits per user would have been \$50,000 and is dropped.

---

## **9\. Content, rights and consent**

* **Library videos.** PI owns the channel. Embedding YouTube videos in the app (Phase 1\) is allowed under YouTube's terms provided the player and branding stay intact.  
* **Interviews.** Before an interview is published, PI holds the SME's signed release and the agreement with the interviewing coach, covering publication, editing by the PI team and the use of the transcript (BR-57). The date of the release is held on the video record, maintained by PI Admin.  
* **Extracting insights.** In Phase 1 the PI team exports the transcript and PIapp uses AI to generate and store insights from it, for PI Admin to approve. It needs written clearance from PI as channel owner, the SME's consent (BR-57), and a takedown process that removes an SME's insights within 7 days. Legal review of this is a hard gate before launch.  
* **Ownership.** PIapp owns all content: interview videos, questions and video answers. Answer videos are visible only to the asker and the coach who recorded them and are never added to the library. PIapp stores them to deliver the service. Calls are held outside PIapp on the client's own conferencing app, and PIapp does not record them (BR-76).  
* **Agreements needed.** Client contract, DPA, coach agreement with code of conduct (including that PIapp owns the content, and no soliciting of users off-platform), SME release, user privacy notice and terms of use (G-26).

---

## **10\. Coaching boundaries and safety**

* **Scope.** PIapp is performance coaching. It is not therapy, medical, legal or HR-investigation advice. The app says so at sign-up and where a user asks a question.  
* **Crisis.** On signs of crisis or risk of harm, the AI stops validating the question and shows crisis resources and the client's own support resources. Coaches follow the same rule in video answers and calls. The coach agreement gives coaches a named PI contact for escalation, and every answer and session has a "report a problem" route.  
* **Named colleagues.** No advice on actions against named colleagues beyond general constructive guidance, and no claims about named individuals. This binds coaches as well as the AI.  
* **Backstory.** A client backstory cannot override these boundaries.  
* **Screening before sending.** Every question passes a safety classifier before it can be sent to a coach. If it is flagged, the question is not sent to a coach, the user is shown crisis and support resources, and the Client Admin is notified (PI Admin in the MVP) (BR-38, D-23). Video answers and calls cannot be screened in advance, so the controls on them are the coach code of conduct, the report route and PI Admin's ability to withdraw an answer (G-17).  
* **Support resources.** The client's own staff-support resources (for example an employee assistance line) are captured at onboarding (§5.2) so the safety flow can show them.

---

## **11\. Privacy and data**

* **Roles.** The client is data controller for user data and PI is processor. Coaches are PI's contractors, and their own data is controlled by PI. SMEs appear in videos under a release and have no account. A DPA template is needed before the first pilot.  
* **Residency.** US data residency only (D-15).  
* **Retention.** Personal data, including questions, answer videos, notes and the user's twin, is kept indefinitely (G-33). A user can delete a question that is still open (BR-81). The AI question-validation conversation follows BR-36.  
* **AI providers.** Model providers must not train on PIapp data (BR-37).  
* **Payments.** Payment card data never touches PIapp (Stripe, Phase 4).  
* **Who can see what.**

| Data | User | Coach | PI Admin | Sponsor / Client Admin |
| ----- | ----- | ----- | ----- | ----- |
| Library activity, notes, twin | Own | No | No (aggregates only) | No (aggregates, k ≥ 5\) |
| Question text and answer video | Own | Questions sent to them and their own video answers | Logged access for support, safety or dispute | No: volumes and de-identified topics only (BR-75) |
| Session details | Own | Own sessions | Metadata; no call content | No: volumes only |
| Credit counts | Own | Own earnings | All | Client totals; counts for an approval (BR-66) |

* **Sub-processors.** YouTube (library video), a video-hosting provider (answer videos), an AI model provider, Apple push notifications, Google sign-in and calendar providers. Calendar access is limited to free/busy times and booking events. The list is finalised in the Technical Spec and the DPA.  
* **Auditing.** Administrator actions, including any access to question or answer content, are logged (CAP-32).

---

## **12\. Success measures**

v3.0 left this table empty. Targets are deferred until after the MVP. The measures below are correct and are tracked from launch. Measures about a coaching agent (conversations, citations, weekly briefing) are removed until one is scheduled (G-07).

| Measure | Definition | Tracked from |
| ----- | ----- | ----- |
| Seats activated | Invited users who sign in and complete a profile within 30 days | Launch |
| Monthly active users | Users who watch, ask or book at least once in the month ÷ seats | Launch |
| Videos watched per active user per month | From VIDEO\_USER | Launch |
| Notes per active user per month | From VIDEO\_NOTE | Launch |
| Questions asked per active user per month | Questions sent | Launch |
| Sessions completed | Sessions marked complete | Launch |
| Open questions | Questions open and their age (questions never lapse); median time to answer | Launch |
| Answers rated helpful | Share of rated answers scored helpful | Phase 2 (no ratings in the MVP) |
| Sessions rated helpful | Share of rated sessions scored helpful | Phase 2 (no ratings in the MVP) |
| Credit utilisation | Credits spent ÷ credits allocated | Launch |
| Credit requests | Count of credit requests and their outcome (tests the limit, G-02) | Launch |
| Active coaches and response | Coaches active and available; requests answered or declined | Launch |
| Library coverage | Published interview videos; categories with at least 3 videos | Launch |
| Client renewal | Client renews at term; Sponsor satisfaction | End of term |
| Statement disputes | Payout statements disputed | Phase 4 |

---

## **13\. Risks**

| ID | Risk | Impact | Mitigation |
| ----- | ----- | ----- | ----- |
| R-01 | Coach supply is too thin or slow: 10 coaches must each be vetted and record interviews before launch | Late launch; slow answers; refunds | Recruit ahead of rollout; report of open questions by age; user can delete and re-ask (BR-81); coach availability switch (BR-80); cap open requests per coach (G-20) |
| R-02 | Coach economics are unattractive: \$10 for a video answer, \$80 for an hour | Coaches decline requests or leave | Test with 2–3 coaches before launch; revisit split or tiers (G-04, G-29) |
| R-03 | Coach quality or conduct varies | Brand damage | Vetting, code of conduct, ratings (Phase 2, CAP-34), PI review, removal |
| R-04 | Dependence on Jez: sole vetting authority and the Sponsor relationship | Bottleneck; key-person risk | Document vetting criteria; second PI vetter after MVP |
| R-05 | Credit use differs from the plan of about 10 credits per user per year | Unused credits (low renewal) or frequent requests for more | Track utilisation (§12); PI Admin reallocates unused credits at client level |
| R-06 | A user needs more than the credit limit | Approval friction; PI concierge load | Credit requests (BR-69); set the client's limit above planned use (G-02) |
| R-07 | Coach answers on phones vary in lighting, sound and length | Poor user experience | Recording guidance, preview and re-record, trim only (G-22) |
| R-08 | Sensitive personal or HR matters shared in questions or calls | Trust; legal | BR-40, BR-71, §10 boundaries, privacy notice; coach escalation route |
| R-09 | Safety cannot screen video answers or calls | Duty of care | Code of conduct, report route, withdraw answer (G-17) |
| R-10 | Coach sees more than the user intended | Trust | BR-71 consent screen; no access to notes or other questions |
| R-11 | Credit disputes and refund handling | Support load; margin | Append-only ledger; BR-62 rules; adjustment with reason |
| R-12 | Video hosting cost and compliance for answer videos | Margin; privacy | Choose a provider with retention limits (Technical Spec); calls are held outside PIapp |
| R-13 | iPhone-only reach: Android or desktop users, App Store rules for a B2B credits app | Low adoption; delay | Check the client's devices; unlisted distribution; email fallback (G-21) |
| R-14 | Rights and consent not obtainable for some SMEs | Thinner library; insights withdrawn | Written release before publishing (BR-57); takedown within 7 days |
| R-15 | PI team capacity to edit, export transcripts and categorise each video | Delay to library growth | Standard load checklist; estimate hours per video (G-23) |
| R-16 | Sponsor expects to see individuals' use | Employee trust | BR-42 in the contract; demonstrate the aggregate view; sponsor report (G-15) |
| R-17 | Sponsor leaves | Renewal | Second executive owner and a Client Admin named at contract |
| R-18 | Confidential coaching knowledge leaks into the product | Breach | BR-13 and approval log |
| R-19 | PI concierge workload: manual setup, approvals, invoicing, payouts | Slow response; errors | Pilot support model (G-27); Client Admin portal in Phase 3 |
| R-20 | Single pilot client | Narrow learning; client-specific design | Choose a representative client; design measures in §12 for reuse |
| R-21 | Tax and payments for international coaches | Payouts blocked | Stripe Connect for KYC and tax forms in Phase 4; manual process before (G-05) |
| R-22 | Coach conflict of interest or solicitation of users off-platform | Trust; legal | Coach agreement (outside PIapp); conflict declaration (G-28) |

---

## **14\. Decisions and open questions**

### **14.1 Decisions made**

These come from the sections validated in v3.0.

| ID | Decision |
| ----- | ----- |
| D-01 | PIapp is a two-sided B2B marketplace: coaches get access to client work; clients offer employees cost-effective coaching |
| D-02 | Three services: Content (free, login required), Q\&A (video answers) and One-on-one |
| D-03 | Credits are the common currency: \$50 each; no minimum purchase in the MVP (PI Admin allocates credits); user limit of 12 before approval (default; set per client); every request is credit-checked before submission; coach receives 20% (default; set per coach) |
| D-04 | Q\&A costs 1 credit per coach per question; one-on-one costs 3, 5 or 8 credits for 20, 40 or 60 minutes |
| D-05 | A user chooses one or more coaches, by search or from three AI suggestions |
| D-06 | Coach video answers are portrait, under 3 minutes, crop only, and hosted by PIapp |
| D-07 | Coaches are vetted by the PI team (Jez for the MVP), record 10 expert-interview videos, and 10 coaches are needed to launch |
| D-08 | MVP is an iPhone app for users and coaches plus a PI Admin website run as a concierge service |
| D-09 | Phase 2 incorporates trial feedback; Phase 3 adds the Client Admin portal; Phase 4 adds billing |
| D-10 | Categories exist globally and per client; the client backstory and terminology frame searches |
| D-11 | Defaults are held at app level and overridden by client (user credit limit, credits per service) or coach (percentage). Only PI Admin updates them; clients and coaches can see their own |
| D-12 | Coaches can switch themselves available or unavailable (vacation mode) |
| D-13 | Terminology is held at app level and client level (term, explanation; CSV upload; each line editable); client terminology overrides app terminology |
| D-14 | A question never lapses: it stays open until answered, or deleted by the user who submitted it |
| D-15 | Data residency is US only (was Q-05) |
| D-16 | Coaches are paid in US dollars (part of Q-12) |
| D-17 | Unspent credits stay at client level and can be reallocated (was Q-19) |
| D-18 | Coach answers are never added to the library (was Q-21) |
| D-19 | PIapp owns all content: interview videos, questions and video answers |
| D-20 | No bundling with the CxO's one-to-one coaching |
| D-21 | Sessions are hosted outside PIapp on the corporate conferencing app; a cancelled session is refunded, and a session can be rescheduled by a link |
| D-22 | Targets are deferred until after the MVP; the §12 measures are tracked from launch |
| D-23 | A question flagged by the safety check is not sent to a coach; the user sees support resources and the Client Admin (PI Admin in the MVP) is notified (was Q-22) |

### **14.2 Open questions carried from v2.1**

Q-05, Q-19, Q-21 and Q-22 were answered in review (D-15, D-17, D-18, D-23). One remains. Its wording is reconstructed from references in v2.1 **\[P\]**. All new gaps are in Appendix A.

| ID | Question | Needed by |
| ----- | ----- | ----- |
| Q-12 | Coach payouts are in US dollars (D-16). Still open: when coaches are paid, and how tax forms are handled. See G-05 | Before Phase 4; manual process before |

---

## **15\. Change log**

| Version | Date | Change |
| ----- | ----- | ----- |
| 5.0 | 13 Nov 2026 | Review decisions applied to v4.0. SME appears in videos only and is not stored; credit check and credit requests (BR-69); no minimum purchase; defaults per client and per coach; coach availability switch; terminology at app and client level; questions never lapse; sessions hosted outside PIapp; PIapp owns all content; indefinite data retention; targets deferred; insight schema (§5.7); flagged questions are not sent and notify the Client Admin (PI Admin in the MVP); BR-05, BR-30..34 and BR-79 retired; confirmed proposals unmarked. Unconfirmed proposals remain marked **\[P\]** |
| 4.0 | 12 Nov 2026 | Expanded and clarified §1–5 (decisions unchanged). Fixed numbering: Functionality is §5, Capabilities is §6. Rewrote §6–15 to match §1–5. Added Appendix A (gap register) and B (traceability) |
| 3.0 | 28 Oct 2026 | Business-led rewrite of §1–5: marketplace framing; three services; credit economics; coach qualification; four phases. §6–15 not updated |
| 2.1 | 22 Oct 2026 | Merged v1.2 with the 16 Oct revised spec: Coach role, credits, weekly briefing, Q\&A, one-on-one, dashboards; BR-60..77; Q-16..24 |
| 2.0 | 16 Oct 2026 | Ian's draft (partial: exec summary and roles) |
| 1.2 | 27 Sep 2026 | SME portal and revenue share |
| 1.1 | 27 Sep 2026 | Sponsor |
| 1.0 | 27 Sep 2026 | First issue |

**What changed in §6–15 from v2.1 to v5.0** (v4.0 and v5.0 together)

* **§6 Capabilities.** Credits, coach accounts, Q\&A, one-on-one, inbox and iPhone moved into Phase 1\. Client Admin portal stays Phase 3\. Billing and payouts stay Phase 4\. SME portal removed. Agent, MCP, memory, weekly briefing and insight graph are unscheduled; skills are limited to question refinement. Ratings and personal stats moved to Phase 2\. New CAP-30 to CAP-38.  
* **§7 Business rules.** Credit rules rewritten: defaults per client and coach, credit check, no minimum purchase, no lapse. Q\&A routing is a user-chosen set of coaches. Agent rules BR-30..34 removed. SME rules BR-50–53, 55, 56 retired, and BR-05 and BR-79 retired. New BR-08, 09, 24, 25, 35–38, 57, 66–69, 78, 80–83.  
* **§8 Commercial.** Prices, split and worked economics added. Manual invoicing and payouts through Phase 3\.  
* **§9–11.** Extraction now sits in Phase 1 (AI-generated insights), so release and takedown rules apply from launch. PIapp owns all content. Personal data is kept indefinitely. Safety and privacy rewritten for video Q\&A; calls are outside PIapp.  
* **§12–13.** Success measures populated; targets deferred until after the MVP; agent measures removed. Risks re-based on the coach marketplace.  
* **§14.** Decisions list added; open questions restated.

**Companion specs to re-baseline.** The UI and Technical specs (v2.1) still assume the agent, web parity, Q\&A in Phase 3 and one-on-one in Phase 4\. They need updating to §5, §6 and §7 here.

---

## **Appendix A. Gap register**

This register lists errors, inconsistencies, missing detail and undecided items found in or around §1–5. Items in validated text have not been changed unless marked as fixed; each proposed resolution needs a decision.

**Priority:** **A** \= decide before build starts. **B** \= decide before the pilot goes live. **C** \= can wait. **Done** \= fixed in v5.0.

| ID | Type | Where | Gap | Proposed resolution | Owner | Priority |
| ----- | ----- | ----- | ----- | ----- | ----- | ----- |
| G-01 | Error | §1.6 | 50 users × 20 credits × \$50 is \$50,000, not \$25,000 | Resolved in review: plan with \$25,000 (500 credits, about 10 credits per user per year). The 20-credits-per-user assumption is dropped | Ian, Jez | Done |
| G-02 | Undecided | §1.4 | The period of the credit limit (per year, per contract, lifetime) is undefined. At about 10 credits per user per year the default limit of 12 is above the plan | Make the period the contract term | Jez | B |
| G-03 | Ambiguity | §1.5 | "Coaches need to record 10 interviews": per coach (about 100 videos for 10 coaches) or 10 in total? Who finds the SMEs? Can PI edit that volume? Is it a condition for a coach to go live? | Confirm per coach. PI schedules SMEs and editing. Make it a condition of "active" | Jez | A |
| G-04 | Undecided | §1.4, §4 | The coach's percentage is 20% by default and can be set per coach, but no rule says when it should differ. \$10 per \$50 answer and \$80 per hour may not attract coaches. What the other 80% funds is not stated (SMEs are not compensated) | Decide when a coach's percentage differs from 20% and how the remainder is used. Test \$10 per answer with 2–3 coaches | Jez | A |
| G-05 | Missing | §1.6, §8 | Coaches earn from Phase 1 but payouts are Phase 4\. The currency is US dollars. How and when are they paid until then? | Monthly manual payout from the ledger in US dollars, set in the coach agreement | Jez, Ian | B |
| G-06 | Inconsistency | Whole v3.0 | No §5; two §6; "set up user" under coach management; "PIApp for client"; typos; terms drifting (join code and invite code; question and question request) | Fixed in v5.0 (§15). Re-point the companion specs | Ian | Done |
| G-07 | Inconsistency | §2.4, §3, §4 | The vision and positioning describe an AI that coaches ("at 2am", memory, weekly briefing). The MVP has an AI that refines questions using skills, but no coaching agent | Decide: schedule the coaching agent, or reword the vision to "agent later" and drop claims the MVP cannot meet | Jez, Ian | A |
| G-08 | Inconsistency | §1.2, §5.4 | Notes are in the content service but not in user functionality; personal stats dropped | Keep notes in the MVP (v5.0 assumes yes); stats to Phase 2 | Ian | B |
| G-09 | Missing | §1.2 | Q\&A edge cases: most coaches per question; follow-up or reply to an answer; edit after sending; coach asking for clarification; deleting a question | Phase 1: no threads (a follow-up is a new question); at most 3 coaches; coach may decline **\[P\]** | Ian | B |
| G-10 | Missing | §1.2 | Questions never lapse, so there is no deadline or re-route. A question sent to a slow, unavailable or departed coach stays open, with the user's credit reserved, until the user deletes it. A decline needs a reason and notifies PI Admin | PI Admin report of open questions by age; reminder to the coach after 3 working days **\[P\]**; user can delete and re-ask | Jez | B |
| G-11 | Missing | §1.2, §5 | One-on-one: calls are hosted outside PIapp (Zoom, Teams, Slack). Decided: a cancelled session is refunded at any time, and a session can be rescheduled through a link. Open: who creates the meeting link and how it reaches both people; instant booking or coach acceptance; time zones; who marks a no-show; calls that run short | The booking creates a calendar invite carrying the link the coach supplies **\[P\]**; instant booking against the calendar **\[P\]**; coach marks a no-show **\[P\]** | Jez, Ian | A |
| G-12 | Partly decided | §1.4 | Credit allocation is handled outside PIapp in the MVP, unspent credits stay at client level, and a used-up client blocks booking (BR-61, BR-68, BR-83). Open: whether a minimum purchase returns with billing in Phase 4 | Revisit with Phase 4 billing | Jez, Ian | C |
| G-13 | Missing | §1.4, §5.2 | Credit request: the flow is decided (BR-69); still open are the response time, how many credits an approval adds, and what the approver sees | Response time set in the pilot plan; approve in steps of 12 **\[P\]**; approver sees counts only | Ian | B |
| G-14 | Inconsistency | §4.2 | Client Admin and Sponsor have roles but no Phase 1 sign-in, yet the roles table lets the Client Admin invite users and control join codes | PI Admin acts on request (§5.1); define request channel and response time | Ian | B |
| G-15 | Missing | §4.2 | Sponsor report: contents, cadence, format. k ≥ 5 may hide most breakdowns for a 50-user client | Monthly template; thresholds apply to breakdowns, not totals | Ian | B |
| G-16 | Missing | §4.2 | PI Admin access to question and answer content for support, safety and disputes is not stated | Logged access with reason code (BR-40) | Ian, Legal | A |
| G-17 | Missing | §1.2, §10 | Safety: the classifier covers typed questions only; video answers and calls are unscreened; no coach escalation route; a user may disclose a crisis to the AI; client support resources not captured | Capture support resources at onboarding; named PI escalation contact; report-a-problem; BR-36 | Jez, Legal | A |
| G-18 | Missing | §5.6 | Data model lacked twin, notes, video-category link, approvals, invites, notifications, ratings, parent question and no-show status | Resolved: added to §5.6 after review | Ian | Done |
| G-19 | Missing | §4.1, §5 | Digital twin: how it is built, its fields, what is shared with a coach, whether coach twins are visible to users, how it drives matching | Short form at first sign-in (role, goals, style); user picks fields to share | Jez, Ian | B |
| G-20 | Missing | §1.2, §5.4 | AI suggestions: criteria, transparency, load across 10 coaches (a few may get most requests), coach pause | Criteria as in BR-77; cap open requests per coach; coach "pause" switch | Ian | B |
| G-21 | Missing | §1.6, §5.1 | iPhone only: Android and desktop users at the client; App Store distribution and review of a B2B credits app; managed devices; push or email; languages; accessibility | Check the client's device mix; unlisted distribution; email fallback; English only in MVP | Ian | A |
| G-22 | Missing | §1.2, §5.3 | Answer video: file size, 3-minute limit, what "cropping only" means (trim?), re-record, captions, hosting and retention, weak connections | Trim only; auto captions; provider chosen in the Technical Spec | Ian | B |
| G-23 | Missing | §5.2 | Content operations: no global category list; who builds client categories and terminology; transcript export and categorising each video at load; insight approval workload | Starter taxonomy session with Jez; estimate admin hours per client | Jez, Ian | B |
| G-24 | Missing | §5.2 | Dashboards and reporting have no metric list; administrator operations (MFA, suspend a coach, withdraw an answer, backup targets) not specified | §12 measures become the dashboard list; add admin operations to the Technical Spec | Ian | B |
| G-25 | Missing | §12 | Targets are deferred until after the MVP (decided). Ratings are not in the MVP, so the "rated helpful" measures cannot be tracked until Phase 2\. The pilot term is not stated | Track the other measures from launch; add ratings in Phase 2; confirm the pilot term | Jez, Ian | B |
| G-26 | Missing | §9 | Agreements: client contract, DPA, coach agreement with code of conduct, SME release, privacy notice, terms; coaches' contractor status; indemnity insurance. Content ownership is decided (PIapp owns interview videos, questions and video answers); the coach agreement must say so | List, assign owners, legal review | Jez, Legal | A |
| G-27 | Missing | §1.6 | Pilot plan: client, term, launch date, date coaches are ready, support model and hours, training for users and coaches, how feedback reaches Phase 2 | One-page pilot plan | Jez, Ian | A |
| G-28 | Missing | §4 | Coach conflicts: a coach may also coach the Sponsor or a competitor; confidential company detail in questions. Soliciting users off-platform is outside PIapp's scope | Coach agreement and conflict declaration (outside PIapp) | Jez, Legal | B |
| G-29 | Undecided | §1.4 | Prices are set per client and the share per coach; there are no per-coach prices. Does a premium coach cost more credits? | Same prices for every coach in the MVP; revisit in Phase 2 | Jez | C |
| G-30 | Missing | §5.2 | Terminology: CSV layout (header row, encoding); whether an upload adds, merges or replaces; how a client term matches an app term (case, plural); how terminology is used (search, the AI question conversation, the coach's client summary); who edits client terminology before Phase 3 | Two columns with a header; upload updates lines with the same term and adds new ones; match ignoring case; used in search, the AI conversation and the coach summary **\[P\]** | Ian | B |
| G-31 | Missing | §1.4 | Settings changes: how a price or limit change affects requests already reserved; history of changes; what happens to a coach's earnings when their percentage changes; what an unavailable coach's open questions and booked sessions do | Charge at the price when requested; log every change (BR-82); percentage in force at spend time; open questions stay open, booked sessions stand (BR-80) | Ian | B |
| G-32 | Missing | §7.3 | Sign-in: email and Google are specified; the first client may require SAML single sign-on | Ask the first client for its identity provider before build | Ian | A |
| G-33 | Undecided | §7.3, §11 | Personal data is kept indefinitely, including after a user leaves. This may conflict with deletion rights that the client's DPA or privacy law give employees | Confirm with legal; word the DPA and privacy notice to match | Jez, Legal | A |
| G-34 | Missing | §7.6, §10 | Safety flag: what the notified person sees and does. A flag names the user, which sits against the rule that a Client Admin sees no individual's data (BR-40, BR-42). Follow-up with the user is not defined | In the MVP PI Admin is the notified person and can open the question under BR-40. For Phase 3, decide whether a Client Admin sees only that a flag occurred, or who **\[P\]**; define follow-up with the user | Jez, Legal | A |

---

## **Appendix B. Traceability: validated v3.0 decisions to v5.0**

| v3.0 content | Kept in v5.0 at |
| ----- | ----- |
| Two-sided marketplace; B2B with Sponsor, Client, Users | §1.1, D-01 |
| Content service (free, login, YouTube library, client categories) | §1.2, §5.4, BR-04, BR-08 |
| Q\&A flow, AI validation and split, choose coaches, portrait video under 3 minutes | §1.2, §5.3, §5.4, §5.5, BR-72, BR-73 |
| One-on-one flow | §1.2, §5.5, BR-77 |
| Credit price, 12-credit limit, 20% coach (now defaults, overridable per client or coach; minimum purchase superseded in v5.0: none in MVP) | §1.4, BR-61, BR-65, BR-66, BR-69 |
| Q\&A and one-on-one credit costs | §1.4, BR-63 |
| Coach qualification, 10 interviews, 10 coaches at launch | §1.5, BR-70 |
| Phases 1–4 | §1.6, §6 |
| Problem, assets, opportunity | §2 |
| Vision, positioning, differentiators | §3 |
| 16 entities and the roles (SME appears in videos only and is not stored in PIapp) | §4.1, §4.2 |
| PI Admin, coach and user functions | §5.2, §5.3, §5.4 |
| 14-entity data model | §5.6 |

