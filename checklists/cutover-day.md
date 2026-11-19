# Cutover-day checklist

Copy this into your incident channel and tick items with timestamps.

## T-60 minutes
- [ ] Incident commander, scribe, database lead, application lead and communications lead present
- [ ] Replication lag is low and stable
- [ ] Latest backup verified; rollback artifacts ready
- [ ] Dashboards open: error rate, latency, queue depth, database, replication
- [ ] Status page and customer notice ready to publish

## T-0: freeze and final sync
- [ ] Announce start; enable maintenance mode if used
- [ ] Stop writes at the source (record the time)
- [ ] Wait for lag to reach zero
- [ ] Run validation queries and compare results
- [ ] Reset sequences on the target

## Switch
- [ ] Promote the target database
- [ ] Point services to the new database and start workers
- [ ] Shift traffic to the first step (for example 10%)
- [ ] Run smoke tests: sign in, a core write, a core read, an integration call, a file upload and download

## Verify and ramp
- [ ] Compare error rate and latency to the baseline for 15 minutes
- [ ] Decision: go, hold or roll back (use the agreed triggers)
- [ ] Ramp to 50%, repeat checks; ramp to 100%, repeat checks
- [ ] Source database set to read-only

## Close
- [ ] Publish status update
- [ ] Reconciliation check scheduled for the next morning
- [ ] Handover to the on-call engineer with open items
- [ ] Short review within 48 hours: what went well, what to change
