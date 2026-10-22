# Data Dictionary and Business Rules to Confirm

## Core entities
- `users`: login identity and active status.
- `roles`, `user_roles`: role assignment; server-side permission checks.
- `customers`: agency clients/accounts.
- `airlines`: canonical airline directory.
- `portal_accounts`: reference to secret storage, not plaintext credentials.
- `bookings`: booking lifecycle and source reference.
- `passengers`: passenger details required for ticketing.
- `pnrs`: PNR code and source context; do not assume global uniqueness without validation.
- `tickets`: ticket number, passenger/booking, lifecycle status, source.
- `ticket_price_components`: typed fare/tax/EMD/charge values.
- `payments`: money received or paid.
- `payment_allocations`: payment applied to one or more receivable items.
- `financial_accounts`: cash, bank, airline, receivable and payable accounts.
- `financial_transactions`: immutable movement/source reference.
- `reconciliation_cases`: matched/unmatched/mismatch cases and human resolution.
- `integration_runs`: connector run status and counts.
- `staged_records`: normalized source rows awaiting validation/review.
- `audit_events`: actor, action, entity, timestamp and correlation ID.

## Rules requiring business sign-off
1. What does “profit” mean in reports: gross margin, ticket contribution, or net profit after overhead?
2. How are TOPUP/advance payments represented relative to airline wallet balance and airline payable?
3. Is EMD a cost component, service document, or informational field for this workflow?
4. Are refunds/cancellations in MVP? If yes, what states and reversal rules apply?
5. Are all amounts PKR, or must currency conversion be supported?
6. What date controls sales reporting: booking date, issue date, transaction date or settlement date?
7. How should opening balances be imported and approved?
8. Can a payment cover multiple tickets? Can one ticket be paid in installments or overpaid?
9. What uniqueness rules apply to ticket numbers, PNRs and portal source IDs?
10. Which roles may view customer balances, issue tickets, record payments, and resolve discrepancies?

## Money and audit conventions
- Use PostgreSQL `NUMERIC(14,2)` (or precision approved for the agency) and Python `Decimal`.
- Keep currency explicit.
- Store timestamps in UTC; display in the agency's confirmed timezone.
- Never silently update posted financial records; use reversal/adjustment and audit.
- Store extraction source, time, validation result and confidence where applicable.
