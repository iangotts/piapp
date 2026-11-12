# **PIapp — Business Specification v3.0**

|  |  |
| ----- | ----- |
| Product | PIapp — Performance Intelligence app |
| Owner | Ian Gotts, for Jez Cartwright / Performance Intelligence |
| Version | 3.0 28 Oct |
| Status | NOTES revising V2.1 |
| Companion specs | PIapp-UI-Spec-v2*1.md, PIapp-Technical-Spec-v2*1.md |
| Supersedes | v1.2 (27 Sep) and the 16 Oct "business revised spec" v2.0 draft. The earlier v2.0 files I produced on 22 Oct are withdrawn (they wrongly dropped SME, Sponsor and credits) |

---

## **1\. Executive summary**

Jez Cartwright's Performance Intelligence coaching is high-touch, one-to-one work with CxOs at large corporations. It does not scale down the organisation, which is where the need has grown. AI-driven flattening is removing the middle managers who used to coach and translate the business for junior staff, and those staff turn to general AI that gives generic, context-free, often wrong advice.

It is a marketplace

- Coaches get access to client work, with very little friction  
- Clients can offer their employees cost-effective coaching

PIapp packages Performance Intelligence for every level of a client organisation. It is a B2B product: the buyer is usually a CxO Jez already coaches (the **sponsor**), the organisation is the **client**, its employees are **users**. PIapp offers 3 things, paid for with a common currency of **credits**:

1. **Content** Search the PI **video expert-interview** library on YouTube in the client's own categories and terminology, with save, favourite, share and notes. Need to be logged on but no cost.   
2. **Q\&A.** Any user asks a question in the app. There is an AI conversation to validate the question (make sure not ambiguous or if it is multiple questions split it).  User can chose one or more coaches to answer (via search) or AI suggests 3 coaches that match and user can select one or more.  The coach gets a notification and records a **video answer**. Record video on their phone (portrait, less 3mins, only cropping, not editing) and uploads to answer to the app and marks the question complete.  
3. **One-on-one.** The user is matched with a coach, sets up a call and books it.  Coach notified of call.   Conducts call and closes when complete.

Credits/payment approach

- Client buys a block of credits that users can use. A credit costs \$50. Minimum of \$10,000 (200 credits)  
- A user can use up to 12 credits before needing approval to use more  
- Coach receives 20%  
- Content viewing : free  
- Q\&A: each question & answer from a coach is 1 credit.  Same question to 2 coaches is 2 credits  
- One-on-one:  20min call is 3 credits, 40min is 5, 60min is 8 credits

Coach qualification

- Vetted and approved by Performance-Intelligence team.  Initially for MVP this is Jez  
- Coaches need to record 10 **video expert-interview.** 10-20 min,  landscape with coach interviewing SME.  Edited by Performance-Intelligence team.   
- For launch of MVP there need to be 10 coaches

Phasing

Phase 1 \- MVP Launch

- First  client with a block of credits for a team of 50\.  Assume each user consumes 20 credits in a year.  50 x 20 credits \= \$25,000  
- 10 vetted coaches  
- UI  
  - iPhone app is primary interface for users and coaches  
  - PI admin website for concierge activities  
    - Set up client and users	  
    - Manage coaches and their videos  
    - Load credits  
    - Allow user access to more that 12 credits  
    - Reporting across all PIapp and PIApp for client

Phase 2

- Incorporate feedback from MVP trial

Phase 3

- Client Admin portal 

Phase 4

- Billing \- collecting and distributing money for credits

## **2\. Problem and opportunity**

* Coaching scarcity: one coach, a handful of CxOs.  
* Coaching gap: the middle-management coaching layer is gone.  
* Bad substitute: general AI has no company knowledge and no proven method.  
* Assets exist: the PI YouTube channel (long-form expert interviews by top performance coaches), and a network of coaches who can answer questions and coach one-to-one.  
* Precedent: Ian's Inspiring Excellence app (Bubble, 2021\) proved the video model.

Opportunity: sell Jez's method as an organisational capability, with scalable self-serve content and agent at the base and human coaches, paid per use, on top.

## **3\. Vision and positioning**

Vision: every person in a client organisation has coaching that knows their company, from the agent at 2am to a video answer from a named coach to a one-to-one call.

Positioning: "Jez Cartwright's Performance Intelligence — the coaching your CxOs get, for everyone else, in your company's language."

Versus generic AI: **grounded** (vetted expert insights, cited to expert and video moment); **contextual** (client backstory and terminology); **methodical** (awareness, discerning reality, effective choices, grounded confidence, "the elephant in the room"); **remembering** (per user, and across the client); **human on demand** (real coaches when AI isn't enough).

## **4\. Terminology and roles**

### **4.1 Entities**

| Entity | Definition |
| ----- | ----- |
| Client | A customer organisation (tenant). Backstory, users, credits, billing, analytics |
| Sponsor | The CxO who buys PIapp for the client; budget holder and executive owner |
| User | A person inside a client who uses PIapp for their own coaching |
| Coach | A vetted PI coach who answers questions by video and runs one-on-one calls. Network-wide (not tied to one client) |
| SME (Expert) | A person interviewed in a video.  |
| Video | A YouTube video from the PI channel, with PI metadata |
| Insight | An atomic, citable idea extracted from a video transcript  |
| Category | PI-managed classification for videos and insights. Theser are global (PI-app level) and also by client |
| Skill | A coaching playbook the agent follows |
| Backstory | The client's corporate background used as context to frame every search and answer |
| Digital twin | A person's own profile (role, goals, style). Users and coaches each have one |
| Question | A user's request for a coach's video answer |
| Answer | A coaches video answer |
| Session | A booked one-on-one call between a user and a coach |
| Credit | The unit users spend and coaches/SMEs earn  |
| Inbox | A coach's (and user's) queue of requests and notifications |

### **4.2 Roles**

| Role | Scope | Can | Cannot |
| ----- | ----- | ----- | ----- |
| PI Admin | All clients | Load and manage YouTube assets; manage categories, SMEs, coaches, skills; approve insights; create clients and users; maintain any backstory; see analytics across all clients; control billing and credits | Read an individual user's private conversations, notes, twin or memory (BR-40) |
| Sponsor (CxO) | One client | Nominate Client Admins; approve the backstory; see client aggregate analytics and themes (k ≥ 5); receive the sponsor report; use PIapp as a user (Phase 3\) | See any individual's activity, notes, conversations, questions, twin or memory, including direct reports |
| Client Admin | One client | Maintain backstory and glossary; invite, deactivate and manage users; see client & user analytics; allocate and top up client credits and manage billing (Phase 3\) | See other clients; edit videos, categories or insights; read individuals' private data or question content |
| User | Self, one client | Search and watch; save, favourite, share; notes; own stats; weekly briefing; agent; manage own twin; ask coaches questions; book one-on-ones; spend credits; top up where the client allows | See other users' data; change backstory |
| Coach | Network-wide, own work only | Maintain own profile and twin; set availability; receive requests in an inbox; record video answers; run one-on-one sessions; see own earnings and sessions | Answer or see questions not directed at them (BR-72); see a user's conversations, notes, memory or other coaches' questions or earnings |
| SME | Own content only  | See aggregate performance of own videos and insights; edit profile (PI approves); manage consent; flag an insight for correction; see credits earned and statements (Phase 4\) | See any user's identity or activity; see client names unless the client agreed (BR-53); see other SMEs' performance |

### 

### **6\. Functionality (MVP)**

### **6.1 PI Admin experience (Web)**

Client management  

- Set up client profile: name, backstory, terminology  
- Add users and send invite code  
- Manage credits: add, top up, approve user allocation  
- Dashboard: User signup, user credit usage

Coach management

- Set up user and send invite code  
- Upload video to YouTube  
- Evaluate video transcript to categorize and provide AI insights  
- Dashboard: answers, sessions, credits earned

App management

- Dashboard: users, credit usage, questions, answers, sessions  
- Backup/restore

### **6.2 Coach experience (Mobile)**

- Sign in from PI Admin invite email   
- Sign in using email or Google, & password reset  
- Update profile; headshot, bio, digital twin  
- Connect calendar for session availability  
- Check inbox for questions and session bookings  
- Record and upload answers  
- Run session and mark complete  
- Dashboard: views of videos, questions & answer history, session history  
- Notifications: question request, session request, session scheduled

### **6.3 User experience (Mobile)**

- Sign in from PI Admin invite email   
- Sign in using email or Google, & password reset  
- Update profile (headshot, bio) and digital twin, connect to calendar to get sessions sync'd  
- Videos; search by category or AI match on profile, watch, fave, save, share, list of saves, fave, watched   
- Questions; create a question, AI validates/.refines question, edit, submit to coach or coaches (search coach or AI recommends), list of answer to questions  
- Sessions; request session (search coach or AI recommends); past and upcoming, book session date/time and cancel/reschedule, sync to calendar  
- Notifications: new videos, answers to submitted questions, session scheduled, out of credits  
- Credits; history of usage, 

**6.4 Data Model**

**6.5 Open Questions**

- How do users schedule sessions with coaches? Provide coach calendar availability like calendly?  
- 

## 

## **6\. Capabilities**

| ID | Capability | Phase |
| ----- | ----- | ----- |
| CAP-01 | Asset management: load YouTube videos, summaries, SME, categories, tags; approval before publish | 1 |
| CAP-02 | Category management | 1 |
| CAP-03 | Client onboarding: create client, users, backstory, glossary | 1 |
| CAP-04 | Authentication: login, password reset, invitation or join-code acceptance | 1 |
| CAP-05 | Video search in client terminology | 1 |
| CAP-06 | Personal library: save, favourite, history | 1 |
| CAP-07 | Share a video inside the client, or by link | 1 |
| CAP-08 | Notes pinned to a video (timestamp) and a notes view | 1 |
| CAP-09 | Personal stats | 1 |
| CAP-24 | User registration, personal profile (twin) and client profile; user dashboard (basic: stats; credit panels from Phase 3\) | 1 |
| CAP-18 | Analytics: PI Admin across clients; Client Admin for own client | 1 basic, 3 full |
| CAP-10 | Insight extraction into a graph | 2 |
| CAP-11 | Skills management | 2 |
| CAP-12 | Coach agent (web), grounded, cited, backstory-aware | 2 |
| CAP-13 | MCP server | 2 |
| CAP-14 | Digital twin (users) | 2 |
| CAP-23 | Weekly briefing curated from profile | 2 |
| CAP-15 | iOS app with web parity | 3 |
| CAP-16 | Client Admin self-service: users, backstory, credits | 3 |
| CAP-17 | Conversation memory and client-level learning | 3 |
| CAP-21 | SME portal: dashboard (video activity, credits earned), profile, consent, insight corrections | 3 |
| CAP-26 | Coach accounts and portal: profile and twin, availability, inbox, earnings, sessions | 3 |
| CAP-27 | Q\&A: post a question, choose or auto-match a coach, coach records video answer | 3 |
| CAP-25 | Credits: ledger, client allocation, reserve/spend/refund, earnings | 3 (internal ledger, manual allocation) |
| CAP-29 | Inbox and notifications for users and coaches | 3 |
| CAP-28 | One-on-one: match, schedule, book, run, spend credits | 4 |
| CAP-19 | Billing: subscriptions, seats, credit packs, user top-up, client self-service | 4 |
| CAP-22 | Payouts: credits earned by SMEs and coaches converted to money, monthly statements | 4 |
| CAP-20 | Android app | 4 |

Note on CAP-17: Phase 2 stores conversation threads for continuity; Phase 3 adds long-term memory and client learning (ADR-012).

## **6\. Business rules**

**Content and curation** \- BR-01 Only videos from the PI YouTube channel, or channels PI Admin approves, are loaded. \- BR-02 A video is not visible until a PI Admin publishes it (draft → in review → published/rejected). \- BR-03 Every published video has one primary SME, at least one category and a summary. \- BR-04 PI library videos play only in YouTube's embedded player; never downloaded, re-hosted or cached. (Coach answer videos are different content, see BR-73.) \- BR-05 A video can be restricted to specific clients; default all clients. \- BR-06 An insight is not usable by the agent until approved. \- BR-07 Every insight carries attribution: SME, video, timestamp.

**Client context** \- BR-10 Each client has one versioned backstory; the agent uses the current published version. \- BR-11 A client glossary maps client terms and acronyms to PI categories and plain meanings. \- BR-12 Backstory content is confidential to the client and PI; never used for another client's users. \- BR-13 The backstory is built only from material the client provides and the Sponsor (or Client Admin delegate) approves in writing. Nothing learned in confidential one-to-one coaching enters a backstory, skill or learning without the CxO's explicit written approval.

**Users and access** \- BR-20 A user belongs to exactly one client. Coaches and SMEs are network-wide accounts with no client. \- BR-21 Users join by invitation or a client join code controlled by the Client Admin; no open self-registration. \- BR-22 Deactivation removes access immediately; personal data kept 30 days then deleted unless the client requests otherwise. Unspent personal credits are handled per BR-61. \- BR-23 Sharing is within the client by default. Public share links are a per-client PI Admin setting, off by default.

**Agent and memory** \- BR-30 The agent answers only from approved insights, the client backstory, the user's twin and memory; otherwise it says so and suggests videos or a coach. \- BR-31 Every substantive claim is cited to an insight (SME, video, timestamp). \- BR-32 Where experts disagree, show both positions. \- BR-33 Client-level memory holds only de-identified, aggregated learnings (k ≥ 5). \- BR-34 A user can view and delete their own memory and conversation history.

**Privacy** \- BR-40 No admin role, Sponsor or coach can read an individual's agent conversations, notes, twin or memory. Admins see aggregates only. (A coach sees only what a user sends them, BR-71.) \- BR-41 Analytics for Sponsor and Client Admin use a minimum group size of 5 users. \- BR-42 The Sponsor has no extra visibility of individuals. Stated in the client contract and user privacy notice. \- BR-43 Themes (what people ask about, including Q\&A topics) are reported as de-identified topics with counts, never quotes.

**Credits** (new) \- BR-60 Credits are the single unit for paid interactions: coach Q\&A, one-on-one sessions, and agent usage above the client's allowance. \- BR-61 Credits come from (a) the client allocation (pool or per seat, set by contract; managed by the Client Admin) or (b) a user top-up, only where the client enables it. Whether unspent personal top-up credits are refundable on leaving is open (Q-19). \- BR-62 Credits are reserved when a request is made and spent when the coach delivers (answer published or session completed). They are refunded if the coach declines, does not respond within the service window (proposed 5 working days for Q\&A), or the session is cancelled inside the free-cancellation window. \- BR-63 PI Admin sets the credit price of each service, per coach tier if needed. Prices are shown before the user confirms. \- BR-64 The credit ledger is append-only. Every spend and earning has a matching entry. \- BR-65 Coaches and SMEs earn credits (§8.2). Conversion to money is by agreement (Q-12, Q-20).

**Q\&A and one-on-one** (new) \- BR-70 Coaches are vetted and invited by PI Admin, accept a code of conduct, and are bound by §10 boundaries. \- BR-71 A coach sees only: the question text, the asker's first name and role, the twin fields the user chooses to share, and a short client context summary. Never the user's agent conversations, notes, memory or other questions. The user sees this list before sending. \- BR-72 A question is directed to one coach: either the user's choice or an automatic match (topic fit, skills, availability, load, language). A coach may decline; the question is then re-matched. Coaches cannot see questions not allocated to them. \- BR-73 A coach's video answer is recorded in-app, hosted by PIapp (not YouTube), and visible only to the asker, unless the user shares it inside the client (BR-23). Adding answers to the library needs the user's and the coach's consent (Q-21). \- BR-74 Coaches see their own earnings only. \- BR-75 Sponsor and Client Admin see Q\&A and session volumes and de-identified topics at k ≥ 5; never the question, the answer video or who asked. \- BR-76 Calls are not recorded by default; recording needs both parties' consent. \- BR-77 Coach matching for one-on-one uses the same criteria as BR-72, plus calendar availability; the user can choose another coach from a shortlist.

**SMEs** \- BR-50 An SME sees only their own content's performance, in aggregate. No user is identified. \- BR-51 SME breakdowns use k ≥ 5\. \- BR-52 SME accounts are created by PI Admin by invitation, linked to the SME record. \- BR-53 Client names are not shown to SMEs by default; sector shown only where ≥ 5 clients. \- BR-54 An SME can flag an extracted insight as inaccurate; it is withdrawn from the agent until PI Admin reviews it (target 5 working days). \- BR-55 SME earnings apply only to SMEs who accepted the current agreement and granted extraction consent. Withdrawing consent stops future accrual; amounts earned are still paid. \- BR-56 Engagement by the SME, PI staff and test accounts is excluded from attribution.

## **7\. Phased scope**

The revised spec defines the new features but not their phases. Phases below are a proposal (Q-18); Phases 1, 2 and 4 follow the earlier brief where it applied.

### **Phase 1 — Search and watch YouTube**

In: PI Admin console (categories, assets, SMEs, client onboarding, users, backstory, glossary, basic analytics); User web app (registration with personal and client profile, login and reset, search, save, favourite, share, stats, notes, basic dashboard). Sponsor report: PI Admin exports a monthly aggregate PDF per client. Exit: one pilot client with ≥ 25 active users; catalogue published and categorised; backstory approved.

### **Phase 2 — Agent and briefing**

In: insight extraction to graph; skills; web conversation interface; MCP server; digital twin; conversation threads; **weekly briefing**; attribution ledger from the first agent answer (watch minutes and citations per SME). Gate: rights and consent clearance (§9) before extraction. Jez reviews answer quality before client users see the agent.

### **Phase 3 — iOS, humans and memory**

In: iOS app; Client Admin console; Sponsor dashboard; long-term memory and client learning; SME portal; **Coach accounts and portal; Q\&A with coach video answers; credit ledger (client allocation set manually, no card payments yet); inbox**.

### **Phase 4 — Billing, one-on-one and Android**

In: Stripe billing, seats, credit packs, user top-up, client billing self-service; **one-on-one matching, scheduling and booking**; payouts for coaches and SMEs with statements; Android app. Gate: coach and SME payout agreements reviewed by a lawyer and accepted by the first cohort; tax onboarding.

## **8\. Commercial model**

* Buyer: the Sponsor, usually an existing Jez coaching client. Contract per client; route to market is Jez's CxO relationships, then referrals. No self-serve client sign-up.  
* Complements one-to-one coaching of the CxO; bundling is an option to test.  
* Pricing structure (proposed, no prices set): annual platform fee, per-seat licence, and a credit allocation per client; additional credit packs; users may top up where allowed. Tiers: Video, Coach (agent, MCP, memory), and credit-funded human services.  
* Phases 1–3 are contracted pilots invoiced manually; Stripe is Phase 4\.

### **8.1 Credit economy**

* **Spend.** Users spend credits on Q\&A (a fixed price per question, per coach tier), one-on-one sessions (price per length), and agent usage above allowance.  
* **Reserve, spend, refund** per BR-62.  
* **Visibility.** The user dashboard shows credits spent and balance; the Client Admin sees client totals.

### **8.2 Earnings for coaches and SMEs**

* **Coaches** earn a share of the credits spent on their delivered answers and sessions (percentage open, Q-12).  
* **SMEs** earn credits from attribution units: minutes watched of their published videos (at most once per user per video per day) and citations of their insights in agent or MCP answers, weighted up when the user opens the clip or rates the answer helpful. Weights are set by PI and published in the agreement. Multi-SME videos split equally unless PI Admin sets otherwise; whether the interviewer earns a share is open (Q-13).  
* **Funding.** SME credits come from a defined percentage of net subscription revenue forming a monthly pool, split by units (as in v1.2); this is separate from coach earnings, which are paid from the credits users spend. Alternative to test: a fixed credit rate per unit, which is simpler but not capped by revenue (Q-20).  
* **Statements.** Monthly statement per SME and coach; payouts quarterly above a threshold; disputes within 60 days.  
* **Start.** Accrual starts at Phase 4 go-live unless PI pays retrospectively on Phase 2–3 records (Q-14). Phase 3 coach credits are tracked in the ledger and settled manually.

## **9\. Content, rights and consent**

* Embedding YouTube videos (Phase 1\) is allowed under YouTube's terms with the player and branding intact.  
* Extracting and reusing what experts say (Phase 2\) needs written clearance from PI as channel owner; per-SME consent (off by default); a takedown process removing an SME's insights within 7 days; caption access authorised by the channel owner. Legal review is a hard gate.  
* Coach answer videos and call content belong to the coach and user under the coach agreement: PIapp stores them to deliver the service; reuse needs consent (BR-73).

## **10\. Coaching boundaries and safety**

* Performance coaching only; not therapy, medical, legal or HR-investigation advice. The product says so.  
* On signs of crisis or risk of harm the agent stops coaching and gives crisis resources. Coaches must follow the same rule in Q\&A and calls; the platform gives them an escalation route and the user's client support resources.  
* No advice on actions against named colleagues beyond general constructive guidance; no claims about named individuals.  
* A client backstory cannot override these boundaries.  
* Questions sent to coaches are screened by the same safety classifier before allocation; a positive result shows the user support resources and does not route to a coach without the user's confirmation (Q-22).

## **11\. Privacy and data**

* The client is data controller for user data; PI is processor. Coaches and SMEs are PI's contractors; their own data is controlled by PI. A DPA template is needed before the first pilot.  
* US data residency by default; EU is open (Q-05).  
* Conversations, questions and memory are kept until the user deletes them or leaves (then 30 days); coach answer videos follow the same rule for the asker's copy.  
* Model providers must not train on PIapp data. Payment card data never touches PIapp (Stripe).

## **12\. Success measures**

| Measure | Phase 1 | Phase 2+ |
| ----- | ----- | ----- |
| Weekly active users / seats | 40% | 50% |
| Videos watched per active user per month | 4 | — |
| Notes per active user per month | 2 | — |
| Agent conversations per active user per month | — | 6 |
| Weekly briefing open rate | — | 50% |
| Answers rated helpful | — | 80% |
| Answers with at least one citation | — | 100% |
| Q\&A answered within service window | — | 95% |
| Coach answer rated helpful | — | 85% |
| Credit utilisation (spent / allocated) | — | 60% |
| Client renewal | — | 90% |
| SMEs signed in monthly (Phase 3\) | — | 60% of consented SMEs |
| Statement disputes (Phase 4\) | — | \< 2% |
| Seat expansion after pilot | — | ≥ 2× |

## **13\. Risks**

| Risk | Impact | Mitigation |
| ----- | ----- | ----- |
| Rights/consent not obtainable for some SMEs | Thinner corpus | Per-SME consent; consented SMEs only; commission new interviews with consent |
| Corpus too small | Weak answers | Gate Phase 2 on coverage per skill; Jez-authored insights |
| Users share sensitive personal/HR matters | Trust, legal | BR-40, BR-71, safety boundaries, privacy statement |
| Coach quality or conduct varies | Brand damage | Vetting, code of conduct, ratings, PI review, removal |
| Coach supply too thin for demand; slow answers | Refunds, poor experience | Auto-match with load limits, service window, refunds, recruit ahead of rollout |
| Coach sees more than the user intended | Trust | BR-71 consent screen; no access to conversations |
| Credit disputes and refund handling | Support load, margin | Append-only ledger, clear rules BR-62, admin adjustment with reason |
| Video hosting and call tooling cost and compliance | Margin | Hosted-video and call providers per ADR-018/019 with retention limits |
| Client memory leaks individual statements | Trust | BR-33, k ≥ 5, PI review |
| YouTube API/caption limits | Delay | Owner OAuth; manual transcript fallback |
| Model cost exceeds seat revenue | Margin | Credits, per-seat caps, cost dashboard |
| Sponsor expects to see individuals' use | Employee trust | BR-42 in contract; demo the aggregate view |
| Sponsor leaves | Renewal | Second executive owner and a Client Admin at contract |
| Confidential coaching knowledge leaks into the product | Breach | BR-13 and approval log |
| Attribution gamed | Unfair payouts | Once-per-user-per-day rule, BR-56, anomaly checks |
| Tax and payments for international coaches and SMEs | Payout blocked | Stripe Connect handles KYC and tax forms |

## **14\. Decisions and open questions**

**Decisions** \- D-01 B2B; D-02 invitation or join-code entry only; D-04 threads Phase 2, memory Phase 3; D-05 no admin or Sponsor reads individual conversations; D-06 no swipe feed. \- D-07 Buyer is the Sponsor; D-08 SME portal Phase 3; D-09 SME earnings are usage-based (video minutes plus citations), now expressed in credits. \- D-10 Credits are the single currency for paid interactions (from the revised spec). \- D-11 Coaches are a network-wide role, separate from users and SMEs (from the revised spec). \- D-12 Weekly briefing is back in scope (it was dropped in v1.0).

**Open questions for Ian / Jez** \- Q-01 Product name; Q-02 who runs PI Admin; Q-03 client-exclusive content; Q-04 SSO in Phase 1; Q-05 EU residency; Q-06 Jez's method as skills; Q-07 pilot client; Q-08 multi-client users (currently no); Q-09 does an executive's use connect to their coaching with Jez (default no); Q-10 pilot shape; Q-11 Sponsor "ask about my organisation" view. \- Q-12 Percentage of net revenue to the SME pool; coach share of credits spent. \- Q-13 Does the PI interviewer share in a video's units? Q-14 Retrospective payment or start at Phase 4? Q-15 Will any client agree to be named to SMEs? \- **Q-16** Your revised spec's §1 lists "Set up Client profile" for a user. I assumed this means confirming client and team and choosing client terms, with the backstory itself owned by the Client Admin or PI Admin. Correct? \- **Q-17** Your §1 lists "Coach gets notified in inbox of request to record video" under One-on-one. I assumed that is a copy of the Q\&A line and that a one-on-one request notifies the coach to confirm or propose a time. Correct? \- **Q-18**Phases for the new features. I proposed: weekly briefing Phase 2; coach portal, Q\&A and credit ledger Phase 3; one-on-one and payments Phase 4\. Do you want any earlier? \- **Q-19** Are unspent personal top-up credits refundable? Do client-allocated credits expire (for example annually)? \- **Q-20** Credit economics: are coach and SME credits converted to cash at a fixed rate, or paid from a revenue pool? Who sets the credit price of a question and a session? \- **Q-21** May coach answers be reused in the library or the agent corpus (with consent) so one answer helps many users? \- **Q-22** Should a safety-flagged question still go to a coach, or only show support resources? \- **Q-23** Coach network: are coaches only PI-vetted partners, or can client-internal coaches (for example an HR coach) be added to a single client? \- **Q-24** Video calls: use an existing tool (Zoom or Google Meet links) or build calls into PIapp?

## **15\. Changes from v1.2 and from the 16 Oct draft**

| Item | v2.1 treatment |
| ----- | ----- |
| Registration flows, user, SME and coach dashboards | Added (§4.3, UI) |
| Credits, top-up, spend, earn | Added (§8.1, BR-60..65); Phase 3 ledger, Phase 4 payments |
| Coach role and entity | Added (§4.2, BR-70..77) |
| Weekly briefing | Added (CAP-23, Phase 2); it was dropped in v1.0 |
| Q\&A with coach video answers | Added (CAP-27, Phase 3\) |
| One-on-one booking | Added (CAP-28, Phase 4\) |
| SME portal, revenue share, Sponsor | Retained from v1.2; SME earnings now expressed as credits |
| Public sign-up (revised spec: "create user account") | Kept invitation or join code (BR-21) |

## **16\. Change log**

| Version | Date | Change |
| ----- | ----- | ----- |
| 2.1 | 22 Oct 2026 | Merged v1.2 with the 16 Oct revised spec: Coach role, credits, weekly briefing, Q\&A, one-on-one, dashboards; BR-60..77; Q-16..24 |
| 2.0 | 16 Oct 2026 | Ian's draft (partial: exec summary and roles) |
| 1.2 | 27 Sep 2026 | SME portal and revenue share |
| 1.1 | 27 Sep 2026 | Sponsor |
| 1.0 | 27 Sep 2026 | First issue |

