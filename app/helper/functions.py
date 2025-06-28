from kivy.app import App

import os
from typing import cast

from helper.settings import Strings, Settings
from helper.file_handling import (
    load_total_storage,
    map_selected_city_2short_name,
)
from helper.game_class import ToolQuestion
from helper.custom_types import *


strings = Strings()
settings = Settings()


def change_screen_to(move_to: str, transition_direction: str = "right"):
    app = App.get_running_app()
    app.root.current = move_to
    app.root.transition.direction = transition_direction


def remove_tool_tags(tool_name: str) -> str:
    return tool_name.split("<Bild:")[0].split("<Raumbild:")[0].strip()


def isolate_tag_value(tool_name: str, tag: str) -> str:
    if tag in tool_name:
        start = tool_name.index(tag) + len(tag)
        end = tool_name.index(">", start)
        tool_image_file_str = tool_name[start:end]
        return os.path.join(".", "assets", *tool_image_file_str.split("/")) + ".jpg"
    return ""


def invert_firetruck_equipment(firetruck: dict[str, list[str]]) -> dict[str, list[str]]:
    tools_locations = {}
    for location, tools in firetruck.items():
        for tool in tools:
            clean_tool_name = remove_tool_tags(tool)
            if clean_tool_name in tools_locations:
                tools_locations[clean_tool_name].append(location)
            else:
                tools_locations[clean_tool_name] = [location]
    return tools_locations


def get_firetruck_storage(
    selected_firetruck: str, selected_city: str
) -> firetruckStorage:
    total_storage = load_total_storage(selected_city)

    if isinstance(total_storage[selected_firetruck]["Tools"], dict):
        firetruck = total_storage[selected_firetruck]["Tools"]
        firetruck = cast(dict, firetruck)
    else:
        raise TypeError(
            f"Firetruck {selected_firetruck} is not configured correctly. Tools key is not a dict."
        )

    rooms: list = list(firetruck.keys())
    tools: list = list(set([tool for room in firetruck.values() for tool in room]))
    tools_locations: dict = invert_firetruck_equipment(firetruck)
    return rooms, tools, tools_locations


def get_ToolQuestion_instances(
    selected_firetruck: str, selected_city: str
) -> tuple[list[str], list[ToolQuestion]]:

    # TODO: merge get_firetruck_storage + get_ToolQuestion_instances after refactoring all screens

    (rooms, tools, tools_locations) = get_firetruck_storage(
        selected_firetruck, selected_city
    )

    tool_questions = []

    for tool in tools:
        clean_tool_name = remove_tool_tags(tool)

        tool_questions.append(
            ToolQuestion(
                firetruck=selected_firetruck,
                tool=break_tool_name(clean_tool_name),
                rooms=list(set(tools_locations.get(clean_tool_name, []))),
                tool_image_name=isolate_tag_value(tool, "<Bild:"),
                room_image_name=isolate_tag_value(tool, "<Raumbild:"),
            )
        )

    return (rooms, tool_questions)


def get_firetruck_layout_value(selected_firetruck: str, selected_city: str) -> str:
    total_storage = load_total_storage(selected_city)

    if isinstance(total_storage[selected_firetruck]["Layout"], str):
        layout = total_storage[selected_firetruck]["Layout"]
        layout = cast(str, layout)
    else:
        raise TypeError(
            f"Firetruck {selected_firetruck} is not configured correctly. Layout key is not a str."
        )

    return layout


def get_firetruck_abbreviation_values(selected_city: str) -> dict:
    total_storage = load_total_storage(selected_city)

    abbs = dict()

    for firetruck in total_storage.keys():
        if isinstance(total_storage[firetruck]["Abb"], str):
            abb = total_storage[firetruck]["Abb"]
            abb = cast(str, abb)

            abbs[firetruck] = abb
        else:
            raise TypeError(
                f"Firetruck {firetruck} is not configured correctly. Abb key is not a str."
            )

    return abbs


def mode_str2bool(selected_mode: str) -> tuple:
    mode_training: bool = (
        True if selected_mode == strings.BUTTON_STR_TRAINING else False
    )
    mode_training_new: bool = (
        True if selected_mode == strings.BUTTON_STR_TRAINING_NEW else False
    )
    mode_game: bool = True if selected_mode == strings.BUTTON_STR_GAME else False
    mode_browse: bool = True if selected_mode == strings.BUTTON_STR_BROWSE else False
    mode_images: bool = True if selected_mode == strings.BUTTON_STR_IMAGES else False
    mode_exam: bool = True if selected_mode == strings.BUTTON_STR_EXAM else False
    return (
        mode_training,
        mode_training_new,
        mode_game,
        mode_browse,
        mode_images,
        mode_exam,
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


def create_scores_text(scores: scores, selected_city: str) -> str:
    spacing = "      "
    separator = "  -  "
    # divider = "  |  "
    factor = settings.FIRETRUCK_TRAINING_STRIKE_FACTOR

    filtered_scores = scores.get(map_selected_city_2short_name(selected_city), {})

    if selected_city == "Hallein":
        output = "Stadt Hallein\n\n"
    else:
        output = selected_city + "\n\n"

    # always display firetrucks on top
    output_2add, total_score, total_strike = create_firetruck_score_text(
        filtered_scores.get("firetrucks")
    )

    output += output_2add + "\n"

    output_2add, total_score_2add = create_competition_score_text(
        filtered_scores.get("competitions")
    )
    output += output_2add
    total_score += total_score_2add

    output += "________________________________________\n"
    output += f"Gesamt Best{separator}{str(total_score)} Punkte\n"
    output += (
        f"Gesamt Best Strikes{separator}{str(total_strike)} x {factor} Punkte\n+\n"
    )
    output += "========================================\n"

    total = total_score + total_strike * factor
    output += f"Gesamtpunktzahl{separator}{str(total)} Punkte"
    return output


def create_firetruck_score_text(
    scores,
    spacing: str = "      ",
    separator: str = "  -  ",
) -> tuple[str, int, int]:
    total_score = 0
    total_strike = 0

    output = f"{strings.BUTTON_STR_FIRETRUCKS}:\n"

    for truck, data in scores.items():
        data = cast(dict, data)

        if isinstance(data.get("high_score"), int):
            score = data.get("high_score", 0)
            score = cast(int, score)

        total_score += score
        dynamic_spacing = " " * (14 - len(str(score)) * 2)
        output += f"{spacing}{spacing}Best:{dynamic_spacing}{score}"

        if isinstance(data.get("high_strike"), int):
            strike = data.get("high_strike", 0)
            strike = cast(int, strike)

        total_strike += strike
        dynamic_spacing = " " * (10 - len(str(strike)))
        output += f"{spacing}Best Strike:{spacing}{strike}{separator}{truck}\n"

    return output, total_score, total_strike


def create_competition_score_text(
    scores,
    spacing: str = "      ",
    separator: str = "  -  ",
) -> tuple[str, int]:
    total_score = 0

    output = f"{strings.BUTTON_STR_COMPETITIONS}:\n"

    for comp, data in scores.items():
        if isinstance(data.get("high_score"), int):
            score = data.get("high_score", 0)
            score = cast(int, score)
        total_score += score
        dynamic_spacing = " " * (14 - len(str(score)) * 2)
        output += f"{spacing}{spacing}Best:{dynamic_spacing}{score}{separator}{comp}\n"

    return output, total_score
