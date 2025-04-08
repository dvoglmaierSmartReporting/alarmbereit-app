import sys
import os
import re

try:
    # [Your update logic here...]
    # For example:
    if not os.path.exists("app/app-version"):
        raise FileNotFoundError("Missing app-version file")

    # Read version from the source-of-truth file
    with open("app/app-version", "r") as f:
        new_version = f.read().strip()

    # --- Update buildozer.spec ---
    spec_file = "app/buildozer.spec"
    with open(spec_file, "r") as f:
        spec_lines = f.readlines()

    with open(spec_file, "w") as f:
        for line in spec_lines:
            if line.startswith("version ="):
                f.write(f"version = {new_version}\n")
            else:
                f.write(line)

    # --- Update feuerwehr.kv ---
    kv_file = "app/feuerwehr.kv"
    with open(kv_file, "r") as f:
        kv_content = f.read()

    # Replace the version label text line
    kv_content = re.sub(
        r'text:\s*"Version\s+[0-9]+\.[0-9]+\.[0-9]+"',
        f'text: "Version {new_version}"',
        kv_content,
    )

    with open(kv_file, "w") as f:
        f.write(kv_content)

    print(f"Updated version to {new_version} in buildozer.spec and feuerwehr.kv")
except Exception as e:
    print(f"Error: {e}", file=sys.stderr)
    sys.exit(1)

sys.exit(0)
