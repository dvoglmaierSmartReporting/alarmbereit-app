from kivy.uix.screenmanager import Screen

from random import shuffle

from helper.file_handling import load_total_competition_questions
from helper.settings import Strings
from helper.game_class import CompetitionQuestion

strings = Strings()


class Bewerb_Training(Screen):
    def __init__(self, **kwargs):
        super(Bewerb_Training, self).__init__(**kwargs)
        # update button strings
        self.solution_button.text = strings.BUTTON_STR_SOLUTION  # type: ignore
        self.random_question_button.text = strings.BUTTON_STR_RANDOM_QUESTION  # type: ignore

    def select_competition(self, selected_competition):
        # troubleshooting: fix competition
        # self.selected_competition = "Funk"
        self.selected_competition = selected_competition

    def shuffle_questions(self):
        shuffle(self.question_ids)

    def reset_competition_questions(self):
        self.competition_dict = load_total_competition_questions().get(
            self.selected_competition
        )

        self.question_ids = list(self.competition_dict.keys())  # type: ignore
        self.question_ids_bak = list(self.competition_dict.keys())  # type: ignore

        self.question_ids_min = min([int(x) for x in self.question_ids])
        self.question_ids_max = max([int(x) for x in self.question_ids])

    def check_arrow_buttons(self):
        if self.current_question.question_id == self.question_ids_min:
            self.previous_question_button.disabled = True  # type: ignore
        else:
            self.previous_question_button.disabled = False  # type: ignore

        if self.current_question.question_id == self.question_ids_max:
            self.next_question_button.disabled = True  # type: ignore
        else:
            self.next_question_button.disabled = False  # type: ignore

    def play(self):
        # init GameCore class instance
        # self.game = GameCore()

        # (re)set game specific elements
        self.reset_competition_questions()

        self.current_question = CompetitionQuestion(
            competition=self.selected_competition,
            question_id=0,
            question="dummy question",
            answers=["dummy answers"],
        )

        self.next_question()

    def display_question(self):
        self.question_id_label.text = (  # type: ignore
            f"{self.current_question.question_id} von {self.question_ids_max}   "
        )
        self.question_label.text = self.current_question.question  # type: ignore

    def random_question(self):
        # move scrollview back to top
        self.ids.question_scrollview.scroll_y = 1

        self.solution_button.disabled = False  # type: ignore

        self.previous_question_button.disabled = False  # type: ignore
        self.next_question_button.disabled = False  # type: ignore

        if len(self.question_ids) == 0:
            self.question_ids = list(set(self.question_ids_bak))

        self.shuffle_questions()
        # troubleshooting: fix question
        # self.current_question_id = "22" # -> "Xaver"
        # self.current_question_id = self.question_ids.pop()
        upcoming_question_id = self.question_ids.pop()

        self.current_question = CompetitionQuestion(
            competition=self.selected_competition,
            question_id=upcoming_question_id,
            question=self.competition_dict.get(upcoming_question_id).get("Q"),  # type: ignore
            answers=self.competition_dict.get(upcoming_question_id).get("A"),  # type: ignore
        )

        self.display_question()

    def next_question(self, previous: bool = False):
        # move scrollview to top
        self.ids.question_scrollview.scroll_y = 1

        self.solution_button.disabled = False  # type: ignore

        if not previous:
            upcoming_question_id = int(self.current_question.question_id) + 1
        else:
            upcoming_question_id = int(self.current_question.question_id) - 1

        self.current_question = CompetitionQuestion(
            competition=self.selected_competition,
            question_id=upcoming_question_id,
            question=self.competition_dict.get(upcoming_question_id).get("Q"),  # type: ignore
            answers=self.competition_dict.get(upcoming_question_id).get("A"),  # type: ignore
        )

        # remove viewed question from list
        if upcoming_question_id in self.question_ids:
            self.question_ids.remove(upcoming_question_id)

        self.check_arrow_buttons()

        self.display_question()

    def reveal_answer(self):
        self.solution_button.disabled = True  # type: ignore

        self.question_label.text += "\n\n" + self.current_question.correct_answer  # type: ignore
        self.ids.question_label.height = self.ids.question_label.texture_size[1]
