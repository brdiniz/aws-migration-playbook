# ADR 0003: Separate AWS accounts for production and non-production

> Worked example for the fictional "Acme SaaS". Replace the facts with your own.

- **Status:** Accepted
- **Date:** 2026-01-20
- **Deciders:** Head of Engineering, Security lead

## Context

We are starting on AWS with a small platform team. Customers ask about environment isolation and access control in security questionnaires. We want strong isolation without the overhead of a large multi-account landing zone on day one.

## Options considered

### Option A: One account for everything
- Pros: simplest to set up
- Cons: weak isolation, noisy IAM, hard to apply different guardrails, a mistake in staging can touch production

### Option B: Separate production and non-production accounts under AWS Organizations
- Pros: clear blast-radius boundary, separate billing and budgets, different policies per environment, easy to explain to customers
- Cons: some cross-account setup (networking, container registry, pipelines)

### Option C: One account per environment and per workload, with a full landing zone
- Pros: strongest isolation and a scalable pattern
- Cons: more setup and ongoing governance than we need now

## Decision

We will use Option B with an organisation, a dedicated production account, a non-production account for development and staging, a small shared-services account for the pipeline and registry if needed, and centralised audit logging. Access is through SSO with role-based permission sets.

## Consequences

- Easier: production guardrails, cost visibility, customer security reviews
- Harder: cross-account pipelines and registry access need setup and testing
- Revisit if the number of workloads or regulatory scope grows enough that a fuller landing zone is justified

## Validation

An access review confirms no long-lived admin credentials exist, and an engineer can deploy to staging but cannot modify production without the production role.
