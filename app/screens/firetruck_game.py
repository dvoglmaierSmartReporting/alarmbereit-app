from kivy.properties import BooleanProperty
from kivy.uix.screenmanager import Screen
from kivy.clock import Clock

from popups.text_popup import TextPopup

from helper.functions import (
    change_screen_to,
    get_firetruck_layouts,
)
from helper.file_handling import (
    save2scores_file,
    get_selected_city_state,
    get_selected_firetruck,
    add2running_score,
)
from helper.settings import Settings
from helper.strings import Strings, GameEndText
from helper.game_class import GameCore
from helper.firetruck_layouts import build_answer_layout

from screens.screen_base import BaseMethods


settings = Settings()
strings = Strings()


class Firetruck_Game(Screen, BaseMethods):
    timer_change_label_visible = BooleanProperty(False)

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

        self.load_score_content()

        self.check_tool_list()

        self.first_tool = True

        self.reset_timer()

        self.update_score_labels()

        Clock.schedule_interval(self.update_timer, settings.FIRETRUCK_GAME_INTERVAL_SEC)

        self.next_tool()

    def next_tool(self, *args):
        self.accept_answers = True

        if len(self.current_tool_list) == 0:
            self.percentages.append(self.current_percentage)

            self.save_score_percentage()

            self.reset_current_tool_list()

            self.update_score_labels()

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

        float = build_answer_layout(self.room_layout, "firetruck_game")

        self.ids.firetruck_rooms_layout.add_widget(float)

    def on_answer(self, instance):
        self.first_tool = False

        if not self.accept_answers:  # Check if answer processing is enabled
            return  # Ignore the button press if answer processing is disabled

        # do not accept identical answer
        if instance.text in self.current_tool_question.room_answered:
            return

        if len(self.current_tool_question.rooms_to_be_answered) <= 1:
            self.single_correct_answer = True
        else:
            self.single_correct_answer = False

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

        # Disable answer processing after an answer is selected
        self.accept_answers = False

        # tool ends here. document tool and given answers in question history
        self.game.questions.append(self.current_tool_question)

        Clock.schedule_once(self.next_tool, settings.FIRETRUCK_GAME_FEEDBACK_SEC)

        self.save_score_content()

    def correct_answer(self):
        self.increment_score()

        self.game.answers_correct += 1

        # increment if all tool answers are correct
        if self.single_correct_answer:
            self.current_correct_answers += 1

        if (
            self.game.answers_correct % settings.FIRETRUCK_GAME_CORRECT_FOR_EXTRA_TIME
            == 0
        ):
            self.add_time()

    def incorrect_answer(self):
        pass

    def end_game(self):
        Clock.unschedule(self.update_timer)

        add2running_score(
            city=self.selected_city,
            to_add=int(self.game.score),
        )

        if self.game.score > self.high:
            self.save_score_content()

        if not self.first_tool:
            message = GameEndText(
                answers_total=self.game.questions_len,
                answers_correct=self.game.answers_correct,
                score=self.game.score,
                is_new_highscore=self.game.score > self.high,
            ).TEXT

            info_popup = TextPopup(
                message=message,
                title=strings.TITLE_INFO_POPUP,
                size_hint=(0.6, 0.6),
            )
            info_popup.open()

        change_screen_to("firetruck_menu")
