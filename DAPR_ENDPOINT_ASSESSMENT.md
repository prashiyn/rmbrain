# Dapr Endpoint Assessment

## Current Status

### `/dapr/subscribe` Endpoint

**Services with POST (need to change to GET)**:
1. ❌ `task_service/cds_task/main.py` - Line 101: `@app.post("/dapr/subscribe")`
2. ❌ `cas_service/cas_audit/main.py` - Line 51: `@app.post("/dapr/subscribe")`
3. ❌ `interaction_service/cds_interaction/app/main.py` - Line 38: `@app.post("/dapr/subscribe")`
4. ❌ `document_service/cds_document/api.py` - Line 126: `@app.post("/dapr/subscribe")`
5. ❌ `product_service/app/main.py` - Line 28: `@app.post("/dapr/subscribe")`
6. ❌ `policy_service/app/subscribers/policy_events.py` - Line 13: `@router.post("/dapr/subscribe")`

**Services already using GET (correct)**:
1. ✅ `client_service/cds_client/main.py` - Line 33: `@app.get("/dapr/subscribe")`
2. ✅ `riskprofile_service/app/main.py` - Line 46: `@app.get("/dapr/subscribe")`
3. ✅ `relationship_service/cds_relationship/main.py` - Line 39: `@app.get("/dapr/subscribe")`

**Services without `/dapr/subscribe` endpoint**:
- `bff_service` - No subscription endpoint (stateless)
- `rmbrain-mainapp` - Need to check

### `/dapr/config` Endpoint

**Status**: No services have this endpoint defined. The 404 errors are **expected and safe** - this endpoint is optional and only needed for custom Dapr configuration.

**Action**: No changes needed (404 is acceptable)

## Required Changes

### Files to Update (6 endpoint files + 4 test files):

**Endpoint Files**:
1. ✅ `task_service/cds_task/main.py` - Changed `@app.post` to `@app.get`
2. ✅ `cas_service/cas_audit/main.py` - Changed `@app.post` to `@app.get`
3. ✅ `interaction_service/cds_interaction/app/main.py` - Changed `@app.post` to `@app.get`
4. ✅ `document_service/cds_document/api.py` - Changed `@app.post` to `@app.get`
5. ✅ `product_service/app/main.py` - Changed `@app.post` to `@app.get`
6. ✅ `policy_service/app/subscribers/policy_events.py` - Changed `@router.post` to `@router.get`

**Test Files** (updated to match):
1. ✅ `cas_service/tests/test_api.py` - Changed `client.post` to `client.get`
2. ✅ `interaction_service/tests/test_api.py` - Changed `client.post` to `client.get`
3. ✅ `document_service/tests/test_api.py` - Changed `client.post` to `client.get`
4. ✅ `product_service/tests/test_routes.py` - Changed `client.post` to `client.get`

**Note**: `riskprofile_service/tests/test_api.py` already uses `client.get` (correct)

## Why This Fix Works

Dapr sidecar uses **GET** requests to discover:
- Subscriptions: `GET /dapr/subscribe` - Returns list of subscription configurations
- Config: `GET /dapr/config` - Returns custom Dapr configuration (optional)

Using POST causes 405 Method Not Allowed errors because FastAPI's POST handler doesn't accept GET requests.

