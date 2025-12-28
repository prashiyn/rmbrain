# RM Brain - Dapr Microservices Monorepo

A microservices monorepo built on Dapr, following a centralized configuration architecture for all Dapr components, configurations, and subscriptions.

## 📋 Table of Contents

- [Overview](#overview)
- [Repository Structure](#repository-structure)
- [Dapr Architecture](#dapr-architecture)
- [Quick Start](#quick-start)
- [Running Services](#running-services)
- [Dapr Configuration](#dapr-configuration)
- [Service Ports](#service-ports)
- [Development Workflow](#development-workflow)
- [Component Management](#component-management)
- [Configuration Management](#configuration-management)
- [Troubleshooting](#troubleshooting)
- [Best Practices](#best-practices)

## Overview

This repository contains multiple microservices that communicate via Dapr's building blocks (pub/sub, state management, service invocation). All Dapr-related configuration is **centralized** in the `/dapr` directory, following the architecture defined in `.cursor/rules.md`.

### Key Principles

- **Centralized Configuration**: All Dapr components, configs, and subscriptions live in `/dapr`
- **Service Isolation**: Each service implements business logic only
- **Standardized Ports**: Each service has unique Dapr ports to avoid conflicts
- **Environment-Driven**: Services use environment variables for configuration
- **Multi-App Support**: Run all services together or individually

## Repository Structure

```
rmbrain/
├── dapr/                      # Centralized Dapr configuration
│   ├── components/           # All Dapr components (pubsub, state stores, etc.)
│   ├── config/               # Global Dapr configuration (tracing, metrics, resiliency)
│   └── subscriptions/        # Declarative pub/sub subscriptions
│
├── bff_service/              # Backend for Frontend
├── cas_service/              # Canonical Audit Service
├── client_service/           # Client Data Service
├── document_service/          # Document Management Service
├── interaction_service/      # Interaction Service
├── policy_service/           # Canonical Policy Service
├── product_service/          # Product Data Service
├── relationship_service/     # Relationship Service
├── riskprofile_service/      # Risk Profile Service
├── rmbrain-mainapp/          # Main Application
├── task_service/            # Task Service
│
├── dapr.yaml                 # Multi-app Dapr configuration (runs all services)
├── .cursor/                  # Cursor IDE rules and configuration
└── README.md                 # This file
```

## Dapr Architecture

### Centralized Configuration

All Dapr resources are centralized in `/dapr`:

- **Components** (`/dapr/components/`): Pub/sub, state stores, bindings, secrets
- **Config** (`/dapr/config/`): Tracing, metrics, resiliency policies
- **Subscriptions** (`/dapr/subscriptions/`): Declarative pub/sub subscriptions

### Service Configuration

Each service has its own `dapr.yaml` file that:
- References centralized components: `../dapr/components`
- References centralized config: `../dapr/config/global-config.yaml`
- Defines service-specific settings (ports, environment variables, command)

### Why Centralized?

1. **Consistency**: All services use the same pub/sub and state store components
2. **Maintainability**: Update components once, affects all services
3. **Environment Parity**: Same configuration across dev, staging, production
4. **Compliance**: Follows `.cursor/rules.md` architecture guidelines

## Quick Start

### Prerequisites

- **Dapr CLI**: Install from [dapr.io](https://docs.dapr.io/getting-started/install-dapr-cli/)
- **Python 3.11+**: Required for all services
- **PostgreSQL**: For services that require a database
- **Redis** (optional): For production pub/sub and state store
- **uv** (recommended): Python package manager

### Initial Setup

1. **Set up databases** (REQUIRED before running services):
   ```bash
   # Run the database setup script
   ./scripts/setup_databases.sh
   
   # Or see scripts/SETUP_DATABASES.md for manual setup
   ```
   
   This creates all 9 PostgreSQL databases and initializes schemas.

2. **Initialize Dapr** (if not already done):
   ```bash
   dapr init
   ```

3. **Verify Dapr installation**:
   ```bash
   dapr --version
   dapr list
   ```

3. **Start Redis** (if using Redis components):
   ```bash
   # Using Docker
   docker run -d -p 6379:6379 redis:latest
   
   # Or use Dapr's default Redis (started by dapr init)
   ```

## Running Services

### Option 1: Run All Services (Multi-App)

**Prerequisites**: 
1. **Set up databases** (see Initial Setup step 1 above)
2. Install dependencies for all services:
```bash
# Install dependencies for each service
for dir in bff_service cas_service client_service document_service interaction_service policy_service product_service relationship_service riskprofile_service rmbrain-mainapp task_service; do
  echo "Installing dependencies in $dir"
  (cd "$dir" && uv sync)
done
```

Run all services simultaneously using the root `dapr.yaml`:

```bash
# From repository root
dapr run -f dapr.yaml
```

This will:
- Start all 11 services with their Dapr sidecars
- Use centralized components from `/dapr/components`
- Apply global config from `/dapr/config/global-config.yaml`
- Assign unique ports to each service (see [Service Ports](#service-ports))

**Note**: This is useful for integration testing and local development of the full system.

**Important**: 
- Ensure all service dependencies are installed before running (see [Setting Up a Service](#setting-up-a-service))
- Commands use `uv run python -m uvicorn` which ensures Python from the local virtual environment is used
- Each service has its own virtual environment (`.venv`), and `uv run` automatically uses the correct environment

### Option 2: Run Individual Service

Run a single service for development/debugging:

```bash
# Navigate to service directory
cd <service-name>

# Run with service's dapr.yaml
dapr run -f dapr.yaml
```

Example:
```bash
cd task_service
dapr run -f dapr.yaml
```

The service's `dapr.yaml` will:
- Reference `../dapr/components` (centralized)
- Reference `../dapr/config/global-config.yaml` (centralized)
- Use service-specific ports and environment variables

### Option 3: Manual Dapr Run

For more control, run Dapr manually:

```bash
dapr run \
  --app-id <service-id> \
  --app-port 8000 \
  --dapr-http-port <http-port> \
  --dapr-grpc-port <grpc-port> \
  --components-path ../dapr/components \
  --config ../dapr/config/global-config.yaml \
  -- <command>
```

Example for task service:
```bash
dapr run \
  --app-id cds-task \
  --app-port 8000 \
  --dapr-http-port 3510 \
  --dapr-grpc-port 60011 \
  --components-path ../dapr/components \
  --config ../dapr/config/global-config.yaml \
  -- uv run python -m uvicorn cds_task.main:app --host 0.0.0.0 --port 8000
```

## Dapr Configuration

### Components

Components are defined in `/dapr/components/`:

#### Available Components

- **`pubsub.yaml`**: In-memory pub/sub (development)
- **`rmbrain-pubsub.yaml`**: Redis pub/sub (production)
- **`statestore.yaml`**: In-memory state store (development)
- **`rmbrain-statestore.yaml`**: Redis state store (production)

#### Using Components

Services reference components by name in their code:
- `pubsub` or `rmbrain-pubsub` for pub/sub operations
- `statestore` or `rmbrain-statestore` for state operations

The component name must match the `metadata.name` in the component YAML file.

### Global Configuration

Global Dapr configuration is in `/dapr/config/global-config.yaml`:

- **Tracing**: OpenTelemetry integration
- **Metrics**: Prometheus metrics
- **HTTP Pipeline**: Middleware (rate limiting, CORS)
- **Pub/Sub Features**: Routing, dead letter queues
- **Access Control**: Service-to-service authorization policies

### Resiliency

Resiliency policies are in `/dapr/config/resiliency.yaml`:

- **Retry Policies**: Automatic retry for failed requests
- **Circuit Breakers**: Prevent cascading failures
- **Timeouts**: Request timeout configuration

## Service Ports

Each service has unique Dapr ports to avoid conflicts:

| Service | App Port | Dapr HTTP | Dapr gRPC |
|---------|----------|-----------|-----------|
| bff-service | 8000 | 3500 | 60001 |
| cas-audit | 8001 | 3501 | 60002 |
| cds-client | 8002 | 3502 | 60003 |
| cds-document | 8003 | 3503 | 60004 |
| cds-interaction | 8004 | 3504 | 60005 |
| cps-policy | 8005 | 3505 | 60006 |
| cds-product | 8006 | 3506 | 60007 |
| cds-relationship | 8007 | 3507 | 60008 |
| cds-riskprofile | 8008 | 3508 | 60009 |
| rmbrain-mainapp | 8009 | 3509 | 60010 |
| cds-task | 8010 | 3510 | 60011 |

**Note**: gRPC ports use the 60000 series to avoid conflicts with Dapr's internal services which use the 50000 series.

### Accessing Services via Dapr

Use Dapr service invocation to call services:

```bash
# Call a service via Dapr
curl http://localhost:<dapr-http-port>/v1.0/invoke/<app-id>/method/<endpoint>
```

Example:
```bash
# Call task service health endpoint
curl http://localhost:3510/v1.0/invoke/cds-task/method/health

# Call policy service authorize endpoint
curl -X POST http://localhost:3505/v1.0/invoke/cps-policy/method/api/v1/authorize \
  -H "Content-Type: application/json" \
  -d '{"actor": {...}, "action": "view_task", ...}'
```

## Development Workflow

### Setting Up a Service

1. **Navigate to service directory**:
   ```bash
   cd <service-name>
   ```

2. **Install dependencies** (REQUIRED before running):
   ```bash
   uv sync
   # or
   pip install -r requirements.txt
   ```
   
   **Important**: Services will fail to start with "Failed to spawn: uvicorn" if dependencies aren't installed.

3. **Set up database** (if required):
   ```bash
   # Create database
   createdb <database-name>
   
   # Run migrations
   # (check service README for specific instructions)
   ```

4. **Configure environment**:
   - Edit `dapr.yaml` for service-specific settings
   - Or create `.env` file (if service supports it)

5. **Run the service**:
   ```bash
   dapr run -f dapr.yaml
   ```

### Making Changes

#### Adding a New Component

1. Create component YAML in `/dapr/components/`:
   ```yaml
   apiVersion: dapr.io/v1alpha1
   kind: Component
   metadata:
     name: my-component
     namespace: default
   spec:
     type: <component-type>
     version: v1
     metadata:
       - name: <setting>
         value: <value>
   ```

2. Reference it in service code by the `metadata.name`

#### Modifying Global Config

1. Edit `/dapr/config/global-config.yaml`
2. Changes apply to all services on next restart
3. For service-specific config, add to service's `dapr.yaml` `env` section

#### Adding a New Service

1. Create service directory in repository root
2. Create `dapr.yaml` with:
   - Unique ports (check existing services)
   - Reference to `../dapr/components`
   - Reference to `../dapr/config/global-config.yaml`
3. Add service to root `dapr.yaml` for multi-app support

### Testing

#### Run Service Tests

```bash
cd services/<service-name>
uv run pytest
```

#### Integration Testing

1. Start all services:
   ```bash
   dapr run -f dapr.yaml
   ```

2. Run integration tests (if available):
   ```bash
   # From repository root or test directory
   pytest tests/integration/
   ```

## Component Management

### Development vs Production

**Development** (in-memory):
- `pubsub.yaml` - In-memory pub/sub
- `statestore.yaml` - In-memory state store

**Production** (Redis):
- `rmbrain-pubsub.yaml` - Redis pub/sub
- `rmbrain-statestore.yaml` - Redis state store

### Switching Components

To switch from in-memory to Redis:

1. Update service code to use `rmbrain-pubsub` instead of `pubsub`
2. Or update component file to use Redis type
3. Ensure Redis is running

### Component Naming

- Use descriptive names: `rmbrain-pubsub`, `rmbrain-statestore`
- Include namespace: `namespace: default`
- Document component purpose in comments

## Configuration Management

### Database Configuration

This repository uses a **hybrid approach** for database configuration:

- **Development**: Database URLs are defined in `dapr.yaml` files (root and service-level) with localhost defaults
- **Production**: Override database URLs using `.env` files in each service directory (not committed to git)

#### Database URLs in dapr.yaml

All services with databases have `DATABASE_URL` defined in:
- Root `dapr.yaml` - Used when running all services together (`dapr run -f dapr.yaml`)
- Service `dapr.yaml` - Used when running individual services

**Development defaults** (localhost):
- `postgresql://postgres:postgres@localhost:5432/<database_name>` (standard PostgreSQL)
- `postgresql+asyncpg://postgres:postgres@localhost:5432/<database_name>` (async PostgreSQL)

#### Using .env Files for Production

1. **Copy the example file**:
   ```bash
   cd <service-name>
   cp .env.example .env
   ```

2. **Update with production credentials**:
   ```bash
   # Edit .env file
   DATABASE_URL=postgresql://user:password@prod-host:5432/database_name
   ```

3. **The service will automatically load** `.env` file (via `pydantic_settings`)

**Important**: 
- `.env` files are excluded from git (via `.gitignore`)
- Never commit production credentials
- Use `.env.example` as a template

#### Database Schema Names

| Service | Database Name |
|---------|--------------|
| cas-audit | `cas_audit` |
| cds-client | `cds_client` |
| cds-document | `cds_document` |
| cds-interaction | `interaction_db` |
| cds-product | `cds_product` |
| cds-relationship | `relationship_db` |
| cds-riskprofile | `riskprofile_db` |
| rmbrain-mainapp | `rmbrain_mainapp` |
| cds-task | `cds_task` |

### Environment Variables

Services use environment variables for configuration:

**Required Variables** (set in `dapr.yaml`):
- `APP_ID`: Service identifier
- `APP_PORT`: Application port (usually 8000)
- `DAPR_HTTP_PORT`: Dapr HTTP port (unique per service)
- `DAPR_GRPC_PORT`: Dapr gRPC port (unique per service)

**Service-Specific Variables**:
- `DATABASE_URL`: Database connection string (see [Database Configuration](#database-configuration) above)
- `DAPR_PUBSUB_NAME`: Pub/sub component name
- `LOG_LEVEL`: Logging level

### Overriding Configuration

1. **Via Environment Variables**:
   ```bash
   export DATABASE_URL="postgresql://user:pass@localhost/db"
   dapr run -f dapr.yaml
   ```

2. **Via .env File** (if service supports it):
   ```bash
   # Create .env in service directory
   DATABASE_URL=postgresql://user:pass@localhost/db
   ```

3. **Via dapr.yaml**:
   Edit the `env` section in service's `dapr.yaml`

## Troubleshooting

### Service Won't Start

1. **Install dependencies first** (IMPORTANT):
   ```bash
   # Navigate to service directory
   cd <service-name>
   
   # Install dependencies using uv
   uv sync
   
   # Or using pip
   pip install -r requirements.txt
   ```
   
   **Error**: `Failed to spawn: uvicorn` usually means:
   - Dependencies aren't installed (run `uv sync` in service directory)
   - Virtual environment doesn't exist (run `uv sync` to create it)
   - Using `python -m uvicorn` ensures the correct Python from the venv is used

2. **Check Dapr is running**:
   ```bash
   dapr list
   ```

3. **Check ports are available**:
   ```bash
   # Check if port is in use
   lsof -i :<port>
   ```

4. **Check component files exist**:
   ```bash
   ls -la ../dapr/components/
   ```

5. **Check config file exists**:
   ```bash
   ls -la ../dapr/config/global-config.yaml
   ```

### Components Not Loading

1. **Verify component path**:
   - Should be `../dapr/components` from service directory
   - Or `./dapr/components` from repository root

2. **Check component YAML syntax**:
   ```bash
   # Validate YAML
   yamllint dapr/components/*.yaml
   ```

3. **Check component name matches**:
   - Component `metadata.name` must match what service code uses

### Port Conflicts

If you see port conflicts (especially gRPC ports):

1. **Check which service is using the port**:
   ```bash
   dapr list
   lsof -i :<port>
   ```

2. **Stop conflicting service**:
   ```bash
   dapr stop --app-id <service-id>
   ```

3. **Note**: gRPC ports are in the 60000 series to avoid Dapr's internal 50000 series ports

4. **Or change port in service's dapr.yaml**

### Events Not Publishing/Receiving

1. **Check pub/sub component is loaded**:
   ```bash
   # Check Dapr logs
   dapr logs --app-id <service-id>
   ```

2. **Verify topic names match**:
   - Publisher and subscriber must use same topic name

3. **Check pub/sub component type**:
   - In-memory pub/sub doesn't persist across restarts
   - Use Redis for production

### Service Invocation Failing

1. **Check target service is running**:
   ```bash
   dapr list
   ```

2. **Verify app-id matches**:
   - Service invocation uses `app-id` from `dapr.yaml`

3. **Check Dapr HTTP port**:
   - Use correct Dapr HTTP port for the target service

## Best Practices

### 1. Component Management

- ✅ **DO**: Keep all components in `/dapr/components/`
- ✅ **DO**: Use consistent naming conventions
- ✅ **DO**: Document component purpose
- ❌ **DON'T**: Create service-specific component directories
- ❌ **DON'T**: Duplicate components across services

### 2. Configuration

- ✅ **DO**: Use centralized global config
- ✅ **DO**: Override via environment variables when needed
- ✅ **DO**: Document service-specific requirements
- ❌ **DON'T**: Hardcode configuration in code
- ❌ **DON'T**: Create service-specific config files (unless necessary)

### 3. Port Management

- ✅ **DO**: Use unique ports for each service
- ✅ **DO**: Document port assignments
- ✅ **DO**: Check port availability before starting
- ❌ **DON'T**: Reuse ports across services
- ❌ **DON'T**: Use ports below 3500 (reserved for Dapr)

### 4. Development

- ✅ **DO**: Run services individually during development
- ✅ **DO**: Use multi-app mode for integration testing
- ✅ **DO**: Test with both in-memory and Redis components
- ❌ **DON'T**: Modify centralized components without testing
- ❌ **DON'T**: Commit local environment-specific changes

### 5. Service Design

- ✅ **DO**: Use environment variables for configuration
- ✅ **DO**: Expose `/health` endpoint
- ✅ **DO**: Use Dapr SDK for pub/sub and state
- ✅ **DO**: Follow event-driven architecture
- ❌ **DON'T**: Bypass Dapr for inter-service communication
- ❌ **DON'T**: Implement custom retry logic (use Dapr resiliency)

## Additional Resources

- **Dapr Documentation**: [https://docs.dapr.io](https://docs.dapr.io)
- **Dapr Python SDK**: [https://github.com/dapr/python-sdk](https://github.com/dapr/python-sdk)
- **Repository Rules**: See `.cursor/rules.md` for architecture guidelines
- **Service Documentation**: See individual service `README.md` files

## Getting Help

- Check service-specific README files in `/<service-name>/README.md`
- Review Dapr logs: `dapr logs --app-id <service-id>`
- Check Dapr status: `dapr list` and `dapr components list`
- Review centralized config: `/dapr/README.md`

---

**Last Updated**: 2025-01-20  
**Dapr Version**: 1.x  
**Python Version**: 3.11+

