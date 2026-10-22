# Testing Plan

## Test layers
1. Unit: field normalizers, monetary parsing, duplicate fingerprints, status transitions, matching rules.
2. Integration: FastAPI + PostgreSQL transactions, staging import, audit event creation, job status updates.
3. Connector contract: parser fixtures saved from authorized test/sanitized pages; do not depend on a live portal for every CI run.
4. End-to-end: sync/import -> staged row -> validated ticket -> payment allocation -> reconciliation -> dashboard.
5. Security: role bypass, unauthorized ticket/ledger access, secrets leakage, AI prompt injection and query scope.
6. UAT: agency owner/accountant validates opening balances and example ticket/payment cases.

## Required scenarios
- Same source record imported twice.
- Same ticket number appears in two records with conflicting passenger or amount.
- Portal returns partial data or changes a field label.
- Browser/session times out before confirming whether the action succeeded.
- Portal authentication fails or MFA is required.
- Network failure occurs after source fetch but before database commit.
- Payment is partial, split across tickets, or over-allocated.
- Ticket is cancelled/refunded after payment.
- Ticket cost exists but customer payment is missing.
- Payment exists but ticket cannot be found.
- Two users attempt to resolve the same reconciliation case.
- Agent tries to read accountant-only ledger data.
- AI is asked to reveal passenger data or perform a financial mutation.
- Report date boundary crosses midnight in agency timezone.
- Database restore from backup.

## Release gates
- No critical data integrity or authorization failures.
- Replaying the same connector fixture does not duplicate business records.
- Every failed/partial run is visible and diagnosable.
- All monetary calculations use Decimal/NUMERIC.
- Reconciliation cases retain reason, evidence and resolution history.
- Dashboard totals match the API report for identical filters.
- AI answer has source metric and filters; AI cannot mutate records.
- Backup restoration is demonstrated.
