# ADR 0002: Migrate the primary database with continuous replication and a short write freeze

> Worked example for the fictional "Acme SaaS". Replace the facts with your own, and verify what your current provider allows before choosing an option.

- **Status:** Accepted
- **Date:** 2026-02-02
- **Deciders:** Head of Engineering, Data lead
- **Consulted:** Application leads, Customer success

## Context

The primary PostgreSQL database is 400 GB and grows by about 2% per month. Customers are in several time zones, and the contract allows a maintenance window of up to 30 minutes with notice. The current provider limits access to replication features, so the options available to us depend on what it exposes.

## Options considered

### Option A: Dump and restore in a maintenance window
- Pros: simplest, uses standard tools, easy to rehearse
- Cons: at this size, the window is far longer than 30 minutes, so it does not fit the contract

### Option B: Logical replication from source to target
- Pros: near-zero downtime, native to PostgreSQL, supports an initial copy followed by streaming changes
- Cons: depends on the source allowing the required access; sequences, schema changes and large objects need handling; needs monitoring for lag and for tables without primary keys

### Option C: A managed change-data-capture service (such as AWS DMS)
- Pros: built for this, works with limited source access, includes validation features
- Cons: data type and constraint edge cases, extra moving parts, needs careful testing and tuning

### Option D: Application-level dual writes
- Pros: full control
- Cons: highest engineering effort and the highest risk of divergence

## Decision

We will use continuous replication into the target database (Option B if the source allows it, otherwise Option C), followed by a final write freeze, a lag-to-zero check, validation queries, and a switch. We will rehearse the full sequence at least three times with production-sized data and record the timings.

## Consequences

- Easier: the production window shrinks to the freeze, final sync and switch, which fits the 30-minute allowance
- Harder: we must monitor replication health for weeks, and freeze schema changes during the sync period
- Risks: silent divergence (mitigated by checksums on critical tables and row counts), lag spikes under load (mitigated by sizing the target and alerting on lag), sequence drift (mitigated by a scripted sequence reset in the runbook)
- Rollback: before writes land on the target, point traffic back to the source. After that point, rollback needs reverse replication, which we will test in a rehearsal before cutover

## Validation

The third rehearsal completes inside the agreed window with zero validation mismatches, and a restore of the target from backup into a clean environment succeeds.
