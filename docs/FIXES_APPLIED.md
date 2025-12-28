# Dapr Configuration Fixes Applied

## Issues Identified

1. **Port Conflict**: gRPC ports in 50000 series conflicted with Dapr's internal services
2. **Uvicorn Not Found**: Services failing with "Failed to spawn: uvicorn" error

## Fixes Applied

### 1. Port Configuration ✅

**Changed**: All gRPC ports from 50000 series to 60000 series

**Updated Files**:
- `/dapr.yaml` (root multi-app configuration)
- All service `dapr.yaml` files (11 services)
- `/README.md` (port assignment table)
- `/dapr/README.md` (port assignment table)

**New Port Assignments**:
- bff-service: 60001
- cas-audit: 60002
- cds-client: 60003
- cds-document: 60004
- cds-interaction: 60005
- cps-policy: 60006
- cds-product: 60007
- cds-relationship: 60008
- cds-riskprofile: 60009
- rmbrain-mainapp: 60010
- cds-task: 60011

### 2. Uvicorn Dependency Issue ⚠️

**Issue**: Services fail with "Failed to spawn: uvicorn" because dependencies aren't installed.

**Solution**: Install dependencies before running services.

**Updated Documentation**:
- Added prerequisite note in `/README.md` about installing dependencies
- Added troubleshooting section for "Service Won't Start"
- Added note in "Running Services" section about dependency installation

## Next Steps

### Before Running Services

1. **Install dependencies for each service**:
   ```bash
   # Install all at once
   for dir in bff_service cas_service client_service document_service interaction_service policy_service product_service relationship_service riskprofile_service rmbrain-mainapp task_service; do
     echo "Installing dependencies in $dir"
     (cd "$dir" && uv sync)
   done
   
   # Or install individually
   cd <service-name>
   uv sync
   ```

2. **Verify Dapr is initialized**:
   ```bash
   dapr --version
   dapr init  # if not already done
   ```

3. **Start services**:
   ```bash
   # From repository root
   dapr run -f dapr.yaml
   ```

## Verification

After applying fixes, verify:

1. **Ports are available**:
   ```bash
   # Check gRPC ports (should be free)
   lsof -i :60001-60011
   ```

2. **Dependencies are installed**:
   ```bash
   # Check if uvicorn is available
   cd <service-name>
   uv run which uvicorn
   ```

3. **Dapr can start services**:
   ```bash
   # Try starting a single service first
   cd bff_service
   dapr run -f dapr.yaml
   ```

## Summary

✅ **Port conflicts resolved**: All gRPC ports moved to 60000 series  
⚠️ **Dependencies required**: Services must have dependencies installed before running  
📝 **Documentation updated**: README includes troubleshooting and prerequisites  

---

**Date**: 2025-01-20  
**Status**: Port fixes applied, dependency installation documented

