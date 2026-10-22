# Architecture Validation

## Target architecture
React UI -> FastAPI REST API -> domain services -> PostgreSQL.
Background worker -> connector interface -> authorized airline API or permitted Playwright automation -> staging/normalized records -> validated domain service.
AI assistant -> approved metric/query layer -> read-only database access -> answer with filters, period and as-of timestamp.

## Validate these boundaries
- React must never calculate authoritative balances or decide permissions.
- All writes pass through FastAPI domain services and database transactions.
- Connector code must not write business tables directly; it should stage and validate source data.
- External portal calls run asynchronously; user requests should receive a job ID rather than waiting for a browser session.
- Retries must be idempotent. A repeated sync cannot create a duplicate ticket or duplicate financial posting.
- LLM output is untrusted. No arbitrary SQL execution, direct ticket issuance, refund, or financial posting by AI.
- Financial postings should be corrected with reversal/adjustment records, not silent destructive edits.
- Use NUMERIC/Decimal for money; never binary floating point.
- Store timestamps in UTC and display agency-local time. Confirm timezone with the business.
- Use structured logs with correlation IDs; redact credentials, tokens and unnecessary passenger information.

## Recommended component boundaries
1. `auth`: users, roles, permission checks.
2. `customers`: customer master data.
3. `ticketing`: bookings, passengers, PNRs, tickets, ticket status.
4. `finance`: payments, allocations, expenses, accounts, journal/ledger.
5. `integrations`: connector configs, sync jobs, staged source records.
6. `reconciliation`: matching, exceptions, review resolution.
7. `reporting`: metric definitions and exports.
8. `assistant`: question interpretation over approved metrics.
9. `audit`: append-only business event records.

## Connector contract
Each connector should expose equivalents of:
- `health_check()`
- `fetch_records(cursor_or_window)`
- `normalize(raw_record)`
- `validate(normalized_record)`
- `record_run_result(...)`

Do not couple core ticketing logic to portal-specific CSS selectors or page structure.

## Architecture validation checklist
- [ ] Existing codebase inspected; working modules reused.
- [ ] Connector permission/terms confirmed for the selected portal.
- [ ] Portal operation is tested in sandbox/test account where available.
- [ ] Manual/CSV fallback documented.
- [ ] Duplicate source record replay test passes.
- [ ] Failed sync can be retried without duplicate business records.
- [ ] Role checks enforced server-side.
- [ ] Database transaction protects ticket and related records.
- [ ] Audit event written for sensitive operations.
- [ ] Backup restore tested.
- [ ] AI endpoint cannot mutate records and cannot access unauthorized data.

## Decision records still required
- ADR-001: existing schema vs new migrations.
- ADR-002: official API vs permitted browser automation for each portal.
- ADR-003: financial ledger model and posting policy.
- ADR-004: auth/session strategy.
- ADR-005: AI query strategy.
- ADR-006: sync frequency, retention and timezone.
