# 1. Assessment

The goal of the assessment is to answer three questions with evidence: **why** move, **what** is actually running, and **how ready** the organisation is. Do it in two to three weeks, not two to three months.

## 1.1 Why move (write it down)

Pick the real drivers and rank them. Typical ones for a PaaS exit:

- Cost at scale (PaaS dyno and add-on pricing versus reserved or committed AWS capacity)
- Missing capabilities (private networking, regional data residency, fine-grained scaling, custom instance types)
- Compliance and customer requirements (SSO, audit logging, data location)
- Reliability limits (noisy neighbours, limited failover control)
- Strategic fit (a parent company or key customers standardise on AWS)

If cost is the only driver, run the [cost model](06-cost-model.md) first. Many PaaS exits do not save money in year one once engineering time is counted.

## 1.2 Discovery checklist

Capture each item in a table with an owner. Unknowns are findings, not blanks.

**Application**
- [ ] Services and processes (web, workers, schedulers, one-off jobs) with language and framework versions
- [ ] Background job system, queues, cron and scheduled tasks
- [ ] Build process, buildpacks or Dockerfiles, and what the build depends on
- [ ] Environment variables and secrets (count, owners, rotation history)
- [ ] File storage and uploads (where they live today)
- [ ] Inbound and outbound integrations, with IP allowlisting in either direction

**Data**
- [ ] Databases, engine and version, size, growth rate, peak connections
- [ ] Extensions in use, custom functions, replication or follower setups
- [ ] Backup and restore process, and when it was last tested
- [ ] Caches and search indexes, and whether they can be rebuilt

**Traffic and operations**
- [ ] Request volume by hour and day, peak patterns, regional distribution
- [ ] Latency and error baselines (p50, p95, p99) for key endpoints
- [ ] DNS, TLS certificates, CDN and WAF setup
- [ ] Monitoring, logging, alerting and on-call process
- [ ] Deployment frequency and the release process

**Organisation**
- [ ] Who has AWS experience, who has operated Postgres or similar at this scale
- [ ] Contracts and commitments with the current provider and its end dates
- [ ] Compliance obligations and customer contract clauses about hosting

## 1.3 Choosing a strategy per component (the 6 Rs)

| Strategy | When it fits a PaaS exit | Example |
|---|---|---|
| Rehost | Fastest path, little change to the app | Containerise as is and run on a managed container service |
| Replatform | Swap a component for a managed AWS equivalent | Managed Postgres instead of a PaaS add-on |
| Refactor | Only where the move forces it | Replace a filesystem dependency with object storage |
| Repurchase | A SaaS tool replaces a self-run component | Hosted search or email delivery |
| Retire | Components nobody uses | Old add-ons, unused staging apps |
| Retain | Not worth moving yet | A small internal tool with no pressure |

Default to **rehost plus replatform the database**. Refactor only what blocks the move.

## 1.4 Readiness score

Score each dimension from 0 (not ready) to 3 (ready). Anything scoring 0 or 1 becomes a task in the foundations workstream.

| Dimension | 0 | 3 |
|---|---|---|
| Infrastructure as code | Console clicks only | All infrastructure in code with review |
| CI/CD | Manual deploys | Automated, tested, rollback in minutes |
| Observability | Logs only | Metrics, traces, alerts tied to SLOs |
| Security baseline | Shared admin credentials | SSO, least privilege, audit logging |
| Data restore | Never tested | Restore drill passed in the last quarter |
| Team skills | No AWS experience | Several engineers have run production on AWS |

A total under 9 out of 18 suggests starting with a smaller pilot service and investing in foundations before moving anything critical.

## 1.5 Output of the assessment

- A ranked list of drivers with target metrics
- An inventory of components with a strategy for each
- The readiness score and the gaps to close
- A first version of the [risk register](05-risk-register.md)
- A go or no-go recommendation with a rough range for cost and duration
