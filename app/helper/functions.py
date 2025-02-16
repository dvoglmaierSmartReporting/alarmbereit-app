from helper.settings import Strings, Settings
from helper.file_handling import load_total_storage, load_total_competition_questions

strings = Strings()
settings = Settings()


def invert_firetruck_equipment(firetruck: dict) -> dict:
    tools_locations = {}
    for location, tools in firetruck.items():
        for tool in tools:
            if tool in tools_locations:
                tools_locations[tool].append(location)
            else:
                tools_locations[tool] = [location]
    return tools_locations


def get_firetruck_storage(selected_firetruck: str) -> tuple[list, list, dict]:
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


def create_scores_content() -> dict:
    scores = {"firetrucks": {}, "competitions": {}}

    total_storage = load_total_storage()

    for truck in total_storage.keys():
        scores.get("firetrucks").update(  # type:ignore
            {truck: {"high_score": 0, "high_strike": 0}}
        )

    total_questions = load_total_competition_questions()

    for question in total_questions.keys():
        scores.get("competitions").update({question: {"high_score": 0}})  # type:ignore

    return scores


def create_scores_text(scores: dict) -> str:
    output = ""
    spacing = "    "
    separator = "  -  "
    # divider = "  |  "
    total_score = 0
    total_strike = 0
    total = 0
    factor = settings.FIRETRUCK_STRIKE_FACTOR

    for category in scores:
        if category == "competitions":
            output += f"{strings.BUTTON_STR_COMPETITIONS}:\n"

            for comp in scores.get(category):  # type: ignore
                score = scores.get(category).get(comp).get("high_score")  # type: ignore
                total_score += score
                output += f"{spacing}Best:{spacing}{score}{separator}{comp}\n"

            # output += "\n"

        elif category == "firetrucks":
            output += f"{strings.BUTTON_STR_FIRETRUCKS}:\n"

            for comp in scores.get(category):  # type: ignore
                score = scores.get(category).get(comp).get("high_score")  # type: ignore
                total_score += score
                output += f"{spacing}Best:{spacing}{score}"
                strike = scores.get(category).get(comp).get("high_strike")  # type: ignore
                total_strike += strike
                # output += f"{divider}Best Strike:{spacing}{strike} x {str(factor)}{separator}{comp}\n"
                output += f"{spacing}Best Strike:{spacing}{strike}{separator}{comp}\n"

    output += "________________________________________________\n"
    output += f"Gesamt Best{separator}{str(total_score)} Punkte\n"
    output += f"Gesamt Best Strikes{separator}{str(total_strike)} x {factor} Punkte\n+\n"
    output += "==========================================\n"

    total = total_score + total_strike * factor
    output += f"Gesamtpunktzahl{separator}{str(total)} Punkte"
    return output

