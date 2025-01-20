from kivy.app import App

from helper.settings import Strings

import yaml
from shutil import copyfile
import os

strings = Strings()


def load_total_storage(
    file_path: str = "/".join(__file__.split("/")[:-2])
    + "/content/feuerwehr_tools_storage.yaml",
) -> dict:
    with open(
        file_path,
        "r",
    ) as file:
        try:
            return yaml.safe_load(file)
        except yaml.YAMLError as exc:
            print(exc)
            return dict()
        # except FileNotFoundError:
        #     print(f"Error: File at {file_path} not found.")
        # except yaml.YAMLError as e:
        #     print(f"Error: Failed to parse YAML file at {file_path}. Details: {e}")
        # except Exception as e:
        #     print(f"An unexpected error occurred: {e}")


def load_total_competition_questions(
    file_path: str = "/".join(__file__.split("/")[:-2])
    + "/content/feuerwehr_competition_questions_multiple_choice.yaml",
) -> dict:
    # with open("./app/content/feuerwehr_competition_questions.yaml", "r") as file:
    with open(
        file_path,
        "r",
    ) as file:
        try:
            return yaml.safe_load(file)
        except yaml.YAMLError as exc:
            print(exc)
            return dict()
        # except FileNotFoundError:
        #     print(f"Error: File at {file_path} not found.")
        # except yaml.YAMLError as e:
        #     print(f"Error: Failed to parse YAML file at {file_path}. Details: {e}")
        # except Exception as e:
        #     print(f"An unexpected error occurred: {e}")


def copy_file_to_writable_dir(file_path: str, file_name: str):
    file_current_dir = os.path.dirname(os.path.abspath(__file__))
    file_relative_path = os.path.join(file_current_dir, file_path, file_name)
    src = os.path.normpath(file_relative_path)
    dst = os.path.join(
        App.get_running_app().user_data_dir, file_name  # type:ignore
    )

    # if not os.path.exists(dst):
    #     copyfile(src, dst)
    print(f"{dst = }")
    copyfile(src, dst)


def read_scores_file(
    file_path: str = os.path.join(
        App.get_running_app().user_data_dir, "scores.yaml"  # type:ignore
    )
):
    try:
        with open(
            file_path,
            "r",
        ) as file:
            return yaml.safe_load(file)

    except Exception as e:
        print(f"Error reading file: {e}")
        return dict()
    # except FileNotFoundError:
    #     print(f"Error: File at {file_path} not found.")
    # except yaml.YAMLError as e:
    #     print(f"Error: Failed to parse YAML file at {file_path}. Details: {e}")
    # except Exception as e:
    #     print(f"An unexpected error occurred: {e}")


def get_scores_file_key(firetruck: str, key: str, questions: str = "firetrucks"):
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

    try:
        with open(
            os.path.join(
                App.get_running_app().user_data_dir, "scores.yaml"  # type:ignore
            ),
            "w",
        ) as file:
            yaml.dump(content, file)
    except Exception as e:
        print(f"Error writing to file: {e}")
    # except FileNotFoundError:
    #     print(f"Error: File at {file_path} not found.")
    # except yaml.YAMLError as e:
    #     print(f"Error: Failed to parse YAML file at {file_path}. Details: {e}")
    # except Exception as e:
    #     print(f"An unexpected error occurred: {e}")
