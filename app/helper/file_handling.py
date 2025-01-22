from kivy.app import App

from helper.settings import Strings

import yaml
from shutil import copyfile
import os

strings = Strings()


def load_total_storage() -> dict:
    # main.cfg is source-of-truth for firetruck content and scores
    config = read_main_cfg()
    if config.get("content").get("use_default"):  # type:ignore
        file_path = "/".join(__file__.split("/")[:-2]) + "/content/firetruck_tools.yaml"
    else:
        file_path = os.path.join(
            App.get_running_app().user_data_dir,  # type:ignore
            "custom_firetruck_tools.yaml",
        )

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
    + "/content/competition_questions_multiple_choice.yaml",
) -> dict:
    # with open("./app/content/competition_questions.yaml", "r") as file:
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


# # def read_scores_file(file_path: str = ""):
# def read_scores_file():
#     # main.cfg is source-of-truth for firetruck content and scores
#     config = read_main_cfg()
#     if config.get("content").get("use_default"):  # type:ignore
#         file_path = os.path.join(
#             App.get_running_app().user_data_dir,  # type:ignore
#             "scores.yaml",
#         )
#     else:
#         file_path = os.path.join(
#             App.get_running_app().user_data_dir,  # type:ignore
#             "custom_scores.yaml",
#         )

#     # # avoiding .user_data_dir in default
#     # if file_path == "":
#     #     file_path = os.path.join(
#     #         App.get_running_app().user_data_dir, "scores.yaml"  # type:ignore
#     #     )

#     try:
#         with open(
#             file_path,
#             "r",
#         ) as file:
#             return yaml.safe_load(file)

#     except Exception as e:
#         print(f"Error reading file: {e}")
#         return dict()
#     # except FileNotFoundError:
#     #     print(f"Error: File at {file_path} not found.")
#     # except yaml.YAMLError as e:
#     #     print(f"Error: Failed to parse YAML file at {file_path}. Details: {e}")
#     # except Exception as e:
#     #     print(f"An unexpected error occurred: {e}")


def read_scores_file():
    config = read_main_cfg()
    file_path_default = os.path.join(
        App.get_running_app().user_data_dir,  # type:ignore
        "scores.yaml",
    )
    file_path_custom = os.path.join(
        App.get_running_app().user_data_dir,  # type:ignore
        "custom_scores.yaml",
    )

    if config.get("content").get("use_default"):  # type:ignore
        try:
            with open(
                file_path_default,
                "r",
            ) as file:
                # return default scores.yaml
                return yaml.safe_load(file)

        except Exception as e:
            print(f"Error reading file: {e}")
            return dict()

    else:
        try:
            with open(
                file_path_default,
                "r",
            ) as file:
                default = yaml.safe_load(file)

        except Exception as e:
            print(f"Error reading file: {e}")
            return dict()

        try:
            with open(
                file_path_custom,
                "r",
            ) as file:
                custom = yaml.safe_load(file)

        except Exception as e:
            print(f"Error reading file: {e}")
            return dict()

        competitions = default.get("competitions")
        custom.update(competitions)
        return custom


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

    # main.cfg is source-of-truth for firetruck content and scores
    config = read_main_cfg()
    if config.get("content").get("use_default"):  # type:ignore
        file_path = os.path.join(
            App.get_running_app().user_data_dir,  # type:ignore
            "scores.yaml",
        )
    else:
        file_path = os.path.join(
            App.get_running_app().user_data_dir,  # type:ignore
            "custom_scores.yaml",
        )

    try:
        with open(file_path, "w") as file:
            yaml.dump(content, file)
    except Exception as e:
        print(f"Error writing to file: {e}")
    # except FileNotFoundError:
    #     print(f"Error: File at {file_path} not found.")
    # except yaml.YAMLError as e:
    #     print(f"Error: Failed to parse YAML file at {file_path}. Details: {e}")
    # except Exception as e:
    #     print(f"An unexpected error occurred: {e}")


def read_main_cfg(file_path: str = "") -> dict:
    if file_path == "":
        file_path = os.path.join(
            App.get_running_app().user_data_dir,  # type:ignore
            "main.cfg",
        )

    try:
        with open(file_path, "r") as file:
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


def update_main_cfg(to_update: dict, file_path: str = ""):
    content = read_main_cfg()

    content.update(to_update)

    try:
        with open(file_path, "w") as file:
            yaml.dump(content, file)
    except Exception as e:
        print(f"Error writing to file: {e}")
    # except FileNotFoundError:
    #     print(f"Error: File at {file_path} not found.")
    # except yaml.YAMLError as e:
    #     print(f"Error: Failed to parse YAML file at {file_path}. Details: {e}")
    # except Exception as e:
    #     print(f"An unexpected error occurred: {e}")
