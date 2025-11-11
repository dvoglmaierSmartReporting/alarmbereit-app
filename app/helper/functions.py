from kivy.app import App

import os
from typing import cast

from helper.settings import Settings
from helper.strings import Strings
from helper.file_handling import load_total_storage
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

    # selected_firetruck = selected_firetruck.strip()

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
    # TODO only one can be True
    mode_training: bool = (
        True if selected_mode == strings.BUTTON_STR_TRAINING else False
    )
    mode_training_new: bool = (
        True if selected_mode == strings.BUTTON_STR_TRAINING_WITH_IMAGES else False
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
        output = (
            tool_name[:max_character_half]
            + tool_name_lst[0]
            + "\n"
            + " ".join(tool_name_lst[1:])
        )
        return output.strip()
    return tool_name
