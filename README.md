# Airline Ticketing FYP — Implementation Pack

Stack selected for this plan: FastAPI backend + React frontend. Current reported stage: airline automation. Target time remaining: 4–8 weeks.

## Assumptions and limitations
- This pack is based on the project report and architecture plan in the conversation. The actual source repository and live airline portal access were not inspected in this task.
- Airline API availability, RPA permissions, portal terms, test credentials, current schema, and actual spreadsheet columns remain unverified.
- Recommended delivery strategy: finish one safe end-to-end workflow and one authorized connector; do not attempt all portals unless access and schedule allow.
- Use the SQL as a reviewable starting migration, not as a production migration without checking existing tables and business/accounting rules.
- The OpenAPI file is a contract starter, not a complete generated FastAPI schema.
- No CAPTCHA/MFA bypass or unauthorized automation is in scope.

## Pack contents
- `docs/architecture-validation.md`: architecture checks and decisions
- `docs/implementation-plan.md`: 4–8 week schedule and priorities
- `docs/data-dictionary.md`: entity definitions and unresolved rules
- `database/erd.mmd`: Mermaid ERD starter
- `database/schema.sql`: PostgreSQL starter schema
- `api/openapi-starter.yaml`: API contract starter
- `planning/backlog.csv`: prioritized work backlog with acceptance criteria
- `tests/test-plan.md`: testing matrix and release gates
- `tests/reconciliation-cases.csv`: high-value edge-case test data

## First 48 hours
1. Confirm one airline portal's authorized integration method and allowed actions.
2. Inventory the existing repo and identify what's already implemented; do not rebuild working modules.
3. Profile a sanitized workbook export and agree accounting definitions with the agency/accountant.
4. Run a vertical slice on mock/import data before connecting the live portal.
5. Freeze the MVP scope and demo criteria with the supervisor.
