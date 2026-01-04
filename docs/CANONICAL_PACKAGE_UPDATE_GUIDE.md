# Canonical Package Update Guide

## Overview

When changes are made to the `canonical` package (e.g., adding new events, updating schemas), you need to ensure all services pick up these changes. This guide outlines the steps to refresh the package in all services.

## Current Setup

The `canonical` package is:
- Located at: `/media/prashanth/extmnt1/rmbrain/canonical/`
- Structured as a Python package with `src/canonical/` layout
- Installed in all services via `file://` dependency in `pyproject.toml`
- Already configured in all 11 services

## Steps to Reflect Changes

### Step 1: Verify Canonical Package Structure

Ensure the changes are in the correct location:

```bash
# Check canonical package structure
ls -la /media/prashanth/extmnt1/rmbrain/canonical/src/canonical/events/
```

The package structure should be:
```
canonical/
├── pyproject.toml
└── src/
    └── canonical/
        ├── __init__.py
        ├── registry.py
        ├── entities/        # Entity schemas
        ├── events/          # Event schemas (your new changes)
        └── semantics/       # Semantic constraints
```

### Step 2: Update All Services

Since all services use `file://` dependencies, you need to refresh the package installation in each service. There are two approaches:

#### Option A: Update All Services at Once (Recommended)

Create a script to update all services:

```bash
#!/bin/bash
# update_canonical_in_all_services.sh

REPO_ROOT="/media/prashanth/extmnt1/rmbrain"
SERVICES=(
    "task_service"
    "bff_service"
    "policy_service"
    "relationship_service"
    "interaction_service"
    "client_service"
    "document_service"
    "product_service"
    "riskprofile_service"
    "cas_service"
    "rmbrain-mainapp"
)

echo "Updating canonical package in all services..."

for service in "${SERVICES[@]}"; do
    echo "Updating $service..."
    cd "$REPO_ROOT/$service"
    
    # Sync dependencies (this will refresh the canonical package)
    uv sync
    
    echo "✓ $service updated"
done

echo "All services updated!"
```

#### Option B: Update Services Individually

For each service, run:

```bash
cd /media/prashanth/extmnt1/rmbrain/<service_name>
uv sync
```

This will:
- Re-read the `pyproject.toml`
- Reinstall/refresh the `canonical` package from the file:// path
- Update the package cache

### Step 3: Verify Changes Are Accessible

Test that the new events are accessible from a service:

```python
# In any service, test loading a new event
from canonical import load_event_schema, list_events

# List all events (should include new ones)
all_events = list_events()
print(f"Total events: {len(all_events)}")

# Try loading a new event
try:
    new_event_schema = load_event_schema("your.new.event", "v1")
    print("✓ New event schema loaded successfully")
except Exception as e:
    print(f"✗ Error loading new event: {e}")
```

### Step 4: Clear Python Cache (If Needed)

If changes still don't appear, clear Python cache:

```bash
# In each service directory
find . -type d -name __pycache__ -exec rm -r {} + 2>/dev/null
find . -type f -name "*.pyc" -delete
```

## Services That Need Updates

All 11 services have the `canonical` dependency:

1. ✅ `task_service`
2. ✅ `bff_service`
3. ✅ `policy_service`
4. ✅ `relationship_service`
5. ✅ `interaction_service`
6. ✅ `client_service`
7. ✅ `document_service`
8. ✅ `product_service`
9. ✅ `riskprofile_service`
10. ✅ `cas_service`
11. ✅ `rmbrain-mainapp`

## Quick Update Script

Here's a ready-to-use script:

```bash
#!/bin/bash
# update_all_services.sh

REPO_ROOT="/media/prashanth/extmnt1/rmbrain"
SERVICES=(
    "task_service"
    "bff_service"
    "policy_service"
    "relationship_service"
    "interaction_service"
    "client_service"
    "document_service"
    "product_service"
    "riskprofile_service"
    "cas_service"
    "rmbrain-mainapp"
)

echo "🔄 Updating canonical package in all services..."
echo ""

for service in "${SERVICES[@]}"; do
    SERVICE_PATH="$REPO_ROOT/$service"
    
    if [ ! -d "$SERVICE_PATH" ]; then
        echo "⚠️  Skipping $service (directory not found)"
        continue
    fi
    
    echo "📦 Updating $service..."
    cd "$SERVICE_PATH"
    
    # Run uv sync to refresh dependencies
    if uv sync > /dev/null 2>&1; then
        echo "   ✓ $service updated successfully"
    else
        echo "   ✗ Failed to update $service"
    fi
done

echo ""
echo "✅ Update complete!"
echo ""
echo "To verify, test loading a new event from any service:"
echo "  python -c \"from canonical import list_events; print(list_events())\""
```

## How File:// Dependencies Work

When using `file://` dependencies in `pyproject.toml`:

```toml
"canonical @ file:///media/prashanth/extmnt1/rmbrain/canonical"
```

- The package is installed in editable mode (if using `-e`) or as a link
- Changes to the source are **usually** immediately available
- However, Python's import cache may need to be cleared
- Running `uv sync` ensures the package is properly linked/installed

## Troubleshooting

### Changes Not Appearing?

1. **Check package structure**: Ensure files are in `src/canonical/events/`
2. **Run uv sync**: Refresh the package installation
3. **Clear cache**: Remove `__pycache__` directories
4. **Restart services**: If services are running, restart them
5. **Check imports**: Verify you're importing from `canonical`, not a cached version

### Verify Package Installation

```bash
# In any service directory
cd /media/prashanth/extmnt1/rmbrain/task_service
uv pip list | grep canonical
```

Should show:
```
canonical           1.0.0    (file:///media/prashanth/extmnt1/rmbrain/canonical)
```

### Test Loading New Events

```python
# test_canonical_update.py
from canonical import load_event_schema, list_events

# List all events
events = list_events()
print(f"Available events: {len(events)}")

# Try loading a specific new event
try:
    schema = load_event_schema("client_link.created", "v1")
    print("✓ New event schema loaded successfully")
    print(f"  Event ID: {schema.get('$id', 'N/A')}")
except Exception as e:
    print(f"✗ Error: {e}")
```

## Best Practices

1. **After making changes to canonical**:
   - Run `uv sync` in all services (or use the script above)
   - Test loading new schemas from at least one service
   - Clear Python cache if needed

2. **Version Management**:
   - Consider bumping version in `canonical/pyproject.toml` when making significant changes
   - Document changes in `canonical/README.md` or CHANGELOG

3. **Automation**:
   - Consider adding a pre-commit hook or CI step to verify canonical package updates
   - Use the update script in your development workflow

## Related Documentation

- `canonical/README.md` - Canonical package documentation
- `docs/CANONICAL_LIBRARY_MIGRATION_COMPLETE.md` - Package migration details
- `canonical/src/canonical/registry.py` - Schema loading functions

---

**Note**: Since you're using `file://` dependencies, changes are usually immediately available. However, running `uv sync` ensures proper package linking and clears any caching issues.
