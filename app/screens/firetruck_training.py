from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen
from kivy.clock import Clock

from random import shuffle
from typing import cast

from popups.text_popup import TextPopup

from helper.functions import (
    get_ToolQuestion_instances,
    change_screen_to,
    get_firetruck_layout_value,
)
from helper.file_handling import save_to_scores_file, get_score_value
from helper.settings import (
    Settings,
    Strings,
    Firetruck_TrainingText_AllTools,
    Firetruck_TrainingText_HalfTools,
)
from helper.game_class import GameCore
from helper.firetruck_layouts import build_answer_layout


settings = Settings()
strings = Strings()


class Firetruck_Training(Screen):
    def select_city(self, selected_city: str):
        self.selected_city = selected_city

    def select_firetruck(self, selected_firetruck: str):
        # troubleshooting: fix firetruck
        # self.selected_firetruck = "Tank1" "Rüst+Lösch"
        self.selected_firetruck = selected_firetruck

        self.firetruck_label = cast(Label, self.firetruck_label)
        self.firetruck_label.text = selected_firetruck

        self.room_layout = get_firetruck_layout_value(
            selected_firetruck, self.selected_city
        )

    def update_strike_label(self):
        self.strike_label = cast(Label, self.strike_label)
        self.strike_label.text = str(self.game.answers_correct_strike)

    def update_high_strike_label(self):
        self.high_strike_label = cast(Label, self.high_strike_label)
        self.high_strike_label.text = f"Best: {str(self.current_high_strike)}"

    def reset_strike(self, *arg):
        self.game.answers_correct_strike = 0
        self.update_strike_label()

    def increment_strike(self):
        self.game.answers_correct_strike += settings.FIRETRUCK_TRAINING_CORRECT_POINTS
        self.update_strike_label()

    def reset_tool_list(self):
        (self.firetruck_rooms, self.tool_questions) = get_ToolQuestion_instances(
            self.selected_firetruck, self.selected_city
        )
        self.tool_amount = len(self.tool_questions)

        shuffle(self.tool_questions)

    def play(self):
        # init GameCore class instance
        self.game = GameCore()

        # (re)set game specific elements
        self.reset_tool_list()

        self.reset_strike()

        self.current_high_strike = get_score_value(
            city=self.selected_city,
            questions="firetrucks",
            truck_or_comp=self.selected_firetruck,
            key="high_strike",
        )

        self.update_high_strike_label()

        self.next_tool()

    def next_tool(self, *args):
        self.accept_answers = True  # Enable answer processing for the new tool

        if len(self.tool_questions) == 0:
            self.reset_tool_list()

            # all tools have been trained
            info_popup = TextPopup(
                message=Firetruck_TrainingText_AllTools(self.tool_amount).TEXT,
                title=strings.TITLE_INFO_POPUP,
                size_hint=(0.6, 0.6),
            )
            info_popup.open()

        if len(self.tool_questions) == self.tool_amount // 2:
            # half of tools have been trained
            info_popup = TextPopup(
                message=Firetruck_TrainingText_HalfTools(self.tool_amount).TEXT,
                title=strings.TITLE_INFO_POPUP,
                size_hint=(0.6, 0.6),
            )
            info_popup.open()

        # Reset image boxes
        self.ids.firetruck_rooms_layout.clear_widgets()

        # troubleshooting: fix tool
        # self.current_tool = "Handfunkgerät"  # "Druckschlauch B"
        self.current_tool_question = self.tool_questions.pop()

        self.tool_label = cast(Label, self.tool_label)

        self.tool_label.text = self.current_tool_question.tool

        float = build_answer_layout(self.room_layout, "firetruck_training")

        self.ids.firetruck_rooms_layout.add_widget(float)

    def correct_answer(self):
        self.increment_strike()

        self.game.answers_correct_total += settings.FIRETRUCK_TRAINING_CORRECT_POINTS

        if self.game.answers_correct_strike > self.current_high_strike:
            self.current_high_strike = self.game.answers_correct_strike
            self.update_high_strike_label()
            save_to_scores_file(
                city=self.selected_city,
                questions="firetrucks",
                truck_or_comp=self.selected_firetruck,
                key="high_strike",
                value=self.game.answers_correct_strike,
            )

        self.feedback_green = True

    def incorrect_answer(self):
        self.feedback_green = False

        # self.reset_strike()
        Clock.schedule_once(self.reset_strike, settings.FIRETRUCK_TRAINING_FEEDBACK_SEC)

    def on_answer(self, instance):
        if not self.accept_answers:  # Check if answer processing is enabled
            return  # Ignore the button press if answer processing is disabled

        # do not accept identical answer
        if instance.text in self.current_tool_question.room_answered:
            return

        # process actual answer
        if instance.text in self.current_tool_question.rooms:
            self.correct_answer()

        else:
            self.incorrect_answer()

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
                pass

            else:
                # answer in correct answers
                instance.background_color = (0, 0, 1, 1)

                self.tool_label.text += "\n"
                self.tool_label.text += strings.HINT_STR_MULTIPLE_ANSWERS

                return

        # document given answers in class instance
        self.current_tool_question.room_answered.append(instance.text)

        self.accept_answers = (
            False  # Disable answer processing after an answer is selected
        )

        # tool ends here. document tool and given answers in question history
        self.game.questions.append(self.current_tool_question)

        Clock.schedule_once(self.next_tool, settings.FIRETRUCK_TRAINING_FEEDBACK_SEC)

    def go_back(self, *args) -> None:
        change_screen_to("firetruck_menu")
