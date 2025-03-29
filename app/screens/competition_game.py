from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.layout import Layout
from kivy.uix.widget import Widget
from kivy.uix.progressbar import ProgressBar
from kivy.uix.screenmanager import Screen
from kivy.clock import Clock

from random import shuffle
from typing import cast

from helper.file_handling import (
    load_total_competition_questions,
    save_to_scores_file,
    get_scores_key,
)
from helper.settings import Settings
from helper.game_class import GameCore, CompetitionQuestion

settings = Settings()

answer_idx: dict = {0: "A", 1: "B", 2: "C", 3: "D"}


class Bewerb_Game(Screen):
    def select_competition(self, selected_competition):
        # troubleshooting: fix competition
        # self.selected_competition = "Funk"
        self.selected_competition = selected_competition

        self.competition_label = cast(Label, self.competition_label)
        self.competition_label.text = selected_competition

    def hide_label(self, *args):
        self.extra_time_label = cast(Label, self.extra_time_label)
        self.extra_time_label.opacity = 0

    def reset_timer(self):
        self.time_left = settings.COMPETITION_GAME_START_TIME_SEC

        # self.set_progress_bar()
        self.progress_bar = cast(ProgressBar, self.progress_bar)
        self.progress_bar.max = settings.COMPETITION_GAME_START_TIME_SEC

    def add_time(self):
        self.time_left = round(
            self.time_left + settings.COMPETITION_GAME_EXTRA_TIME_SEC, 1
        )

        self.extra_time_label.text = f"+ {settings.COMPETITION_GAME_EXTRA_TIME_SEC} s"

        self.extra_time_label.opacity = 1

        Clock.schedule_once(
            self.hide_label,
            settings.COMPETITION_GAME_DISPLAY_EXTRA_TIME_SEC,
        )

    def update_progress_bar(self):
        self.progress_bar.value = self.time_left

    def update_timer(self, *args):
        # update game time
        self.update_progress_bar()

        if self.time_left > 0.0:
            self.time_left = round(
                self.time_left - settings.COMPETITION_GAME_INTERVAL_SEC, 1
            )

        else:
            # Clock.unschedule(self.update_timer)  # Stop the timer when it reaches 0
            self.end_game()
            pass

    def increment_score(self, add: int = settings.COMPETITION_GAME_CORRECT_POINTS):
        self.score_label = cast(Label, self.score_label)

        self.game.score += add
        self.score_label.text = str(self.game.score)

    def update_score_labels(self):
        self.high_score_label = cast(Label, self.high_score_label)

        self.score_label.text = str(self.game.score)
        self.high_score_label.text = f"Best: {str(self.current_high_score)}"

    def end_game(self):
        Clock.unschedule(self.update_timer)  # Stop the timer when it reaches 0

        if self.game.score > self.current_high_score:
            save_to_scores_file(
                self.selected_competition, "high_score", self.game.score, "competitions"
            )

        app = App.get_running_app()
        app.root.current = "bewerb_menu"
        app.root.transition.direction = "right"

    def reset_competition_questions(self):
        self.competition_dict = load_total_competition_questions().get(
            self.selected_competition, {}
        )

        self.question_ids = list(self.competition_dict.keys())
        self.question_ids_bak = list(self.competition_dict.keys())

        self.question_ids_min = min([int(x) for x in self.question_ids])
        self.question_ids_max = max([int(x) for x in self.question_ids])

        shuffle(self.question_ids)

    def play(self):
        # init GameCore class instance
        self.game = GameCore()

        # (re)set game specific elements
        self.reset_competition_questions()

        self.reset_timer()

        # self.current_question = CompetitionQuestion(
        #     competition=self.selected_competition,
        #     question_id=0,
        #     question="dummy question",
        #     answers=["dummy answers"],
        # )

        self.current_high_score = get_scores_key(
            firetruck=self.selected_competition,
            key="high_score",
            questions="competitions",
        )

        self.update_score_labels()

        Clock.schedule_interval(
            self.update_timer, settings.COMPETITION_GAME_INTERVAL_SEC
        )

        # start game
        self.next_question()

    def next_question(self, *args):
        # move scrollview to top
        self.ids.question_scrollview.scroll_y = 1

        # Enable answer processing for the new tool
        self.accept_answers = True

        while True:
            if len(self.question_ids) == 0:
                self.reset_competition_questions()

            # select question
            current_question_id = self.question_ids.pop()
            current_question_q = self.competition_dict.get(current_question_id, {}).get(
                "Q"
            )
            current_question_q = cast(str, current_question_q)
            current_question_a = self.competition_dict.get(current_question_id, {}).get(
                "A"
            )
            current_question_a = cast(list[str], current_question_a)

            self.current_question = CompetitionQuestion(
                competition=self.selected_competition,
                question_id=current_question_id,
                question=current_question_q,
                answers=current_question_a,
            )

            # avoid missing question content
            if not self.current_question.question == "-- fehlt --":
                break

        self.display_question()

        self.answer_buttons_layout = cast(Layout, self.answer_buttons_layout)
        self.answer_buttons_layout.clear_widgets()

        for letter in answer_idx.values():
            btn = Button(text=letter, font_size="45sp")
            btn.bind(on_press=self.on_answer)  # type: ignore[attr-defined]
            self.answer_buttons_layout.add_widget(btn)

    def display_question(self):
        self.question_id_label = cast(Label, self.question_id_label)
        self.question_label = cast(Label, self.question_label)

        self.question_id_label.text = (
            f"{self.current_question.question_id} von {self.question_ids_max}"
        )

        text = self.current_question.question + "\n\n"

        for letter, answer in zip(
            answer_idx.values(), self.current_question.shuffled_answers
        ):
            text += f"[b]{letter}:[/b]  {answer}\n\n"

        self.question_label.text = text

    def correct_answer(self):
        self.increment_score()

        self.game.answers_correct_total += 1

        if (
            self.game.answers_correct_total
            % settings.COMPETITION_GAME_CORRECT_FOR_EXTRA_TIME
            == 0
        ):
            self.add_time()

    def incorrect_answer(self):
        pass

    def on_answer(self, instance):
        if not self.accept_answers:  # Check if answer processing is enabled
            return  # Ignore the button press if answer processing is disabled

        correct_answer_button = answer_idx.get(
            self.current_question.correct_answer_position
        )

        # process actual answer
        if instance.text == correct_answer_button:
            self.correct_answer()
        else:
            self.incorrect_answer()

        children = self.answer_buttons_layout.children

        # always identify and indicate the correct answer
        for child in children:
            if child.text == correct_answer_button:
                child.background_color = (0, 1, 0, 1)

        # indicate incorrect answer
        if instance.text != correct_answer_button:
            instance.background_color = (1, 0, 0, 1)

        # document given answers in class instance
        for key, value in answer_idx.items():
            if value == instance.text:
                given_answer_idx = key

        self.current_question.given_answer.append(
            (
                instance.text == correct_answer_button,  # was the answer correct?
                instance.text,  # given answer by user, button and text
                self.current_question.shuffled_answers[given_answer_idx],
            )
        )

        self.accept_answers = (
            False  # Disable answer processing after an answer is selected
        )

        # tool ends here. document tool and given answers in question history
        self.game.questions.append(self.current_question)

        Clock.schedule_once(self.next_question, settings.COMPETITION_GAME_FEEDBACK_SEC)
