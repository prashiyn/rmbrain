# Alembic Quick Reference

## Common Commands

### Generate Migrations

```bash
# Auto-generate from model changes
uv run alembic revision --autogenerate -m "Description"

# Create empty migration (manual)
uv run alembic revision -m "Description"
```

### Apply Migrations

```bash
# Apply all pending migrations
uv run alembic upgrade head

# Apply to specific revision
uv run alembic upgrade <revision>

# Apply next migration only
uv run alembic upgrade +1
```

### Rollback Migrations

```bash
# Rollback one migration
uv run alembic downgrade -1

# Rollback to specific revision
uv run alembic downgrade <revision>

# Rollback all migrations
uv run alembic downgrade base
```

### Check Status

```bash
# Current migration version
uv run alembic current

# Migration history
uv run alembic history

# Show pending migrations
uv run alembic heads
```

### Run for All Services

```bash
# Apply all migrations
./scripts/run_alembic_migrations.sh upgrade head

# Check status
./scripts/run_alembic_migrations.sh current

# Rollback one
./scripts/run_alembic_migrations.sh downgrade -1
```

## Service Locations

| Service | Alembic Config | Models Location |
|---------|---------------|-----------------|
| client_service | `client_service/alembic.ini` | `cds_client/models.py` |
| task_service | `task_service/alembic.ini` | `cds_task/models.py` |
| document_service | `document_service/alembic.ini` | `cds_document/models.py` |
| interaction_service | `interaction_service/alembic.ini` | `cds_interaction/models/` |
| product_service | `product_service/alembic.ini` | `app/repository/product_repo.py` |
| relationship_service | `relationship_service/alembic.ini` | `cds_relationship/db/models.py` |
| riskprofile_service | `riskprofile_service/alembic.ini` | `app/repository/models.py` |
| cas_service | `cas_service/alembic.ini` | `cas_audit/models.py` |
| rmbrain-mainapp | `rmbrain-mainapp/alembic.ini` | `app/models.py` |

## Workflow

1. **Edit models** → Make changes to SQLAlchemy models
2. **Generate migration** → `uv run alembic revision --autogenerate -m "Description"`
3. **Review migration** → Check `alembic/versions/` file
4. **Apply migration** → `uv run alembic upgrade head`
5. **Test** → Verify changes work correctly

## Troubleshooting

**Migration not detecting changes?**
- Ensure models are imported in `alembic/env.py`
- Check that models inherit from `Base`
- Verify `__tablename__` is set

**Import errors?**
- Check module paths in `alembic/env.py`
- Ensure service dependencies are installed (`uv sync`)
- Verify Python path is correct

**Connection errors?**
- Check `DATABASE_URL` environment variable
- Verify database exists and is accessible
- Check PostgreSQL is running
