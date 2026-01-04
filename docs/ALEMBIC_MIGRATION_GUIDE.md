# Alembic Migration Guide

## Overview

All services now use **Alembic** for database migrations instead of manual SQL files. Alembic provides:
- **Auto-generation** of migrations from SQLAlchemy model changes
- **Version control** and rollback capabilities
- **Industry standard** tooling for SQLAlchemy projects
- **Better maintainability** as services grow

## Quick Start

### 1. Install Dependencies

```bash
# Install dependencies for a specific service
cd <service>
uv sync
```

### 2. Generate Initial Migration

```bash
# Generate initial migration from existing models
cd <service>
uv run alembic revision --autogenerate -m "Initial migration"
```

### 3. Apply Migrations

```bash
# Apply all pending migrations
cd <service>
uv run alembic upgrade head
```

### 4. Run Migrations for All Services

```bash
# From repository root
./scripts/run_alembic_migrations.sh upgrade head
```

## Service Configuration

### Sync Services (Standard SQLAlchemy)

- **client_service** - `cds_client`
- **document_service** - `cds_document`
- **product_service** - `cds_product`
- **relationship_service** - `cds_relationship`
- **riskprofile_service** - `cds_riskprofile`
- **cas_service** - `cas_audit`

### Async Services (Async SQLAlchemy)

- **task_service** - `cds_task`
- **interaction_service** - `cds_interaction`
- **rmbrain-mainapp** - `rmbrain_mainapp`

## Common Alembic Commands

### Generate New Migration

```bash
# Auto-generate migration from model changes
uv run alembic revision --autogenerate -m "Description of changes"

# Create empty migration (manual)
uv run alembic revision -m "Description of changes"
```

### Apply Migrations

```bash
# Apply all pending migrations
uv run alembic upgrade head

# Apply up to a specific revision
uv run alembic upgrade <revision>

# Apply next migration only
uv run alembic upgrade +1
```

### Rollback Migrations

```bash
# Rollback one migration
uv run alembic downgrade -1

# Rollback to a specific revision
uv run alembic downgrade <revision>

# Rollback all migrations
uv run alembic downgrade base
```

### Check Migration Status

```bash
# Show current migration status
uv run alembic current

# Show migration history
uv run alembic history

# Show pending migrations
uv run alembic heads
```

## Migration Workflow

### 1. Make Model Changes

Edit your SQLAlchemy models in the service's models file:

```python
# Example: Add a new column
class Client(Base):
    __tablename__ = "clients"
    
    client_id = Column(String, primary_key=True)
    # ... existing columns ...
    new_field = Column(String, nullable=True)  # New field
```

### 2. Generate Migration

```bash
cd <service>
uv run alembic revision --autogenerate -m "Add new_field to clients"
```

### 3. Review Generated Migration

Check the generated migration file in `alembic/versions/`:

```python
def upgrade() -> None:
    op.add_column('clients', sa.Column('new_field', sa.String(), nullable=True))

def downgrade() -> None:
    op.drop_column('clients', 'new_field')
```

### 4. Apply Migration

```bash
uv run alembic upgrade head
```

### 5. Test Migration

- Test the upgrade path
- Test the downgrade path (if needed)
- Verify data integrity

## Running Migrations for All Services

### Using the Helper Script

```bash
# Apply all migrations
./scripts/run_alembic_migrations.sh upgrade head

# Check status for all services
./scripts/run_alembic_migrations.sh current

# Rollback all services by one migration
./scripts/run_alembic_migrations.sh downgrade -1
```

### Manual Service-by-Service

```bash
# Client Service
cd client_service && uv run alembic upgrade head && cd ..

# Task Service
cd task_service && uv run alembic upgrade head && cd ..

# ... repeat for each service
```

## Migration Best Practices

### 1. Always Review Auto-Generated Migrations

Alembic's autogenerate is smart but not perfect:
- Review generated SQL before applying
- Check for data type changes
- Verify index creation/dropping
- Ensure foreign key constraints are correct

### 2. Use Descriptive Migration Messages

```bash
# Good
uv run alembic revision --autogenerate -m "Add email field to clients table"

# Bad
uv run alembic revision --autogenerate -m "update"
```

### 3. Test Migrations on Development First

- Always test migrations on a development database
- Test both upgrade and downgrade paths
- Verify data integrity after migration

### 4. Never Modify Existing Migrations

- Once a migration is applied to production, never modify it
- Create new migrations to fix issues
- Document any manual steps required

### 5. Use Transactions

Alembic automatically wraps migrations in transactions. For PostgreSQL:
- Each migration runs in a transaction
- If migration fails, it's automatically rolled back
- This ensures database consistency

### 6. Handle Data Migrations Separately

For data migrations (not just schema changes):
- Create separate migration files
- Use `op.execute()` for custom SQL
- Test with production-like data volumes

## Troubleshooting

### Migration Conflicts

If multiple developers create migrations simultaneously:

```bash
# Check for multiple heads
uv run alembic heads

# Merge branches if needed
uv run alembic merge -m "Merge branches" <rev1> <rev2>
```

### Migration Errors

If a migration fails:

1. **Check the error message** - Usually indicates the issue
2. **Rollback if needed**:
   ```bash
   uv run alembic downgrade -1
   ```
3. **Fix the migration file** and try again
4. **Or create a new migration** to fix the issue

### Database Connection Issues

Ensure `DATABASE_URL` is set correctly:

```bash
# Check environment variable
echo $DATABASE_URL

# Or set it explicitly
export DATABASE_URL="postgresql://postgres:postgres@localhost:5432/<database>"
uv run alembic upgrade head
```

### Model Import Errors

If Alembic can't import models:

1. Check `alembic/env.py` imports are correct
2. Ensure all models are imported in the models module
3. Verify the module path matches your service structure

## Migration from SQL Files

### Initial Setup

For services with existing SQL migrations:

1. **Generate initial Alembic migration**:
   ```bash
   cd <service>
   uv run alembic revision --autogenerate -m "Initial migration from SQL"
   ```

2. **Review the generated migration** - It should match your existing schema

3. **Apply the migration**:
   ```bash
   uv run alembic upgrade head
   ```

4. **Verify schema matches** - Compare with existing SQL files

5. **Archive old SQL files** - Keep them for reference but use Alembic going forward

## Service-Specific Notes

### Async Services

For async services (task, interaction, rmbrain-mainapp):
- Alembic handles async engines automatically
- Use the same commands as sync services
- The `env.py` file uses async engine configuration

### Services with Multiple Models

If a service has models in multiple files:
- Ensure all model files are imported in `alembic/env.py`
- Use `from module import *` to import all models
- Alembic will detect all models from `Base.metadata`

## Production Deployment

### Pre-Deployment Checklist

- [ ] All migrations tested on staging
- [ ] Migration rollback tested
- [ ] Database backup created
- [ ] Migration scripts reviewed
- [ ] Downtime window scheduled (if needed)

### Deployment Process

1. **Backup database**:
   ```bash
   pg_dump -h <host> -U <user> -d <database> > backup_$(date +%Y%m%d_%H%M%S).sql
   ```

2. **Run migrations**:
   ```bash
   cd <service>
   uv run alembic upgrade head
   ```

3. **Verify migration**:
   ```bash
   uv run alembic current
   ```

4. **Check application logs** for errors

5. **Rollback if necessary**:
   ```bash
   uv run alembic downgrade -1
   # Or restore from backup
   ```

## Additional Resources

- [Alembic Documentation](https://alembic.sqlalchemy.org/)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)

## Migration Scripts Location

All Alembic configurations are in:
- `alembic.ini` - Main configuration file
- `alembic/env.py` - Migration environment setup
- `alembic/script.py.mako` - Migration template
- `alembic/versions/` - Generated migration files
