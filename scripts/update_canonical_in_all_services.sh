#!/bin/bash
# Update canonical package in all services

REPO_ROOT="/media/prashanth/extmnt1/rmbrain"
SERVICES=(
    "task_service"
    "bff_service"
    "policy_service"
    "relationship_service"
    "interaction_service"
    "client_service"
    "document_service"
    "product_service"
    "riskprofile_service"
    "cas_service"
    "rmbrain-mainapp"
)

echo "🔄 Updating canonical package in all services..."
echo ""

for service in "${SERVICES[@]}"; do
    SERVICE_PATH="$REPO_ROOT/$service"
    
    if [ ! -d "$SERVICE_PATH" ]; then
        echo "⚠️  Skipping $service (directory not found)"
        continue
    fi
    
    echo "📦 Updating $service..."
    cd "$SERVICE_PATH" || continue
    
    # Run uv sync to refresh dependencies
    if uv sync > /dev/null 2>&1; then
        echo "   ✓ $service updated successfully"
    else
        echo "   ✗ Failed to update $service"
    fi
done

echo ""
echo "✅ Update complete!"
echo ""
echo "To verify, test loading events from any service:"
echo "  cd task_service && python -c \"from canonical import list_events; print('Events:', len(list_events()))\""
