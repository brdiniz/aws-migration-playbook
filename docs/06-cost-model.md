# 6. Cost model

A migration business case fails when it compares a PaaS invoice to an incomplete AWS estimate. Build both sides honestly.

## 6.1 Current-state costs

Start from the last 6 to 12 months of invoices, not from the pricing page.

- Compute (dynos or equivalent), by process type
- Databases and replicas, including high-availability tiers
- Add-ons: cache, search, logging, monitoring, scheduler, email
- Bandwidth or overage charges
- Support plans
- Tools that exist only because of the platform

## 6.2 Target-state costs

| Category | What to include |
|---|---|
| Compute | Tasks or instances sized from real CPU and memory use, headroom for peaks, non-production environments |
| Database | Instance class, storage and IOPS, Multi-AZ, backups and retention, read replicas |
| Network | NAT gateways (hourly and per GB), load balancers, cross-AZ and internet egress, CDN |
| Storage | Object storage, snapshots, container registry |
| Observability | Logs ingestion and retention, metrics, traces, any vendor you keep |
| Security | Audit logging, threat detection, WAF, secrets, key management |
| Support | AWS support plan |
| Commitments | Savings Plans or reserved capacity, applied only after a few months of stable usage |

Use the AWS Pricing Calculator for the final numbers. Prices vary by region and change over time.

## 6.3 One-time and hidden costs

- Engineering time for the migration (loaded cost, not just salaries)
- Double-running both environments during the stability window
- Training and any external help
- Tooling for infrastructure as code, CI and observability
- Customer-facing costs: incident handling, credits, communications

## 6.4 Ongoing cost of ownership

A PaaS bundles operations work that you now own: patching, upgrades, capacity planning, on-call. Estimate the engineering time per month and price it. If you cannot, assume a meaningful fraction of at least one engineer.

## 6.5 Using the calculator

```bash
python tools/cost_compare.py examples/acme-saas.json
```

The input is a JSON file with current monthly costs, target monthly costs, one-time costs, and a horizon. The output shows the monthly delta, the break-even month, and a cumulative view over the horizon. Run it with a pessimistic and an optimistic case before you present the result.

## 6.6 Presenting the result

- Show a range, not one number
- Separate hard savings from avoided risk and from new capability
- State the assumptions on one page
- Re-check the model after the first full month of production usage and publish the actuals
