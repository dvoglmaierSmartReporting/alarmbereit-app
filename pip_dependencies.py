import argparse
import subprocess
import re


def main(package_names: str) -> None:

    if "," in package_names:
        pkgs = package_names.split(",")

    else:
        pkgs = [package_names]

    print(pkgs)
    for pkg in pkgs:

        output = subprocess.run(["pipdeptree", "-p", pkg], capture_output=True)
        stdout = output.stdout.decode("utf-8")
        print(stdout)

        lines = stdout.split("\n")

        output_str = ""

        deps = lines[1:-1]

        pattern_dep = r"[\w-]+(?=\s*\[required:)"
        pattern_version = r"installed:\s*([0-9.]+)"

        for dep in deps[::-1]:
            m = re.search(pattern_dep, dep)
            output_str += m.group() + "=="

            mv = re.search(pattern_version, dep)
            output_str += mv.group(1) + ","

        output_str += lines[0]
        print(output_str + "\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "package_names", type=str, help="package names, comma separated"
    )

    args = parser.parse_args()

    package_names = args.package_names

    main(package_names)
