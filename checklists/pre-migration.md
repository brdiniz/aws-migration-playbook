# Pre-migration checklist

Use as a gate before moving production traffic. Every unchecked box needs an owner and a date.

## Foundations
- [ ] Accounts, SSO and least-privilege roles in place; no long-lived admin keys
- [ ] Infrastructure defined in code, reviewed, and reproducible from scratch
- [ ] CI/CD deploys to production with automatic rollback on failed health checks
- [ ] Budgets and cost anomaly alerts configured per account
- [ ] Audit logging and threat detection enabled
- [ ] Tagging policy applied (owner, environment, service)

## Observability and operations
- [ ] Dashboards for the four golden signals per service
- [ ] Alerts for error rate, latency, queue depth, database CPU, connections, storage and replication lag
- [ ] On-call rotation covers the cutover period and has been exercised in a game day
- [ ] Runbooks exist for the top failure scenarios
- [ ] Baseline metrics captured from the old platform for comparison

## Data
- [ ] Target database sized from real metrics
- [ ] Connection pooling tested under load
- [ ] Three full rehearsals completed with production-sized data, timings recorded
- [ ] Validation queries and checksums defined and passing
- [ ] Restore from backup tested into a clean environment
- [ ] Reverse-replication or rollback plan tested and documented

## Application
- [ ] No dependency on the local filesystem or platform-specific features
- [ ] Secrets and configuration verified against the old environment
- [ ] Load and soak tests meet or beat the baseline
- [ ] Scheduled jobs and workers verified, including idempotency on retries
- [ ] Static egress IPs allocated and shared with integration owners

## People and communication
- [ ] Customers and integration owners notified with the agreed lead time
- [ ] Incident commander and roles named for cutover day
- [ ] Rollback triggers agreed in writing
- [ ] Change freeze announced
