#!/usr/bin/env python3
import os
import ast
import sys
from pathlib import Path
from typing import Set


def extract_imports_from_file(file_path: str) -> Set[str]:
    """Extract all import statements from a Python file."""
    imports = set()

    try:
        with open(file_path, "r", encoding="utf-8") as file:
            content = file.read()

        # Parse the Python file into an AST
        tree = ast.parse(content)

        # Walk through all nodes in the AST
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                # Handle 'import module' statements
                for alias in node.names:
                    imports.add(alias.name)
            elif isinstance(node, ast.ImportFrom):
                # Handle 'from module import ...' statements
                if node.module:
                    imports.add(node.module)

    except (SyntaxError, UnicodeDecodeError, FileNotFoundError) as e:
        print(f"Error parsing {file_path}: {e}", file=sys.stderr)

    return imports


def find_all_python_files(root_dir: str) -> list:
    """Find all Python files in the directory tree."""
    python_files = []

    for root, dirs, files in os.walk(root_dir):
        # Skip common non-source directories
        dirs[:] = [
            d
            for d in dirs
            if d not in {".git", "__pycache__", ".pytest_cache", "venv", "env", ".venv"}
        ]

        for file in files:
            if file.endswith(".py"):
                python_files.append(os.path.join(root, file))

    return python_files


def main():
    # Get the current directory or use command line argument
    if len(sys.argv) > 1:
        project_root = sys.argv[1]
    else:
        project_root = os.getcwd()

    if not os.path.exists(project_root):
        print(f"Error: Directory '{project_root}' does not exist.", file=sys.stderr)
        sys.exit(1)

    print(f"Scanning Python files in: {project_root}", file=sys.stderr)
    print("=" * 50, file=sys.stderr)

    # Find all Python files
    python_files = find_all_python_files(project_root)
    print(f"Found {len(python_files)} Python files", file=sys.stderr)
    print("=" * 50, file=sys.stderr)

    # Collect all unique imports
    all_imports = set()

    for file_path in python_files:
        file_imports = extract_imports_from_file(file_path)
        all_imports.update(file_imports)

    # Sort and output unique imports
    sorted_imports = sorted(all_imports)

    print("Unique imports found:")
    print("=" * 20)
    for import_name in sorted_imports:
        print(import_name)

    print(f"\nTotal unique imports: {len(sorted_imports)}")


if __name__ == "__main__":
    main()
