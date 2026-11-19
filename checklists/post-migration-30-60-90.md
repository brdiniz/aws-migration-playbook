# Post-migration: 30 / 60 / 90 days

## First 30 days: stabilise
- [ ] Daily review of error rates, latency and cost for the first two weeks
- [ ] Reconcile data between old and new for critical tables
- [ ] Tune alert thresholds to cut noise without missing real issues
- [ ] Confirm backups run and test one restore
- [ ] Source environment kept read-only, with a documented decommission date

## Days 31-60: optimise
- [ ] Right-size tasks, instances and databases from real utilisation
- [ ] Review NAT, data transfer and cross-AZ costs; add endpoints where they help
- [ ] Set log retention and sampling policies
- [ ] Identify steady workloads and evaluate Savings Plans or reserved capacity
- [ ] Compare actual costs with the business case and note the differences

## Days 61-90: close out
- [ ] Decommission the old environment and cancel contracts and add-ons
- [ ] Remove old credentials, DNS records and allowlist entries
- [ ] Run a game day on the new platform (failover, restore, regional dependency)
- [ ] Publish the results: availability, latency, deploy frequency, cost, against the baseline
- [ ] Hold a retrospective and update the playbook with what you learned
