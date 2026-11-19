# 5. Risk register (starter)

Score likelihood and impact from 1 (low) to 5 (high). Review weekly. A risk with no owner is not managed.

| # | Risk | L | I | Early warning signs | Mitigation | Owner |
|---|---|---:|---:|---|---|---|
| 1 | Data loss or corruption during the migration | 2 | 5 | Validation mismatches in rehearsals | Three full rehearsals, checksums on critical tables, tested restore, source kept read-only | Data lead |
| 2 | Cutover window overruns | 3 | 4 | Rehearsal timings drifting upward | Time every step, agree a hard stop and rollback trigger, shrink the data moved in the window | Migration lead |
| 3 | Performance regression on the new stack | 3 | 4 | Staging load tests worse than baseline | Size from real metrics, add a connection pooler, load test with production-like data, keep traffic shift gradual | App lead |
| 4 | Cost overrun | 4 | 3 | Budget alerts, NAT and data transfer growth | Model costs up front, tag everything, anomaly alerts, endpoints for S3 and DynamoDB, review weekly during migration | Platform lead |
| 5 | Team skills gap on AWS operations | 3 | 4 | Slow resolution of staging incidents | Training, pairing, game days, a time-boxed external advisor | Engineering manager |
| 6 | Third-party integrations break due to IP or auth changes | 3 | 3 | Partners not responding to notices | Inventory integrations early, notify at least four weeks ahead, static egress IPs | Integration owner |
| 7 | Double-running cost drags on | 3 | 2 | Old environment still billed after cutover | Fixed stability window, decommission date, owner for shutdown | Platform lead |
| 8 | Security gaps in the new environment | 2 | 5 | Findings in pre-launch review | Security baseline in foundations, review before production traffic | Security lead |
| 9 | Scope creep (refactors, features) | 4 | 3 | Change requests entering the plan | ADR process for scope, feature freeze near cutover | Migration lead |
| 10 | Key-person dependency | 3 | 4 | One person holds the runbooks in their head | Pair on every critical task, written runbooks, rehearsals run by different people | Engineering manager |
| 11 | Compliance or contract issues (data location, subprocessors) | 2 | 4 | Customer questionnaires mention hosting | Check contracts early, update subprocessor lists, choose regions deliberately | Legal and product |
| 12 | Undiscovered dependencies | 3 | 3 | Surprises in staging | Traffic and egress capture, config diff between old and new, shadow traffic | App lead |

## How to use it

1. Copy the table into your tracker and replace the examples with your own.
2. Add a date and trend to each risk at every review.
3. Link each high risk (score of 12 or more) to a specific mitigation task with an owner and a date.
