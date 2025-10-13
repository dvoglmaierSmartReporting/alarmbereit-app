from kivy.uix.screenmanager import Screen
from kivy.clock import Clock

from popups.text_popup import TextPopup

from helper.functions import get_firetruck_layouts
from helper.file_handling import (
    get_selected_city_state,
    get_selected_firetruck,
)
from helper.settings import Settings
from helper.strings import (
    Strings,
    Firetruck_TrainingText_AllTools,
    Firetruck_TrainingText_HalfTools,
)
from helper.game_class import GameCore
from helper.firetruck_layouts import build_answer_layout

from screens.screen_base import BaseMethods


settings = Settings()
strings = Strings()


class Firetruck_Training(Screen, BaseMethods):
    def on_pre_enter(self):
        self.selected_city, _ = get_selected_city_state()

        self.selected_firetruck = get_selected_firetruck()

        self.current_screen = self.get_current_screen()

        self.ids.firetruck_label.text = self.selected_firetruck

        self.room_layout = get_firetruck_layouts(
            self.selected_firetruck, self.selected_city
        )

        self.play()

    def play(self):
        self.game = GameCore()

        self.reset_tool_list()

        self.load_high_score()

        self.reset_score()

        self.next_tool()

    def next_tool(self, *args):
        self.accept_answers = True

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

        # troubleshooting: fix first popped tool
        # self.set_first_tool("Unterlegplatte")  # for testing
        self.current_tool_question = self.tool_questions.pop()

        self.ids.tool_label.text = self.current_tool_question.tool

        float = build_answer_layout(self.room_layout, "firetruck_training")

        self.ids.firetruck_rooms_layout.add_widget(float)

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

        if self.color_layout(instance):
            return

        # document given answers in class instance
        self.current_tool_question.room_answered.append(instance.text)

        self.accept_answers = (
            False  # Disable answer processing after an answer is selected
        )

        # tool ends here. document tool and given answers in question history
        self.game.questions.append(self.current_tool_question)

        Clock.schedule_once(self.next_tool, settings.FIRETRUCK_TRAINING_FEEDBACK_SEC)
