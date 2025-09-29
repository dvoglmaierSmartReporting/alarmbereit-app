from kivy.app import App

import os
from typing import cast
from tabulate import tabulate

from helper.settings import Settings
from helper.strings import Strings
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


def tool_name_2image_name(tool_name: str) -> str:
    return (
        tool_name.lower()
        .replace("ä", "ae")
        .replace("ö", "oe")
        .replace("ü", "ue")
        .replace("ß", "ss")
        .replace('"', "")
        .replace("/", "")
    )


def get_ToolQuestion_instances(
    selected_firetruck: str, selected_city: str
) -> tuple[list[str], list[ToolQuestion]]:
    total_storage = load_total_storage(selected_city)

    if isinstance(total_storage[selected_firetruck]["Tools"], dict):
        firetruck = total_storage[selected_firetruck]["Tools"]
        firetruck = cast(dict, firetruck)
    else:
        raise TypeError(
            f"Firetruck {selected_firetruck} is not configured correctly. Tools key is not a dict."
        )

    rooms: list = list(firetruck.keys())

    # tools can have multiple entries for same tools in multiple locations,
    # because of varying tag strings
    tools: list = list(set([tool for room in firetruck.values() for tool in room]))

    tools_locations: dict = invert_firetruck_equipment(firetruck)
    tool_questions = []
    already_registered_tools = []

    for tool in tools:
        clean_tool_name = remove_tool_tags(tool)

        if clean_tool_name in already_registered_tools:
            continue
        else:
            already_registered_tools.append(clean_tool_name)

        image_tag = isolate_tag_value(tool, "<Bild:")

        if image_tag:
            tool_image_name = image_tag
        else:
            tool_image_name = (
                "assets/tools/" + tool_name_2image_name(clean_tool_name) + ".jpg"
            )

        # room can be used to identify room_image_name
        # but tag shall overrule auto-detection
        # so, check if Raumbild-tag is present
        # if not, use room name
        room_tag = isolate_tag_value(tool, "<Raumbild:")
        rooms = list(set(tools_locations.get(clean_tool_name, [])))

        # a tool can have multiple rooms
        # which to display?
        #
        # DECISION: use only one room for now
        # TODO: allow multiple rooms in the future

        if room_tag:
            room_image_name = room_tag
        else:
            room_name = str(rooms[0]).lower()
            if " / " in room_name:
                # room image file name convention
                # replace " / " with "_"
                room_name = "_".join(room_name.split(" / "))
            room_image_name = "assets/hallein_rl/" + room_name + ".jpg"

        tool_questions.append(
            ToolQuestion(
                firetruck=selected_firetruck,
                tool=break_tool_name(clean_tool_name),
                rooms=rooms,
                tool_image_name=tool_image_name,
                room_image_name=room_image_name,
            )
        )

    return (rooms, tool_questions)


def get_firetruck_layouts(selected_firetruck: str, selected_city: str) -> str:
    total_storage = load_total_storage(selected_city)

    if isinstance(total_storage[selected_firetruck]["Layout"], str):
        layout = total_storage[selected_firetruck]["Layout"]
        layout = cast(str, layout)
    else:
        raise TypeError(
            f"Firetruck {selected_firetruck} is not configured correctly. Layout key is not a str."
        )

    return layout


def get_firetruck_abbreviations(selected_city: str) -> dict:
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


def break_tool_name(tool_name: str, max_character: int = 27) -> str:
    if len(tool_name) >= max_character:
        max_character_half = max_character // 2 + 1
        tool_name_lst: list = tool_name[max_character_half:].split(" ")
        return (
            tool_name[:max_character_half]
            + tool_name_lst[0]
            + "\n"
            + " ".join(tool_name_lst[1:])
        )
    return tool_name


def create_scores_text(scores: scores, selected_city: str) -> str:
    spacing = "   "
    separator = " - "
    section_line_char = "="
    section_line = "\n\n" + section_line_char * 30 + "\n\n"
    # doubleline = "\n========================================\n\n"

    factor = settings.FIRETRUCK_TRAINING_STRIKE_FACTOR

    filtered_scores = scores.get(map_selected_city_2short_name(selected_city), {})
    filtered_scores = cast(departmentScores, filtered_scores)
    truck_scores = filtered_scores.get("firetrucks")
    truck_scores = cast(departmentTruckScores, truck_scores)

    # Text generation
    if selected_city == "Hallein":
        output = "Stadt Hallein"
    elif selected_city == "Bad Dürrnberg":
        output = f"LZ {selected_city}"
    else:
        output = selected_city

    output += section_line

    output += create_firetruck_score_text(
        truck_scores, spacing=spacing, separator=separator
    )

    total_score = sum_firetruck_scores(truck_scores)

    output += f"Summe - {dot_separator(total_score)} Punkte"

    output += section_line

    output += create_firetruck_score_text(
        truck_scores,
        spacing=spacing,
        separator=separator,
        key="high_strike",
    )

    total_strike = sum_firetruck_scores(truck_scores, key="high_strike")

    output += f"Summe - {total_strike} x {factor} = {total_strike * factor} Punkte\n\n"
    output += f"([i]Punkte aus {strings.BUTTON_STR_TRAINING} werden mit\nFaktor {factor} multipliziert[/i])"
    output += section_line

    total = total_score + total_strike * factor
    output += f"[b]Gesamtpunktzahl{separator}{dot_separator(total)} Punkte[/b]"
    return output


def extra_charactor(number: int) -> int:
    if 999_999 >= number >= 1_000:
        return len(str(number)) + 1
    return len(str(number))


def dot_separator(number: int) -> str:
    return f"{number:,}".replace(",", ".")


def create_firetruck_score_text(
    scores: departmentTruckScores,
    spacing: str,
    separator: str,
    key: str = "high_score",
) -> str:
    # output = strings.BUTTON_STR_FIRETRUCKS + ":\n\n"
    output = ""

    # longest_key = len(max(scores.keys(), key=len))

    # # define score column width
    # characters = 0
    # for data in scores.values():
    #     if isinstance(data.get(key), int):
    #         score = data.get(key, 0)
    #         score = cast(int, score)

    #         if extra_charactor(score) > characters:
    #             characters = extra_charactor(score)
    # characters += 1

    if key == "high_score":
        # game mode
        # output += strings.BUTTON_STR_GAME + ":\n\n"
        header = strings.BUTTON_STR_GAME
    else:
        # training mode
        # output += strings.BUTTON_STR_TRAINING + ":\n\n"
        header = strings.BUTTON_STR_TRAINING

    # for truck, data in scores.items():
    #     data = cast(dict, data)

    #     truck_space = spacing + " " * (longest_key - len(truck)) + truck + separator

    #     if isinstance(data.get(key), int):
    #         score = data.get(key, 0)
    #         score = cast(int, score)

    #     score_space = " " * (characters - extra_charactor(score)) + dot_separator(score)
    #     output += truck_space + score_space + "\n"

    # output += "\n"

    to_plot = []
    for truck, score in scores.items():
        to_plot.append([truck, score.get(key, 0)])
    output += tabulate(to_plot, headers=[header, "Punkte"])

    # output += "\n"

    return output + "\n\n"


def sum_firetruck_scores(scores: departmentTruckScores, key: str = "high_score") -> int:
    total = 0

    for data in scores.values():
        data = cast(dict, data)

        if isinstance(data.get(key), int):
            score = data.get(key, 0)
            score = cast(int, score)

        total += score

    return total
