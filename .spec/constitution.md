# Constitution — PIapp

Rules every agent and every human obeys on this project. Short on purpose. If a rule is not checkable, it does not belong here.

## 1. Authority
1. The Business Spec is the authority. Tech and UI specs implement it; they never override it.
2. Precedence when documents disagree: Business Spec > decision log > Tech Spec > UI Spec > code.
3. A conflict is never resolved silently. Record it in the decision log, then fix the lower document.

## 2. Identifiers
1. Every requirement has a stable ID (BR-, CAP-, D-, G-). IDs are never reused or renumbered.
2. Tech and UI specs must cover every authority ID (implemented, or explicitly "deferred: <reason>").
3. `scripts/trace_check.py` must pass before any spec is called final and before any build starts.

## 3. Change control
1. Spec changes come before code changes. No code that implements something the spec does not say.
2. Every spec change bumps the version and adds a changelog line naming the IDs touched.
3. Every decision with a trade-off gets a decision-log entry (what, why, alternatives, what would reverse it).

## 4. Human gates (agent stops and asks)
1. Before spec status moves from Draft to Approved.
2. Before any change that is hard to undo: data migration, deleting data, spending money, publishing, changing credentials.
3. When two authority statements contradict each other.
4. When an assumption would change scope, cost, or a user-visible behaviour.

## 5. Review
1. Reviews run in a fresh context by `spec-reviewer` (read-only). The author never grades their own work.
2. A blocker finding stops the pipeline. Major findings need a fix or a logged decision to accept.

## 6. Build
1. Plan before build; small, reversible steps; each step names the IDs it satisfies.
2. Each step has a verification (test, command, or a written manual check) defined before the step is built.
3. Never mark a step done on the agent's say-so; show the verification result.

## 7. Drift
1. Code, specs and decisions are re-compared at every milestone with `spec-drift`.
2. Drift is fixed in the direction the decision log says, not whichever is easier.

## 8. Project-specific rules
1. Credits are an append-only ledger. Never UPDATE or DELETE a `credit_txn` row; corrections are new rows with a reason (BR-69).
2. Credit checks are server-side with locking. Client checks are display only.
3. US data residency (D-15). Do not add a sub-processor or region without a decision-log entry and human approval.
4. Questions never lapse (D-14). SMEs appear only in videos and are never stored as people (BR-57).
5. Calls are held outside PIapp (D-21). Do not build call hosting, recording or storage.
6. PI Admin access to member content goes only through the audited `admin_open_content()` path (BR-40).
7. Anything on the parked list (Tech Spec Appendix B) is out of scope until promoted by a decision.
