from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen

from typing import cast

from helper.functions import mode_str2bool, change_screen_to
from helper.settings import Strings


strings = Strings()


class Fahrzeugkunde_Menu(Screen):
    def on_button_release(self, instance):
        self.mode_label = cast(Label, self.mode_label)
        # on question selection, read mode label text from current screen
        mode = mode_str2bool(self.mode_label.text.strip())
        (
            mode_training,
            mode_training_new,
            mode_game,
            mode_browse,
            mode_images,
            mode_exam,
        ) = mode

        # bind firetruck selection
        app = App.get_running_app()
        app_root = app.root

        if mode_training:
            change_screen_to("fahrzeugkunde_training", transition_direction="left")
            # continue game with selected firetruck
            screen = app_root.get_screen("fahrzeugkunde_training")
            screen.select_firetruck(instance.text.split(" ")[0])
            screen.play()

        elif mode_training_new:
            change_screen_to("fahrzeugkunde_training_new", transition_direction="left")
            # continue game with selected firetruck
            screen = app_root.get_screen("fahrzeugkunde_training_new")
            screen.select_firetruck(instance.text.split(" ")[0])
            screen.play()

        if mode_game:
            change_screen_to("fahrzeugkunde_game", transition_direction="left")
            # continue game with selected firetruck
            screen = app_root.get_screen("fahrzeugkunde_game")
            screen.select_firetruck(instance.text.split(" ")[0])
            screen.play()

        elif mode_browse:
            change_screen_to("fahrzeugkunde_browse", transition_direction="left")
            # continue game with selected firetruck
            screen = app_root.get_screen("fahrzeugkunde_browse")
            screen.select_firetruck(instance.text.split(" ")[0])
            screen.display_all_tools()

        elif mode_images:
            change_screen_to("fahrzeugkunde_images", transition_direction="left")
            # continue game with selected firetruck
            screen = app_root.get_screen("fahrzeugkunde_images")
            screen.select_firetruck(instance.text.split(" ")[0])
            screen.load_image()

        elif mode_exam:
            change_screen_to("fahrzeugkunde_training", transition_direction="left")

        #     screen = app.root.get_screen("fahrzeugkunde_exam")
        #     screen.select_firetruck(instance.text.split(" ")[0])
        #     screen.load_image()

    def go_back(self, *args) -> None:
        change_screen_to("fahrzeugkunde_mode")
