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

# Function to run SQL migration file
run_sql_migration() {
    local service_name=$1
    local db_name=$2
    local migration_file=$3
    
    if [ -f "$migration_file" ]; then
        echo -e "${YELLOW}Running migration: $migration_file${NC}"
        psql -h "$DB_HOST" -p "$DB_PORT" -U "$DB_USER" -d "$db_name" -f "$migration_file" > /dev/null
        echo -e "  ${GREEN}✓${NC} Migration applied"
    else
        echo -e "  ${YELLOW}⚠${NC} Migration file not found: $migration_file"
    fi
}

# Function to run Python init script
run_python_init() {
    local service_dir=$1
    local script_path=$2
    
    if [ -f "$script_path" ]; then
        echo -e "${YELLOW}Running Python init: $script_path${NC}"
        cd "$service_dir"
        uv run python "$script_path" 2>&1 | grep -v "^$" || true
        cd - > /dev/null
        echo -e "  ${GREEN}✓${NC} Python init completed"
    else
        echo -e "  ${YELLOW}⚠${NC} Python init script not found: $script_path"
    fi
}

# Get the script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

cd "$REPO_ROOT"

# 1. CAS Audit Service
echo ""
echo -e "${GREEN}=== CAS Audit Service ===${NC}"
create_database "cas_audit"
run_python_init "cas_service" "scripts/init_db.py"

# 2. CDS Client Service
echo ""
echo -e "${GREEN}=== CDS Client Service ===${NC}"
create_database "cds_client"
run_sql_migration "client_service" "cds_client" "client_service/migrations/init.sql"

# 3. CDS Document Service
echo ""
echo -e "${GREEN}=== CDS Document Service ===${NC}"
create_database "cds_document"
run_sql_migration "document_service" "cds_document" "document_service/migrations/init.sql"

# 4. CDS Interaction Service
echo ""
echo -e "${GREEN}=== CDS Interaction Service ===${NC}"
create_database "interaction_db"
echo -e "  ${YELLOW}ℹ${NC} Schema will be auto-created on service startup (SQLAlchemy)"

# 5. CDS Product Service
echo ""
echo -e "${GREEN}=== CDS Product Service ===${NC}"
create_database "cds_product"
echo -e "  ${YELLOW}ℹ${NC} Schema will be auto-created on service startup (SQLAlchemy)"

# 6. CDS Relationship Service
echo ""
echo -e "${GREEN}=== CDS Relationship Service ===${NC}"
create_database "relationship_db"
echo -e "  ${YELLOW}ℹ${NC} Schema will be auto-created on service startup (SQLAlchemy)"

# 7. CDS Risk Profile Service
echo ""
echo -e "${GREEN}=== CDS Risk Profile Service ===${NC}"
create_database "riskprofile_db"
echo -e "  ${YELLOW}ℹ${NC} Schema will be auto-created on service startup (SQLAlchemy)"

# 8. RMBrain Main App
echo ""
echo -e "${GREEN}=== RMBrain Main App ===${NC}"
create_database "rmbrain_mainapp"
echo -e "  ${YELLOW}ℹ${NC} Schema will be auto-created on service startup (SQLAlchemy)"

# 9. CDS Task Service
echo ""
echo -e "${GREEN}=== CDS Task Service ===${NC}"
create_database "cds_task"
run_sql_migration "task_service" "cds_task" "task_service/migrations/init.sql"

echo ""
echo -e "${GREEN}=== Database Setup Complete ===${NC}"
echo ""
echo "All databases have been created. Services will auto-create tables on first startup"
echo "if they use SQLAlchemy's create_all() method."
echo ""
echo "To start all services, run:"
echo "  dapr run -f dapr.yaml"
echo ""

