from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen
from kivy.animation import Animation
from kivy.clock import Clock

from random import shuffle

from helper.functions import get_ToolQuestion_instances, change_screen_to
from helper.file_handling import save_to_scores_file, get_score_value
from helper.settings import Settings, Strings
from helper.game_class import GameCore
from helper.firetruck_layouts import build_answer_layout, build_second_answer_layout


settings = Settings()
strings = Strings()


class Firetruck_Exam(Screen):
    def select_firetruck(self, selected_firetruck: str):
        # troubleshooting: fix firetruck
        # self.selected_firetruck = "Tank1" "Rüst+Lösch"
        self.selected_firetruck = selected_firetruck

        self.ids.firetruck_label.text = selected_firetruck

    def update_strike_label(self):
        self.ids.strike_label.text = str(self.game.answers_correct_strike)

    def update_high_strike_label(self):
        self.ids.high_strike_label.text = f"Best: {str(self.current_high_strike)}"

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
        # init GameCore class instance and layouts
        self.game = GameCore()
        self.first_layout = None
        self.second_layout = None

        # (re)set game specific elements
        self.reset_tool_list()

        self.reset_strike()

        self.current_high_strike = get_score_value(
            self.selected_firetruck, "high_strike"
        )

        self.update_high_strike_label()

        self.next_tool()

    def transit_out(self, dt):
        self.second_layout = build_second_answer_layout("G1", "fahrzeugkunde_exam")
        self.second_layout.pos_hint = {"x": 1}  # start off-screen right

        self.ids.firetruck_rooms_layout.add_widget(self.second_layout)

        # Animate both layouts at the same time
        anim_out = Animation(pos_hint={"x": -1}, duration=0.5)
        anim_in = Animation(pos_hint={"x": 0}, duration=0.5)

        anim_out.start(self.first_layout)  # move first layout out
        anim_in.start(self.second_layout)  # move second layout in

    def next_tool(self, *args):
        self.accept_answers = True  # Enable answer processing for the new tool

        if len(self.tool_questions) == 0:
            self.reset_tool_list()

        # Reset image boxes
        self.ids.firetruck_rooms_layout.clear_widgets()

        # troubleshooting: fix tool
        # self.current_tool = "Handfunkgerät"  # "Druckschlauch B"
        self.current_tool_question = self.tool_questions.pop()

        self.ids.tool_label.text = self.current_tool_question.tool

        self.first_layout = build_answer_layout(
            self.selected_firetruck, "fahrzeugkunde_exam"
        )
        self.first_layout.pos_hint = {"x": 0}
        self.ids.firetruck_rooms_layout.add_widget(self.first_layout)

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

                self.ids.tool_label.text += "\n"
                self.ids.tool_label.text += strings.HINT_STR_MULTIPLE_ANSWERS

                return

        # document given answers in class instance
        self.current_tool_question.room_answered.append(instance.text)

        self.accept_answers = (
            False  # Disable answer processing after an answer is selected
        )

        # tool ends here. document tool and given answers in question history
        self.game.questions.append(self.current_tool_question)

        # process actual answer
        if instance.text in self.current_tool_question.rooms:
            self.correct_answer()

            Clock.schedule_once(
                self.transit_out, settings.FIRETRUCK_TRAINING_FEEDBACK_SEC
            )

        else:
            self.incorrect_answer()

            Clock.schedule_once(
                self.next_tool, settings.FIRETRUCK_TRAINING_FEEDBACK_SEC
            )

    def on_second_answer(self, instance):
        if not self.accept_answers:
            return

        float_layout = self.second_layout

        for child in float_layout.children:
            if (
                isinstance(child, Button)
                and child.text in self.current_tool_question.rooms
            ):
                child.background_color = (0, 1, 0, 1)

        if instance.text not in self.current_tool_question.rooms:
            instance.background_color = (1, 0, 0, 1)

        self.current_tool_question.room_answered.append(instance.text)
        self.accept_answers = False
        self.game.questions.append(self.current_tool_question)

        if instance.text in self.current_tool_question.rooms:
            self.correct_answer()
        else:
            self.incorrect_answer()

        Clock.schedule_once(
            self.transition_back_to_first, settings.FIRETRUCK_TRAINING_FEEDBACK_SEC
        )

    def transition_back_to_first(self, dt):
        # Remove old first layout if it's still present
        if self.first_layout in self.ids.firetruck_rooms_layout.children:
            self.ids.firetruck_rooms_layout.remove_widget(self.first_layout)

        self.next_tool()  # recreate and assign new first_layout

        # Start first layout off-screen left
        self.first_layout.pos_hint = {"x": -1}
        self.ids.firetruck_rooms_layout.add_widget(self.first_layout)

        # Animate both
        anim_in = Animation(pos_hint={"x": 0}, duration=0.5)
        anim_out = Animation(pos_hint={"x": 1}, duration=0.5)

        anim_in.start(self.first_layout)
        anim_out.bind(on_complete=lambda *args: self.cleanup_second_layout())
        anim_out.start(self.second_layout)

    def cleanup_second_layout(self):
        if (
            self.second_layout
            and self.second_layout in self.ids.firetruck_rooms_layout.children
        ):
            self.ids.firetruck_rooms_layout.remove_widget(self.second_layout)
            self.second_layout = None

    def go_back(self, *args) -> None:
        change_screen_to("firetruck_menu")
