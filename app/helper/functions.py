from kivy.app import App

from helper.settings import Strings

import yaml
from shutil import copyfile
import os

strings = Strings()


def load_total_storage() -> dict:
    with open(
        "/".join(__file__.split("/")[:-2]) + "/content/feuerwehr_tools_storage.yaml",
        "r",
    ) as file:
        try:
            return yaml.safe_load(file)
        except yaml.YAMLError as exc:
            print(exc)
            return dict()


def load_total_competition_questions() -> dict:
    # with open("./app/content/feuerwehr_competition_questions_mc.yaml", "r") as file:
    # with open("./app/content/feuerwehr_competition_questions.yaml", "r") as file:
    with open(
        "/".join(__file__.split("/")[:-2])
        + "/content/feuerwehr_competition_questions_multiple_choice.yaml",
        "r",
    ) as file:
        try:
            return yaml.safe_load(file)
        except yaml.YAMLError as exc:
            print(exc)
            return dict()


def invert_firetruck_equipment(firetruck: dict) -> dict:
    tools_locations = {}
    for location, tools in firetruck.items():
        for tool in tools:
            if tool in tools_locations:
                tools_locations[tool].append(location)
            else:
                tools_locations[tool] = [location]
    return tools_locations


def load_firetruck_storage(selected_firetruck: str) -> tuple[list, list, dict]:
    total_storage = load_total_storage()
    firetruck: dict = total_storage[selected_firetruck]
    rooms: list = list(firetruck.keys())
    tools: list = list(set([tool for room in firetruck.values() for tool in room]))
    tools_locations: dict = invert_firetruck_equipment(firetruck)

    return rooms, tools, tools_locations


def mode_str2bool(selected_mode: str) -> tuple:
    mode_training: bool = (
        True if selected_mode == strings.BUTTON_STR_TRAINING else False
    )
    mode_game: bool = True if selected_mode == strings.BUTTON_STR_GAME else False
    mode_browse: bool = True if selected_mode == strings.BUTTON_STR_BROWSE else False
    mode_images: bool = True if selected_mode == strings.BUTTON_STR_IMAGES else False
    return (
        mode_training,
        mode_game,
        mode_browse,
        mode_images,
    )


def mode_bool2str(mode: tuple) -> str:
    mode_training, mode_game, mode_browse, mode_images = mode
    if mode_training:
        return strings.BUTTON_STR_TRAINING
    if mode_game:
        return strings.BUTTON_STR_GAME
    if mode_browse:
        return strings.BUTTON_STR_BROWSE
    if mode_images:
        return strings.BUTTON_STR_IMAGES
    return ""


def break_tool_name(tool_name: str) -> str:
    if len(tool_name) >= 29:
        tool_name_lst: list = tool_name[14:].split(" ")
        return tool_name[:14] + tool_name_lst[0] + "\n" + " ".join(tool_name_lst[1:])
    return tool_name


def place_scores_file_to_writable_dir():
    src = os.path.join(os.path.dirname(__file__), "storage/scores.yaml")
    dst = os.path.join(
        App.get_running_app().user_data_dir, "scores.yaml"  # type:ignore
    )

    if not os.path.exists(dst):
        copyfile(src, dst)


def read_scores_file():
    try:
        with open(
            # "/".join(__file__.split("/")[:-2]) + "/storage/scores.yaml", "r"
            os.path.join(
                App.get_running_app().user_data_dir, "scores.yaml"  # type:ignore
            ),
            "r",
        ) as file:
            return yaml.safe_load(file)

    except Exception as e:
        print(f"Error reading file: {e}")
        return dict()


def read_scores_file_key(firetruck: str, key: str, questions: str = "firetrucks"):
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
            # "/".join(__file__.split("/")[:-2]) + "/storage/scores.yaml", "w"
            os.path.join(
                App.get_running_app().user_data_dir, "scores.yaml"  # type:ignore
            ),
            "w",
        ) as file:
            yaml.dump(content, file)
    except Exception as e:
        print(f"Error writing to file: {e}")
