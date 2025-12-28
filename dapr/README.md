# Dapr Configuration Directory

This directory contains all centralized Dapr configuration following the standardized structure defined in `.cursor/rules.md`.

## Directory Structure

```
dapr/
├── components/         # All Dapr components (pubsub, state stores, bindings, secrets)
├── config/            # Global Dapr configuration (tracing, metrics, resiliency)
└── subscriptions/     # Declarative pub/sub subscriptions
```

## Components

### Pub/Sub Components
- `pubsub.yaml` - In-memory pubsub (development)
- `rmbrain-pubsub.yaml` - Redis pubsub (production)

### State Store Components
- `statestore.yaml` - In-memory state store (development)
- `rmbrain-statestore.yaml` - Redis state store (production)

## Configuration

### Global Configuration
- `global-config.yaml` - Main Dapr configuration including:
  - Tracing (OpenTelemetry)
  - Metrics
  - HTTP pipeline handlers (rate limiting, CORS)
  - Pub/sub features (routing, dead letter)
  - Access control policies

### Resiliency
- `resiliency.yaml` - Resiliency policies for inter-service communication:
  - Retry policies
  - Circuit breaker policies

## Usage

### Running All Services

From the repository root, run:

```bash
dapr run -f dapr.yaml
```

This will start all microservices with their Dapr sidecars using the centralized configuration.

### Running Individual Services

Individual services can still use their local `dapr.yaml` files for debugging:

```bash
cd <service-name>
dapr run -f dapr.yaml
```

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

## Rules

Following `.cursor/rules.md`:

1. **Components**: All Dapr components live in `/dapr/components`
2. **Config**: All global Dapr configuration lives in `/dapr/config`
3. **Subscriptions**: All declarative pub/sub subscriptions live in `/dapr/subscriptions`
4. **Service YAMLs**: Service-level `dapr.yaml` files are for single-service debugging only
5. **No Inline Config**: Services MUST NOT inline Dapr component configuration

## Adding New Components

When adding new Dapr components:

1. Create the component YAML file in `/dapr/components/`
2. Use consistent naming: `<component-type>-<name>.yaml`
3. Include namespace: `default`
4. Document any production-specific settings

## Adding New Configurations

When adding new Dapr configurations:

1. Create the config YAML file in `/dapr/config/`
2. Reference it in the root `dapr.yaml` if needed
3. Follow the existing structure for consistency

