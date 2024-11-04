from kivy.app import App
from kivy.uix.screenmanager import Screen
from kivy.clock import Clock

from random import shuffle

from helper.functions import (
    load_total_competition_questions,
    read_scores_file_key,
    save_to_scores_file,
)
from helper.settings import Settings
from helper.game_class import GameCore, CompetitionQuestion

settings = Settings()


class Bewerb_Game(Screen):
    # def __init__(self, **kwargs):
    #     super(Bewerb_Game, self).__init__(**kwargs)

    def select_competition(self, selected_competition):
        # troubleshooting: fix competition
        # self.selected_competition = "Funk"
        self.selected_competition = selected_competition
        self.competition_label.text = f"   {selected_competition}"  # type: ignore

    def hide_label(self, *args):
        self.extra_time_label.opacity = 0  # type: ignore

    def reset_timer(self):
        self.time_left = settings.COMPETITION_START_TIME_GAME_SEC

        # self.timer_label.text = f"{str(self.time_left)} s  "
        self.timer_label.text = f""  # type: ignore

        self.set_progress_bar()

    def add_time(self, extra_time: float):
        self.time_left = round(self.time_left + extra_time, 1)

        self.extra_time_label.text = f"+ {settings.COMPETITION_EXTRA_TIME} s  "  # type: ignore

        self.extra_time_label.opacity = 1  # type: ignore

        Clock.schedule_once(
            self.hide_label,
            settings.DISPLAY_EXTRA_TIME_LABEL,
        )

    def set_progress_bar(self):
        self.progress_bar.max = settings.COMPETITION_START_TIME_GAME_SEC  # type: ignore

    def update_progress_bar(self):
        self.progress_bar.value = self.time_left  # type: ignore

    def update_timer(self, *args):
        # update game time
        self.update_progress_bar()

        if self.time_left > 0.0:
            self.time_left = round(self.time_left - settings.INTERVAL_GAME_SEC, 1)

            if not self.time_left == 0.0:
                # self.timer_label.text = f"{str(self.time_left)} s  "
                self.timer_label.text = f""  # hide label for UI testing  # type: ignore

            else:
                self.timer_label.text = "Ende  "  # type: ignore
                # todo: disable buttons between game end and menu screen animation
        else:
            Clock.unschedule(self.update_timer)  # Stop the timer when it reaches 0
            self.end_game()
            pass

    def increment_score(self, add: int = 100):
        self.game.score += add
        self.score_label.text = f"{str(self.game.score)}  "  # type: ignore

    def update_score_labels(self):
        self.score_label.text = f"{str(self.game.score)}  "  # type: ignore
        self.high_score_label.text = f"Best: {str(self.current_high_score)}  "  # type: ignore

    def end_game(self):
        if self.game.score > self.current_high_score:
            save_to_scores_file(
                self.selected_competition, "high_score", self.game.score, "competitions"
            )

        app = App.get_running_app()
        app.root.current = "bewerb_menu"  # type: ignore
        app.root.transition.direction = "right"  # type: ignore

## CONTINUE HERE!

    def shuffle_questions(self):
        shuffle(
            self.question_ids
        )  # moved to self.play()  # reverted!! needs to be executed each new load

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
        self.game = GameCore()

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

    # def random_question(self):
    #     # move scrollview to top
    #     self.ids.question_scrollview.scroll_y = 1

    #     self.solution_button.disabled = False  # type: ignore

    #     self.previous_question_button.disabled = False  # type: ignore
    #     self.next_question_button.disabled = False  # type: ignore

    #     if len(self.question_ids) == 0:
    #         # self.reset_competition_questions()
    #         self.question_ids = list(set(self.question_ids_bak))

    #     self.shuffle_questions()
    #     # troubleshooting: fix question
    #     # self.current_question_id = "22" # -> "Xaver"
    #     # self.current_question_id = self.question_ids.pop()
    #     upcoming_question_id = self.question_ids.pop()

    #     self.current_question = CompetitionQuestion(
    #         competition=self.selected_competition,
    #         question_id=upcoming_question_id,
    #         question=self.competition_dict.get(upcoming_question_id).get("Q"),  # type: ignore
    #         answers=self.competition_dict.get(upcoming_question_id).get("A"),  # type: ignore
    #     )

    #     self.display_question()

    def next_question(self, previous: bool = False):
        # move scrollview to top
        self.ids.question_scrollview.scroll_y = 1

        # self.solution_button.disabled = False  # type: ignore

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

        # self.check_arrow_buttons()

        self.display_question()

    # def reveal_answer(self):
    #     self.solution_button.disabled = True  # type: ignore

    #     # self.question_label.text += "\n\n" + self.current_answer  # type: ignore
    #     self.question_label.text += "\n\n" + self.current_question.correct_answer  # type: ignore
    #     self.ids.question_label.height = self.ids.question_label.texture_size[1]
