# Hybrid Database Configuration Implementation Plan

## Assessment Summary

### Current State

#### Root `dapr.yaml` - DATABASE_URL Status:
- ✅ **cas-audit**: Has `DATABASE_URL` (line 49)
- ❌ **cds-client**: Missing `DATABASE_URL` (needs: `postgresql://postgres:postgres@localhost:5432/cds_client`)
- ❌ **cds-document**: Missing `DATABASE_URL` (needs: `postgresql://postgres:postgres@localhost:5432/cds_document`)
- ✅ **cds-interaction**: Has `DATABASE_URL` (line 110)
- ✅ **cds-product**: Has `DATABASE_URL` (line 155)
- ❌ **cds-relationship**: Missing `DATABASE_URL` (needs: `postgresql://postgres:postgres@localhost:5432/relationship_db`)
- ✅ **cds-riskprofile**: Has `DATABASE_URL` (line 196)
- ❌ **rmbrain-mainapp**: Missing `DATABASE_URL` (needs: `postgresql+asyncpg://postgres:postgres@localhost:5432/rmbrain_mainapp`)
- ❌ **cds-task**: Missing `DATABASE_URL` (needs: `postgresql+asyncpg://postgres:postgres@localhost:5432/cds_task`)

#### Service-Level `dapr.yaml` - DATABASE_URL Status:
- ✅ **cas_service**: Has `DATABASE_URL` in service dapr.yaml
- ❌ **client_service**: Missing `DATABASE_URL` in service dapr.yaml
- ❌ **document_service**: Missing `DATABASE_URL` in service dapr.yaml
- ✅ **interaction_service**: Has `DATABASE_URL` in service dapr.yaml
- ✅ **product_service**: Has `DATABASE_URL` in service dapr.yaml
- ❌ **relationship_service**: Has comment but no `DATABASE_URL` in service dapr.yaml
- ✅ **riskprofile_service**: Has `DATABASE_URL` in service dapr.yaml
- ❌ **rmbrain-mainapp**: Missing `DATABASE_URL` in service dapr.yaml
- ✅ **task_service**: Has `DATABASE_URL` in service dapr.yaml

#### .env.example Files:
- ❌ None exist - need to create for all 9 services with databases

#### .gitignore:
- ⚠️ Need to verify root .gitignore includes `.env` patterns
- ⚠️ Need to verify service-level .gitignore files include `.env` patterns

## Implementation Plan

### Step 1: Update Root `dapr.yaml`
**File**: `/dapr.yaml`
**Changes**: Add `DATABASE_URL` to env section for 5 missing services:
1. cds-client (line ~69)
2. cds-document (line ~89)
3. cds-relationship (line ~175)
4. rmbrain-mainapp (line ~216)
5. cds-task (line ~236)

**No code changes** - only YAML configuration

### Step 2: Update Service-Level `dapr.yaml` Files
**Files to update** (5 services):
1. `client_service/dapr.yaml` - Add `DATABASE_URL` to env section
2. `document_service/dapr.yaml` - Add `DATABASE_URL` to env section
3. `relationship_service/dapr.yaml` - Replace comment with `DATABASE_URL`
4. `rmbrain-mainapp/dapr.yaml` - Add `DATABASE_URL` to env section
5. `task_service/dapr.yaml` - Already has it, verify it matches root

**No code changes** - only YAML configuration

### Step 3: Create `.env.example` Files
**Files to create** (9 services with databases):
1. `cas_service/.env.example`
2. `client_service/.env.example`
3. `document_service/.env.example`
4. `interaction_service/.env.example`
5. `product_service/.env.example`
6. `relationship_service/.env.example`
7. `riskprofile_service/.env.example`
8. `rmbrain-mainapp/.env.example`
9. `task_service/.env.example`

**Content**: Template with development defaults and production comments

### Step 4: Verify/Update .gitignore Files
**Files to check/update**:
- Root `.gitignore` (if exists)
- Service-level `.gitignore` files (9 services)

**Patterns to ensure**:
```
.env
.env.local
.env.*.local
```

### Step 5: Update Documentation
**Files to update**:
- `README.md` - Add section about database configuration
- `DATABASE_CONFIGURATION_REVIEW.md` - Mark implementation as complete

## Detailed Changes

### Root `dapr.yaml` Changes

#### 1. cds-client (after line 69):
```yaml
      DAPR_PUBSUB_NAME: "pubsub"
      DATABASE_URL: "postgresql://postgres:postgres@localhost:5432/cds_client"
```

#### 2. cds-document (after line 89):
```yaml
      DAPR_PUBSUB_NAME: "pubsub"
      DATABASE_URL: "postgresql://postgres:postgres@localhost:5432/cds_document"
```

#### 3. cds-relationship (after line 175):
```yaml
      DAPR_PUBSUB_NAME: "pubsub"
      DATABASE_URL: "postgresql://postgres:postgres@localhost:5432/relationship_db"
```

#### 4. rmbrain-mainapp (after line 216):
```yaml
      DAPR_PUBSUB_NAME: "pubsub"
      DATABASE_URL: "postgresql+asyncpg://postgres:postgres@localhost:5432/rmbrain_mainapp"
```

#### 5. cds-task (after line 236):
```yaml
      DAPR_PUBSUB_NAME: "pubsub"
      DATABASE_URL: "postgresql+asyncpg://postgres:postgres@localhost:5432/cds_task"
```

### Service-Level `dapr.yaml` Changes

#### 1. client_service/dapr.yaml (after line 20):
```yaml
      DAPR_PUBSUB_NAME: "pubsub"
      DATABASE_URL: "postgresql://postgres:postgres@localhost:5432/cds_client"
```

#### 2. document_service/dapr.yaml (after line 20):
```yaml
      DAPR_PUBSUB_NAME: "pubsub"
      DATABASE_URL: "postgresql://postgres:postgres@localhost:5432/cds_document"
```

#### 3. relationship_service/dapr.yaml (replace line 36):
```yaml
      DAPR_PUBSUB_NAME: "pubsub"
      DATABASE_URL: "postgresql://postgres:postgres@localhost:5432/relationship_db"
```

#### 4. rmbrain-mainapp/dapr.yaml (after line 20):
```yaml
      DAPR_PUBSUB_NAME: "pubsub"
      DATABASE_URL: "postgresql+asyncpg://postgres:postgres@localhost:5432/rmbrain_mainapp"
```

#### 5. task_service/dapr.yaml:
- Already has `DATABASE_URL` on line 21 - verify it matches root

### .env.example Template

Standard template for all services:
```bash
# Database Configuration
# Development default (used when running from root dapr.yaml)
# Production: Override this value in .env file (not committed to git)
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/SERVICE_DB

# Production example (uncomment and update):
# DATABASE_URL=postgresql://user:password@prod-host:5432/SERVICE_DB
```

Note: Replace `SERVICE_DB` with actual database name for each service.

## Verification Checklist

After implementation, verify:
- [ ] All 9 services have `DATABASE_URL` in root `dapr.yaml`
- [ ] All 9 services have `DATABASE_URL` in service `dapr.yaml`
- [ ] All 9 services have `.env.example` files
- [ ] Root `.gitignore` includes `.env` patterns
- [ ] Service `.gitignore` files include `.env` patterns
- [ ] No code files were modified (only config files)
- [ ] Documentation updated

## Risk Assessment

**Low Risk Changes**:
- ✅ Only modifying YAML configuration files
- ✅ Only adding environment variables (no code logic changes)
- ✅ Creating new template files (.env.example)
- ✅ Updating .gitignore (safe operation)

**No Code Changes**:
- ✅ No Python files modified
- ✅ No application logic changed
- ✅ No database connection code changed
- ✅ Only configuration updates

## Next Steps

1. Review this plan
2. Implement changes in order (Step 1 → Step 5)
3. Verify all changes
4. Test with `dapr run -f dapr.yaml`

