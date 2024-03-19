import yaml
import json


def yaml_to_json():

    # choose indent tabs
    ind = 1

    with open("feuerwehr_tools_storage.yaml", "r") as f:
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
    output = (
        " " * 4 * (ind - 1)
        + "def load_total_storage():\n"
        + " " * 4 * ind
        + "total_storage = {\n"
    )
    output += indented_json_output
    output += "\n\n" + " " * 4 * ind + "return total_storage"

    return output


if __name__ == "__main__":

    print(yaml_to_json())
