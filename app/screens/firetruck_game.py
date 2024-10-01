from kivy.app import App
from kivy.uix.button import Button
from kivy.properties import BooleanProperty
from kivy.uix.screenmanager import Screen
from kivy.clock import Clock


from random import shuffle
import yaml

from helper.functions import load_firetruck_storage
from helper.settings import Settings
from helper.game_class import GameCore, ToolQuestion


settings = Settings()


class Fahrzeugkunde_Game(Screen):
    timer_change_label_visible = BooleanProperty(False)
    timer_change_add = BooleanProperty(True)

    def select_firetruck(self, selected_firetruck: str):
        # troubleshooting: fix firetruck
        # self.selected_firetruck = "Tank1" "Rüst+Lösch"
        self.selected_firetruck = selected_firetruck
        self.firetruck_label.text = f"   {selected_firetruck}"  # type: ignore

    def forward_mode_2_fk_game(self, mode: tuple):
        self.mode_training: bool = mode[0]
        self.mode_game: bool = mode[1]
        self.mode_browse: bool = mode[2]
        self.mode_images: bool = mode[3]

    # def display_timer_change_label(self, *args):
    #     # state switch between True and False
    #     self.timer_change_label_visible = not self.timer_change_label_visible

    # def display_timer_change_add(self):
    #     self.timer_change_add = not self.timer_change_add

    def reset_timer(self):
        self.time_left = settings.START_TIME_GAME_SEC
        # self.timer_label.text = f"{str(self.time_left)} s  "
        self.timer_label.text = f""  # type: ignore

        self.set_progress_bar()

    def reset_extra_timer(self):
        # init self.counter

        # for testing...
        # self.extra_time_left = settings.MAX_EXTRA_TIME_SEC
        # factor = self.tool_counter % settings.RENEW_EXTRA_TIME_INT
        factor = 10 % settings.RENEW_EXTRA_TIME_INT  # to be fixed!!
        self.extra_time_left = max(
            settings.MAX_EXTRA_TIME_SEC - factor * settings.EXTRA_TIME_REDUCTION_SEC,
            0,
        )

        # self.extra_time_label.text = f"{str(self.extra_time_left)} s  "

    # def reset_tool_counter(self):
    #     self.tool_counter = 0

    def add_time(self):
        # max extra time reduces during game
        # extra_time = max(settings.MAX_EXTRA_TIME_SEC - self.tool_counter * settings.EXTRA_TIME_REDUCTION_SEC, 0)

        self.time_left = round(self.time_left + self.extra_time_left, 1)

        # self.tool_counter += 1

    # def subtract_time(self):
    #     # to be replaced by extra_time
    #     time_punishment = settings.PUNISHMENT_GAME_SEC
    #     self.time_left = round(
    #         max(0, self.time_left - time_punishment), 1
    #     )

    def set_progress_bar(self):
        self.progress_bar.max = settings.START_TIME_GAME_SEC  # type: ignore

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
            Clock.unschedule(self.update_timer)  # Stop the timer when it reaches 0
            self.end_game()
            pass

        # def update_extra_timer(self, *args):
        # update extra_time_label

        # update extra time
        if self.extra_time_left > 0.0:
            self.extra_time_left = round(
                self.extra_time_left - settings.INTERVAL_GAME_SEC, 1
            )

            self.extra_time_label.text = f"{str(self.extra_time_left)} s  "  # type: ignore

        else:
            self.extra_time_label.text = ""  # type: ignore

            # Clock.unschedule(
            #     self.update_extra_timer
            # )  # Stop the timer when it reaches 0

    # def update_score(self):
    # self.score_label.text = f"{str(self.score)}  "  # type: ignore

    # def reset_score(self):
    #     self.score = 0
    #     self.update_score()

    def increment_score(self, add: int = 100):
        # self.score += add
        self.game.score += add
        # self.update_score()
        self.score_label.text = f"{str(self.game.score)}  "  # type: ignore

    def save_high_score(self):
        with open(
            "/".join(__file__.split("/")[:-2]) + "/storage/high_strike.yaml", "w"
        ) as f:
            # with open("./app/storage/high_score.yaml", "w") as f:
            # yaml.dump({"high_score": self.score}, f)
            yaml.dump({"high_score": self.game.score}, f)

    def end_game(self):
        self.save_high_score()

        app = App.get_running_app()
        app.root.current = "fahrzeugkunde_menu"  # type: ignore
        app.root.transition.direction = "right"  # type: ignore

    def reset_tool_list(self):
        (self.firetruck_rooms, self.tools, self.tools_locations) = (
            load_firetruck_storage(self.selected_firetruck)
        )

        shuffle(self.tools)

    def play(self):
        ## init GameCore class instance
        self.game = GameCore()

        # reset game specific elements
        self.reset_tool_list()

        # self.reset_score()
        # inited as self.game.score = 0

        # self.reset_tool_counter()
        # not needed, it is property of GameCore()

        self.reset_timer()

        Clock.schedule_interval(self.update_timer, settings.INTERVAL_GAME_SEC)

        # start game
        self.next_tool()

        # self.accept_answers = True  # Flag to indicate if answers should be processed

    def break_tool_name(self, tool_name: str) -> str:
        if len(tool_name) >= 29:
            tool_name_lst: list = tool_name[14:].split(" ")
            return (
                tool_name[:14] + tool_name_lst[0] + "\n" + " ".join(tool_name_lst[1:])
            )
        return tool_name

    def next_tool(self, *args):
        self.accept_answers = True  # Enable answer processing for the new tool

        if len(self.tools) == 0:
            self.reset_tool_list()

        # troubleshooting: fix tool
        # self.current_tool = "Handfunkgerät"  # "Druckschlauch B"
        # self.current_tool = self.tools.pop()
        # current_tool = self.tools.pop()

        # self.correct_storage = set(self.tools_locations.get(self.current_tool))  # type: ignore
        # correct_storage = set(self.tools_locations.get(current_tool))

        current_tool = self.tools.pop()
        ### for testing only!
        # only multiple answers
        # while True:
        #     current_tool = self.tools.pop()
        #     rooms = self.tools_locations.get(current_tool)
        #     if len(rooms) <= 1:
        #         continue

        #     break
        ###

        self.current_question = ToolQuestion(
            firetruck=self.selected_firetruck,
            # tool=self.tools.pop(),
            tool=current_tool,
            rooms=list(
                set(self.tools_locations.get(current_tool))  # type: ignore
            ),  # = self.correct_storages
        )
        print(f"{self.current_question.rooms = }")

        # tool_text = self.current_tool
        # tool_text = current_tool
        # tool_text = str(self.current_question.tool)  # avoid updating class property
        # if len(tool_text) >= 29:
        #     tool_text_lst = tool_text[14:].split(" ")
        #     tool_text = (
        #         tool_text[:14] + tool_text_lst[0] + "\n" + " ".join(tool_text_lst[1:])
        #     )
        # self.tool_label.text = tool_text  # type: ignore

        self.tool_label.text = self.break_tool_name(self.current_question.tool)  # type: ignore

        self.firetruck_rooms_layout.clear_widgets()  # type: ignore

        for storage in self.firetruck_rooms:
            btn = Button(text=storage, font_size="28sp")
            btn.bind(on_press=self.on_answer)  # type: ignore
            self.firetruck_rooms_layout.add_widget(btn)  # type: ignore

        # reset tool specific elements
        # self.tool_counter += 1

        # bonus: reset extra time option after x played tools
        self.reset_extra_timer()

        # if self.tool_counter == settings.RENEW_EXTRA_TIME_INT:
        #     self.reset_tool_counter()

        # Clock.schedule_interval(self.update_extra_timer, settings.INTERVAL_GAME_SEC)

    def correct_answer(self):
        self.increment_score()

        # todo: fix color setting

        # if not self.timer_change_add:
        #     # if False, switch to True
        #     self.display_timer_change_add()

        # self.display_timer_change_label()

        # Clock.schedule_once(self.display_timer_change_label, settings.FEEDBACK_GAME_SEC)

        # extra_time = max_extra_time - self.counter * interval
        # add extra_time to total
        # display green!
        self.add_time()

        # self.tool_counter += 1

    def incorrect_answer(self):
        # todo: fix color setting

        # if self.timer_change_add:
        #     # if True, switch to False
        #     self.display_timer_change_add()

        # self.display_timer_change_label()

        # Clock.schedule_once(self.display_timer_change_label, settings.FEEDBACK_GAME_SEC)

        # self.subtract_time()
        pass

    def on_answer(self, instance):
        if not self.accept_answers:  # Check if answer processing is enabled
            return  # Ignore the button press if answer processing is disabled

        # Clock.unschedule(self.update_extra_timer)

        # do not accept identical answer
        if instance.text in self.current_question.room_answered:
            return

        # process actual answer
        if instance.text in self.current_question.rooms:
            # correct answer
            self.correct_answer()
        else:
            # incorrect answer
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
