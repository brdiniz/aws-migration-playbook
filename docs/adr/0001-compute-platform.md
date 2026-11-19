# ADR 0001: Run application workloads on ECS with Fargate

> Worked example for the fictional "Acme SaaS". Replace the facts with your own.

- **Status:** Accepted
- **Date:** 2026-01-15
- **Deciders:** Head of Engineering, Platform lead
- **Consulted:** Application leads, Security

## Context

Acme SaaS runs a monolithic web application and background workers on a PaaS. The team has strong application skills and limited infrastructure operations experience. We need to move to AWS within six months without growing the platform team. Nobody on the team currently operates Kubernetes in production.

## Options considered

### Option A: ECS on Fargate
- Managed container scheduling with no servers to patch
- Pros: lowest operational load, simple mental model, good integration with load balancers, IAM and logging
- Cons: less portable than Kubernetes, a higher per-vCPU price than well-packed EC2, some limits on host-level tuning

### Option B: ECS on EC2
- Pros: cheaper at steady high utilisation, full control of instances
- Cons: you own patching, capacity and bin-packing

### Option C: EKS
- Pros: portable skills and tooling, a large ecosystem
- Cons: significant operational overhead and a steeper learning curve, which the team cannot absorb now

### Option D: Plain EC2 with configuration management
- Pros: familiar to many engineers
- Cons: most operational work, slow deployments, hardest to make elastic

## Decision

We will run web and worker services on ECS with Fargate, deployed from a CI/CD pipeline using immutable container images. We will revisit EC2 capacity providers for steady workloads once usage is stable.

## Consequences

- Easier: deployments, scaling and patching; the platform team stays small
- Harder: host-level debugging; some cost optimisation options need extra work later
- Risk: a Fargate cost premium. Mitigated by right-sizing tasks and reviewing Savings Plans after three months of stable usage
- Revisit when monthly compute spend is high and steady enough that EC2 capacity pays for the added operational work, or when the team gains Kubernetes experience for other reasons

## Validation

At 90 days after cutover: deployment frequency at or above baseline, no more than one platform-caused incident per month, and compute cost within the range set in the business case.
