# ADR-0001: Initial Repository Structure

Date: $(date +%Y-%m-%d)

## Status
Proposed

## Context
Need a single repo to showcase multiple domains with mixed languages.

## Decision
Use a monorepo with per-module tooling and path-filtered CI.

## Consequences
- Pros: Simpler navigation, shared docs, cohesive portfolio
- Cons: Mixed tooling requires per-folder isolation
