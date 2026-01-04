# Database Configuration and Migration Guide

## Overview

This document provides comprehensive information about database setup, migrations, and management for all services in the RM Brain monorepo.

## Database Summary

### Services with Databases

| Service | Database Name | Type | Connection String | Migration Method |
|---------|--------------|------|-------------------|------------------|
| cas-audit | `cas_audit` | PostgreSQL | `postgresql://postgres:postgres@localhost:5432/cas_audit` | Alembic |
| cds-client | `cds_client` | PostgreSQL | `postgresql://postgres:postgres@localhost:5432/cds_client` | Alembic |
| cds-document | `cds_document` | PostgreSQL | `postgresql://postgres:postgres@localhost:5432/cds_document` | Alembic |
| cds-interaction | `interaction_db` | PostgreSQL (async) | `postgresql+asyncpg://postgres:postgres@localhost:5432/interaction_db` | Alembic |
| cds-product | `cds_product` | PostgreSQL | `postgresql://postgres:postgres@localhost:5432/cds_product` | Alembic |
| cds-relationship | `relationship_db` | PostgreSQL | `postgresql://postgres:postgres@localhost:5432/relationship_db` | Alembic |
| cds-riskprofile | `riskprofile_db` | PostgreSQL | `postgresql://postgres:postgres@localhost:5432/riskprofile_db` | Alembic |
| rmbrain-mainapp | `rmbrain_mainapp` | PostgreSQL (async) | `postgresql+asyncpg://postgres:postgres@localhost:5432/rmbrain_mainapp` | Alembic |
| cds-task | `cds_task` | PostgreSQL (async) | `postgresql+asyncpg://postgres:postgres@localhost:5432/cds_task` | Alembic |

**Total Databases**: 9 PostgreSQL databases  
**Services without databases**: 2 (bff-service, cps-policy)

## Initial Database Setup

### Quick Start

1. **Create all databases** using the setup script:
   ```bash
   ./scripts/setup_databases.sh
   ```

2. **Run all Alembic migrations** using the migration runner:
   ```bash
   ./scripts/run_alembic_migrations.sh upgrade head
   ```

### Manual Setup

#### 1. Create Databases

```bash
# Set PostgreSQL connection details (if different from defaults)
export POSTGRES_USER=postgres
export POSTGRES_PASSWORD=postgres
export POSTGRES_HOST=localhost
export POSTGRES_PORT=5432
export PGPASSWORD=postgres

# Create all databases
createdb -h localhost -U postgres cas_audit
createdb -h localhost -U postgres cds_client
createdb -h localhost -U postgres cds_document
createdb -h localhost -U postgres interaction_db
createdb -h localhost -U postgres cds_product
createdb -h localhost -U postgres relationship_db
createdb -h localhost -U postgres riskprofile_db
createdb -h localhost -U postgres rmbrain_mainapp
createdb -h localhost -U postgres cds_task
```

#### 2. Run Migrations

Use the migration runner script (recommended):
```bash
./scripts/run_alembic_migrations.sh upgrade head
```

Or run migrations individually:
```bash
# Client Service
psql -h localhost -U postgres -d cds_client -f client_service/migrations/init.sql

# Task Service
psql -h localhost -U postgres -d cds_task -f task_service/migrations/init.sql

# Document Service
psql -h localhost -U postgres -d cds_document -f document_service/migrations/init.sql

# Interaction Service
psql -h localhost -U postgres -d interaction_db -f interaction_service/migrations/init.sql

# Product Service
psql -h localhost -U postgres -d cds_product -f product_service/migrations/init.sql

# Relationship Service
psql -h localhost -U postgres -d relationship_db -f relationship_service/migrations/init.sql

# Risk Profile Service
psql -h localhost -U postgres -d riskprofile_db -f riskprofile_service/migrations/init.sql

# CAS Audit Service
psql -h localhost -U postgres -d cas_audit -f cas_service/migrations/init.sql

# RMBrain Main App
psql -h localhost -U postgres -d rmbrain_mainapp -f rmbrain-mainapp/migrations/init.sql
```

## Database Migrations

### Migration System: Alembic

All services now use **Alembic** for database migrations instead of manual SQL files. Alembic provides:
- **Auto-generation** of migrations from SQLAlchemy model changes
- **Version control** and rollback capabilities
- **Industry standard** tooling for SQLAlchemy projects
- **Better maintainability** as services grow

> **Note**: Legacy SQL migration files in `migrations/` directories are kept for reference but are no longer used. All new migrations should use Alembic.

### Quick Start

```bash
# Generate initial migration from models
cd <service>
uv run alembic revision --autogenerate -m "Initial migration"

# Apply migrations
uv run alembic upgrade head

# Run migrations for all services
./scripts/run_alembic_migrations.sh upgrade head
```

### Migration Structure

Each service has an `alembic/` directory containing:
- `alembic.ini` - Alembic configuration file
- `alembic/env.py` - Migration environment setup (sync or async)
- `alembic/script.py.mako` - Migration template
- `alembic/versions/` - Generated migration files

### Running Migrations

#### Using the Alembic Runner (Recommended)

The Alembic runner script (`scripts/run_alembic_migrations.sh`) provides:
- Runs Alembic commands across all services
- Sequential migration execution
- Error handling and reporting
- Color-coded output for easy reading

```bash
# Apply all migrations
./scripts/run_alembic_migrations.sh upgrade head

# Check migration status
./scripts/run_alembic_migrations.sh current

# Rollback one migration
./scripts/run_alembic_migrations.sh downgrade -1
```

#### Running Individual Service Migrations

```bash
# Navigate to service directory
cd <service>

# Apply all pending migrations
uv run alembic upgrade head

# Generate new migration from model changes
uv run alembic revision --autogenerate -m "Description of changes"

# Check current migration version
uv run alembic current

# Rollback one migration
uv run alembic downgrade -1
```

### Creating New Migrations

1. **Make changes to SQLAlchemy models** in the service's models file

2. **Generate migration automatically**:
   ```bash
   cd <service>
   uv run alembic revision --autogenerate -m "Add new_field to clients table"
   ```

3. **Review the generated migration** in `alembic/versions/`:
   ```python
   def upgrade() -> None:
       op.add_column('clients', sa.Column('new_field', sa.String(), nullable=True))

   def downgrade() -> None:
       op.drop_column('clients', 'new_field')
   ```

4. **Apply the migration**:
   ```bash
   uv run alembic upgrade head
   ```

5. **Test the migration** - Verify both upgrade and downgrade paths

### Migration Best Practices

1. **Always review auto-generated migrations** - Alembic is smart but not perfect
2. **Use descriptive migration messages** - Clear descriptions help with debugging
3. **Test migrations on development first** - Never apply untested migrations to production
4. **Never modify existing migrations** - Create new migrations to fix issues
5. **Use transactions** - Alembic automatically wraps migrations in transactions
6. **Handle data migrations separately** - Use `op.execute()` for custom SQL
7. **Version control all migrations** - Commit migration files to git

For detailed Alembic usage, see [ALEMBIC_MIGRATION_GUIDE.md](./ALEMBIC_MIGRATION_GUIDE.md).

## Service-Specific Migration Details

### Client Service (`cds_client`)

**Tables:**
- `clients` - Client entity data
- `client_links` - Relationships between clients
- `processed_events` - Event idempotency tracking

**Migration Location:** `client_service/migrations/init.sql`

### Task Service (`cds_task`)

**Tables:**
- `tasks` - Task entity data
- `processed_events` - Event idempotency tracking

**Migration Location:** `task_service/migrations/init.sql`

### Document Service (`cds_document`)

**Tables:**
- `documents` - Document entity data
- `processed_events` - Event idempotency tracking

**Migration Location:** `document_service/migrations/`
- `init.sql` - Initial schema
- `add_category_column.sql` - Example migration
- `update_processed_events_canonical.sql` - Canonical structure update

### Interaction Service (`interaction_db`)

**Tables:**
- `interactions` - Interaction entity data
- `processed_events` - Event idempotency tracking

**Migration Location:** `interaction_service/migrations/init.sql`

### Product Service (`cds_product`)

**Tables:**
- `products` - Product entity data
- `processed_events` - Event idempotency tracking

**Migration Location:** `product_service/migrations/init.sql`

### Relationship Service (`relationship_db`)

**Tables:**
- `relationships` - Relationship entity data
- `processed_events` - Event idempotency tracking

**Migration Location:** `relationship_service/migrations/init.sql`

### Risk Profile Service (`riskprofile_db`)

**Tables:**
- `risk_profiles` - Risk profile entity data
- `suitability_assessments` - Suitability assessment data
- `processed_events` - Event idempotency tracking

**Migration Location:** `riskprofile_service/migrations/init.sql`

### CAS Audit Service (`cas_audit`)

**Tables:**
- `audit_events` - Audit event data

**Migration Location:** `cas_service/migrations/init.sql`

### RMBrain Main App (`rmbrain_mainapp`)

**Tables:**
- `plugins` - Plugin registry
- `tenant_plugins` - Tenant plugin configuration
- `plugin_event_registry` - Plugin event registry
- `event_mappings` - Event mapping configuration

**Migration Location:** `rmbrain-mainapp/migrations/init.sql`

## Database Access Configuration

### Environment Variables

Database connections are configured via `DATABASE_URL` environment variables in `dapr.yaml`:

```yaml
env:
  DATABASE_URL: "postgresql://postgres:postgres@localhost:5432/<database_name>"
```

### Connection String Format

- **Synchronous PostgreSQL**: `postgresql://user:password@host:port/database`
- **Asynchronous PostgreSQL**: `postgresql+asyncpg://user:password@host:port/database`

### Services Using Async Connections

- `cds-interaction` - Uses `postgresql+asyncpg://`
- `cds-task` - Uses `postgresql+asyncpg://`
- `rmbrain-mainapp` - Uses `postgresql+asyncpg://`

All other services use synchronous PostgreSQL connections.

## Verification

### Check Database Existence

```bash
psql -h localhost -U postgres -l | grep -E "(cas_audit|cds_|interaction|relationship|riskprofile|rmbrain)"
```

### Verify Tables

```bash
# Check tables in a specific database
psql -h localhost -U postgres -d cds_client -c "\dt"

# Check all tables across all databases
for db in cas_audit cds_client cds_document interaction_db cds_product relationship_db riskprofile_db rmbrain_mainapp cds_task; do
  echo "=== $db ==="
  psql -h localhost -U postgres -d "$db" -c "\dt" | head -20
done
```

### Verify Migration Status

```bash
# Check if processed_events table exists (should be in all CDS services)
psql -h localhost -U postgres -d cds_client -c "SELECT COUNT(*) FROM information_schema.tables WHERE table_name = 'processed_events';"
```

## Troubleshooting

### Database Already Exists

If a database already exists, the setup script will skip it. This is safe.

### Migration Errors

Common issues and solutions:

1. **Tables already exist**: 
   - Migrations use `IF NOT EXISTS`, so this is safe to ignore
   - If you need to recreate, drop tables first: `DROP TABLE IF EXISTS <table_name> CASCADE;`

2. **Permission errors**:
   ```sql
   -- As postgres superuser
   ALTER USER postgres CREATEDB;
   GRANT ALL PRIVILEGES ON DATABASE <database_name> TO <user>;
   ```

3. **Connection errors**:
   ```bash
   # Check if PostgreSQL is running
   pg_isready -h localhost -p 5432
   
   # Check service status
   sudo systemctl status postgresql
   ```

4. **Syntax errors in migrations**:
   - Review the SQL file for syntax issues
   - Test the migration on a test database first
   - Ensure PostgreSQL version compatibility

### Rollback Migrations

PostgreSQL doesn't have built-in rollback for DDL statements. To rollback:

1. **Create a rollback migration**:
   ```sql
   -- rollback_add_column.sql
   ALTER TABLE documents DROP COLUMN IF EXISTS new_column;
   ```

2. **Or restore from backup**:
   ```bash
   pg_restore -h localhost -U postgres -d <database_name> <backup_file>
   ```

## Production Considerations

### Pre-Production Checklist

- [ ] All migrations tested on staging environment
- [ ] Database backups created
- [ ] Migration scripts reviewed and approved
- [ ] Rollback plan documented
- [ ] Database connection strings configured
- [ ] Connection pooling configured appropriately
- [ ] Indexes verified for performance
- [ ] Foreign key constraints verified

### Production Migration Process

1. **Backup databases**:
   ```bash
   pg_dump -h localhost -U postgres -d <database_name> > backup_<timestamp>.sql
   ```

2. **Run migrations during maintenance window**:
   ```bash
   ./scripts/run_alembic_migrations.sh upgrade head
   ```

3. **Verify migrations**:
   ```bash
   # Check table counts
   psql -h localhost -U postgres -d <database_name> -c "SELECT COUNT(*) FROM <table_name>;"
   ```

4. **Monitor application logs** for errors

5. **Rollback if necessary** (use backups or rollback migrations)

## Next Steps

After setting up databases and running migrations:

1. **Verify all databases exist** (see Verification section)
2. **Start services**: `dapr run -f dapr.yaml`
3. **Check service logs** to ensure schemas were created successfully
4. **Run service health checks** to verify database connectivity

## Additional Resources

- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)
- [Dapr Documentation](https://docs.dapr.io/)