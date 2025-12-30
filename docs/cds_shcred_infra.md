Making CDS Event Schemas Shared Infrastructure
The Correct, Scalable Pattern
1. First Principles (Lock These In)

Event schemas in RM Brain are:

Canonical contracts
Cross-service
Cross-plugin
Cross-agent
Versioned
Audit-relevant
Therefore:

They must live outside individual CDS service codebases.
CDS services implement them — they must not own them.


3. The Correct Solution: Canonical Event Schema Registry

Event schemas are promoted to first-class shared infrastructure, just like:

OpenAPI specs
Policy rules
Prompt registries

4. Final Architecture (Authoritative)
```text
rmbrain/
├── canonical/
│   ├── events/
│   │   ├── interaction/
│   │   │   ├── interaction.created.v1.json
│   │   │   ├── interaction.persisted.v1.json
│   │   └── task/
│   │       ├── task.created.v1.json
│   │       └── task.updated.v1.json
│   ├── entities/
│   │   ├── interaction.v1.json
│   │   ├── task.v1.json
│   └── semantics/
│       ├── interaction.v1.semantic.yaml
│       └── task.v1.semantic.yaml
```

5. Ownership Model (Clear & Clean)

| Artifact             | Owner              |
| -------------------- | ------------------ |
| Event schemas        | Canonical Registry |
| Entity schemas       | Canonical Registry |
| Semantic constraints | Canonical Registry |
| Validation logic     | Canonical SDK      |
| Runtime enforcement  | Event Engine       |
| Persistence          | CDS services       |


6. How CDS Services Use These Schemas
At Build Time

Import schemas from canonical registry
Generate validators
Generate OpenAPI if needed

At Runtime

Validate inbound events
Validate outbound events

📌 No local schema definitions allowed

7. How Main App Uses These Schemas

The Main App needs them for:

Event validation
Agent proposal validation
Workflow guardrails
Plugin event enforcement

So the Main App (rmbrain-mainapp):

Loads schemas from the same canonical registry
Uses the same Canonical Schema SDK
Never redefines them

8. Distribution Strategy (Best Practice)
Option A — Monorepo (Recommended for You)

Since you’re already running a monorepo-style architecture:
```
rm-brain/
├── canonical-registry/
├── cds-task/
├── cds-interaction/
├── main-app/
```
Canonical registry is a top-level module

All services depend on it
CI enforces compatibility

✅ Simple
✅ Fast
✅ No runtime dependency

9. Versioning Strategy (Critical)
Rules (Non-Negotiable)

Schemas are append-only

Breaking changes require new version

Old versions remain valid

Event name includes version

Example:
```text
interaction.created.v1
interaction.created.v2
```
10. CI/CD Guardrails (Highly Recommended)

Add CI checks:

CDS service cannot define event schema
Main app cannot define event schema
Plugins cannot define canonical event schema
Schema changes require approval
This prevents silent drift.

11. Cursor Instructions (Authoritative)

Event schemas are shared canonical infrastructure.

RULES:
- Event schemas must live in a shared canonical registry
- CDS services must consume schemas, not define them
- Main App must load schemas from the canonical registry
- No service or plugin may redefine canonical event schemas

VERSIONING:
- Event names include version
- Schemas are append-only
- Breaking changes require new versions

DO NOT:
- Duplicate schemas across services
- Fetch schemas at runtime from services
- Allow local schema divergence
