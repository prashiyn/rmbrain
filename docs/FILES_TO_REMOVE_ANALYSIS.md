# Files to Remove Analysis - Pre-Alembic Database Files

## Analysis Summary

After migrating to Alembic, several files from the pre-Alembic setup are now redundant and can be safely removed.

## Files to Remove

### 1. SQL Migration Scripts

**`scripts/run_migrations.sh`**
- **Status**: ✅ Safe to remove
- **Reason**: Replaced by `scripts/run_alembic_migrations.sh`
- **Function**: Ran SQL migrations from `migrations/*.sql` files
- **Replacement**: Use `./scripts/run_alembic_migrations.sh upgrade head`

### 2. Python Init Scripts

**`cas_service/scripts/init_db.py`**
- **Status**: ✅ Safe to remove
- **Reason**: Replaced by Alembic migrations
- **Function**: Used `Base.metadata.create_all()` to create tables
- **Replacement**: Use `uv run alembic upgrade head`

**`relationship_service/cds_relationship/db/migrations.py`**
- **Status**: ✅ Safe to remove
- **Reason**: Replaced by Alembic migrations
- **Function**: Custom migration module with `create_tables()` and `create_indexes()`
- **Replacement**: Use Alembic migrations

### 3. SQL Migration Files

**All `migrations/*.sql` files in service directories:**
- **Status**: ⚠️ **Keep for reference initially, then archive**
- **Reason**: These were the initial schema definitions
- **Recommendation**: 
  - Keep until initial Alembic migrations are generated and verified
  - Then move to `migrations/archive/` or remove
  - Files:
    - `client_service/migrations/init.sql`
    - `task_service/migrations/init.sql`
    - `task_service/migrations/migrate_processed_events.sql`
    - `document_service/migrations/init.sql`
    - `document_service/migrations/add_category_column.sql`
    - `document_service/migrations/update_processed_events_canonical.sql`
    - `interaction_service/migrations/init.sql`
    - `product_service/migrations/init.sql`
    - `relationship_service/migrations/init.sql`
    - `riskprofile_service/migrations/init.sql`
    - `cas_service/migrations/init.sql`
    - `rmbrain-mainapp/migrations/init.sql`

## Files to Update (Not Remove)

### 1. Database Setup Script

**`scripts/setup_databases.sh`**
- **Status**: ⚠️ **Update, don't remove**
- **Reason**: Still useful for creating databases
- **Action**: Remove SQL migration references, keep database creation
- **Update**: Change to use Alembic or just create databases

### 2. init_db() Functions in Code

**Status**: ⚠️ **Keep for now, but mark as deprecated**
- **Reason**: Some services call `init_db()` on startup
- **Files**:
  - `client_service/cds_client/main.py` - `init_db()` function
  - `cas_service/cas_audit/main.py` - calls `init_db()`
  - `task_service/cds_task/main.py` - calls `init_db()`
  - `interaction_service/cds_interaction/app/main.py` - calls `init_db()`
  - `product_service/app/main.py` - calls `init_db()`
  - `riskprofile_service/app/main.py` - calls `init_db()`
  - `rmbrain-mainapp/app/main.py` - calls `init_db()`

- **Recommendation**: 
  - These should be replaced with Alembic migrations
  - For now, keep them but add deprecation warnings
  - Update services to run Alembic migrations on startup or remove these calls

## Files to Keep

### Test Files
- All `tests/conftest.py` files that use `create_all()` - These are fine for test setup
- Test-specific database initialization is acceptable

### Documentation
- Keep documentation files but update references to mention Alembic
- Archive old SQL migration documentation

## Removal Plan

### Phase 1: Remove Scripts (Safe)
1. Remove `scripts/run_migrations.sh`
2. Remove `cas_service/scripts/init_db.py`
3. Remove `relationship_service/cds_relationship/db/migrations.py`

### Phase 2: Archive SQL Migrations (After Verification)
1. After initial Alembic migrations are generated and verified
2. Move SQL files to `migrations/archive/` or remove
3. Update documentation

### Phase 3: Update Code (Future)
1. Remove or deprecate `init_db()` calls in main.py files
2. Update services to use Alembic migrations
3. Update `scripts/setup_databases.sh` to remove SQL migration references
