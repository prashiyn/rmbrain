# Canonical Schemas Documentation Links

## Summary

Symbolic links have been created in all service `docs/` folders to provide easy access to the `canonical_schemas` package documentation.

## Links Created

Each service's `docs/` folder now contains two symbolic links:

1. **`canonical_schemas_README.md`** → Points to `../../canonical_schemas/README.md`
2. **`canonical_schemas_USAGE_EXAMPLES.md`** → Points to `../../canonical_schemas/USAGE_EXAMPLES.md`

## Services with Links

All 11 services now have these documentation links:

1. ✅ `task_service/docs/`
2. ✅ `bff_service/docs/`
3. ✅ `policy_service/docs/`
4. ✅ `relationship_service/docs/`
5. ✅ `interaction_service/docs/`
6. ✅ `client_service/docs/`
7. ✅ `document_service/docs/`
8. ✅ `product_service/docs/`
9. ✅ `riskprofile_service/docs/`
10. ✅ `cas_service/docs/`
11. ✅ `rmbrain-mainapp/docs/`

## Usage

From any service's `docs/` folder, you can now access:

```bash
# View the README
cat canonical_schemas_README.md

# View usage examples
cat canonical_schemas_USAGE_EXAMPLES.md

# Or open in your editor
code canonical_schemas_README.md
```

## Link Structure

```
<service>/docs/
├── canonical_schemas_README.md -> ../../canonical_schemas/README.md
└── canonical_schemas_USAGE_EXAMPLES.md -> ../../canonical_schemas/USAGE_EXAMPLES.md
```

## Benefits

1. **Easy Access**: Documentation is accessible from each service's docs folder
2. **Single Source**: All links point to the same source files (no duplication)
3. **Auto-Update**: When canonical_schemas documentation is updated, all links automatically reflect changes
4. **IDE Support**: IDEs can follow the links to show the documentation

## Maintenance

- Links are relative, so they work regardless of absolute paths
- If the canonical_schemas package is moved, links will need to be recreated
- Links use relative paths (`../../canonical_schemas/`) for portability

---

**Status**: ✅ **COMPLETE**
**Date**: Links created
**Services**: 11 services with documentation links
