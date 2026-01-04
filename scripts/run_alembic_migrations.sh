#!/bin/bash
# Alembic Migration Runner
# This script runs Alembic migrations for all services

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Get script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

cd "$REPO_ROOT"

# Function to run Alembic migration
run_alembic() {
    local service_dir=$1
    local service_name=$2
    local command=$3

    if [ ! -d "$service_dir" ]; then
        echo -e "  ${YELLOW}⚠${NC} Service directory not found: $service_dir"
        return 1
    fi

    if [ ! -f "$service_dir/alembic.ini" ]; then
        echo -e "  ${YELLOW}⚠${NC} Alembic not configured: $service_dir"
        return 1
    fi

    echo -e "  ${BLUE}Running:${NC} alembic $command"
    cd "$service_dir"
    
    if uv run alembic $command 2>&1; then
        echo -e "  ${GREEN}✓${NC} Completed successfully"
        cd "$REPO_ROOT"
        return 0
    else
        echo -e "  ${RED}✗${NC} Failed"
        cd "$REPO_ROOT"
        return 1
    fi
}

# Main execution
COMMAND="${1:-upgrade head}"

echo -e "${BLUE}=== Alembic Migration Runner ===${NC}"
echo ""
echo -e "Command: ${GREEN}alembic $COMMAND${NC}"
echo ""

# Services with databases
SERVICES=(
    "client_service:cds-client"
    "task_service:cds-task"
    "document_service:cds-document"
    "interaction_service:cds-interaction"
    "product_service:cds-product"
    "relationship_service:cds-relationship"
    "riskprofile_service:cds-riskprofile"
    "cas_service:cas-audit"
    "rmbrain-mainapp:rmbrain-mainapp"
)

SUCCESS_COUNT=0
FAIL_COUNT=0

for service_entry in "${SERVICES[@]}"; do
    IFS=':' read -r service_dir service_name <<< "$service_entry"
    echo -e "${GREEN}=== $service_name ===${NC}"
    
    if run_alembic "$service_dir" "$service_name" "$COMMAND"; then
        ((SUCCESS_COUNT++))
    else
        ((FAIL_COUNT++))
    fi
    echo ""
done

echo -e "${BLUE}=== Summary ===${NC}"
echo -e "  ${GREEN}✓${NC} Successful: $SUCCESS_COUNT"
if [ $FAIL_COUNT -gt 0 ]; then
    echo -e "  ${RED}✗${NC} Failed: $FAIL_COUNT"
fi

exit $FAIL_COUNT
