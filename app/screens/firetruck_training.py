from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.screenmanager import Screen
from kivy.clock import Clock

from random import shuffle
from typing import cast

from helper.functions import get_ToolQuestion_instances
from helper.file_handling import save_to_scores_file, get_scores_key
from helper.settings import Settings, Strings
from helper.game_class import GameCore


settings = Settings()
strings = Strings()


class Fahrzeugkunde_Training(Screen):
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

        self.current_high_strike = get_scores_key(
            self.selected_firetruck, "high_strike"
        )

        self.update_high_strike_label()

        self.next_tool()

    def get_7_rooms_layout(self) -> list[tuple[str, float, float, float, float]]:
        return [
            ("Fahrer / GK", 0.5, 0.15, 0.25, 1),
            ("Mannschaft", 0.5, 0.16, 0.25, 0.85),
            ("G1", 0.27, 0.175, 0.085, 0.68),
            ("G3", 0.205, 0.175, 0.15, 0.505),
            ("G5", 0.27, 0.175, 0.085, 0.33),
            ("G2", 0.27, 0.175, 0.65, 0.68),
            ("G4", 0.205, 0.175, 0.65, 0.505),
            ("G6", 0.27, 0.175, 0.65, 0.33),
            ("G7 / Heck", 0.4, 0.145, 0.3, 0.145),
            ("Dach", 0.2, 0.4, 0.4, 0.61),
        ]

    def get_5_rooms_layout(self) -> list[tuple[str, float, float, float, float]]:
        return [
            ("Fahrer / GK", 0.5, 0.15, 0.25, 1),
            ("Mannschaft", 0.5, 0.16, 0.25, 0.85),
            ("G1", 0.27, 0.175, 0.085, 0.68),
            ("G3", 0.205, 0.35, 0.15, 0.505),
            ("G2", 0.27, 0.175, 0.65, 0.68),
            ("G4", 0.205, 0.35, 0.65, 0.505),
            ("G5 / Heck", 0.4, 0.145, 0.3, 0.145),
            ("Dach", 0.2, 0.4, 0.4, 0.61),
        ]

    def get_leiter_layout(self):
        return [
            ("Korb", 0.3, 0.13, 0.35, 1),
            ("Mannschaft", 0.55, 0.155, 0.225, 0.86),
            ("G1", 0.27, 0.2, 0.085, 0.68),
            ("G3", 0.185, 0.185, 0.085, 0.45),
            ("G5", 0.185, 0.125, 0.085, 0.14),
            ("G2", 0.27, 0.2, 0.65, 0.68),
            ("G4", 0.185, 0.185, 0.735, 0.45),
            ("G6", 0.185, 0.125, 0.735, 0.14),
            ("Dach", 0.28, 0.43, 0.43, 0.45),
        ]

    def get_voraus_layout(self):
        return [
            ("Fahrer / GK", 0.55, 0.13, 0.225, 0.90),
            ("Mannschaft", 0.55, 0.13, 0.225, 0.75),
            ("G1", 0.22, 0.415, 0.18, 0.61),
            ("G1\ntief", 0.1, 0.155, 0.08, 0.35),
            ("G2", 0.22, 0.415, 0.605, 0.61),
            ("G2\ntief", 0.1, 0.155, 0.825, 0.35),
            ("G3", 0.4, 0.185, 0.3, 0.19),
        ]

    def get_ruest_layout(self):
        return [
            ("Mannschaft", 0.55, 0.13, 0.225, 0.99),
            ("G1\nlinks", 0.15, 0.22, 0.08, 0.81),
            ("G1\ninnen", 0.15, 0.45, 0.23, 0.81),
            ("G1\nrechts", 0.15, 0.22, 0.08, 0.58),
            ("G3", 0.23, 0.265, 0.15, 0.355),
            ("G2\nrechts", 0.15, 0.22, 0.77, 0.81),
            ("G2\ninnen", 0.15, 0.45, 0.62, 0.81),
            ("G2\nlinks", 0.15, 0.22, 0.77, 0.58),
            ("G4", 0.23, 0.265, 0.62, 0.355),
            ("G5 / Heck", 0.4, 0.08, 0.3, 0.085),
            ("Dach", 0.2, 0.4, 0.4, 0.61),
        ]

    def build_answer_layout(self, firetruck: str) -> FloatLayout:
        # display background and buttons
        float = FloatLayout(size_hint=(1, 1))

        if firetruck in ["RüstLösch", "Tank1", "TankDürrnberg"]:
            bgd_image = "./assets/layouts/truck.jpg"
            buttons = self.get_7_rooms_layout()

        elif firetruck in ["Pumpe", "PumpeDürrnberg"]:
            bgd_image = "./assets/layouts/truck.jpg"
            buttons = self.get_5_rooms_layout()

        elif firetruck in ["Leiter"]:
            bgd_image = "./assets/layouts/leiter.jpg"
            buttons = self.get_leiter_layout()

        elif firetruck in ["Rüst"]:
            bgd_image = "./assets/layouts/ruest.jpg"
            buttons = self.get_ruest_layout()

        elif firetruck in ["Voraus"]:
            bgd_image = "./assets/layouts/voraus.jpg"
            buttons = self.get_voraus_layout()

        else:
            raise NotImplementedError

        background = Image(
            source=bgd_image,
            fit_mode="fill",
            size_hint=(1, 1),
            pos_hint={"center_x": 0.5, "center_y": 0.5},
        )
        float.add_widget(background)

        # room setup for RüstLösch == TestTruck

        for text, w, h, x, top in buttons:
            btn = Button(
                text=text,
                font_size="25sp",
                background_color=(0.7, 0.7, 0.7, 0.7),
                size_hint=(w, h),
                pos_hint={"x": x, "top": top},
            )
            btn.bind(on_press=self.on_answer)
            float.add_widget(btn)

        return float

    def next_tool(self, *args):
        self.accept_answers = True  # Enable answer processing for the new tool

        if len(self.tool_questions) == 0:
            self.reset_tool_list()

        # Reset image boxes
        self.ids.firetruck_rooms_layout.clear_widgets()

        # troubleshooting: fix tool
        # self.current_tool = "Handfunkgerät"  # "Druckschlauch B"
        self.current_tool_question = self.tool_questions.pop()

        self.tool_label = cast(Label, self.tool_label)

        self.tool_label.text = self.current_tool_question.tool

        # for storage in self.firetruck_rooms:
        #     btn = Button(text=storage, font_size="28sp", disabled=storage == "")
        #     btn.bind(on_press=self.on_answer)
        #     self.ids.firetruck_rooms_layout.add_widget(btn)

        float = self.build_answer_layout(self.selected_firetruck)

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

        # self.reset_strike()
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
        # children = self.ids.firetruck_rooms_layout.children  # children is reversed
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

        Clock.schedule_once(self.next_tool, settings.FIRETRUCK_TRAINING_FEEDBACK_SEC)
