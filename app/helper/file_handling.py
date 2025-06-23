from kivy.app import App
from kivy.config import Config

import yaml
from shutil import copyfile
import os
from typing import cast

from helper.settings import Strings
from helper.custom_types import *

strings = Strings()


def load_from_yaml(file_path: str) -> dict:
    try:
        with open(file_path, "r") as file:
            return yaml.safe_load(file)
    except Exception as e:
        print(f"Error reading file: {e}")
        print(f"{file_path = }")
        return dict()
    # except FileNotFoundError:
    #     print(f"Error: File at {file_path} not found.")
    # except yaml.YAMLError as e:
    #     print(f"Error: Failed to parse YAML file at {file_path}. Details: {e}")
    # except Exception as e:
    #     print(f"An unexpected error occurred: {e}")


def save_to_yaml(file_path: str, content: dict) -> None:
    try:
        with open(file_path, "w") as file:
            yaml.dump(content, file)
    except Exception as e:
        print(f"Error writing to file: {e}")
        print(f"{file_path = }")
    # except FileNotFoundError:
    #     print(f"Error: File at {file_path} not found.")
    # except yaml.YAMLError as e:
    #     print(f"Error: Failed to parse YAML file at {file_path}. Details: {e}")
    # except Exception as e:
    #     print(f"An unexpected error occurred: {e}")


def get_user_data_dir() -> str:
    get_running_app = App.get_running_app()
    get_running_app = cast(App, get_running_app)
    return get_running_app.user_data_dir


def load_total_firetruck_storage(selected_city: str) -> totalStorage:
    if selected_city == "Hallein":
        content_file = "firetruck_tools_Hallein.yaml"
    elif selected_city == "Bad Dürrnberg":
        content_file = "firetruck_tools_Dürrnberg.yaml"
    elif selected_city == "Altenmarkt a.d. Alz":
        content_file = "firetruck_tools_Altenmarkt.yaml"

    file_path = "/".join(__file__.split("/")[:-2]) + "/content/" + content_file

    return load_from_yaml(file_path)


def load_bdlp_storage() -> totalStorage:
    default_file_path = "/".join(__file__.split("/")[:-2]) + "/content/bdlp_tools.yaml"
    return load_from_yaml(default_file_path)


def load_total_storage(selected_city: str) -> totalStorage:
    output = load_total_firetruck_storage(selected_city)

    # # add BDLP content for default and custom firetruck contents
    # output.update(load_bdlp_storage())
    return output


def load_total_competition_questions() -> totalQuestion:
    default_file_path = (
        "/".join(__file__.split("/")[:-2])
        + "/content/competition_questions_multiple_choice.yaml"
    )

    return load_from_yaml(default_file_path)


def copy_file_to_writable_dir(
    file_path: str, file_name: str, new_file_name: str = ""
) -> None:
    file_current_dir = os.path.dirname(os.path.abspath(__file__))
    file_relative_path = os.path.join(file_current_dir, file_path, file_name)
    src = os.path.normpath(file_relative_path)

    # at default keep file name
    if new_file_name == "":
        new_file_name = file_name

    dst = os.path.join(
        get_user_data_dir(),
        new_file_name,
    )

    # if not os.path.exists(dst):
    #     copyfile(src, dst)
    copyfile(src, dst)


def read_scores_file() -> dict:
    scores_file_path = os.path.join(
        get_user_data_dir(),
        "scores.yaml",
    )
    file_path = scores_file_path

    return load_from_yaml(file_path)


def map_selected_city_2short_name(city: str) -> str:
    if city in ["Bad Dürrnberg"]:
        return "Dürrnberg"
    elif city in ["Altenmarkt a.d. Alz", "Altenmarkt ad Alz", "Altenmarkt Alz"]:
        return "Altenmarkt"
    elif city in ["Stadt Hallein"]:
        return "Hallein"

    return city


def map_selected_city_2long_name(city: str) -> str:
    if "Hallein" in city:
        return "Hallein"
    elif "Dürrnberg" in city:
        return "Bad Dürrnberg"
    elif "Altenmarkt" in city:
        return "Altenmarkt a.d. Alz"

    return city


def get_logo_file_path(selected_city: str) -> str:
    if selected_city in ["Hallein", "Bad Dürrnberg"]:
        return "assets/FFH_Logohalter_negativ.png"
    if selected_city in ["Altenmarkt a.d. Alz"]:
        return "assets/altenmarkt.png"
    return "assets/FFH_Logohalter_negativ.png"


def get_score_value(
    city: str,
    questions: str,
    truck_or_comp: str,
    key: str,
) -> int:
    return (
        read_scores_file()
        .get(map_selected_city_2short_name(city), {})
        .get(questions, {})
        .get(truck_or_comp, {})
        .get(key, 0)
    )


def save_to_scores_file(
    city: str,
    questions: str,
    truck_or_comp: str,
    key: str,
    value: int,
) -> None:
    content = read_scores_file()

    city = map_selected_city_2short_name(city)

    if not city in content.keys():
        raise ValueError(f"City {city} not found in scores.yaml")

    if not questions in content.get(city, {}).keys():
        raise ValueError(f"Questions {questions} not found in scores.yaml > {city}")

    if not truck_or_comp in content.get(city, {}).get(questions, {}).keys():
        raise ValueError(
            f"Firetruck {truck_or_comp} not found in scores.yaml > {city} > {questions}"
        )

    if (
        not key
        in content.get(city, {}).get(questions, {}).get(truck_or_comp, {}).keys()
    ):
        raise ValueError(
            f"Key {key} not found in scores.yaml > {city} > {questions} > {truck_or_comp}"
        )

    content[city][questions][truck_or_comp][key] = value

    scores_file_path = os.path.join(
        get_user_data_dir(),
        "scores.yaml",
    )
    save_to_yaml(scores_file_path, content)


def update_main_cfg(to_update: dict) -> None:
    for key, value in to_update.items():
        Config.set("content", key, value)
    Config.write()


def get_selected_city_state() -> tuple[str, str]:
    return Config.get("content", "city"), Config.get("content", "state")


def transfer_file(file_path: str, file_name: str, new_file_name: str = "") -> None:
    file_current_dir = os.path.dirname(os.path.abspath(__file__))
    file_relative_path = os.path.join(file_current_dir, file_path, file_name)
    src = os.path.normpath(file_relative_path)

    if new_file_name == "":
        new_file_name = file_name

    dst = os.path.join(
        get_user_data_dir(),
        new_file_name,
    )
    dst_file_exists = os.path.exists(dst)

    if not dst_file_exists:
        copy_file_to_writable_dir(file_path, file_name, new_file_name)

    else:
        existing_content = load_from_yaml(dst)
        new_content = load_from_yaml(src)

        updated_content = update_yaml_values(existing_content, new_content)

        save_to_yaml(dst, updated_content)


def update_yaml_values(source_yaml: dict, target_yaml: dict) -> dict:
    if not isinstance(source_yaml, dict) or not isinstance(target_yaml, dict):
        return target_yaml

    for key, value in source_yaml.items():
        if key in target_yaml:
            if isinstance(value, dict) and isinstance(target_yaml[key], dict):
                update_yaml_values(value, target_yaml[key])
            else:
                target_yaml[key] = value

    return target_yaml
