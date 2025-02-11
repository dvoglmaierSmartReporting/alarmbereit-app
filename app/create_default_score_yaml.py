import yaml


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


def load_total_storage() -> dict:
    default_file_path = (
        "/".join(__file__.split("/")[:-2]) + "/app/content/firetruck_tools.yaml"
    )

    return load_from_yaml(default_file_path)


def load_total_competition_questions() -> dict:
    default_file_path = (
        "/".join(__file__.split("/")[:-2])
        + "/app/content/competition_questions_multiple_choice.yaml"
    )

    return load_from_yaml(default_file_path)


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


def main():
    content = create_scores_content()

    file_path = "./scores.yaml"

    save_to_yaml(file_path, content)


if __name__ == "__main__":
    main()
