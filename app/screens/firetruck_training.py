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
    TrainingText_AllTools,
    TrainingText_HalfTools,
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

        self.load_default_tool_list()

        self.get_current_tool_list()

        self.first_tool = True

        self.check_tool_list()

        self.load_high_score()

        self.reset_score()

        self.next_tool()

    def next_tool(self, *args):
        self.accept_answers = True

        if len(self.current_tool_list) == 0:
            self.reset_current_tool_list()

            self.save_truck_data(key="set", value=self.current_tool_list, current=True)

            if not self.first_tool:
                self.correct_answers = self.get_truck_data(
                    "correct_answers", current=True
                )

                percentage = round(
                    (self.correct_answers / self.set_length) * 100.0,
                    1,
                )

                results = self.get_truck_data("percentages")
                if results is None:
                    results = []

                # keep in 2 lines; append is returning None
                results.append(percentage)
                self.save_truck_data(key="percentages", value=results)

                # all tools have been trained
                info_popup = TextPopup(
                    message=TrainingText_AllTools(
                        self.set_length, self.correct_answers, self.percentage
                    ).TEXT,
                    title=strings.TITLE_INFO_POPUP,
                    size_hint=(0.6, 0.6),
                )
                info_popup.open()

            self.save_truck_data(key="correct_answers", value=0, current=True)

            self.update_score_labels()

        if len(self.current_tool_list) == self.set_length // 2:
            # half of tools have been trained

            self.correct_answers = self.get_truck_data("correct_answers", current=True)

            info_popup = TextPopup(
                message=TrainingText_HalfTools(
                    self.set_length, self.correct_answers, self.percentage
                ).TEXT,
                title=strings.TITLE_INFO_POPUP,
                size_hint=(0.6, 0.6),
            )
            info_popup.open()

        # Reset image boxes
        self.ids.firetruck_rooms_layout.clear_widgets()

        # troubleshooting: fix first popped tool
        # self.set_first_tool("Unterlegplatte")  # for testing
        self.current_tool_name = self.current_tool_list.pop()

        self.current_tool_question = [
            item
            for item in self.default_tool_list
            if item.tool == self.current_tool_name
        ][0]

        self.ids.tool_label.text = self.current_tool_question.tool

        float = build_answer_layout(self.room_layout, "firetruck_training")

        self.ids.firetruck_rooms_layout.add_widget(float)

    def on_answer(self, instance):
        self.first_tool = False

        if not self.accept_answers:  # Check if answer processing is enabled
            return  # Ignore the button press if answer processing is disabled

        self.save_truck_data(key="set", value=self.current_tool_list, current=True)

        # do not accept identical answer
        if instance.text in self.current_tool_question.room_answered:
            return

        # process actual answer
        if instance.text in self.current_tool_question.rooms:
            self.correct_answer()

        else:
            self.incorrect_answer()

        self.update_score_labels()

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
