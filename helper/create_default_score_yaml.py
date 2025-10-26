import yaml
import os
import glob


def load_from_yaml(file_path: str) -> dict:
    try:
        with open(file_path, "r") as file:
            return yaml.safe_load(file)
    except Exception as e:
        print(f"Error reading file: {e}")
        print(f"{file_path = }")
        return dict()


def save_to_yaml(file_path: str, content: dict) -> None:
    try:
        with open(file_path, "w") as file:
            yaml.dump(content, file)
    except Exception as e:
        print(f"Error writing to file: {e}")
        print(f"{file_path = }")


# def load_total_storage() -> dict:
#     default_file_path = (
#         "/".join(__file__.split("/")[:-2]) + "/app/content/firetruck_tools.yaml"
#     )

#     return load_from_yaml(default_file_path)


# def load_total_storage() -> dict:
#     base_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "app", "content")
#     pattern = os.path.join(base_dir, "firetruck_tools_*.yaml")
#     all_files = glob.glob(pattern)

#     combined_data = {}
#     for file_path in all_files:
#         data = load_from_yaml(file_path)
#         if data:
#             if not isinstance(data, dict):
#                 raise ValueError(f"YAML file {file_path} must contain a dictionary at the top level.")
#             combined_data.update(data)

#     return combined_data


def load_total_storage() -> dict:
    base_dir = os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "..", "app", "content"
    )
    pattern = os.path.join(base_dir, "firetruck_tools_*.yaml")
    all_files = glob.glob(pattern)

    firetruck_scores = {}

    combined_data = {}
    for file_path in all_files:
        filename = os.path.basename(file_path)
        key_part = filename.removeprefix("firetruck_tools_").removesuffix(".yaml")

        data = load_from_yaml(file_path)
        if data is None:
            continue

        firetruck_scores[key_part] = {}

        for truck in data.keys():
            firetruck_scores[key_part].update(  # type:ignore
                {truck: {"high_score": 0, "high_strike": 0}}
            )

    return firetruck_scores


def load_total_competition_questions() -> dict:
    default_file_path = (
        "/".join(__file__.split("/")[:-2])
        + "/app/content/competition_questions_multiple_choice.yaml"
    )

    return load_from_yaml(default_file_path)


def create_scores_content() -> dict:
    scores = {"firetrucks": {}, "competitions": {}}

    total_storage = load_total_storage()
    scores["firetrucks"].update(total_storage)

    # for truck in total_storage.keys():
    #     scores.get("firetrucks").update(  # type:ignore
    #         {truck: {"high_score": 0, "high_strike": 0}}
    #     )

    total_questions = load_total_competition_questions()

    for question in total_questions.keys():
        scores.get("competitions").update({question: {"high_score": 0}})  # type:ignore

    return scores


def main():
    content = create_scores_content()

    file_path = "./scores.yaml"

    save_to_yaml(file_path, content)


if __name__ == "__main__":
    main()
