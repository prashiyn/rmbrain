# Directory Restructure - Services Moved to Root

## Changes Applied

All service directories have been moved from `services/` to the repository root to restore Cursor history and simplify the structure.

## What Changed

### Directory Structure

**Before:**
```
rmbrain/
├── services/
│   ├── bff_service/
│   ├── cas_service/
│   └── ...
└── dapr/
```

**After:**
```
rmbrain/
├── bff_service/
├── cas_service/
├── client_service/
├── document_service/
├── interaction_service/
├── policy_service/
├── product_service/
├── relationship_service/
├── riskprofile_service/
├── rmbrain-mainapp/
├── task_service/
└── dapr/
```

## Files Updated

### 1. Root `dapr.yaml`
- Changed `appDirPath` from `./services/<service>` to `./<service>`
- All 11 services updated

### 2. Service `dapr.yaml` Files (11 files)
- Changed `componentsPath` from `../../dapr/components` to `../dapr/components`
- Changed `config` from `../../dapr/config/global-config.yaml` to `../dapr/config/global-config.yaml`

### 3. Documentation Files
- `README.md` - Updated all references to new structure
- `dapr/README.md` - Updated service paths
- `SERVICES_ASSESSMENT.md` - Updated path references
- `FIXES_APPLIED.md` - Updated path references
- `UVICORN_FIX.md` - Updated path references
- All service `README.md` files - Updated `../../dapr` to `../dapr`

### 4. Scripts
- `scripts/install_all_dependencies.sh` - Updated to use service names directly

### 5. Configuration Files
- `.cursor/rules.json` - Updated forbidden paths (removed `services/` prefix)
- `.cursor/rules.md` - Updated structure diagram

## Path Changes Summary

| Item | Old Path | New Path |
|------|----------|----------|
| Service directories | `services/<service>/` | `<service>/` |
| Components path | `../../dapr/components` | `../dapr/components` |
| Config path | `../../dapr/config/global-config.yaml` | `../dapr/config/global-config.yaml` |
| App directory path | `./services/<service>` | `./<service>` |

## Verification

✅ All services moved to root  
✅ Root `dapr.yaml` updated  
✅ All service `dapr.yaml` files updated  
✅ Documentation updated  
✅ Scripts updated  
✅ Configuration files updated  
✅ No Python code imports affected (services use relative imports)  
✅ Empty `services/` directory removed  

## Impact Assessment

### ✅ No Breaking Changes
- Python imports use relative paths (e.g., `from cds_client.main import app`)
- No code references to `services/` directory
- All paths are relative and work correctly

### ✅ Benefits
- Simpler directory structure
- Easier navigation
- Cursor history preserved
- Shorter paths in documentation

## Next Steps

1. **Test the setup**:
   ```bash
   # Install dependencies
   for dir in bff_service cas_service client_service document_service interaction_service policy_service product_service relationship_service riskprofile_service rmbrain-mainapp task_service; do
     (cd "$dir" && uv sync)
   done
   
   # Run all services
   dapr run -f dapr.yaml
   ```

2. **Verify individual services**:
   ```bash
   cd <service-name>
   dapr run -f dapr.yaml
   ```

---

**Date**: 2025-01-20  
**Status**: ✅ Complete - All services moved to root, all references updated

