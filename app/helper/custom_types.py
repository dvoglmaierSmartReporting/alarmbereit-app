from typing import TypeAlias

totalStorage: TypeAlias = dict[str, dict[str, str | dict[str, list[str]]]]
totalQuestion: TypeAlias = dict[str, dict[int, dict[str, str | list[str]]]]
mainConfig: TypeAlias = dict[str, dict[str, str]]
floatButtons: TypeAlias = list[tuple[str, float, float, float, float]]
scores: TypeAlias = dict[
    str, dict[str, dict[str, int] | dict[str, dict[str, dict[str, int]]]]
]
firetruckStorage: TypeAlias = tuple[list[str], list[str], dict[str, list[str]]]
