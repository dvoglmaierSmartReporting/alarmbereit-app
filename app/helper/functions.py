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
        .replace(".", "")
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
                "./assets/tools/" + tool_name_2image_name(clean_tool_name) + ".jpg"
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

            # TODO: make dynamic for other cities
            # now it only works for hallein_
            room_image_name = (
                f"./assets/hallein_{selected_firetruck.lower()}/{room_name.lower()}.jpg"
            )

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
    factor = settings.FIRETRUCK_TRAINING_STRIKE_FACTOR
    factor_image = settings.FIRETRUCK_TRAINING_STRIKE_IMAGE_FACTOR

    city = map_selected_city_2short_name(selected_city)

    filtered_scores = scores.get(city, {})
    filtered_scores = cast(departmentScores, filtered_scores)

    running_score = filtered_scores.get("running_score")

    truck_scores = filtered_scores.get("firetrucks")
    truck_scores = cast(departmentTruckScores, truck_scores)

    table = list()
    total_score = 0
    total_strike = 0
    total_strike_image = 0

    third_column = True if city == "Hallein" else False

    for truck, data in truck_scores.items():
        score = data.get("high_score", 0)
        total_score += score

        strike = data.get("high_strike", 0)
        total_strike += strike

        if truck == "Leiter":
            strike_image = data.get("high_strike_image", 0)
            total_strike_image += strike_image
            strike_image = str(strike_image)
        else:
            strike_image = ""

        if third_column:
            table.append([truck, separate(str(score)), str(strike), strike_image])
        else:
            table.append([truck, separate(str(score)), str(strike)])

    empty_line = ["", "", ""]
    factor_line = [
        "Faktor",
        "-",
        f"x {factor}",
    ]
    hypon_line = ["-" * 10, "-" * 10, ""]
    equal_line = ["=" * 13, "=" * 10, ""]

    sum = [
        "Punkte",
        separate(str(total_score)),
        separate(str(total_strike * factor)),
    ]

    total = [
        "GESAMT",
        separate(
            str(
                total_score
                + (total_strike * factor)
                + (total_strike_image * factor_image)
            )
        ),
        "",
    ]

    running_score_line = ["Running Score", separate(str(running_score)), ""]
    if third_column:
        empty_line.append("")
        factor_line.append(f"x {factor_image}")
        hypon_line.append("")

        sum.append(separate(str(total_strike_image * factor_image)))

        total.append("")

        equal_line.append("")
        running_score_line.append("")

    headers = ["FAHRZEUG", "ZEITDRUCK", "ÜBUNG"]
    colalign = ["right", "right", "right"]
    if third_column:
        headers.append("BILDER")
        colalign.append("right")

    table.append(empty_line)
    table.append(factor_line)
    table.append(empty_line)
    table.append(sum)
    table.append(empty_line)
    table.append(hypon_line)
    table.append(empty_line)
    table.append(total)

    # Output running score
    table.append(empty_line)
    table.append(empty_line)
    table.append(empty_line)
    table.append(equal_line)
    table.append(running_score_line)
    table.append(equal_line)

    return tabulate(
        table,
        headers=headers,
        tablefmt="rounded_outline",
        colalign=colalign,
    )


def separate(string: str) -> str:
    # every 3rd character from the end, insert a underscore
    reversed_string = string[::-1]
    parts = [reversed_string[i : i + 3] for i in range(0, len(reversed_string), 3)]
    return "_".join(parts)[::-1]
