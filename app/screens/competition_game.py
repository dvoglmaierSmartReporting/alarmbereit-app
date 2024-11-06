from kivy.app import App
from kivy.uix.button import Button
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

answer_idx: dict = {0: "A", 1: "B", 2: "C", 3: "D"}


class Bewerb_Game(Screen):
    def select_competition(self, selected_competition):
        # troubleshooting: fix competition
        # self.selected_competition = "Funk"
        self.selected_competition = selected_competition
        self.competition_label.text = f"   {selected_competition}"  # type: ignore

    def hide_label(self, *args):
        self.extra_time_label.opacity = 0  # type: ignore

    def reset_timer(self):
        self.time_left = settings.COMPETITION_START_TIME_SEC

        # self.timer_label.text = f"{str(self.time_left)} s  "
        self.timer_label.text = f""  # type: ignore

        # self.set_progress_bar()
        self.progress_bar.max = settings.COMPETITION_START_TIME_SEC  # type: ignore

    def add_time(self):
        self.time_left = round(self.time_left + settings.COMPETITION_EXTRA_TIME_SEC, 1)

        self.extra_time_label.text = f"+ {settings.COMPETITION_EXTRA_TIME_SEC} s  "  # type: ignore

        self.extra_time_label.opacity = 1  # type: ignore

        Clock.schedule_once(
            self.hide_label,
            settings.DISPLAY_EXTRA_TIME_LABEL_SEC,
        )

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

    def reset_competition_questions(self):
        self.competition_dict = load_total_competition_questions().get(
            self.selected_competition
        )

        self.question_ids = list(self.competition_dict.keys())  # type: ignore
        self.question_ids_bak = list(self.competition_dict.keys())  # type: ignore

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

        self.current_high_score = read_scores_file_key(
            firetruck=self.selected_competition,
            key="high_score",
            questions="competitions",
        )

        self.update_score_labels()

        Clock.schedule_interval(self.update_timer, settings.INTERVAL_GAME_SEC)

        # start game
        self.next_question()

    def next_question(self, *args):
        # move scrollview to top
        self.ids.question_scrollview.scroll_y = 1

        # Enable answer processing for the new tool
        self.accept_answers = True

        if len(self.question_ids) == 0:
            self.reset_competition_questions()

        # select question
        current_question = self.question_ids.pop()

        self.current_question = CompetitionQuestion(
            competition=self.selected_competition,
            question_id=current_question,
            question=self.competition_dict.get(current_question).get("Q"),  # type: ignore
            answers=self.competition_dict.get(current_question).get("A"),  # type: ignore
        )

        self.display_question()

        self.answer_buttons_layout.clear_widgets()  # type: ignore

        for letter in answer_idx.values():
            btn = Button(text=letter, font_size="45sp")
            btn.bind(on_press=self.on_answer)  # type: ignore
            self.answer_buttons_layout.add_widget(btn)  # type: ignore

    def display_question(self):
        self.question_id_label.text = (  # type: ignore
            f"{self.current_question.question_id} von {self.question_ids_max}   "
        )

        text = self.current_question.question + "\n\n"

        for letter, answer in zip(
            answer_idx.values(), self.current_question.shuffled_answers
        ):
            text += f"[b]{letter}:[/b]  {answer}\n\n"

        self.question_label.text = text  # type: ignore

    def correct_answer(self):
        self.increment_score()

        self.game.answers_correct_total += 1

        if (
            self.game.answers_correct_total
            % settings.COMPETITION_CORRECT_FOR_EXTRA_TIME
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

        children = self.answer_buttons_layout.children  # type: ignore

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
                self.current_question.shuffled_answers[given_answer_idx],  # type: ignore
            )
        )

        self.accept_answers = (
            False  # Disable answer processing after an answer is selected
        )

        # tool ends here. document tool and given answers in question history
        self.game.questions.append(self.current_question)

        Clock.schedule_once(self.next_question, settings.FEEDBACK_GAME_SEC)
