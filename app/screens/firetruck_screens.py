from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.properties import BooleanProperty
from kivy.uix.screenmanager import Screen
from kivy.clock import Clock

from kivy.uix.image import AsyncImage, Image
from kivy.uix.scatter import Scatter
from kivy.uix.floatlayout import FloatLayout

from random import shuffle
import yaml
import os

from helper.functions import load_total_storage, load_firetruck_storage, mode_str2bool
from helper.settings import Settings
from helper.game_class import GameCore


settings = Settings()


class Fahrzeugkunde_Menu(Screen):
    def __init__(self, **kwargs):
        super(Fahrzeugkunde_Menu, self).__init__(**kwargs)
        # load available firetrucks
        total_storage = load_total_storage()
        self.total_firetrucks = list(total_storage.keys())
        # create button for all firetrucks
        for firetruck in self.total_firetrucks:
            btn = Button(text=firetruck, font_size="32sp")
            btn.bind(on_release=self.on_button_release)
            self.firetrucks_layout.add_widget(btn)

    def on_button_release(self, instance):
        # on question selection, read mode label text from current screen
        mode = mode_str2bool(self.mode_label.text.strip())
        mode_training, mode_game, mode_browse, mode_images = mode

        # bind firetruck and mode selection
        app = App.get_running_app()

        if mode_training:
            app.root.current = "fahrzeugkunde_training"
            app.root.transition.direction = "left"
            # continue game with selected firetruck
            fahrzeugkunde_tg_screen = app.root.get_screen("fahrzeugkunde_training")
            fahrzeugkunde_tg_screen.select_firetruck(instance.text)
            fahrzeugkunde_tg_screen.forward_mode_2_fk_training(mode)
            fahrzeugkunde_tg_screen.play()

        if mode_game:
            app.root.current = "fahrzeugkunde_game"
            app.root.transition.direction = "left"
            # continue game with selected firetruck
            fahrzeugkunde_tg_screen = app.root.get_screen("fahrzeugkunde_game")
            fahrzeugkunde_tg_screen.select_firetruck(instance.text)
            fahrzeugkunde_tg_screen.forward_mode_2_fk_game(mode)
            fahrzeugkunde_tg_screen.play()

        elif mode_browse:
            # change screen
            app.root.current = "fahrzeugkunde_browse"
            app.root.transition.direction = "left"
            # continue game with selected firetruck
            fahrzeugkunde_browse_screen = app.root.get_screen("fahrzeugkunde_browse")
            fahrzeugkunde_browse_screen.select_firetruck(instance.text)
            fahrzeugkunde_browse_screen.populate_list()

        elif mode_images:
            app.root.current = "fahrzeugkunde_images"
            app.root.transition.direction = "left"

            fahrzeugkunde_images_screen = app.root.get_screen("fahrzeugkunde_images")
            fahrzeugkunde_images_screen.select_firetruck(instance.text)
            fahrzeugkunde_images_screen.load_image()


class Fahrzeugkunde_Training(Screen):
    strike_label_visible = BooleanProperty(False)

    def select_firetruck(self, selected_firetruck: str):
        # troubleshooting: fix firetruck
        # self.selected_firetruck = "Tank1" "Rüst+Lösch"
        self.selected_firetruck = selected_firetruck
        self.firetruck_label.text = f"   {selected_firetruck}"

    def forward_mode_2_fk_training(self, mode: tuple):
        self.mode_training: bool = mode[0]
        self.mode_game: bool = mode[1]
        self.mode_browse: bool = mode[2]
        self.mode_images: bool = mode[3]

    def update_strike(self):
        self.strike_label.text = f"{str(self.strike)}  "

    def reset_strike(self):
        self.strike = 0
        self.update_strike()

    def increment_strike(self):
        self.strike += 1
        self.update_strike()

    def save_high_strike(self):
        # with open("./app/storage/high_strike.yaml", "w") as f:
        with open(
            "/".join(__file__.split("/")[:-2]) + "/storage/high_strike.yaml", "w"
        ) as f:
            yaml.dump({"high_strike": self.strike}, f)

    # def end_game(self):
    #     self.save_high_strike()

    #     app = App.get_running_app()
    #     app.root.current = "fahrzeugkunde_menu"
    #     app.root.transition.direction = "right"

    def reset_tool_list(self):
        rooms, tools, tools_locations = load_firetruck_storage(self.selected_firetruck)
        self.rooms: list = rooms
        self.tools: list = tools
        self.tools_locations: dict = tools_locations

        shuffle(self.tools)

    def play(self):
        self.reset_tool_list()

        self.reset_strike()

        self.next_tool()

        self.accept_answers = True  # Flag to indicate if answers should be processed

    def next_tool(self, *args):
        self.accept_answers = True  # Enable answer processing for the new tool

        if len(self.tools) == 0:
            self.reset_tool_list()

        # troubleshooting: fix tool
        # self.current_tool = "Handfunkgerät"  # "Druckschlauch B"
        self.current_tool = self.tools.pop()

        self.correct_storage: set = set(self.tools_locations.get(self.current_tool))

        self.correct_storage_multiple = list(self.correct_storage)

        tool_text = self.current_tool
        if len(tool_text) >= 29:
            tool_text_lst = tool_text[14:].split(" ")
            tool_text = (
                tool_text[:14] + tool_text_lst[0] + "\n" + " ".join(tool_text_lst[1:])
            )
        self.tool_label.text = tool_text
        self.rooms_layout.clear_widgets()

        for storage in self.rooms:
            btn = Button(text=storage, font_size="28sp")
            btn.bind(on_press=self.on_answer)
            self.rooms_layout.add_widget(btn)

    def on_answer(self, instance):
        if not self.accept_answers:  # Check if answer processing is enabled
            return  # Ignore the button press if answer processing is disabled

        children = self.rooms_layout.children

        if instance.text in self.correct_storage_multiple:
            # correct answer
            self.increment_strike()

        else:
            # incorrect answer
            self.reset_strike()

        # indicate if correct or incorrect answer
        # for single correct answer
        if len(self.correct_storage_multiple) <= 1:
            # always identify and indicate the correct answer
            for child in children:
                if child.text in self.correct_storage:
                    child.background_color = (0, 1, 0, 1)
            # if, indicate incorrect answer
            if instance.text not in self.correct_storage:
                instance.background_color = (1, 0, 0, 1)

        # for multiple correct answers
        else:
            if instance.text not in self.correct_storage_multiple:
                # if, indicate incorrect and all correct answers and close
                instance.background_color = (1, 0, 0, 1)
                for child in children:
                    if child.text in self.correct_storage_multiple:
                        child.background_color = (0, 1, 0, 1)
                pass

            else:
                # answer in correct answers
                instance.background_color = (0, 1, 0, 1)
                # remove correct answer from set
                self.correct_storage_multiple.remove(instance.text)
                # display string "weitere"
                if self.tool_label.text[-7:] == "weitere":
                    self.tool_label.text += " "
                else:
                    self.tool_label.text += "\n"
                self.tool_label.text += "weitere"
                return

        self.accept_answers = (
            False  # Disable answer processing after an answer is selected
        )

        Clock.schedule_once(self.next_tool, settings.FEEDBACK_TRAINING_SEC)


class Fahrzeugkunde_Game(Screen):
    timer_change_label_visible = BooleanProperty(False)
    timer_change_add = BooleanProperty(True)

    def select_firetruck(self, selected_firetruck: str):
        # troubleshooting: fix firetruck
        # self.selected_firetruck = "Tank1" "Rüst+Lösch"
        self.selected_firetruck = selected_firetruck
        self.firetruck_label.text = f"   {selected_firetruck}"

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
        self.timer_label.text = f""

        self.set_progress_bar()

    def reset_extra_timer(self):
        # init self.counter

        # for testing...
        # self.extra_time_left = settings.MAX_EXTRA_TIME_SEC
        factor = self.tool_counter % settings.RENEW_EXTRA_TIME_INT
        self.extra_time_left = max(
            settings.MAX_EXTRA_TIME_SEC - factor * settings.EXTRA_TIME_REDUCTION_SEC,
            0,
        )

        # self.extra_time_label.text = f"{str(self.extra_time_left)} s  "

    def reset_tool_counter(self):
        self.tool_counter = 0

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
        self.progress_bar.max = settings.START_TIME_GAME_SEC

    def update_progress_bar(self):
        self.progress_bar.value = self.time_left

    def update_timer(self, *args):

        # update game time
        self.update_progress_bar()

        if self.time_left > 0.0:
            self.time_left = round(self.time_left - settings.INTERVAL_GAME_SEC, 1)

            if not self.time_left == 0.0:
                # self.timer_label.text = f"{str(self.time_left)} s  "
                self.timer_label.text = f""  # hide label for UI testing

            else:
                self.timer_label.text = "Ende  "
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

            self.extra_time_label.text = f"{str(self.extra_time_left)} s  "

        else:
            self.extra_time_label.text = ""

            # Clock.unschedule(
            #     self.update_extra_timer
            # )  # Stop the timer when it reaches 0

    def update_score(self):
        self.score_label.text = f"{str(self.score)}  "

    def reset_score(self):
        self.score = 0
        self.update_score()

    def increment_score(self, add: int = 100):
        self.score += add
        self.update_score()

    def save_high_score(self):
        with open(
            "/".join(__file__.split("/")[:-2]) + "/storage/high_strike.yaml", "w"
        ) as f:
            # with open("./app/storage/high_score.yaml", "w") as f:
            yaml.dump({"high_score": self.score}, f)

    def end_game(self):
        self.save_high_score()

        app = App.get_running_app()
        app.root.current = "fahrzeugkunde_menu"
        app.root.transition.direction = "right"

    def reset_tool_list(self):
        rooms, tools, tools_locations = load_firetruck_storage(self.selected_firetruck)
        self.rooms: list = rooms
        self.tools: list = tools
        self.tools_locations: dict = tools_locations

        shuffle(self.tools)

    def play(self):
        ## init GameCore class instance

        # reset game specific elements
        self.reset_tool_list()

        self.reset_score()

        self.reset_tool_counter()

        self.reset_timer()

        Clock.schedule_interval(self.update_timer, settings.INTERVAL_GAME_SEC)

        # start game
        self.next_tool()

        # self.accept_answers = True  # Flag to indicate if answers should be processed

    def next_tool(self, *args):
        self.accept_answers = True  # Enable answer processing for the new tool

        if len(self.tools) == 0:
            self.reset_tool_list()

        # troubleshooting: fix tool
        # self.current_tool = "Handfunkgerät"  # "Druckschlauch B"
        self.current_tool = self.tools.pop()

        self.correct_storage = set(self.tools_locations.get(self.current_tool))

        self.correct_storage_multiple = list(self.correct_storage)

        tool_text = self.current_tool
        if len(tool_text) >= 29:
            tool_text_lst = tool_text[14:].split(" ")
            tool_text = (
                tool_text[:14] + tool_text_lst[0] + "\n" + " ".join(tool_text_lst[1:])
            )
        self.tool_label.text = tool_text
        self.rooms_layout.clear_widgets()

        for storage in self.rooms:
            btn = Button(text=storage, font_size="28sp")
            btn.bind(on_press=self.on_answer)
            self.rooms_layout.add_widget(btn)

        # reset tool specific elements
        self.tool_counter += 1

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

        if instance.text in self.correct_storage_multiple:
            # correct answer
            self.correct_answer()
        else:
            # incorrect answer
            self.incorrect_answer()

        children = self.rooms_layout.children

        # indicate if correct or incorrect answer
        # for single correct answer
        if len(self.correct_storage_multiple) <= 1:
            # always identify and indicate the correct answer
            for child in children:
                if child.text in self.correct_storage:
                    child.background_color = (0, 1, 0, 1)
            # if, indicate incorrect answer
            if instance.text not in self.correct_storage:
                instance.background_color = (1, 0, 0, 1)

        # for multiple correct answers
        else:
            if instance.text not in self.correct_storage_multiple:
                # if, indicate incorrect and all correct answers and close
                instance.background_color = (1, 0, 0, 1)
                for child in children:
                    if child.text in self.correct_storage_multiple:
                        child.background_color = (0, 1, 0, 1)
                pass

            else:
                # answer in correct answers
                instance.background_color = (0, 1, 0, 1)
                # remove correct answer from set
                self.correct_storage_multiple.remove(instance.text)
                # display string "weitere"
                if self.tool_label.text[-7:] == "weitere":
                    self.tool_label.text += " "
                else:
                    self.tool_label.text += "\n"
                self.tool_label.text += "weitere"
                return

        self.accept_answers = (
            False  # Disable answer processing after an answer is selected
        )

        Clock.schedule_once(self.next_tool, settings.FEEDBACK_GAME_SEC)


class Fahrzeugkunde_Browse(Screen):
    def select_firetruck(self, selected_firetruck: str):
        # troubleshooting: fix firetruck
        # self.selected_firetruck = "Tank1" "Rüst+Lösch"
        self.selected_firetruck = selected_firetruck
        self.firetruck_label.text = f"{selected_firetruck}   "

    def load_firetruck(self):
        total_storage = load_total_storage()
        self.firetruck: dict = total_storage[self.selected_firetruck]
        self.rooms: list = list(self.firetruck.keys())

    def populate_list(self):
        self.load_firetruck()
        self.ids.browse_scrollview.scroll_y = 1
        label_container = self.ids.label_list
        label_container.clear_widgets()

        for room in self.rooms:
            label = Label(
                text=f"[b]{str(room)}[/b]",
                markup=True,
                size_hint_y=None,
                font_size="24sp",
                height=90,
                halign="left",
                text_size=(self.width, None),
            )
            label.bind(
                size=label.setter("text_size")
            )  # Update text_size on label size change
            label_container.add_widget(label)

            for tool in self.firetruck.get(room):
                label = Label(
                    text=f"   -  {str(tool)}",
                    size_hint_y=None,
                    size_hint_x=1,
                    font_size="22sp",
                    height=70,
                    halign="left",
                    valign="middle",
                )
                label.text_size = (label.width, None)
                label.bind(
                    width=lambda instance, value: setattr(
                        instance, "text_size", (value, None)
                    )
                )

                label_container.add_widget(label)

        # exceed list by empty entry
        label = Label(
            text="",
            size_hint_y=None,
            size_hint_x=1,
            font_size="22sp",
            height=70,
            halign="left",
            valign="middle",
        )
        label.text_size = (label.width, None)
        label.bind(
            width=lambda instance, value: setattr(instance, "text_size", (value, None))
        )

        label_container.add_widget(label)


class Fahrzeugkunde_Images(Screen):
    # def __init__(self, **kwargs):
    #     super(Fahrzeugkunde_Images, self).__init__(**kwargs)

    def load_image(self):
        self.scatter.clear_widgets()

        image = Image(
            source="assets/Rüst_G1_default-min.jpg",
            # allow_stretch=True,
            # keep_ratio=True,
            fit_mode="contain",
        )
        self.scatter.add_widget(image)

        # Bind the size and position of the image to the scatter
        self.scatter.bind(size=self.update_image_size)
        self.scatter.bind(pos=self.update_image_pos)

    def update_image_size(self, instance, value):
        instance.children[0].size = instance.size

    def update_image_pos(self, instance, value):
        instance.children[0].pos = instance.pos

    def select_firetruck(self, selected_firetruck: str):
        # troubleshooting: fix firetruck
        # self.selected_firetruck = "Tank1" "Rüst+Lösch"
        self.selected_firetruck = selected_firetruck
        self.firetruck_label.text = f"   {selected_firetruck}"
