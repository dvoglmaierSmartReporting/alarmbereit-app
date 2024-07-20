from dataclasses import dataclass, field


# @dataclass
# class Customer:
#     name: str
#     group_name: str
#     group_id: int = field(init=False, default=0)
#     df_reports: DataFrame = field(init=False, repr=False)
#     df_report_versions: DataFrame = field(init=False, repr=False)
#     df_templates: DataFrame = field(init=False, repr=False)

#     def fetch_reports(self, db: Connection) -> DataFrame:
#         if not isinstance(self.group_id, list):
#             group_lst = [str(self.group_id)]


@dataclass
class ToolQuestion:
    tool: bool


# @dataclass
# class CompetitionQuestion:
#     tool: bool


@dataclass
class GameCore:
    answers_correct_total: int = 0
    answers_correct_strike: int = 0

    # concat history to review after a session
    questions: dict = field(
        init=False, repr=False
    )

    score: int = 0
