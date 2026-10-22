# Customized Implementation Plan — 4 to 8 Weeks

## Delivery principle
Since the project is already at airline automation, do not start by rewriting the whole system. First audit the current repository, preserve working code, and connect automation to a stable staging/validation pipeline. The MVP is one complete, demonstrable workflow, not three brittle portal bots.

## Week-by-week plan (minimum viable 4-week path)
### Week 1 — Architecture and automation audit
- Inventory current FastAPI routes, React screens, database models/migrations, tests and current automation code.
- Confirm authorization and permitted integration method for one target portal.
- Define source-to-canonical field mapping for PNR, ticket number, passenger, fare, tax, EMD, charges, customer, booking date, source reference.
- Add connector interface, sync-run state model, structured logs and safe manual/import fallback.
- Deliver: architecture decision records, field mapping, connector risk register, smoke tests.

### Week 2 — Reliable connector and ingestion
- Implement or harden one connector only.
- Use staging records and schema validation before creating/updating business records.
- Add bounded retry/backoff for transient errors; no endless retry for MFA, CAPTCHA, permission or credential errors.
- Add idempotency key/source fingerprint and duplicate review queue.
- Deliver: connector tests with saved fixtures, replay-safe import, sync status UI/API.

### Week 3 — End-to-end ticket and finance correctness
- Connect validated ticket records to customer/ticketing domain service.
- Verify payment allocation, airline payable and ledger policy with the business owner/accountant.
- Implement reconciliation cases and review resolution.
- Deliver: ticket -> payment/cost -> reconciliation -> dashboard vertical slice, plus edge-case tests.

### Week 4 — Hardening and FYP demo
- Run regression, authorization, connector failure, duplicate replay and backup/restore tests.
- Add demo data and a deterministic portal-mock mode.
- Document known limitations, setup, architecture, test results and demo script.
- Deliver: release candidate, screenshots, test report and supervisor review.

## Extension path for 6–8 weeks
### Week 5 — Management reporting
- Finalize KPI definitions and report filters.
- Cross-check dashboard totals against backend query results.
- Add exports and role-aware views.

### Week 6 — Constrained AI assistant
- Start with approved metric/query templates, not arbitrary SQL.
- Return answer + metric + date filters + as-of timestamp + warnings.
- Add benchmark questions and permission/refusal tests.

### Week 7 — Anomaly detection and polish
- Implement deterministic rules first: duplicate ticket, missing payment, mismatch, negative balance, unusually high amount.
- Add statistical/ML detection only if enough clean history exists.
- Show reasons and require human review.

### Week 8 — Pilot and documentation
- User acceptance testing with agency representatives.
- Verify backup restoration and access matrix.
- Complete ERD, API docs, test report, FYP chapter diagrams and final presentation.

## MVP exit criteria
- One authorized connector or explicitly documented import/mock fallback.
- Replaying the same source data does not duplicate tickets or financial postings.
- Every sync has visible status, counts, errors and retry behavior.
- Uncertain extraction or matches are held for review.
- Financial calculations use approved deterministic rules.
- Ticket, payment, reconciliation and dashboard totals agree for the same filters.
- AI is read-only and grounded in approved metrics.
- No critical security or data-integrity tests fail.

## Scope cuts if only 4 weeks remain
1. Support one portal only.
2. Defer forecasting and custom ML.
3. Defer WhatsApp/SMS/customer app.
4. Keep AI assistant to a small allowlisted metric set or defer it until core acceptance passes.
5. Prefer reliable import/manual fallback over risky browser automation if portal authorization is uncertain.
