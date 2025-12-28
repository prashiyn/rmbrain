# Database Configuration Review

## Database Schema Names

| Service | Database Schema Name | Database Type | Connection String Format | Currently in dapr.yaml? |
|---------|---------------------|---------------|-------------------------|------------------------|
| **bff-service** | N/A | None (stateless) | N/A | ❌ No |
| **cas-audit** | `cas_audit` | PostgreSQL | `postgresql://postgres:postgres@localhost:5432/cas_audit` | ✅ Yes |
| **cds-client** | `cds_client` | PostgreSQL | `postgresql://postgres:postgres@localhost:5432/cds_client` | ❌ No |
| **cds-document** | `cds_document` | PostgreSQL | `postgresql://postgres:postgres@localhost:5432/cds_document` | ❌ No |
| **cds-interaction** | `interaction_db` | PostgreSQL (async) | `postgresql+asyncpg://postgres:postgres@localhost:5432/interaction_db` | ✅ Yes |
| **cps-policy** | N/A | None (stateless) | N/A | ❌ No |
| **cds-product** | `cds_product` | PostgreSQL | `postgresql://postgres:postgres@localhost:5432/cds_product` | ✅ Yes |
| **cds-relationship** | `relationship_db` | PostgreSQL | `postgresql://postgres:postgres@localhost:5432/relationship_db` | ❌ No |
| **cds-riskprofile** | `riskprofile_db` | PostgreSQL | `postgresql://postgres:postgres@localhost:5432/riskprofile_db` | ✅ Yes |
| **rmbrain-mainapp** | `rmbrain_mainapp` | PostgreSQL (async) | `postgresql+asyncpg://postgres:postgres@localhost:5432/rmbrain_mainapp` | ❌ No |
| **cds-task** | `cds_task` | PostgreSQL (async) | `postgresql+asyncpg://postgres:postgres@localhost:5432/cds_task` | ❌ No |


## Current Status

### Services with DATABASE_URL in root `dapr.yaml`:
1. ✅ **cas-audit**: `postgresql://postgres:postgres@localhost:5432/cas_audit`
2. ✅ **cds-interaction**: `postgresql+asyncpg://postgres:postgres@localhost:5432/interaction_db`
3. ✅ **cds-product**: `postgresql://postgres:postgres@localhost:5432/cds_product`
4. ✅ **cds-riskprofile**: `postgresql://postgres:postgres@localhost:5432/riskprofile_db`

### Services missing DATABASE_URL in root `dapr.yaml`:
1. ❌ **cds-client**: Now has default in config → `postgresql://postgres:postgres@localhost:5432/cds_client` ✅ (Updated with PostgreSQL default)
2. ❌ **cds-document**: Now uses PostgreSQL → `postgresql://postgres:postgres@localhost:5432/cds_document`
3. ❌ **cds-relationship**: Has default `relationship_db` but not in dapr.yaml → `postgresql://postgres:postgres@localhost:5432/relationship_db`
4. ❌ **rmbrain-mainapp**: Has default `rmbrain_mainapp` but not in dapr.yaml → `postgresql+asyncpg://postgres:postgres@localhost:5432/rmbrain_mainapp`
5. ❌ **cds-task**: Now uses PostgreSQL (async) → `postgresql+asyncpg://postgres:postgres@localhost:5432/cds_task`

### Services without databases:
- **bff-service**: Stateless (no database)
- **cps-policy**: Stateless (no database)

## Configuration Options Analysis

### Option 1: Centralize in root `dapr.yaml` (Recommended for Development)

**Pros:**
- ✅ Single source of truth for all database connections
- ✅ Easy to see all database configurations at once
- ✅ Works well with `dapr run -f dapr.yaml` for running all services
- ✅ Environment variables are automatically passed to services
- ✅ No need for individual `.env` files per service

**Cons:**
- ⚠️ Contains credentials in version control (if committed)
- ⚠️ Less flexible for different environments (dev/staging/prod)
- ⚠️ Harder to override per-service in production

**Implementation:**
```yaml
env:
  DATABASE_URL: "postgresql://postgres:postgres@localhost:5432/cas_audit"
```

### Option 2: Use `.env` files per service (Recommended for Production)

**Pros:**
- ✅ Can be excluded from version control (via `.gitignore`)
- ✅ Different configurations per environment
- ✅ More secure (credentials not in code)
- ✅ Standard practice for 12-factor apps
- ✅ Easy to override per service

**Cons:**
- ⚠️ Need to manage multiple `.env` files
- ⚠️ Must remember to create `.env` files for each service
- ⚠️ Less visible (need to check each service directory)

**Implementation:**
- Create `.env` file in each service directory
- Services already support `.env` files (via `pydantic_settings`)

### Option 3: Hybrid Approach (Best of Both Worlds)

**Pros:**
- ✅ Default values in `dapr.yaml` for development
- ✅ `.env` files can override for production
- ✅ Flexible and secure
- ✅ Works for both local dev and production

**Cons:**
- ⚠️ Slightly more complex setup
- ⚠️ Need to document which takes precedence

**Implementation:**
- Add `DATABASE_URL` to `dapr.yaml` with development defaults
- Create `.env.example` files for each service with production template
- Services load `.env` if it exists (pydantic_settings does this automatically)

## Recommendations

### Immediate Actions:

1. **Add missing DATABASE_URL to root `dapr.yaml`** for:
   - `cds-client` → `postgresql://postgres:postgres@localhost:5432/cds_client`
   - `cds-document` → `postgresql://postgres:postgres@localhost:5432/cds_document` ✅ (Now using PostgreSQL)
   - `cds-relationship` → `postgresql://postgres:postgres@localhost:5432/relationship_db`
   - `rmbrain-mainapp` → `postgresql+asyncpg://postgres:postgres@localhost:5432/rmbrain_mainapp`
   - `cds-task` → `postgresql+asyncpg://postgres:postgres@localhost:5432/cds_task` ✅ (Now using PostgreSQL)

2. ✅ **cds-client**: Database confirmed as `cds_client`, now has PostgreSQL default in config ✅ (Updated)

3. **Create `.env.example` files** for each service with database connections:
   - Template for production use
   - Documented in README files
   - Can be copied to `.env` for local overrides

### Long-term Strategy:

**Recommended: Hybrid Approach**

1. **Development**: Use `dapr.yaml` with default localhost connections
2. **Production**: Use `.env` files (excluded from git) with production credentials
3. **Documentation**: Create `.env.example` files showing required variables

### Implementation Plan:

#### Step 1: Update root `dapr.yaml`
Add `DATABASE_URL` for all services that need databases:
- Use development defaults (localhost, postgres/postgres)
- Document that these can be overridden via `.env` files

#### Step 2: Create `.env.example` files
For each service with a database, create `.env.example`:
```bash
# Database Configuration
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/service_db

# Override for production:
# DATABASE_URL=postgresql://user:password@prod-host:5432/service_db
```

#### Step 3: Update `.gitignore`
Ensure `.env` files are ignored:
```
.env
.env.local
.env.*.local
```

#### Step 4: Document in README
Update main README to explain:
- Default database configs are in `dapr.yaml`
- Production should use `.env` files
- How to create `.env` from `.env.example`

## Database Connection String Patterns

### PostgreSQL (Standard):
```
postgresql://[user]:[password]@[host]:[port]/[database]
```

### PostgreSQL (Async - SQLAlchemy async):
```
postgresql+asyncpg://[user]:[password]@[host]:[port]/[database]
```

### SQLite (In-memory):
```
sqlite:///:memory:
sqlite+aiosqlite:///:memory:  # For async
```

## Questions to Resolve

1. ✅ **cds-client**: Database name is `cds_client`, now has PostgreSQL default in config (updated)
2. ✅ **cds-document**: Now using PostgreSQL with database `cds_document` (migrated from SQLite)
3. ✅ **cds-task**: Now using PostgreSQL (async) with database `cds_task` (migrated from SQLite)
4. **Production credentials**: How should production database credentials be managed?
   - Environment variables in deployment platform?
   - Secret management system?
   - Dapr secret stores?

## Next Steps

1. ✅ Review this document
2. ✅ Investigate `cds-client` database usage (confirmed: `cds_client`, now has PostgreSQL default)
3. ✅ Document, task, and client services migrated/updated to PostgreSQL
4. ⏳ Decide on hybrid vs. dapr.yaml-only approach
5. ⏳ Implement chosen approach (add DATABASE_URL to root dapr.yaml)
6. ⏳ Create `.env.example` files
7. ⏳ Update documentation

---

**Date**: 2025-01-20  
**Status**: ✅ **IMPLEMENTED** - Hybrid approach completed

## Implementation Status

✅ **Step 1**: Root `dapr.yaml` updated with all 9 database URLs  
✅ **Step 2**: Service-level `dapr.yaml` files updated with database URLs  
✅ **Step 3**: `.env.example` files created for all 9 services  
✅ **Step 4**: Root `.gitignore` created with `.env` patterns  
✅ **Step 5**: Documentation updated in README.md  

All services now use the hybrid approach:
- Development: Database URLs in `dapr.yaml` files
- Production: Override via `.env` files (excluded from git)

