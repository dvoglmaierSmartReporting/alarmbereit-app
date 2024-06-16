from helper.firetrucks import load_total_storage
from helper.settings import Strings

strs = Strings()


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
    mode_training: bool = True if selected_mode == strs.BUTTON_STR_TRAINING else False
    mode_game: bool = True if selected_mode == strs.BUTTON_STR_GAME else False
    mode_browse: bool = True if selected_mode == strs.BUTTON_STR_BROWSE else False
    mode_images: bool = True if selected_mode == strs.BUTTON_STR_IMAGES else False
    return (
        mode_training,
        mode_game,
        mode_browse,
        mode_images,
    )


def mode_bool2str(mode: tuple) -> str:
    mode_training, mode_game, mode_browse, mode_images = mode
    if mode_training:
        return strs.BUTTON_STR_TRAINING
    if mode_game:
        return strs.BUTTON_STR_GAME
    if mode_browse:
        return strs.BUTTON_STR_BROWSE
    if mode_images:
        return strs.BUTTON_STR_IMAGES
    return ""
