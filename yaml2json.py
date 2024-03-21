#!/usr/bin/env python3

import yaml
import json


def yaml_to_json(source_file_path: str, function_name: str) -> str:

    # choose indent tabs
    ind = 1

    with open(source_file_path, "r") as f:
        try:
            parsed_yaml = yaml.safe_load(f)

            json_output = json.dumps(parsed_yaml, ensure_ascii=False, indent=4)

        except yaml.YAMLError as e:
            print(e)

    # manipulate indent of each line of dict
    indented_json_output = "\n".join(
        " " * 4 * ind + line for line in json_output.splitlines()[1:]
    )

    # assemble python function as string
    output = f"{' ' * 4 * (ind - 1)}def {function_name}():\n{' ' * 4 * ind}return {{\n"
    output += indented_json_output

    return output


def main() -> None:
    with open("./app/helper/firetrucks.py", "w") as f:
        # todo: validate input data!
        f.write(yaml_to_json("./feuerwehr_tools_storage.yaml", "load_total_storage"))

    with open("./app/helper/competitions.py", "w") as f:
        # todo: validate input data!
        f.write(
            yaml_to_json(
                "./feuerwehr_competition_questions.yaml", "load_total_competition_questions"
            )
        )


if __name__ == "__main__":
    main()
