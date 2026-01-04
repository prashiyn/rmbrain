# Database Migration Setup - Complete

## Summary

All services now have proper database migration infrastructure in place. This document summarizes what was implemented.

## ✅ Completed Tasks

### 1. Migration Files Created

All services now have `migrations/init.sql` files:

- ✅ **client_service** - `migrations/init.sql`
- ✅ **task_service** - `migrations/init.sql`
- ✅ **document_service** - `migrations/init.sql` (already existed, plus additional migrations)
- ✅ **interaction_service** - `migrations/init.sql`
- ✅ **product_service** - `migrations/init.sql`
- ✅ **relationship_service** - `migrations/init.sql`
- ✅ **riskprofile_service** - `migrations/init.sql`
- ✅ **cas_service** - `migrations/init.sql`
- ✅ **rmbrain-mainapp** - `migrations/init.sql`

### 2. Migration Runner Script

Created `scripts/run_alembic_migrations.sh` which:
- Runs Alembic migrations across all services
- Provides color-coded output for easy reading
- Handles errors gracefully
- Supports any Alembic command (upgrade, downgrade, current, etc.)

### 3. Database Access Configuration

All services are properly configured:
- ✅ All services have `DATABASE_URL` in root `dapr.yaml`
- ✅ All services have `database_url` in their `config.py` files with `Field(env="DATABASE_URL")`
- ✅ Connection strings use correct format (sync vs async)

### 4. Documentation

Updated `docs/DATABASE_SUMMARY.md` with:
- Comprehensive migration guide
- Service-specific migration details
- Best practices
- Troubleshooting guide
- Production considerations

## Migration Structure

Each service follows this structure:

```
<service>/
  migrations/
    init.sql              # Initial schema (required)
    <migration_name>.sql  # Additional migrations (optional)
```

## Usage

### Quick Start

1. **Create databases:**
   ```bash
   ./scripts/setup_databases.sh
   ```

2. **Run Alembic migrations for all services:**
   ```bash
   ./scripts/run_alembic_migrations.sh upgrade head
   ```

3. **Run individual service migration:**
   ```bash
   cd <service>
   uv run alembic upgrade head
   ```

## Service Migration Details

### Client Service (`cds_client`)
- **Tables**: `clients`, `client_links`, `processed_events`
- **Alembic Config**: `client_service/alembic.ini`
- **Models**: `cds_client/models.py`

### Task Service (`cds_task`)
- **Tables**: `tasks`, `processed_events`
- **Alembic Config**: `task_service/alembic.ini`
- **Models**: `cds_task/models.py`

### Document Service (`cds_document`)
- **Tables**: `documents`, `processed_events`
- **Alembic Config**: `document_service/alembic.ini`
- **Models**: `cds_document/models.py`

### Interaction Service (`interaction_db`)
- **Tables**: `interactions`, `processed_events`
- **Alembic Config**: `interaction_service/alembic.ini`
- **Models**: `cds_interaction/models/`

### Product Service (`cds_product`)
- **Tables**: `products`, `processed_events`
- **Alembic Config**: `product_service/alembic.ini`
- **Models**: `app/repository/product_repo.py`

### Relationship Service (`relationship_db`)
- **Tables**: `relationships`, `processed_events`
- **Alembic Config**: `relationship_service/alembic.ini`
- **Models**: `cds_relationship/db/models.py`

### Risk Profile Service (`riskprofile_db`)
- **Tables**: `risk_profiles`, `suitability_assessments`, `processed_events`
- **Alembic Config**: `riskprofile_service/alembic.ini`
- **Models**: `app/repository/models.py`

### CAS Audit Service (`cas_audit`)
- **Tables**: `audit_events`
- **Alembic Config**: `cas_service/alembic.ini`
- **Models**: `cas_audit/models.py`

### RMBrain Main App (`rmbrain_mainapp`)
- **Tables**: `plugins`, `tenant_plugins`, `plugin_event_registry`, `event_mappings`
- **Alembic Config**: `rmbrain-mainapp/alembic.ini`
- **Models**: `app/models.py`

## Next Steps

1. **Test migrations** on a development environment
2. **Verify database schemas** match SQLAlchemy models
3. **Create additional migrations** as needed for schema changes
4. **Document any custom migrations** in service README files

## Verification Checklist

- [x] Alembic added to all service dependencies
- [x] Alembic configuration files created for all services
- [x] Helper scripts created (`run_alembic_migrations.sh`, `create_alembic_configs.py`)
- [x] All services have `DATABASE_URL` in root `dapr.yaml`
- [x] All services have `database_url` in `config.py` with env variable support
- [x] Documentation updated
- [x] Pre-Alembic files removed (run_migrations.sh, init_db.py, db/migrations.py)
- [x] SQL migration files kept for reference (can be archived later)

## Notes

- All services use Alembic for migrations
- Alembic automatically handles idempotency
- Migrations use PostgreSQL-specific features (JSONB, TIMESTAMPTZ, ARRAY)
- The `processed_events` table follows a canonical structure across all CDS services
- SQL migration files in `migrations/` directories are kept for reference but are no longer used
