# Canonical Package Update - Quick Reference

## When You Make Changes to Canonical Package

After adding new events, updating schemas, or making any changes to the `canonical` package, follow these steps:

## Quick Steps

### 1. Run Update Script (Easiest)

```bash
cd /media/prashanth/extmnt1/rmbrain
./scripts/update_canonical_in_all_services.sh
```

This will run `uv sync` in all 11 services to refresh the canonical package.

### 2. Manual Update (If Script Doesn't Work)

For each service, run:

```bash
cd /media/prashanth/extmnt1/rmbrain/<service_name>
uv sync
```

### 3. Verify Changes

Test that new events are accessible:

```bash
cd /media/prashanth/extmnt1/rmbrain/task_service
python -c "from canonical import list_events; events = list_events(); print(f'Total events: {len(events)}')"
```

## Why This Is Needed

- The `canonical` package uses `file://` dependencies
- Python may cache imported modules
- `uv sync` refreshes the package link and clears caches
- Ensures all services see the latest changes

## Services Updated

The script updates all 11 services:
- task_service, bff_service, policy_service, relationship_service
- interaction_service, client_service, document_service
- product_service, riskprofile_service, cas_service
- rmbrain-mainapp

## Troubleshooting

**If changes still don't appear:**

1. Clear Python cache:
   ```bash
   find . -type d -name __pycache__ -exec rm -r {} + 2>/dev/null
   ```

2. Restart running services

3. Verify package structure:
   ```bash
   ls -la /media/prashanth/extmnt1/rmbrain/canonical/src/canonical/events/
   ```

## Full Documentation

See `docs/CANONICAL_PACKAGE_UPDATE_GUIDE.md` for detailed information.
