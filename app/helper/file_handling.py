from kivy.app import App

from helper.settings import Strings

import yaml
from shutil import copyfile
import os

strings = Strings()


def load_yaml_and_handle_error(file_path: str) -> dict:
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


def save_to_yaml_and_handle_error(file_path: str, content: dict) -> None:
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


def load_total_storage() -> dict:
    default_file_path = (
        "/".join(__file__.split("/")[:-2]) + "/content/firetruck_tools.yaml"
    )
    file_path = default_file_path

    custom_file_path = os.path.join(
        App.get_running_app().user_data_dir,  # type:ignore
        "custom_firetruck_tools.yaml",
    )
    custom_file_exists = os.path.exists(custom_file_path)

    # main.cfg is source-of-truth for firetruck content and scores
    config = read_main_cfg()
    if (
        not config.get("content").get("use_default")  # type:ignore
        and custom_file_exists
    ):

        file_path = custom_file_path

    return load_yaml_and_handle_error(file_path)


def load_total_competition_questions() -> dict:
    file_path = (
        "/".join(__file__.split("/")[:-2])
        + "/content/competition_questions_multiple_choice.yaml"
    )

    return load_yaml_and_handle_error(file_path)


def copy_file_to_writable_dir(file_path: str, file_name: str, new_file_name: str = ""):
    file_current_dir = os.path.dirname(os.path.abspath(__file__))
    file_relative_path = os.path.join(file_current_dir, file_path, file_name)
    src = os.path.normpath(file_relative_path)

    # at default keep file name
    if new_file_name == "":
        new_file_name = file_name

    dst = os.path.join(
        App.get_running_app().user_data_dir,  # type:ignore
        new_file_name,
    )

    # if not os.path.exists(dst):
    #     copyfile(src, dst)
    print(f"{dst = }")
    copyfile(src, dst)


def read_scores_file():
    scores_file_path = os.path.join(
        App.get_running_app().user_data_dir,  # type:ignore
        "scores.yaml",
    )
    file_path = scores_file_path

    custom_scores_file_path = os.path.join(
        App.get_running_app().user_data_dir,  # type:ignore
        "custom_scores.yaml",
    )
    custom_scores_exists = os.path.exists(custom_scores_file_path)

    config = read_main_cfg()

    if (
        not config.get("content").get("use_default")  # type:ignore
        and custom_scores_exists
    ):
        file_path = custom_scores_file_path

    return load_yaml_and_handle_error(file_path)


def get_scores_key(firetruck: str, key: str, questions: str = "firetrucks"):
    return read_scores_file().get(questions).get(firetruck).get(key)  # type:ignore


def save_to_scores_file(
    firetruck: str, key: str, value: int, questions: str = "firetrucks"
):
    content = read_scores_file()

    if not questions in content.keys():
        raise ValueError(f"Questions {questions} not found in scores.yaml")

    if not firetruck in content.get(questions).keys():  # type:ignore
        raise ValueError(
            f"Firetruck {firetruck} not found in scores.yaml > {questions}"
        )

    if not key in content.get(questions).get(firetruck).keys():  # type:ignore
        raise ValueError(
            f"Key {key} not found in scores.yaml > {questions} > {firetruck}"
        )

    content[questions][firetruck][key] = value

    #
    # competition scores are to be added in both scores files (if custom exists)
    # because this allows to have 2 scores files instead of 4
    #
    # for saving firetruck scores and strikes,
    # main.cfg is source-of-truth for firetruck content and scores
    #
    scores_file_path = os.path.join(
        App.get_running_app().user_data_dir,  # type:ignore
        "scores.yaml",
    )
    custom_scores_file_path = os.path.join(
        App.get_running_app().user_data_dir,  # type:ignore
        "custom_scores.yaml",
    )
    custom_scores_exists = os.path.exists(custom_scores_file_path)
    print(f'{custom_scores_exists = }')

    file_paths = [scores_file_path]

    config = read_main_cfg()

    # overwrite and only update custom firetruck scores
    # it's assumed the file was already created
    if (
        questions == "firetrucks"
        and not config.get("content").get(  # type:ignore
            "use_default"
        )
        and custom_scores_exists
    ):
        file_paths = [custom_scores_file_path]

    # update both scores files' competitions high scores
    elif questions == "competitions" and custom_scores_exists:
        file_paths.append(custom_scores_file_path)
    
    print(f'save-to-scores-file {file_paths = }')
    print(f'{content = }')

    for file_path in file_paths:
        save_to_yaml_and_handle_error(file_path, content)


def read_main_cfg() -> dict:
    file_path = os.path.join(
        App.get_running_app().user_data_dir,  # type:ignore
        "main.cfg",
    )

    return load_yaml_and_handle_error(file_path)


def update_main_cfg(to_update: dict):
    content = read_main_cfg()

    content.update(to_update)

    file_path = os.path.join(
        App.get_running_app().user_data_dir,  # type:ignore
        "main.cfg",
    )

    save_to_yaml_and_handle_error(file_path, content)
