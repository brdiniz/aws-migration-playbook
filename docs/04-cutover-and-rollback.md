# 4. Cutover and rollback

## 4.1 Choosing a cutover pattern

| Pattern | How it works | Good for | Watch out for |
|---|---|---|---|
| Big bang in a window | Stop writes, final sync, switch DNS, start on AWS | Small databases, tolerant customers | Longest downtime, hardest rollback |
| Weighted DNS or load-balancer shift | Send 1%, 10%, 50%, 100% of traffic to the new stack | Stateless front ends | Both stacks must use the same database, which means cross-network latency |
| Database first, then app | Move the database to AWS while the app still runs on the old platform, then move the app | Teams that want to de-risk data early | Added latency between old app and new database during the interim |
| App first with a replica | Run the new app against a read replica or a synced copy for shadow traffic, then switch the primary | Teams with strong observability | Complexity and write handling |
| Tenant by tenant | Move groups of customers, starting with internal and friendly tenants | Multi-tenant apps with routing control | Requires tenant-aware routing and data separation |

For most single-database SaaS products, a **short write-freeze window with a rehearsed final sync** plus **weighted traffic shift for the stateless layer** gives the best balance of risk and effort. Measure the cross-network latency before committing to an interim state where the app and database sit on different platforms.

## 4.2 Cutover runbook outline

Write the real one as a numbered, timed script that anyone on the team can execute.

1. **T-7 days:** freeze unrelated risky changes, confirm the rehearsal timings, notify customers and integration owners
2. **T-1 day:** verify replication lag, backups, alarms, on-call coverage, and that rollback artifacts are ready
3. **T-0 start:** announce, enable maintenance mode if needed, stop writes at the source
4. **Final sync:** wait for lag to reach zero, run the agreed validation queries
5. **Switch:** promote the target database, point the application at it, shift traffic
6. **Verify:** smoke tests, dashboards, error rates, queue depth, sample of real customer flows
7. **Decide:** go to the next traffic step, hold, or roll back, using the table below
8. **After:** keep the source read-only, run reconciliation checks, publish a short status note

## 4.3 Rollback triggers

Agree the triggers **before** cutover and write them in the runbook, so nobody negotiates under pressure.

| Signal | Threshold example | Action |
|---|---|---|
| Error rate | Above baseline by 2x for 10 minutes | Hold and investigate; roll back traffic if unresolved in 20 minutes |
| Latency p95 | Above baseline by 50% for 15 minutes | Hold; roll back traffic if capacity fixes fail |
| Data integrity | Any validation mismatch on critical tables | Stop, roll back, investigate |
| Replication or sync | Lag growing after switch | Stop writes, assess |
| Integration failures | Partner calls failing due to IP or auth | Fix or roll back if no quick fix |
| Elapsed time | Window exceeds the agreed maximum | Roll back |

## 4.4 What rollback really means

- **Before the point of no return** (writes still only on the source): switch traffic back, no data loss.
- **After writes land on the new database:** a rollback needs reverse replication or a replay of the writes. If you cannot do that, say so in the plan and make the go decision stricter.
- Decide in advance **how long the source is kept and in which mode** (read-only, then archived), and who approves deleting it.

## 4.5 Communication

- Customers: what changes, when, expected impact, and who to contact
- Internal: a single channel with timestamped updates and a named incident commander
- Integrations: new IP addresses and any endpoint or certificate changes
