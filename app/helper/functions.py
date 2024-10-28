from helper.settings import Strings

import yaml

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
        + "/content/feuerwehr_competition_questions.yaml",
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


def read_scores_file():
    with open("/".join(__file__.split("/")[:-2]) + "/storage/scores.yaml", "r") as file:
        return yaml.safe_load(file)


def read_scores_file_key(key: str):
    content = read_scores_file()
    # self.current_high_score = content.get(key)
    return content.get(key)


def save_to_scores_file(key: str, value: int):
    content = read_scores_file()
    # content["game_high_score"] = self.game.score
    content[key] = value
    with open("/".join(__file__.split("/")[:-2]) + "/storage/scores.yaml", "w") as file:
        yaml.dump(content, file)
