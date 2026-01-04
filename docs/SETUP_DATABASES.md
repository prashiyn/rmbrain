# Database Setup Guide

This guide explains how to set up all PostgreSQL databases and schemas before running the services.

## Quick Start

Run the setup script to create all databases:

```bash
./scripts/setup_databases.sh
```

Or manually:

```bash
# Set PostgreSQL connection details (if different from defaults)
export POSTGRES_USER=postgres
export POSTGRES_PASSWORD=postgres
export POSTGRES_HOST=localhost
export POSTGRES_PORT=5432

# Run setup
./scripts/setup_databases.sh
```

## Manual Setup

If you prefer to set up databases manually, follow these steps:

### 1. Create All Databases

```bash
# Set PostgreSQL password (if needed)
export PGPASSWORD=postgres

# Create databases
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

### 2. Run Alembic Migrations

All services now use Alembic for database migrations. Run migrations for all services:

```bash
./scripts/run_alembic_migrations.sh upgrade head
```

Or run migrations individually:

```bash
# Client Service
cd client_service && uv run alembic upgrade head && cd ..

# Task Service
cd task_service && uv run alembic upgrade head && cd ..

# Document Service
cd document_service && uv run alembic upgrade head && cd ..

# ... repeat for each service
```

For detailed Alembic usage, see [ALEMBIC_MIGRATION_GUIDE.md](./ALEMBIC_MIGRATION_GUIDE.md).

## Database Schema Summary

| Service | Database Name | Migration Method |
|---------|--------------|------------------|
| cas-audit | `cas_audit` | Alembic |
| cds-client | `cds_client` | Alembic |
| cds-document | `cds_document` | Alembic |
| cds-interaction | `interaction_db` | Alembic |
| cds-product | `cds_product` | Alembic |
| cds-relationship | `relationship_db` | Alembic |
| cds-riskprofile | `riskprofile_db` | Alembic |
| rmbrain-mainapp | `rmbrain_mainapp` | Alembic |
| cds-task | `cds_task` | Alembic |

## Verification

After setup, verify databases exist:

```bash
psql -h localhost -U postgres -l | grep -E "(cas_audit|cds_|interaction|relationship|riskprofile|rmbrain)"
```

You should see all 9 databases listed.

## Troubleshooting

### Database Already Exists

If a database already exists, the setup script will skip it. This is safe.

### Permission Errors

Ensure the PostgreSQL user has permission to create databases:

```sql
-- As postgres superuser
ALTER USER postgres CREATEDB;
```

### Connection Errors

Check PostgreSQL is running:

```bash
# Check if PostgreSQL is running
pg_isready -h localhost -p 5432

# Or check service status
sudo systemctl status postgresql
```

### Migration Errors

If Alembic migrations fail, check the error message. Common issues:
- Database connection errors (check `DATABASE_URL`)
- Model import errors (check `alembic/env.py` imports)
- Migration conflicts (use `alembic merge` to resolve)
- Missing dependencies (run `uv sync`)

For troubleshooting, see [ALEMBIC_MIGRATION_GUIDE.md](./ALEMBIC_MIGRATION_GUIDE.md).

## Next Steps

After setting up databases:

1. **Verify all databases exist** (see Verification above)
2. **Start services**: `dapr run -f dapr.yaml`
3. **Check service logs** to ensure schemas were created successfully

## Production Considerations

For production environments:

1. **Use migrations** instead of auto-creation
2. **Backup databases** before running migrations
3. **Test migrations** on a staging environment first
4. **Use connection pooling** and proper credentials
5. **Monitor database connections** and performance

