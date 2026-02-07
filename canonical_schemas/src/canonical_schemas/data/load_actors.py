"""Load seed actors from JSON for testing.

Usage:
  With canonical_schemas installed:
    from canonical_schemas.data.load_actors import load_seed_actors, get_actor_by_id, get_actors_by_role

  Or load from a custom path:
    from pathlib import Path
    from canonical_schemas.data.load_actors import load_seed_actors_from_path
    actors = load_seed_actors_from_path(Path("/path/to/actors_seed.json"))
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import List

# Default path: same dir as this module (inside the package)
_DATA_DIR = Path(__file__).resolve().parent
ACTORS_SEED_PATH = _DATA_DIR / "actors_seed.json"


def load_seed_actors_from_path(path: Path | None = None) -> List["Actor"]:
    """Load and validate seed actors from a JSON file.

    Returns a list of Actor instances. Raises if the file is missing or invalid.
    """
    from canonical_schemas import Actor

    p = path or ACTORS_SEED_PATH
    with p.open(encoding="utf-8") as f:
        raw = json.load(f)
    if not isinstance(raw, list):
        raise ValueError(f"Expected JSON array, got {type(raw).__name__}")
    return [Actor.model_validate(item) for item in raw]


def load_seed_actors() -> List["Actor"]:
    """Load seed actors from the default actors_seed.json path."""
    return load_seed_actors_from_path(ACTORS_SEED_PATH)


def get_actor_by_id(actor_id: str, actors: List["Actor"] | None = None) -> "Actor | None":
    """Return the first actor with the given actor_id, or None."""
    from canonical_schemas import Actor

    if actors is None:
        actors = load_seed_actors()
    for a in actors:
        if a.actor_id == actor_id:
            return a
    return None


def get_actors_by_role(actor_role: str, actors: List["Actor"] | None = None) -> List["Actor"]:
    """Return all actors with the given actor_role."""
    from canonical_schemas import Actor

    if actors is None:
        actors = load_seed_actors()
    return [a for a in actors if a.actor_role == actor_role]
