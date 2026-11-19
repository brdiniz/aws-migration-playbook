# 3. Workstreams and timeline

Run three workstreams in parallel, with a fourth thread for people and process. The split exists so that a problem in one (usually data) does not stall the others.

## 3.1 The workstreams

### A. Platform foundations
**Goal:** a production-grade AWS environment that no workload depends on yet.

- Accounts, organisation policies, SSO and roles
- Network: VPC, subnets, routing, endpoints, DNS zones
- Infrastructure as code repository, state handling, review process
- CI/CD pipeline that builds, tests, scans and deploys containers
- Observability: metrics, logs, traces, dashboards, alerts, on-call routing
- Security baseline: audit logging, threat detection, secret management
- Cost guardrails: budgets, anomaly alerts, tagging policy

**Exit criteria:** a "hello world" service deploys through the pipeline into production, rolls back automatically on a failed health check, and alerts a human.

### B. Data migration
**Goal:** the production database and files live on AWS, kept in sync with the source until cutover.

- Database target sized from real metrics, not the old plan's labels
- Choose the approach (see [ADR 0002](adr/0002-database-migration-approach.md)): dump and restore in a window, logical replication, or a change-data-capture service
- Rehearse the full migration at least three times with production-sized data and record timings
- Validate: row counts, checksums on critical tables, application-level smoke tests
- File and object migration with checksums
- Backup, restore and failover drills on the new database

**Exit criteria:** a rehearsal completes within the agreed window, validation passes, and the team can restore from backup into a clean environment.

### C. Application migration and cutover
**Goal:** the application runs on AWS, serves a slice of traffic, then all traffic.

- Containerise services and workers, remove local-disk assumptions
- Configuration and secrets moved and verified
- Staging environment on AWS that mirrors production
- Load and soak tests against the new stack, compared to the baseline
- Traffic shifting plan (see [cutover and rollback](04-cutover-and-rollback.md))
- Integration owners informed, IP allowlists updated

**Exit criteria:** 100% of traffic served from AWS for the stability window with metrics at or better than baseline.

### D. People and process
**Goal:** the team can run what it has built.

- Training and pairing on the new stack
- Runbooks and incident response updated for AWS
- On-call rotation tested with game days
- Communication plan for customers and internal stakeholders

## 3.2 Phased timeline (typical for a mid-size SaaS)

| Phase | Weeks | A: Foundations | B: Data | C: Application | Gate |
|---|---|---|---|---|---|
| 0. Assess and plan | 1-3 | Readiness gaps | Sizing, approach decision | Inventory | Go decision and ADRs signed |
| 1. Build foundations | 3-8 | Core build | Target database up, first rehearsal | Containerise, staging | Hello-world service in production |
| 2. Prove it | 8-14 | Observability hardening | Continuous sync running, rehearsals 2 and 3 | Load and soak tests, pilot tenants | Rehearsal inside window, tests at or better than baseline |
| 3. Cut over | 14-16 | On call | Final sync, switch | Traffic shift in steps | Stable at 100% |
| 4. Stabilise | 16-24 | Cost tuning | Source kept read-only | Decommission plan | Stability window passed |

Durations scale with team size and data volume. Treat the gates, not the dates, as the commitment.

## 3.3 Governance

- Weekly steering note: progress against gates, top three risks, decisions needed
- One accountable owner per workstream, one overall lead
- Scope changes (new features, refactors) go through the same ADR process
- A freeze period around cutover for unrelated risky changes

## 3.4 Definition of done

The migration is done when the old environment is decommissioned, the cost and reliability metrics were compared to the baseline and shared, and the lessons learned are written down.
