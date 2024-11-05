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
    rooms: list  # correct locations

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

    @property
    def correct_answer(self) -> str:
        return self.answers[0]

    @property
    def shuffled_answers(self) -> list[str]:
        # return shuffle(self.answers[:])
        return shuffle(self.answers)  # type: ignore

    @property
    def correct_answer_position(self) -> int:
        return self.shuffled_answers.index(self.correct_answer)
