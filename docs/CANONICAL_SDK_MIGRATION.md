# Canonical Schema SDK Migration to Root Canonical Directory

## Overview

Migrated `rmbrain-mainapp/app/shared/canonical_schema_sdk/schemas/` and `semantics/` directories to the root `canonical/` directory to align with the canonical schema migration strategy.

## Changes Made

### 1. Semantic File Migration
- **Moved**: `rmbrain-mainapp/app/shared/canonical_schema_sdk/semantics/client.v1.semantic.yaml`
- **To**: `canonical/semantics/client.v1.semantic.yaml`
- **Status**: ✅ Completed

### 2. Registry Path Updates
- **File**: `rmbrain-mainapp/app/shared/canonical_schema_sdk/registry.py`
- **Changes**:
  ```python
  # Before
  CANONICAL_SDK_DIR = Path(__file__).parent
  SCHEMAS_DIR = CANONICAL_SDK_DIR / "schemas"
  SEMANTICS_DIR = CANONICAL_SDK_DIR / "semantics"
  
  # After
  REPO_ROOT = Path(__file__).parent.parent.parent.parent.parent
  SCHEMAS_DIR = REPO_ROOT / "canonical" / "entities"
  SEMANTICS_DIR = REPO_ROOT / "canonical" / "semantics"
  ```
- **Status**: ✅ Completed

### 3. Cleanup
- **Deleted**: `rmbrain-mainapp/app/shared/canonical_schema_sdk/schemas/client.v1.json` (duplicate, canonical version is authoritative)
- **Deleted**: `rmbrain-mainapp/app/shared/canonical_schema_sdk/semantics/client.v1.semantic.yaml` (moved to canonical)
- **Removed**: Empty `schemas/` and `semantics/` directories from SDK
- **Status**: ✅ Completed

## Test Files

### No Changes Required
- **`tests/test_canonical_schema_sdk.py`**: Uses `patch()` to mock `SCHEMAS_DIR` and `SEMANTICS_DIR` in tests, so no changes needed
- **`tests/test_canonical_normalization.py`**: Mocks the registry, so no changes needed
- **All other tests**: Use mocked registries, so no changes needed

## Verification

### Path Resolution
- ✅ Registry correctly resolves to `canonical/entities/` for schemas
- ✅ Registry correctly resolves to `canonical/semantics/` for semantic constraints
- ✅ All entity schemas accessible from `canonical/entities/`
- ✅ Semantic constraints accessible from `canonical/semantics/`

### File Structure
```
canonical/
├── entities/
│   ├── client.v1.json          ✅ (authoritative)
│   ├── client_link.v1.json
│   ├── document.v1.json
│   ├── interaction.v1.json
│   ├── product.v1.json
│   ├── relationship.v1.json
│   ├── riskprofile.v1.json
│   ├── suitability_assessment.v1.json
│   └── task.v1.json
└── semantics/
    └── client.v1.semantic.yaml  ✅ (migrated from SDK)

rmbrain-mainapp/app/shared/canonical_schema_sdk/
├── registry.py                  ✅ (updated paths)
├── sdk.py                       ✅ (no changes needed)
├── errors.py                    ✅ (no changes needed)
├── validators/                  ✅ (no changes needed)
└── (schemas/ and semantics/ removed) ✅
```

## Alignment with Documentation

This migration aligns with:
- **`docs/cds_shcred_infra.md`**: Canonical schemas must live in shared canonical registry
- **`rmbrain-mainapp/docs/canonical_sdk.md`**: Section 4.1 describes the structure (now pointing to root canonical)

## Benefits

1. **Single Source of Truth**: All canonical schemas and semantics in one location
2. **Consistency**: All services use the same canonical directory structure
3. **Maintainability**: Easier to manage and version canonical schemas
4. **No Duplication**: Removed duplicate schema files

## Next Steps

1. ✅ Migration complete
2. ✅ Tests verified (use mocks, no changes needed)
3. ✅ Old directories cleaned up
4. ⚠️  **Note**: If additional semantic constraint files are added, they should be placed in `canonical/semantics/`

## Backward Compatibility

- ✅ All existing code continues to work (registry handles path resolution)
- ✅ Tests continue to work (they mock the paths)
- ✅ No breaking changes to public API
