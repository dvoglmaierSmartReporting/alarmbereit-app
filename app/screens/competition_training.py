from kivy.uix.screenmanager import Screen

from random import shuffle

from helper.functions import load_total_competition_questions
from helper.settings import Strings

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

    def load_competition_questions(self):
        total_questions = load_total_competition_questions()
        self.competition_dict = total_questions[self.selected_competition]

        self.question_ids = list(self.competition_dict.keys())
        # self.question_ids = [int(question_id) for question_id in list(self.competition_dict.keys())]
        shuffle(
            self.question_ids
        )  # moved to self.play()  # reverted!! needs to be executed each new load

        self.question_ids_min = str(min([int(x) for x in self.question_ids]))
        self.question_ids_max = str(max([int(x) for x in self.question_ids]))

    def play(self):
        self.load_competition_questions()

        # start with smallest question id, then shuffle list
        self.current_question_id = self.question_ids.pop(0)
        # shuffle(self.question_ids)  # moved to load_competition_questions()

        self.previous_question_button.disabled = True  # type: ignore
        self.next_question_button.disabled = False  # type: ignore

        self.process_question()

    def process_question(self):
        self.question_id_label.text = (  # type: ignore
            f"{self.current_question_id} von {self.question_ids_max}"
        )
        # print(f"{self.current_question_id = }")
        # print(f"{self.competition_dict.get(self.current_question_id) = }")
        # print(f"{self.competition_dict.get(self.current_question_id).get("Q") = }")
        self.current_question = self.competition_dict.get(self.current_question_id).get(
            "Q"
        )
        self.question_label.text = self.current_question  # type: ignore

        self.current_answer = self.competition_dict.get(self.current_question_id).get(
            "A"
        )[0]

    def random_question(self):
        self.ids.question_scrollview.scroll_y = 1
        self.previous_question_button.disabled = False  # type: ignore
        self.next_question_button.disabled = False  # type: ignore
        self.solution_button.disabled = False  # type: ignore

        if len(self.question_ids) == 0:
            self.load_competition_questions()

        # troubleshooting: fix question
        # self.current_question_id = "22" # -> "Xaver"
        self.current_question_id = self.question_ids.pop()

        self.process_question()

    def next_question(self, previous: bool = False):
        self.previous_question_button.disabled = False  # type: ignore
        self.next_question_button.disabled = False  # type: ignore
        self.solution_button.disabled = False  # type: ignore

        if previous:
            # self.current_question_id = str(int(self.current_question_id) - 1)
            self.current_question_id = int(self.current_question_id) - 1
        else:
            # self.current_question_id = str(int(self.current_question_id) + 1)
            self.current_question_id = int(self.current_question_id) + 1

        if self.current_question_id == self.question_ids_min:
            self.previous_question_button.disabled = True  # type: ignore
        if self.current_question_id == self.question_ids_max:
            self.next_question_button.disabled = True  # type: ignore

        self.process_question()

    def reveal_answer(self):
        self.solution_button.disabled = True  # type: ignore

        self.question_label.text += "\n\n" + self.current_answer  # type: ignore
        self.ids.question_label.height = self.ids.question_label.texture_size[1]
