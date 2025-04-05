from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.screenmanager import Screen
from kivy.clock import Clock
from kivy.graphics import Color, Rectangle

from random import shuffle
from typing import cast

from helper.functions import get_ToolQuestion_instances
from helper.file_handling import save_to_scores_file, get_score_value
from helper.settings import Settings, Strings
from helper.game_class import GameCore


settings = Settings()
strings = Strings()


class Fahrzeugkunde_Training_New(Screen):
    def select_firetruck(self, selected_firetruck: str):
        # troubleshooting: fix firetruck
        # self.selected_firetruck = "Tank1" "Rüst+Lösch"
        self.selected_firetruck = selected_firetruck

        self.firetruck_label = cast(Label, self.firetruck_label)
        self.firetruck_label.text = selected_firetruck

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
            self.selected_firetruck
        )

        shuffle(self.tool_questions)

    def play(self):
        # init GameCore class instance
        self.game = GameCore()

        # (re)set game specific elements
        self.reset_tool_list()

        self.reset_strike()

        self.current_high_strike = get_score_value(
            self.selected_firetruck, "high_strike"
        )

        self.update_high_strike_label()

        self.next_tool()

    def next_tool(self, *args):
        self.accept_answers = True  # Enable answer processing for the new tool

        if len(self.tool_questions) == 0:
            self.reset_tool_list()

        # Reset image boxes
        self.ids.firetruck_rooms_layout.clear_widgets()

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
        if not self.current_tool_question.tool_image_name == "":
            try:
                tool_image = Image(
                    source=self.current_tool_question.tool_image_name,
                    fit_mode="contain",
                    size_hint_y=3,
                )
                self.ids.tool_image_layout.add_widget(tool_image)
            except Exception as e:
                print(f"Tool image load failed: {e}")
        else:
            placeholder = Label(text="", size_hint_y=3)
            self.ids.tool_image_layout.add_widget(placeholder)

        # display background and buttons
        float = FloatLayout(size_hint=(1, 1))

        background = Image(
            source="./assets/truck_RL/top_down.jpg",
            fit_mode="fill",
            size_hint=(1, 1),
            pos_hint={"center_x": 0.5, "center_y": 0.5},
        )
        float.add_widget(background)

        # room setup for RüstLösch == TestTruck
        buttons = [
            ("Fahrer / GK", 0.5, 0.15, 0.25, 1),
            ("Mannschaft", 0.5, 0.15, 0.25, 0.85),
            ("G1", 0.25, 0.185, 0.1, 0.70),
            ("G3", 0.25, 0.185, 0.1, 0.515),
            ("G5", 0.25, 0.185, 0.1, 0.33),
            ("G2", 0.25, 0.185, 0.65, 0.70),
            ("G4", 0.25, 0.185, 0.65, 0.515),
            ("G6", 0.25, 0.185, 0.65, 0.33),
            ("G7 / Heck", 0.4, 0.145, 0.3, 0.145),
            ("Dach", 0.2, 0.4, 0.4, 0.61),
        ]

        for text, w, h, x, top in buttons:
            btn = Button(
                text=text,
                background_color=(0.5, 0.5, 0.5, 0.5),
                size_hint=(w, h),
                pos_hint={"x": x, "top": top},
            )
            btn.bind(on_press=self.on_answer)
            float.add_widget(btn)

        self.ids.firetruck_rooms_layout.add_widget(float)

    def correct_answer(self):
        self.increment_strike()

        self.game.answers_correct_total += settings.FIRETRUCK_TRAINING_CORRECT_POINTS

        if self.game.answers_correct_strike > self.current_high_strike:
            self.current_high_strike = self.game.answers_correct_strike
            self.update_high_strike_label()
            save_to_scores_file(
                self.selected_firetruck, "high_strike", self.game.answers_correct_strike
            )

        self.feedback_green = True

    def incorrect_answer(self):
        self.feedback_green = False

        Clock.schedule_once(self.reset_strike, settings.FIRETRUCK_TRAINING_FEEDBACK_SEC)

        # todo: check for PB score!

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

        # children = self.firetruck_rooms_layout.children
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
                instance.background_color = (0, 1, 0, 1)

                # display hint for multiple answers
                # if self.tool_label.text[-7:] == strings.HINT_STR_MULTIPLE_ANSWERS:
                #     self.tool_label.text += " "
                # else:
                #     self.tool_label.text += "\n"
                # self.tool_label.text += strings.HINT_STR_MULTIPLE_ANSWERS

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
        if self.current_tool_question.room_image_name != "":
            layout = self.ids.tool_image_layout

            # Clear old widgets (images, etc.)
            layout.clear_widgets()

            # Clear old canvas instructions
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

            # Add the image
            cooldown_image = Image(
                source=self.current_tool_question.room_image_name,
                fit_mode="contain",
                size_hint=(1, 1),
            )
            layout.add_widget(cooldown_image)

        Clock.schedule_once(
            self.next_tool, settings.FIRETRUCK_TRAINING_NEW_FEEDBACK_SEC
        )

    def update_rect(self, *args):
        layout = self.ids.tool_image_layout
        if hasattr(layout, "rect"):
            layout.rect.pos = layout.pos
            layout.rect.size = layout.size
