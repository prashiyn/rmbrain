# Install all at once
for dir in bff_service cas_service client_service document_service interaction_service policy_service product_service relationship_service riskprofile_service rmbrain-mainapp task_service; do
  echo "Installing dependencies in $dir"
  (cd "$dir" && uv sync)
done