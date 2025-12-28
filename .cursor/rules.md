1️⃣ Repo structure
```text
/repo-root
│
├── rules.md                ← Cursor human-readable rules
├── rules.json              ← Cursor machine-enforced rules
│
├── dapr/
│   ├── components/         ← pubsub, state, bindings
│   ├── config/             ← tracing, metrics, resiliency
│   └── subscriptions/      ← declarative pubsub subscriptions
│
├── user-service/
├── payment-service/
└── notification-service/
... all the services
│
├── shared/
│   ├── proto/
│   ├── contracts/
│   └── utils/
│
└── infra/
    ├── k8s/
    ├── terraform/
    └── scripts/
```

# Cursor Rules – Dapr Microservices Monorepo

This repository contains multiple microservices running in a Dapr environment.
All Dapr-related configuration and patterns MUST follow the rules below.

---

## 1. Dapr Configuration Ownership

- All Dapr components (state stores, pubsub, bindings, secrets) live under:
  `/dapr/components`
- All global Dapr configuration (tracing, metrics, resiliency) lives under:
  `/dapr/config`
- All declarative pub/sub subscriptions live under:
  `/dapr/subscriptions`

❌ Services can define their own Dapr YAML files but only limited to running that single service for debugging 
❌ Services MUST NOT inline Dapr component configuration  

---

## 2. Service Responsibilities

Each service:
- Implements business logic only
- Communicates via Dapr using:
  - HTTP
  - gRPC
  - Official Dapr SDKs

Each service MUST:
- Expose a `/health` endpoint
- Use environment variables for:
  - `APP_ID`
  - `APP_PORT`
  - `DAPR_HTTP_PORT`
  - `DAPR_GRPC_PORT`

---

## 3. Sidecar Configuration

- Sidecar injection configuration belongs in infra (Kubernetes / Helm)
- Services must NEVER reference sidecar flags directly
- Use annotations only in deployment manifests

---

## 4. Pub/Sub Rules

- Topics and message contracts must be documented in `/shared/contracts`
- Subscriptions must be declared using Dapr declarative subscriptions
- No runtime subscription logic in code unless explicitly approved

---

## 5. State Management

- State store names are globally consistent
- State keys MUST be namespaced:
  `<appId>:<entity>:<id>`

---

## 6. Secrets & Credentials

- Secrets MUST be resolved via Dapr secret stores
- No plaintext secrets in code or config
- No direct access to cloud secret managers from services

---

## 7. Observability & Resilience

- Tracing MUST use the global Dapr config
- Retries, circuit breakers, and timeouts MUST use Dapr resiliency policies
- Services must not implement custom retry logic for inter-service calls

---

## 8. What Cursor Should Do

When generating or modifying code:
- Prefer Dapr SDK usage
- Reuse existing components and config
- Ask before creating new Dapr components
- Never duplicate Dapr YAMLs inside services
```