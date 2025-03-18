from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen

from helper.functions import mode_str2bool
from helper.file_handling import load_total_storage
from helper.settings import Strings


strings = Strings()


class Fahrzeugkunde_Menu(Screen):
    def on_button_release(self, instance):
        # on question selection, read mode label text from current screen
        mode = mode_str2bool(self.mode_label.text.strip())
        mode_training, mode_game, mode_browse, mode_images = mode

        # bind firetruck selection
        app = App.get_running_app()

        if mode_training:
            app.root.current = "fahrzeugkunde_training"
            app.root.transition.direction = "left"
            # continue game with selected firetruck
            fahrzeugkunde_tg_screen = app.root.get_screen("fahrzeugkunde_training")
            fahrzeugkunde_tg_screen.select_firetruck(instance.text.split(" ")[0])
            # fahrzeugkunde_tg_screen.forward_mode_2_fk_training(mode)
            fahrzeugkunde_tg_screen.play()

        if mode_game:
            app.root.current = "fahrzeugkunde_game"
            app.root.transition.direction = "left"
            # continue game with selected firetruck
            fahrzeugkunde_tg_screen = app.root.get_screen("fahrzeugkunde_game")
            fahrzeugkunde_tg_screen.select_firetruck(instance.text.split(" ")[0])
            # fahrzeugkunde_tg_screen.forward_mode_2_fk_game(mode)
            fahrzeugkunde_tg_screen.play()

        elif mode_browse:
            # change screen
            app.root.current = "fahrzeugkunde_browse"
            app.root.transition.direction = "left"
            # continue game with selected firetruck
            fahrzeugkunde_browse_screen = app.root.get_screen("fahrzeugkunde_browse")
            fahrzeugkunde_browse_screen.select_firetruck(instance.text.split(" ")[0])
            fahrzeugkunde_browse_screen.display_all_tools()

        elif mode_images:
            app.root.current = "fahrzeugkunde_images"
            app.root.transition.direction = "left"

            fahrzeugkunde_images_screen = app.root.get_screen("fahrzeugkunde_images")
            fahrzeugkunde_images_screen.select_firetruck(instance.text.split(" ")[0])
            fahrzeugkunde_images_screen.load_image()
