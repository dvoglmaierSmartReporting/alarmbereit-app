from kivy.app import App
from kivy.config import Config
from kivy.resources import resource_find

import yaml
from shutil import copyfile
import os
from typing import cast

from helper.strings import Strings
from helper.custom_types import *

strings = Strings()


def load_from_txt(file_path: str) -> str:
    try:
        with open(file_path, "r") as file:
            return file.read()
    except Exception as e:
        print(f"Error reading file: {e}")
        print(f"{file_path = }")
        return ""
    # except FileNotFoundError:
    #     print(f"Error: File at {file_path} not found.")
    # except Exception as e:
    #     print(f"An unexpected error occurred: {e}")


def load_app_version() -> str:
    file_path = "/".join(__file__.split("/")[:-2]) + "/app-version"
    try:
        return load_from_txt(file_path).strip()
    except:
        return "0.0.0"


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


class NoAliasDumper(yaml.SafeDumper):
    def ignore_aliases(self, data):
        return True


def save_to_yaml(file_path: str, content: dict) -> None:
    try:
        with open(file_path, "w") as file:
            yaml.dump(content, file, Dumper=NoAliasDumper)
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
        content_file = "firetruck_tools_hallein.yaml"
    elif selected_city == "Bad Dürrnberg":
        content_file = "firetruck_tools_duerrnberg.yaml"
    elif selected_city == "Altenmarkt a.d. Alz":
        content_file = "firetruck_tools_altenmarkt.yaml"

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


def map_selected_city_2short_name(selected_city_long_name: str) -> str:
    if selected_city_long_name in ["Bad Dürrnberg"]:
        return "Dürrnberg"
    elif selected_city_long_name in [
        "Altenmarkt a.d. Alz",
        "Altenmarkt ad Alz",
        "Altenmarkt Alz",
    ]:
        return "Altenmarkt"
    elif selected_city_long_name in ["Stadt Hallein"]:
        return "Hallein"

    return selected_city_long_name


def map_selected_city_2long_name(selected_city_short_name: str) -> str:
    if "Hallein" in selected_city_short_name:
        return "Hallein"
    elif "Dürrnberg" in selected_city_short_name:
        return "Bad Dürrnberg"
    elif "Altenmarkt" in selected_city_short_name:
        return "Altenmarkt a.d. Alz"

    return selected_city_short_name


def get_logo_file_path(selected_long_name: str) -> str:
    # city logos
    if selected_long_name == "Hallein":
        return "assets/FFH_Logohalter.png"
    if selected_long_name == "Dürrnberg":
        return "assets/LZ_Logohalter.png"
    if selected_long_name == "Altenmarkt":
        return "assets/altenmarkt.png"

    # state logos
    if selected_long_name in ["Salzburg", "Bayern"]:
        return "assets/lfv_salzburg.png"

    # default
    return "assets/FFH_Logohalter.png"


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


def update_config(to_update: dict, section: str) -> None:
    # make sure the content section exists
    if not Config.has_section(section):
        Config.add_section(section)

    for key, value in to_update.items():
        Config.set(section, key, value)
    Config.write()


def update_config_content(to_update: dict) -> None:
    update_config(to_update, "content")


def get_selected_city_state() -> tuple[str, str]:
    return Config.get("content", "city"), Config.get("content", "state")


def update_config_firetruck(to_update: dict) -> None:
    update_config(to_update, "firetruck")


def get_selected_mode() -> str:
    section = "firetruck"
    if not Config.has_section(section):
        raise ValueError(f"Config section '{section}' does not exist.")
    if not Config.has_option(section, "mode"):
        raise ValueError(f"Config option 'mode' does not exist in section '{section}'.")
    return Config.get(section, "mode")


def get_selected_firetruck() -> str:
    section = "firetruck"
    if not Config.has_section(section):
        raise ValueError(f"Config section '{section}' does not exist.")
    if not Config.has_option(section, "selected_firetruck"):
        raise ValueError(
            f"Config option 'selected_firetruck' does not exist in section '{section}'."
        )
    return Config.get(section, "selected_firetruck")


def image_file_exists(file_name: str) -> bool:
    # Example: file_name = "assets/images/myicon.png"
    path = resource_find(file_name)
    return path is not None and os.path.isfile(path)


def tool_image_file_exists(image_name: str) -> bool:
    return image_file_exists(image_name)


def room_image_file_exists(
    selected_city: str, selected_firetruck: str, image_name: str
) -> bool:
    if selected_city == "Hallein":
        city = "hallein"
    elif selected_city == "Bad Dürrnberg":
        city = "duerrnberg"
    elif selected_city == "Altenmarkt a.d. Alz":
        city = "altenmarkt"

    if selected_firetruck == "RüstLösch":
        firetruck = "rl"
    elif selected_firetruck == "Rüst":
        firetruck = "r"
    elif selected_firetruck == "Tank1":
        firetruck = "t1"
    elif selected_firetruck == "Tank2":
        firetruck = "t2"
    elif selected_firetruck == "Voraus":
        firetruck = "v"
    elif selected_firetruck == "Leiter":
        firetruck = "l"
    elif selected_firetruck == "Pumpe":
        firetruck = "p"
    elif selected_firetruck == "Tank":
        firetruck = "t"
    elif selected_firetruck == "LF8":
        firetruck = "lf8"
    elif selected_firetruck == "LF20":
        firetruck = "lf20"
    else:
        firetruck = "rl"

    room_image_file_name = f"{city}_{firetruck}/{image_name}"
    return image_file_exists(room_image_file_name)


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

    if not os.path.exists(dst):
        copy_file_to_writable_dir(file_path, file_name, new_file_name)

    else:
        existing_content = load_from_yaml(dst)
        new_content = load_from_yaml(src)

        if file_name == "scores.yaml":
            # Migration 2.3.2 -> 2.4.0
            # up to 2.3.2: no multi-tenancy available
            if (
                "competitions" in existing_content.keys()
                and "firetrucks" in existing_content.keys()
            ):
                updated_content = migrate_to_2_4_0(existing_content, new_content)

            else:
                updated_content = update_yaml_values(existing_content, new_content)

        # elif file_name == "main.cfg":
        #     updated_content = update_yaml_values(existing_content, new_content)

        save_to_yaml(dst, updated_content)


def migrate_to_2_4_0(existing_content: dict, new_content: dict) -> dict:
    for key, values in existing_content.items():
        if key == "competitions":
            # competitions scores are conserved no matter which city is selected
            new_content["Hallein"]["competitions"].update(values)
            new_content["Dürrnberg"]["competitions"].update(values)
            new_content["Altenmarkt"]["competitions"].update(values)

        elif key == "firetrucks":
            for truck, score in values.items():
                if truck in [
                    "Leiter",
                    "Pumpe",
                    "Rüst",
                    "RüstLösch",
                    "Tank1",
                    "Tank2",
                    "Voraus",
                ]:
                    # new_content["Hallein"]["firetrucks"][truck].update(deepcopy(score))
                    new_content["Hallein"]["firetrucks"][truck].update(score)

                elif truck == "PumpeDürrnberg":
                    new_content["Dürrnberg"]["firetrucks"]["Pumpe"].update(score)
                elif truck == "TankDürrnberg":
                    new_content["Dürrnberg"]["firetrucks"]["Tank"].update(score)

    return new_content


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
