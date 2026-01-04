#!/usr/bin/env python3
"""Script to update canonical dependency paths in all service pyproject.toml files.

This script resolves the absolute path to the canonical directory and updates
all service pyproject.toml files to use the correct file:// URL format.
"""

import re
from pathlib import Path

# Get repository root (parent of this script's directory)
REPO_ROOT = Path(__file__).parent.parent.resolve()
CANONICAL_PATH = REPO_ROOT / "canonical"
CANONICAL_ABS = CANONICAL_PATH.resolve()

# File URL format
CANONICAL_URL = f"file://{CANONICAL_ABS}"

# Services to update
SERVICES = [
    "client_service",
    "task_service",
    "document_service",
    "interaction_service",
    "relationship_service",
    "product_service",
    "riskprofile_service",
    "cas_service",
    "policy_service",
    "bff_service",
    "rmbrain-mainapp",
]


def update_pyproject_toml(service_path: Path):
    """Update pyproject.toml with correct canonical path."""
    pyproject_path = service_path / "pyproject.toml"
    
    if not pyproject_path.exists():
        print(f"⚠️  {service_path.name}: pyproject.toml not found")
        return False
    
    content = pyproject_path.read_text()
    
    # Pattern to match canonical dependency line
    pattern = r'("canonical @ )[^"]+(")'
    replacement = f'\\g<1>{CANONICAL_URL}\\g<2>'
    
    new_content = re.sub(pattern, replacement, content)
    
    if new_content != content:
        pyproject_path.write_text(new_content)
        print(f"✅ {service_path.name}: Updated canonical path")
        return True
    else:
        print(f"ℹ️  {service_path.name}: No changes needed")
        return False


def main():
    """Update all service pyproject.toml files."""
    print(f"Repository root: {REPO_ROOT}")
    print(f"Canonical path: {CANONICAL_ABS}")
    print(f"Canonical URL: {CANONICAL_URL}")
    print()
    
    updated_count = 0
    for service_name in SERVICES:
        service_path = REPO_ROOT / service_name
        if service_path.exists():
            if update_pyproject_toml(service_path):
                updated_count += 1
        else:
            print(f"⚠️  {service_name}: Directory not found")
    
    print()
    print(f"✅ Updated {updated_count} service(s)")


if __name__ == "__main__":
    main()
