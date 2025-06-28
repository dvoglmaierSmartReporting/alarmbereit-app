from kivy.config import Config

# Set width and height
Config.set("graphics", "width", "600")
Config.set("graphics", "height", "1000")


from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, NoTransition
from kivy.clock import Clock
from kivy.base import EventLoop
from kivy.lang import Builder


import traceback
import sys

from screens.start_menu import Start_Menu
from screens.login_screen import Login
from screens.info_screen import Info_Screen
from screens.acknowledgement_screen import Acknowledgement_Screen

from screens.firetruck_mode import Fahrzeugkunde_Mode
from screens.firetruck_menu import Fahrzeugkunde_Menu
from screens.firetruck_training import Fahrzeugkunde_Training

# from screens.firetruck_training_new import Fahrzeugkunde_Training_New
from screens.firetruck_game import Fahrzeugkunde_Game
from screens.firetruck_browse import Fahrzeugkunde_Browse
from screens.firetruck_images import Fahrzeugkunde_Images
from screens.competition_menu import Bewerb_Menu
from screens.competition_training import Bewerb_Training
from screens.competition_game import Bewerb_Game

from errors.error_popup import ErrorPopup

from helper.file_handling import transfer_file


if "pytest" in sys.modules:
    Builder.load_file("app/feuerwehr.kv")



class FeuerwehrApp(App):
    def build(self):
        # print(f'{App.get_running_app().user_data_dir = }')
        # App.get_running_app().user_data_dir = '/Users/dominikvoglmaier/Library/Application Support/feuerwehr'

        # print(f'{Config.filename = }')
        # Config.filename = '/Users/dominikvoglmaier/.kivy/config.ini'
        
        try:
            # path relative to app/helper/file_handling.py
            # transfer_file contains migration from 2.3.2 to 2.4.0
            transfer_file("../storage", "scores.yaml")

            # TODO: is main.cfg needed?
            # transfer_file("../storage", "main.cfg")

            self.sm = ScreenManager()
            self.sm.add_widget(Login())
            self.sm.add_widget(Start_Menu())
            self.sm.add_widget(Info_Screen())
            self.sm.add_widget(Acknowledgement_Screen())
            self.sm.add_widget(Fahrzeugkunde_Mode())
            self.sm.add_widget(Fahrzeugkunde_Menu())
            self.sm.add_widget(Fahrzeugkunde_Training())
            # self.sm.add_widget(Fahrzeugkunde_Training_New())
            self.sm.add_widget(Fahrzeugkunde_Game())
            self.sm.add_widget(Fahrzeugkunde_Browse())
            self.sm.add_widget(Fahrzeugkunde_Images())
            self.sm.add_widget(Bewerb_Menu())
            self.sm.add_widget(Bewerb_Training())
            self.sm.add_widget(Bewerb_Game())

            # Android return button
            # Bind keyboard handler after window is initialized
            EventLoop.window.bind(on_keyboard=self.on_android_back_button)

            return self.sm

        except Exception as e:
            error_message = f"An error occurred:\n{str(e)}\n{traceback.format_exc()}"
            print(error_message)
            self.show_error_popup(error_message)
            return None  # Return None to prevent further crashes

    def on_start(self):
        # Avoid app crash at first installation, when Config is not added yet
        if "content" in Config.sections() and Config.has_option("content", "city"):
            if Config.get("content", "city"):
                # Delay screen switch until app is fully initialized
                Clock.schedule_once(self.jump_to_start_menu, 0)

    def jump_to_start_menu(self, dt):
        # Temporarily disable transitions
        original_transition = self.sm.transition
        self.sm.transition = NoTransition()
        self.sm.current = "start_menu"
        self.sm.transition = original_transition

    # test
    def show_error_popup(self, message="An unknown error occurred!"):
        popup = ErrorPopup(message)
        popup.open()

    # Android return button
    def on_android_back_button(self, window, key, *args):
        try:
            if key == 27:  # 27 is the Android back button key code
                current = self.sm.current
                if current in ["start_menu"]:
                    self.stop()  # exit the app
                    return True

                elif current in [
                    "info_screen",
                    "acknowledgement_screen",
                    "fahrzeugkunde_mode",
                    "bewerb_menu",
                ]:
                    self.sm.transition.direction = "right"
                    self.sm.current = "start_menu"
                    return True

                elif current in [
                    "fahrzeugkunde_training",
                    "fahrzeugkunde_training_new",
                    "fahrzeugkunde_game",
                    "fahrzeugkunde_browse",
                    "fahrzeugkunde_images",
                ]:
                    self.sm.transition.direction = "right"
                    self.sm.current = "fahrzeugkunde_menu"
                    return True

                elif current in [
                    "fahrzeugkunde_menu",
                ]:
                    self.sm.transition.direction = "right"
                    self.sm.current = "fahrzeugkunde_mode"
                    return True

                elif current in [
                    "bewerb_training",
                    "bewerb_game",
                ]:
                    self.sm.transition.direction = "right"
                    self.sm.current = "bewerb_menu"
                    return True

            return False

        except Exception as e:
            error_message = f"Android return button {key = }\nAn error occurred:\n{str(e)}\n{traceback.format_exc()}"
            self.show_error_popup(error_message)
            return None  # Return None to prevent further crashes


if __name__ == "__main__":
    FeuerwehrApp().run()
