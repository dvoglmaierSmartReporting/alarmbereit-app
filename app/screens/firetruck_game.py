from kivy.app import App
from kivy.uix.button import Button
from kivy.properties import BooleanProperty
from kivy.uix.screenmanager import Screen
from kivy.clock import Clock


from random import shuffle

from helper.functions import get_firetruck_storage, break_tool_name
from helper.file_handling import save_to_scores_file, get_scores_key
from helper.settings import Settings
from helper.game_class import GameCore, ToolQuestion


settings = Settings()


class Fahrzeugkunde_Game(Screen):
    timer_change_label_visible = BooleanProperty(False)
    # timer_change_add = BooleanProperty(True)

    def select_firetruck(self, selected_firetruck: str):
        # troubleshooting: fix firetruck
        # self.selected_firetruck = "Tank1" "Rüst+Lösch"
        self.selected_firetruck = selected_firetruck
        self.firetruck_label.text = f"   {selected_firetruck}"  # type: ignore

    def hide_label(self, *args):
        self.extra_time_label.opacity = 0  # type: ignore

    def reset_timer(self):
        self.time_left = settings.FIRETRUCK_START_TIME_SEC

        # self.timer_label.text = f"{str(self.time_left)} s  "
        self.timer_label.text = f""  # type: ignore

        # self.set_progress_bar()
        self.progress_bar.max = settings.FIRETRUCK_START_TIME_SEC  # type: ignore

    def add_time(self):
        self.time_left = round(self.time_left + settings.FIRETRUCK_EXTRA_TIME_SEC, 1)

        self.extra_time_label.text = f"+ {settings.FIRETRUCK_EXTRA_TIME_SEC} s  "  # type: ignore

        self.extra_time_label.opacity = 1  # type: ignore

        Clock.schedule_once(
            self.hide_label,
            settings.DISPLAY_EXTRA_TIME_LABEL_SEC,
        )

    def update_progress_bar(self):
        self.progress_bar.value = self.time_left  # type: ignore

    def update_timer(self, *args):
        # update game time
        self.update_progress_bar()

        if self.time_left > 0.0:
            self.time_left = round(self.time_left - settings.INTERVAL_GAME_SEC, 1)

            if not self.time_left == 0.0:
                # self.timer_label.text = f"{str(self.time_left)} s  "
                self.timer_label.text = f""  # hide label for UI testing  # type: ignore

            else:
                self.timer_label.text = "Ende  "  # type: ignore
                # todo: disable buttons between game end and menu screen animation
        else:
            # Clock.unschedule(self.update_timer)  # Stop the timer when it reaches 0
            self.end_game()
            pass

    def increment_score(self, add: int = settings.FIRETRUCK_CORRECT_POINTS):
        self.game.score += add
        self.score_label.text = f"{str(self.game.score)}  "  # type: ignore

    def update_score_labels(self):
        self.score_label.text = f"{str(self.game.score)}  "  # type: ignore
        self.high_score_label.text = f"Best: {str(self.current_high_score)}  "  # type: ignore

    def end_game(self):
        Clock.unschedule(self.update_timer)

        if self.game.score > self.current_high_score:
            save_to_scores_file(self.selected_firetruck, "high_score", self.game.score)

        app = App.get_running_app()
        app.root.current = "fahrzeugkunde_menu"  # type: ignore
        app.root.transition.direction = "right"  # type: ignore

    def reset_tool_list(self):
        (self.firetruck_rooms, self.tools, self.tools_locations) = (
            get_firetruck_storage(self.selected_firetruck)
        )

        shuffle(self.tools)

    def play(self):
        # init GameCore class instance
        self.game = GameCore()

        # (re)set game specific elements
        self.reset_tool_list()

        self.reset_timer()

        self.current_high_score = get_scores_key(
            firetruck=self.selected_firetruck,
            key="high_score",
        )

        self.update_score_labels()

        Clock.schedule_interval(self.update_timer, settings.INTERVAL_GAME_SEC)

        # start game
        self.next_tool()

    def next_tool(self, *args):
        self.accept_answers = True  # Enable answer processing for the new tool

        if len(self.tools) == 0:
            self.reset_tool_list()

        current_tool = self.tools.pop()

        self.current_question = ToolQuestion(
            firetruck=self.selected_firetruck,
            tool=current_tool,
            rooms=list(set(self.tools_locations.get(current_tool))),  # type: ignore
        )

        self.tool_label.text = break_tool_name(self.current_question.tool)  # type: ignore

        self.firetruck_rooms_layout.clear_widgets()  # type: ignore

        for storage in self.firetruck_rooms:
            btn = Button(text=storage, font_size="28sp")
            btn.bind(on_press=self.on_answer)  # type: ignore
            self.firetruck_rooms_layout.add_widget(btn)  # type: ignore

    def correct_answer(self):
        self.increment_score()

        self.game.answers_correct_total += 1

        if (
            self.game.answers_correct_total % settings.FIRETRUCK_CORRECT_FOR_EXTRA_TIME
            == 0
        ):
            self.add_time()

    def incorrect_answer(self):
        pass

    def on_answer(self, instance):
        if not self.accept_answers:  # Check if answer processing is enabled
            return  # Ignore the button press if answer processing is disabled

        # do not accept identical answer
        if instance.text in self.current_question.room_answered:
            return

        # process actual answer
        if instance.text in self.current_question.rooms:
            self.correct_answer()

        else:
            self.incorrect_answer()

        children = self.firetruck_rooms_layout.children  # type: ignore

        # indicate if correct or incorrect answer
        # for single correct answer
        if len(self.current_question.rooms_to_be_answered) <= 1:
            # always identify and indicate the correct answer
            for child in children:
                if child.text in self.current_question.rooms:
                    child.background_color = (0, 1, 0, 1)
            # if, indicate incorrect answer
            if instance.text not in self.current_question.rooms:
                instance.background_color = (1, 0, 0, 1)

        # for multiple correct answers
        else:
            # document given answers in class instance
            # todo: add if answer was correct
            self.current_question.room_answered.append(instance.text)

            if instance.text not in self.current_question.rooms:
                # if, indicate incorrect and all correct answers and close
                instance.background_color = (1, 0, 0, 1)
                for child in children:
                    if child.text in self.current_question.rooms:
                        child.background_color = (0, 1, 0, 1)
                pass

            else:
                # answer in correct answers
                instance.background_color = (0, 1, 0, 1)

                # display string "weitere"
                if self.tool_label.text[-7:] == "weitere":  # type: ignore
                    self.tool_label.text += " "  # type: ignore
                else:
                    self.tool_label.text += "\n"  # type: ignore
                self.tool_label.text += "weitere"  # type: ignore
                return

        # document given answers in class instance
        self.current_question.room_answered.append(instance.text)

        self.accept_answers = (
            False  # Disable answer processing after an answer is selected
        )

        # tool ends here. document tool and given answers in question history
        self.game.questions.append(self.current_question)

        Clock.schedule_once(self.next_tool, settings.FEEDBACK_GAME_SEC)
