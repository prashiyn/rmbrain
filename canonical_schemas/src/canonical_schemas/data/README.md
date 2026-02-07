# Canonical Schemas – Seed Data

Seed data for testing when no user/actor service is available.

## `actors_seed.json`

JSON array of actors that conform to the canonical `Actor` schema (`canonical_schemas.Actor`).

- **Human Internal** (10): multiple RMs, relationship managers, and one each of investment_specialist, product_manager, portfolio_manager, risk_manager, compliance_officer, service_rm.
- **Human External** (5): two clients, two prospects, one external_advisor.
- **System** (1): one `system` actor.
- **Service** (1): one `cds_relationship` service actor.

Each object has: `actor_id`, `actor_role`, `actor_type`, and optional `display_name`.

## Loading in tests

```python
import json
from pathlib import Path
from canonical_schemas import Actor

# Option 1: load raw JSON and validate
from canonical_schemas.data import ACTORS_SEED_PATH
with ACTORS_SEED_PATH.open() as f:
    raw = json.load(f)
actors = [Actor.model_validate(item) for item in raw]

# Option 2: use the loader
from canonical_schemas.data import load_seed_actors, get_actor_by_id, get_actors_by_role

actors = load_seed_actors()
rm = get_actor_by_id("seed_rm_001")
all_clients = get_actors_by_role("client")
```

## Actor IDs (for reference)

| actor_id | actor_role | actor_type |
|----------|------------|------------|
| seed_rm_001, seed_rm_002 | rm | human_internal |
| seed_relationship_manager_001, 002 | relationship_manager | human_internal |
| seed_investment_specialist_001 | investment_specialist | human_internal |
| seed_product_manager_001 | product_manager | human_internal |
| seed_portfolio_manager_001 | portfolio_manager | human_internal |
| seed_risk_manager_001 | risk_manager | human_internal |
| seed_compliance_officer_001 | compliance_officer | human_internal |
| seed_service_rm_001 | service_rm | human_internal |
| seed_client_001, seed_client_002 | client | human_external |
| seed_prospect_001, seed_prospect_002 | prospect | human_external |
| seed_external_advisor_001 | external_advisor | human_external |
| seed_system_001 | system | system |
| seed_cds_relationship_001 | cds_relationship | service |
