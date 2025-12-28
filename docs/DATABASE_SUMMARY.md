# Database Configuration Summary

## Updated Status (After PostgreSQL Migration)

### ✅ Services with DATABASE_URL in root `dapr.yaml` (4/9):
1. **cas-audit**: `postgresql://postgres:postgres@localhost:5432/cas_audit`
2. **cds-interaction**: `postgresql+asyncpg://postgres:postgres@localhost:5432/interaction_db`
3. **cds-product**: `postgresql://postgres:postgres@localhost:5432/cds_product`
4. **cds-riskprofile**: `postgresql://postgres:postgres@localhost:5432/riskprofile_db`

### ❌ Services missing DATABASE_URL in root `dapr.yaml` (5/9):
1. **cds-client**: `postgresql://postgres:postgres@localhost:5432/cds_client` ✅ (Now has default in config)
2. **cds-document**: `postgresql://postgres:postgres@localhost:5432/cds_document` ✅ (Migrated to PostgreSQL)
3. **cds-relationship**: `postgresql://postgres:postgres@localhost:5432/relationship_db`
4. **rmbrain-mainapp**: `postgresql+asyncpg://postgres:postgres@localhost:5432/rmbrain_mainapp`
5. **cds-task**: `postgresql+asyncpg://postgres:postgres@localhost:5432/cds_task` ✅ (Migrated to PostgreSQL)

### 📊 Database Summary

| Service | Database Name | Type | Connection String | In Root dapr.yaml? |
|---------|--------------|------|-------------------|-------------------|
| cas-audit | `cas_audit` | PostgreSQL | `postgresql://...` | ✅ Yes |
| cds-client | `cds_client` | PostgreSQL | `postgresql://...` | ❌ No |
| cds-document | `cds_document` | PostgreSQL | `postgresql://...` | ❌ No |
| cds-interaction | `interaction_db` | PostgreSQL (async) | `postgresql+asyncpg://...` | ✅ Yes |
| cds-product | `cds_product` | PostgreSQL | `postgresql://...` | ✅ Yes |
| cds-relationship | `relationship_db` | PostgreSQL | `postgresql://...` | ❌ No |
| cds-riskprofile | `riskprofile_db` | PostgreSQL | `postgresql://...` | ✅ Yes |
| rmbrain-mainapp | `rmbrain_mainapp` | PostgreSQL (async) | `postgresql+asyncpg://...` | ❌ No |
| cds-task | `cds_task` | PostgreSQL (async) | `postgresql+asyncpg://...` | ❌ No |

**Total Databases**: 9 PostgreSQL databases  
**Services without databases**: 2 (bff-service, cps-policy)

## Recent Changes

✅ **cds-client**: Updated config with PostgreSQL default (`cds_client`)  
✅ **cds-document**: Migrated from SQLite in-memory to PostgreSQL (`cds_document`)  
✅ **cds-task**: Migrated from SQLite in-memory to PostgreSQL async (`cds_task`)

Both services now have PostgreSQL configured in their service-level `dapr.yaml` files, but need to be added to the root `dapr.yaml` for centralized management.

## Next Action Required

Add the 5 missing `DATABASE_URL` entries to root `dapr.yaml` to complete the centralized database configuration.

