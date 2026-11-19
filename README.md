# aws-migration-playbook

A practical, opinionated playbook for moving a production SaaS platform from a PaaS (Heroku is the worked example) or a legacy hosting setup to AWS, without a big-bang cutover and without surprising the business.

It is written for engineering leaders and senior engineers who have to plan the move, justify it, and keep customers unaffected while it happens. Everything here is generic and uses a fictional company, "Acme SaaS", so you can copy it into your own planning documents.

## What is inside

| Part | What it gives you |
|---|---|
| [docs/01-assessment.md](docs/01-assessment.md) | Discovery checklist, the 6 Rs applied to a PaaS exit, and a readiness score |
| [docs/02-target-architecture.md](docs/02-target-architecture.md) | A target AWS architecture with the decisions that matter, plus a diagram |
| [docs/03-workstreams.md](docs/03-workstreams.md) | Three parallel workstreams, a phased timeline, entry and exit criteria |
| [docs/04-cutover-and-rollback.md](docs/04-cutover-and-rollback.md) | Cutover patterns, rollback triggers and a decision table |
| [docs/05-risk-register.md](docs/05-risk-register.md) | The risks that usually hurt, with mitigations and early warning signs |
| [docs/06-cost-model.md](docs/06-cost-model.md) | How to build an honest cost comparison, including costs people forget |
| [docs/adr/](docs/adr/) | An ADR template and three worked decision records |
| [checklists/](checklists/) | Pre-migration, cutover-day and 30/60/90-day post-migration checklists |
| [tools/cost_compare.py](tools/cost_compare.py) | A small calculator: monthly delta, break-even and a 3-year view |

## Principles the playbook is built on

1. **Migrate in slices, not in one night.** Move by service or tenant group, with the ability to send traffic back.
2. **Separate the data move from the application move.** Data is where outages and data loss happen, so it gets its own workstream and its own rollback plan.
3. **Build the foundations first.** Accounts, networking, identity, observability and CI/CD exist and are tested before any production workload moves.
4. **Run both sides in parallel until you trust the new one.** Decommission only after a defined stability window.
5. **Decide in writing.** Each significant choice is an ADR with the alternatives you rejected.
6. **Measure the migration like a product.** Define success metrics (availability, latency, cost, deploy frequency) before you start and compare after.

## Quick start

1. Read [docs/01-assessment.md](docs/01-assessment.md) and fill in the discovery checklist for your platform.
2. Copy [docs/adr/0000-template.md](docs/adr/0000-template.md) and record your first decisions.
3. Use the cost calculator to test whether the business case holds:

   ```bash
   python tools/cost_compare.py examples/acme-saas.json
   ```

4. Turn [docs/03-workstreams.md](docs/03-workstreams.md) into your own plan and risk register.

## Scope and caveats

- The playbook describes a pattern that has worked for multi-tenant web SaaS with a relational database, background workers and a few third-party integrations. Adjust it for regulated data (healthcare, payments) and for very large data volumes.
- Service names and features change. Verify details against current AWS documentation before you commit to them.
- It does not replace a Well-Architected Review or your security team's requirements.

## Contributing

Issues and pull requests are welcome, especially real-world lessons that generalise. Please keep examples free of employer or customer specifics.

## Need help with your migration?

If you want an experienced second pair of eyes on a migration plan, a cost case, or the cutover strategy, I do short advisory engagements for engineering leaders. Contact: brdiniz@icloud.com

## License

MIT. See [LICENSE](LICENSE).
