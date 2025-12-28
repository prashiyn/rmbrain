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

### 2. Run SQL Migrations (where applicable)

#### Client Service
```bash
psql -h localhost -U postgres -d cds_client -f client_service/migrations/init.sql
```

#### Document Service
```bash
psql -h localhost -U postgres -d cds_document -f document_service/migrations/init.sql
```

#### Task Service
```bash
psql -h localhost -U postgres -d cds_task -f task_service/migrations/init.sql
```

### 3. Run Python Init Scripts (where applicable)

#### CAS Service
```bash
cd cas_service
uv run python scripts/init_db.py
cd ..
```

### 4. Services with Auto-Creation

The following services will automatically create their schemas on first startup using SQLAlchemy's `create_all()`:

- **CDS Interaction Service** - Creates tables on startup
- **CDS Product Service** - Creates tables on startup
- **CDS Relationship Service** - Creates tables on startup
- **CDS Risk Profile Service** - Creates tables on startup
- **RMBrain Main App** - Creates tables on startup

These services will initialize their schemas when you run `dapr run -f dapr.yaml`.

## Database Schema Summary

| Service | Database Name | Setup Method |
|---------|--------------|--------------|
| cas-audit | `cas_audit` | Python script (`scripts/init_db.py`) |
| cds-client | `cds_client` | SQL migration (`migrations/init.sql`) |
| cds-document | `cds_document` | SQL migration (`migrations/init.sql`) |
| cds-interaction | `interaction_db` | Auto-created on startup |
| cds-product | `cds_product` | Auto-created on startup |
| cds-relationship | `relationship_db` | Auto-created on startup |
| cds-riskprofile | `riskprofile_db` | Auto-created on startup |
| rmbrain-mainapp | `rmbrain_mainapp` | Auto-created on startup |
| cds-task | `cds_task` | SQL migration (`migrations/init.sql`) |

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

If SQL migrations fail, check the error message. Common issues:
- Tables already exist (safe to ignore)
- Syntax errors in migration files
- Missing dependencies

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

