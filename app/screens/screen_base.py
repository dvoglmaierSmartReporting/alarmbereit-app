from kivy.app import App
from kivy.clock import Clock
from kivy.uix.button import Button

from dataclasses import dataclass
from random import shuffle

from helper.settings import Settings
from helper.functions import *
from helper.file_handling import *


settings = Settings()


@dataclass
class BaseMethods:
    def load_high_score(self):
        self.current_high_score = get_score_value(
            city=self.selected_city,
            questions="firetrucks",
            truck_or_comp=self.selected_firetruck,
            key=self.get_scores_key(),
        )

    def update_score_labels(self):
        self.update_score_label()
        self.update_high_score_label()

    def update_score_label(self):
        self.ids.score_label.text = str(self.game.score)

    def update_high_score_label(self):
        self.ids.high_score_label.text = f"Best: {str(self.current_high_score)}"

    def reset_score(self, *arg):
        self.game.score = 0
        self.update_score_labels()

    def increment_score(self):
        self.game.score += self.get_scores_value()
        self.update_score_label()

    def reset_tool_list(self):
        (self.firetruck_rooms, self.tool_questions) = get_ToolQuestion_instances(
            self.selected_firetruck, self.selected_city
        )
        self.tool_amount = len(self.tool_questions)

        shuffle(self.tool_questions)

    def hide_label(self, *args):
        self.ids.extra_time_label.opacity = 0

    def reset_progress_bar(self):
        self.ids.progress_bar_answer.max = (
            settings.FIRETRUCK_TRAINING_WITH_IMAGES_FEEDBACK_SEC - 0.3
        )
        self.ids.progress_bar_answer.value = 0

    def update_progress_bar(self):
        self.progress_bar.value = self.time_left

    def reset_timer(self):
        self.time_left = settings.FIRETRUCK_GAME_START_TIME_SEC

        self.ids.progress_bar.max = settings.FIRETRUCK_GAME_START_TIME_SEC

    def add_time(self):
        self.time_left = round(
            self.time_left + settings.FIRETRUCK_GAME_EXTRA_TIME_SEC, 1
        )

        # avoid that remaining time (add time) can exceed max progress bar
        if self.time_left > self.progress_bar.max:
            self.progress_bar.max = self.time_left

        self.ids.extra_time_label.text = f"+ {settings.FIRETRUCK_GAME_EXTRA_TIME_SEC} s"

        self.extra_time_label.opacity = 1

        Clock.schedule_once(
            self.hide_label,
            settings.FIRETRUCK_GAME_DISPLAY_EXTRA_TIME_SEC,
        )

    def update_timer(self, *args):
        # update game time
        self.update_progress_bar()

        if self.time_left > 0.0:
            self.time_left = round(
                self.time_left - settings.FIRETRUCK_GAME_INTERVAL_SEC, 1
            )

        else:
            self.end_game()
            pass

    def get_current_screen(self):
        app = App.get_running_app()
        return app.root.current

    def get_scores_key(self):
        if self.current_screen == "firetruck_training":
            return "high_strike"
        elif self.current_screen == "firetruck_training_with_images":
            return "high_strike_image"
        elif self.current_screen == "firetruck_game":
            return "high_score"
        else:
            raise NotImplementedError("scores.yaml key not defined!")

    def get_scores_value(self):
        if self.current_screen in [
            "firetruck_training",
            "firetruck_training_with_images",
            "firetruck_exam",
        ]:
            return settings.FIRETRUCK_TRAINING_CORRECT_POINTS
        elif self.current_screen == "firetruck_game":
            return settings.FIRETRUCK_GAME_CORRECT_POINTS
        else:
            raise NotImplementedError("scores.yaml key not defined!")

    def correct_answer(self):
        self.increment_score()

        self.game.answers_correct += 1

        if self.game.score > self.current_high_score:
            self.current_high_score = self.game.answers_correct

            self.update_high_score_label()

            save_to_scores_file(
                city=self.selected_city,
                questions="firetrucks",
                truck_or_comp=self.selected_firetruck,
                key=self.get_scores_key(),
                value=self.game.score,
            )

        self.feedback_green = True

    def incorrect_answer(self):
        self.feedback_green = False

        Clock.schedule_once(self.reset_score, settings.FIRETRUCK_TRAINING_FEEDBACK_SEC)

    def color_layout(self, instance):
        float_layout = self.ids.firetruck_rooms_layout.children[
            0
        ]  # children is reversed

        # indicate if correct or incorrect answer
        # for single correct answer
        if len(self.current_tool_question.rooms_to_be_answered) <= 1:
            # always identify and indicate the correct answer
            # for child in children:
            for child in float_layout.children:
                if isinstance(child, Button):
                    if child.text in self.current_tool_question.rooms:
                        child.background_color = (0, 1, 0, 1)
            # if, indicate incorrect answer
            if instance.text not in self.current_tool_question.rooms:
                instance.background_color = (1, 0, 0, 1)

        # for multiple correct answers
        else:
            # document given answers in class instance
            self.current_tool_question.room_answered.append(instance.text)

            if instance.text not in self.current_tool_question.rooms:
                # if, indicate incorrect and all correct answers and close
                instance.background_color = (1, 0, 0, 1)
                # for child in children:
                for child in float_layout.children:
                    if isinstance(child, Button):
                        if child.text in self.current_tool_question.rooms:
                            child.background_color = (0, 1, 0, 1)

                return False  # pass

            else:
                # answer in correct answers
                instance.background_color = (0, 0, 1, 1)

                if self.current_screen == "firetruck_training_with_images":
                    self.tool_label.text += "\n"
                    self.tool_label.text += strings.HINT_STR_MULTIPLE_ANSWERS
                else:
                    self.ids.tool_label.text += "\n"
                    self.ids.tool_label.text += strings.HINT_STR_MULTIPLE_ANSWERS

                return True

    def go_back(self, *args) -> None:
        if self.current_screen in [
            "firetruck_training",
            "firetruck_training_with_images",
            "firetruck_browse",
            "firetruck_images",
        ]:
            change_screen_to("firetruck_menu")

        elif self.current_screen in [
            "highscore_screen",
            "acknowledgement_screen",
            "firetruck_menu",
        ]:
            change_screen_to("start_menu")

        elif self.current_screen == "firetruck_game":
            self.end_game()

        else:
            raise NotImplementedError("go_back() not implemented for this screen!")

    # TESTING
    def set_first_tool(self, tool_name: str):
        for idx, tool in enumerate(self.tool_questions):
            if tool.tool == tool_name:
                # move to end of list, so it is picked next
                self.tool_questions.append(self.tool_questions.pop(idx))
                return
