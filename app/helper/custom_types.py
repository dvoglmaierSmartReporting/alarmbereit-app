from typing import TypeAlias

# storage
totalStorage: TypeAlias = dict[str, dict[str, str | dict[str, list[str]]]]
totalQuestion: TypeAlias = dict[str, dict[int, dict[str, str | list[str]]]]
firetruckStorage: TypeAlias = tuple[list[str], list[str], dict[str, list[str]]]

# config
mainConfig: TypeAlias = dict[str, dict[str, str]]

# custom kivy
floatButtons: TypeAlias = list[tuple[str, float, float, float, float]]

# scores
scores: TypeAlias = dict[
    str, dict[str, dict[str, int] | dict[str, dict[str, dict[str, int]]]]
]
departmentScores: TypeAlias = dict[
    str, dict[str, int] | dict[str, dict[str, dict[str, int]]]
]
departmentTruckScores: TypeAlias = dict[str, dict[str, dict[str, int]]]
departmentCompetitionScores: TypeAlias = dict[str, dict[str, int]]
