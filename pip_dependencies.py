#!/usr/bin/env python3

import argparse
import subprocess
import re
import os
import sys


def main(package_names: str) -> None:

    if "," in package_names:
        pkgs = package_names.split(",")

    else:
        pkgs = [package_names]

    print(pkgs)

    collection = dict()
    conflicts = dict()

    for pkg in pkgs:

        output = subprocess.run(["pipdeptree", "-p", pkg], capture_output=True)
        stdout = output.stdout.decode("utf-8")
        print(stdout)

        lines = stdout.split("\n")

        deps = lines[1:-1]
        deps = lines[:-1]

        pattern_dep = r"[\w-]+(?=\s*\[required:)"
        pattern_version = r"installed:\s*([0-9.]+)"

        for dep in deps[::-1]:
            if "==" in dep:
                dep_name, dep_version = dep.split("==")

            else:
                dep_name_regex = re.search(pattern_dep, dep)
                dep_name = dep_name_regex.group()

                dep_version_regex = re.search(pattern_version, dep)
                dep_version = dep_version_regex.group(1)

            if dep_name not in collection.keys():
                collection[dep_name] = dep_version
            else:
                existing_version = collection[dep_name]
                if existing_version != dep_version:
                    conflicts[dep_name] = (existing_version, dep_version)

    if conflicts:
        print("Conflicts detected:")
        for dep_name, versions in conflicts.items():
            print(f"{dep_name}: {versions[0]} vs {versions[1]}")

        sys.exit(1)

    output = list()
    for dep_name, dep_version in collection.items():
        output.append(f"{dep_name}=={dep_version}")
    print(",".join(output))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "package_names", type=str, help="package names, comma separated"
    )

    args = parser.parse_args()

    package_names = args.package_names

    main(package_names)
