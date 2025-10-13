from kivy.uix.button import Button
from kivy.uix.screenmanager import Screen
from kivy.animation import Animation
from kivy.clock import Clock

from helper.file_handling import (
    get_selected_city_state,
    get_selected_firetruck,
)
from helper.settings import Settings
from helper.strings import Strings
from helper.game_class import GameCore
from helper.firetruck_layouts import build_answer_layout  # , build_second_answer_layout

from screens.screen_base import BaseMethods


settings = Settings()
strings = Strings()


class Firetruck_Exam(Screen, BaseMethods):
    def on_pre_enter(self):
        self.selected_city, _ = get_selected_city_state()

        self.selected_firetruck = get_selected_firetruck()

        self.current_screen = self.get_current_screen()

        self.ids.firetruck_label.text = self.selected_firetruck

        # ?

    def play(self):
        self.game = GameCore()

        self.first_layout = None
        self.second_layout = None

        self.reset_tool_list()

        self.load_high_score()

        self.reset_score()

        self.update_score_labels()

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

        # troubleshooting: fix first popped tool
        # self.set_first_tool("Unterlegplatte")  # for testing
        self.current_tool_question = self.tool_questions.pop()

        self.ids.tool_label.text = self.current_tool_question.tool

        self.first_layout = build_answer_layout(
            self.selected_firetruck, "fahrzeugkunde_exam"
        )
        self.first_layout.pos_hint = {"x": 0}
        self.ids.firetruck_rooms_layout.add_widget(self.first_layout)

    def on_answer(self, instance):
        if not self.accept_answers:  # Check if answer processing is enabled
            return  # Ignore the button press if answer processing is disabled

        # do not accept identical answer
        if instance.text in self.current_tool_question.room_answered:
            return

        if self.color_layout(instance):
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
