#!/bin/bash

# Database Setup Script for RM Brain Services
# This script creates all PostgreSQL databases and initializes schemas
# Run this before starting services with: dapr run -f dapr.yaml

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Database configuration
DB_USER="${POSTGRES_USER:-postgres}"
DB_PASSWORD="${POSTGRES_PASSWORD:-postgres}"
DB_HOST="${POSTGRES_HOST:-localhost}"
DB_PORT="${POSTGRES_PORT:-5432}"

# Export for psql
export PGPASSWORD="$DB_PASSWORD"

echo -e "${GREEN}=== RM Brain Database Setup ===${NC}"
echo "PostgreSQL Host: $DB_HOST:$DB_PORT"
echo "PostgreSQL User: $DB_USER"
echo ""

# Function to create database if it doesn't exist
create_database() {
    local db_name=$1
    echo -e "${YELLOW}Creating database: $db_name${NC}"
    
    if psql -h "$DB_HOST" -p "$DB_PORT" -U "$DB_USER" -lqt | cut -d \| -f 1 | grep -qw "$db_name"; then
        echo -e "  ${GREEN}✓${NC} Database '$db_name' already exists"
    else
        psql -h "$DB_HOST" -p "$DB_PORT" -U "$DB_USER" -c "CREATE DATABASE $db_name;" > /dev/null
        echo -e "  ${GREEN}✓${NC} Database '$db_name' created"
    fi
}

# Note: Database migrations are now handled by Alembic
# Run migrations using: ./scripts/run_alembic_migrations.sh upgrade head

# Get the script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

cd "$REPO_ROOT"

# 1. CAS Audit Service
echo ""
echo -e "${GREEN}=== CAS Audit Service ===${NC}"
create_database "cas_audit"
echo -e "  ${YELLOW}ℹ${NC} Run migrations: cd cas_service && uv run alembic upgrade head"

# 2. CDS Client Service
echo ""
echo -e "${GREEN}=== CDS Client Service ===${NC}"
create_database "cds_client"
echo -e "  ${YELLOW}ℹ${NC} Run migrations: cd client_service && uv run alembic upgrade head"

# 3. CDS Document Service
echo ""
echo -e "${GREEN}=== CDS Document Service ===${NC}"
create_database "cds_document"
echo -e "  ${YELLOW}ℹ${NC} Run migrations: cd document_service && uv run alembic upgrade head"

# 4. CDS Interaction Service
echo ""
echo -e "${GREEN}=== CDS Interaction Service ===${NC}"
create_database "interaction_db"
echo -e "  ${YELLOW}ℹ${NC} Run migrations: cd interaction_service && uv run alembic upgrade head"

# 5. CDS Product Service
echo ""
echo -e "${GREEN}=== CDS Product Service ===${NC}"
create_database "cds_product"
echo -e "  ${YELLOW}ℹ${NC} Run migrations: cd product_service && uv run alembic upgrade head"

# 6. CDS Relationship Service
echo ""
echo -e "${GREEN}=== CDS Relationship Service ===${NC}"
create_database "relationship_db"
echo -e "  ${YELLOW}ℹ${NC} Run migrations: cd relationship_service && uv run alembic upgrade head"

# 7. CDS Risk Profile Service
echo ""
echo -e "${GREEN}=== CDS Risk Profile Service ===${NC}"
create_database "riskprofile_db"
echo -e "  ${YELLOW}ℹ${NC} Run migrations: cd riskprofile_service && uv run alembic upgrade head"

# 8. RMBrain Main App
echo ""
echo -e "${GREEN}=== RMBrain Main App ===${NC}"
create_database "rmbrain_mainapp"
echo -e "  ${YELLOW}ℹ${NC} Run migrations: cd rmbrain-mainapp && uv run alembic upgrade head"

# 9. CDS Task Service
echo ""
echo -e "${GREEN}=== CDS Task Service ===${NC}"
create_database "cds_task"
echo -e "  ${YELLOW}ℹ${NC} Run migrations: cd task_service && uv run alembic upgrade head"

echo ""
echo -e "${GREEN}=== Database Setup Complete ===${NC}"
echo ""
echo "All databases have been created."
echo ""
echo "Next steps:"
echo "1. Run Alembic migrations for all services:"
echo "   ./scripts/run_alembic_migrations.sh upgrade head"
echo ""
echo "2. Or run migrations individually:"
echo "   cd <service> && uv run alembic upgrade head"
echo ""
echo "3. Start all services:"
echo "   dapr run -f dapr.yaml"
echo ""

