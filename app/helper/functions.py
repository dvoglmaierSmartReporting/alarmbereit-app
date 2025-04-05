from helper.settings import Strings, Settings
from helper.file_handling import load_total_storage, load_total_competition_questions
from helper.game_class import ToolQuestion
from helper.custom_types import *

import os

strings = Strings()
settings = Settings()


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


def get_firetruck_storage(selected_firetruck: str) -> firetruckStorage:
    total_storage = load_total_storage()
    firetruck: dict = total_storage[selected_firetruck]
    rooms: list = list(firetruck.keys())
    tools: list = list(set([tool for room in firetruck.values() for tool in room]))
    tools_locations: dict = invert_firetruck_equipment(firetruck)
    return rooms, tools, tools_locations


def get_ToolQuestion_instances(
    selected_firetruck: str,
) -> tuple[list[str], list[ToolQuestion]]:
    # merge get_firetruck_storage + get_ToolQuestion_instances after refactoring all screens

    (rooms, tools, tools_locations) = get_firetruck_storage(selected_firetruck)

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


def create_scores_content() -> dict:
    scores = {"firetrucks": {}, "competitions": {}}

    total_storage = load_total_storage()

    for truck in total_storage.keys():
        scores.get("firetrucks", {}).update(
            {truck: {"high_score": 0, "high_strike": 0}}
        )

    total_questions = load_total_competition_questions()

    for question in total_questions.keys():
        scores.get("competitions", {}).update({question: {"high_score": 0}})

    return scores


def create_scores_text(scores: scores) -> str:
    output = ""
    spacing = "      "
    separator = "  -  "
    # divider = "  |  "
    total_score = 0
    total_strike = 0
    total = 0
    factor = settings.FIRETRUCK_TRAINING_STRIKE_FACTOR

    for category, competitions in scores.items():
        if category == "competitions":
            output += f"{strings.BUTTON_STR_COMPETITIONS}:\n"

            for comp, data in competitions.items():
                score = data.get("high_score", 0)
                total_score += score
                dynamic_spacing = " " * (14 - len(str(score)) * 2)
                output += f"{spacing}{spacing}Best:{dynamic_spacing}{score}{separator}{comp}\n"

        elif category == "firetrucks":
            output += f"{strings.BUTTON_STR_FIRETRUCKS}:\n"

            for comp, data in competitions.items():
                score = data.get("high_score", 0)
                total_score += score
                dynamic_spacing = " " * (14 - len(str(score)) * 2)
                output += f"{spacing}{spacing}Best:{dynamic_spacing}{score}"
                strike = data.get("high_strike", 0)
                total_strike += strike
                dynamic_spacing = " " * (10 - len(str(strike)))
                output += f"{spacing}Best Strike:{spacing}{strike}{separator}{comp}\n"

    output += "________________________________________\n"
    output += f"Gesamt Best{separator}{str(total_score)} Punkte\n"
    output += (
        f"Gesamt Best Strikes{separator}{str(total_strike)} x {factor} Punkte\n+\n"
    )
    output += "========================================\n"

    total = total_score + total_strike * factor
    output += f"Gesamtpunktzahl{separator}{str(total)} Punkte"
    return output
