from kivy.uix.image import Image
from kivy.uix.floatlayout import FloatLayout
from kivy.graphics import Color, Rectangle
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen
from kivy.uix.progressbar import ProgressBar
from kivy.clock import Clock

from random import shuffle
from typing import cast

from popups.text_popup import TextPopup

from helper.functions import (
    get_ToolQuestion_instances,
    change_screen_to,
    get_firetruck_layouts,
    break_tool_name,
)
from helper.file_handling import (
    save_to_scores_file,
    get_score_value,
    tool_image_file_exists,
    room_image_file_exists,
)
from helper.settings import Settings
from helper.strings import (
    Strings,
    Firetruck_TrainingText_AllTools,
    Firetruck_TrainingText_HalfTools,
)
from helper.game_class import GameCore
from helper.firetruck_layouts import build_answer_layout


settings = Settings()
strings = Strings()


class Firetruck_Training_With_Images(Screen):
    def select_city(self, selected_city: str):
        self.selected_city = selected_city

    def select_firetruck(self, selected_firetruck: str):
        # troubleshooting: fix firetruck
        # self.selected_firetruck = "Tank1" "Rüst+Lösch"
        self.selected_firetruck = selected_firetruck

        self.firetruck_label = cast(Label, self.firetruck_label)
        self.firetruck_label.text = selected_firetruck

        self.room_layout = get_firetruck_layouts(selected_firetruck, self.selected_city)

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

    def reset_progress_bar(self):
        self.ids.progress_bar_answer.max = (
            settings.FIRETRUCK_TRAINING_WITH_IMAGES_FEEDBACK_SEC - 0.3
        )
        self.ids.progress_bar_answer.value = 0

    def play(self):
        # init GameCore class instance
        self.game = GameCore()

        # (re)set game specific elements
        self.reset_tool_list()

        self.reset_progress_bar()

        self.reset_strike()

        # TODO: high_strike already used!
        # decide on wether overwriting or intorducing a new variable
        # or replacing regular training mode
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
        self.ids.tool_image_layout.clear_widgets()

        layout = self.ids.tool_image_layout
        layout.clear_widgets()
        layout.canvas.before.clear()

        # troubleshooting: fix tool
        # self.current_tool = "Handfunkgerät"  # "Druckschlauch B"
        # current_tool = self.tools.pop()
        self.current_tool_question = self.tool_questions.pop()

        self.tool_label = Label(
            text=self.current_tool_question.tool,
            size_hint_y=1,
            font_size="28sp",
        )
        self.ids.tool_image_layout.add_widget(self.tool_label)

        # display image if available
        # tool image file name is either tag or name of tool + ".jpg"
        # if not self.current_tool_question.tool_image_name == "":
        try:
            if not tool_image_file_exists(self.current_tool_question.tool_image_name):
                raise FileNotFoundError()

            tool_image = Image(
                source=self.current_tool_question.tool_image_name,
                fit_mode="contain",
                size_hint_y=3,
            )
            self.ids.tool_image_layout.add_widget(tool_image)
        except Exception as e:
            print(
                f"Tool image load failed. Error: {e}, Tool file: {self.current_tool_question.tool_image_name}"
            )
            # else:
            placeholder = Label(text=strings.ERROR_IMAGE_NOT_FOUND, size_hint_y=3)
            self.ids.tool_image_layout.add_widget(placeholder)

        # display background and buttons
        float = build_answer_layout(self.room_layout, "firetruck_training_with_images")

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

        # Show location image during cooldown if available
        # self.ids.image_box_answer.clear_widgets()
        #
        # room image file name is either tag or name of room + ".jpg"
        #
        # multiple rooms are ignored for now

        if not self.current_tool_question.room_image_name == "":
            layout = self.ids.tool_image_layout
            layout.clear_widgets()
            layout.canvas.before.clear()

            # Set background color only on the layout
            with layout.canvas.before:
                if self.feedback_green:
                    Color(0, 0.5, 0, 1)  # Green
                else:
                    Color(0.5, 0, 0, 1)  # Red
                layout.rect = Rectangle(pos=layout.pos, size=layout.size)

            # Bind layout's pos/size to update the background rectangle
            layout.bind(pos=self.update_rect, size=self.update_rect)

            # tool name Label
            # tool + " in " + room
            tool_answer = f"{self.current_tool_question.tool} in {', '.join(self.current_tool_question.rooms)}"
            tool_label_answer = Label(
                text=break_tool_name(tool_answer, 35),
                size_hint_y=1,
                font_size="20sp",  # "28sp"
            )
            layout.add_widget(tool_label_answer)

            # progress bar

            interval = settings.FIRETRUCK_TRAINING_WITH_IMAGES_FEEDBACK_SEC / 50

            self.ids.progress_bar_answer.value = (
                settings.FIRETRUCK_TRAINING_WITH_IMAGES_FEEDBACK_SEC
            )

            Clock.schedule_interval(self.update_progress_bar, interval)

            # room image
            try:
                if room_image_file_exists(
                    self.selected_city,
                    self.selected_firetruck,
                    self.current_tool_question.room_image_name,
                ):
                    raise FileNotFoundError()

                # Add the image
                room_image = Image(
                    source=self.current_tool_question.room_image_name,
                    fit_mode="contain",
                    size_hint_y=9,
                )
                layout.add_widget(room_image)

            except Exception as e:
                print(f"Room image load failed: {e}")
                # Add a placeholder label if the image is not found
                placeholder = Label(
                    text=strings.ERROR_IMAGE_NOT_FOUND, size_hint=(1, 1)
                )
                layout.add_widget(placeholder)

        Clock.schedule_once(
            self.next_tool, settings.FIRETRUCK_TRAINING_WITH_IMAGES_FEEDBACK_SEC
        )

    def update_rect(self, *args):
        layout = self.ids.tool_image_layout
        if hasattr(layout, "rect"):
            layout.rect.pos = layout.pos
            layout.rect.size = layout.size

    def update_progress_bar(self, dt):
        interval = settings.FIRETRUCK_TRAINING_WITH_IMAGES_FEEDBACK_SEC / 50
        self.progress_bar_answer.value = max(
            0, self.progress_bar_answer.value - interval
        )

        if self.progress_bar_answer.value <= 0:
            Clock.unschedule(
                self.update_progress_bar
            )  # Stop the timer when it reaches 0

    def go_back(self, *args) -> None:
        change_screen_to("firetruck_menu")
