from dataclasses import dataclass, field
from random import shuffle


@dataclass
class GameCore:
    answers_correct_total: int = 0
    answers_correct_strike: int = 0
    score: int = 0

    # option to store all questions list here
    # instead of funktions in the screen class

    # concat history to review after a session
    questions: list = field(default_factory=list, init=False, repr=False)

    @property
    def questions_len(self) -> int:
        return len(self.questions)


@dataclass
class ToolQuestion:
    firetruck: str
    tool: str
    rooms: list[str]  # correct locations

    # list to document given answers
    room_answered: list = field(default_factory=list, init=False, repr=False)

    # dynamic set for question with multiple answers
    @property
    def rooms_to_be_answered(self) -> set:
        return set(self.rooms) - set(self.room_answered)


@dataclass
class CompetitionQuestion:
    competition: str
    question_id: int
    question: str
    answers: list[str]

    # list to document given answers
    given_answer: list = field(default_factory=list, init=False, repr=False)

    # avoid multiple shuffle executions on answer list
    _shuffled_answers: list[str] = field(default_factory=list, init=False, repr=False)
    _correct_answer_position: int = field(init=False, repr=False)

    def __post_init__(self):
        # shuffle the answers only once and store them in _shuffled_answers
        self._shuffled_answers = self.answers[:]
        shuffle(self._shuffled_answers)

        # find the position of the correct answer in the shuffled list
        self._correct_answer_position = self._shuffled_answers.index(
            self.correct_answer
        )

    @property
    def correct_answer(self) -> str:
        return self.answers[0]

    # NEXT: fix properties; each call shuffles the answers
    @property
    def shuffled_answers(self) -> list[str]:
        return self._shuffled_answers

    @property
    def correct_answer_position(self) -> int:
        return self._correct_answer_position
