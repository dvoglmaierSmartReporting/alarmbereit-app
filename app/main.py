from kivy.config import Config

# Set width and height
Config.set("graphics", "width", "600")
Config.set("graphics", "height", "1000")


from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, NoTransition
from kivy.clock import Clock
from kivy.base import EventLoop
from kivy.lang import Builder
from kivy.core.text import LabelBase


import traceback
import sys

from screens.start_menu import Start_Menu
from screens.login_screen import Login

# from screens.info_screen import Info_Screen
from screens.highscore_screen import Highscore
from screens.acknowledgement_screen import Acknowledgment

# from screens.firetruck_mode import Firetruck_Mode
from screens.firetruck_menu import Firetruck_Menu
from screens.firetruck_training import Firetruck_Training

from screens.firetruck_training_with_images import Firetruck_Training_With_Images
from screens.firetruck_game import Firetruck_Game
from screens.firetruck_browse import Firetruck_Browse
from screens.firetruck_images import Firetruck_Images

# from screens.competition_menu import Competition_Menu
# from screens.competition_training import Competition_Training
# from screens.competition_game import Competition_Game

# from popups.error_popup import ErrorPopup
from popups.text_popup import TextPopup

from helper.file_handling import transfer_file
from helper.strings import Strings


strings = Strings()


if "pytest" in sys.modules:
    Builder.load_file("app/feuerwehr.kv")

    LabelBase.register(
        name="CourierNew",
        fn_regular="app/fonts/courier_prime.ttf",
        fn_bold="app/fonts/courier_prime_bold.ttf",
        fn_italic="app/fonts/courier_prime_italic.ttf",
        fn_bolditalic="app/fonts/courier_prime_bold_italic.ttf",
    )

else:
    LabelBase.register(
        name="CourierNew",
        fn_regular="fonts/courier_prime.ttf",
        fn_bold="fonts/courier_prime_bold.ttf",
        fn_italic="fonts/courier_prime_italic.ttf",
        fn_bolditalic="fonts/courier_prime_bold_italic.ttf",
    )


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

            self.sm = ScreenManager()
            self.sm.add_widget(Login())
            self.sm.add_widget(Start_Menu())
            # self.sm.add_widget(Info_Screen())
            self.sm.add_widget(Highscore())
            self.sm.add_widget(Acknowledgment())
            # self.sm.add_widget(Firetruck_Mode())
            self.sm.add_widget(Firetruck_Menu())
            self.sm.add_widget(Firetruck_Training())
            self.sm.add_widget(Firetruck_Training_With_Images())
            self.sm.add_widget(Firetruck_Game())
            self.sm.add_widget(Firetruck_Browse())
            self.sm.add_widget(Firetruck_Images())
            # self.sm.add_widget(Competition_Menu())
            # self.sm.add_widget(Competition_Training())
            # self.sm.add_widget(Competition_Game())

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
        error_popup = TextPopup(message, title=strings.TITLE_ERROR_POPUP)
        error_popup.open()

    # Android return button
    def on_android_back_button(self, window, key, *args):
        try:
            if key == 27:  # 27 is the Android back button key code
                current = self.sm.current
                if current in ["start_menu"]:
                    self.stop()  # exit the app
                    return True

                elif current in [
                    # "info_screen",
                    "highscore_screen",
                    "acknowledgement_screen",
                    # "firetruck_mode",
                    # "competition_menu",
                    "firetruck_menu",
                ]:
                    self.sm.transition.direction = "right"
                    self.sm.current = "start_menu"
                    return True

                elif current in [
                    "firetruck_training",
                    "firetruck_training_with_images",
                    "firetruck_game",
                    "firetruck_browse",
                    "firetruck_images",
                ]:
                    self.sm.transition.direction = "right"
                    self.sm.current = "firetruck_menu"
                    return True

                # elif current in [
                #     "firetruck_menu",
                # ]:
                #     self.sm.transition.direction = "right"
                #     self.sm.current = "firetruck_mode"
                #     return True

                # elif current in [
                #     "competition_training",
                #     "competition_game",
                # ]:
                #     self.sm.transition.direction = "right"
                #     self.sm.current = "competition_menu"
                #     return True

            return False

        except Exception as e:
            error_message = f"Android return button {key = }\nAn error occurred:\n{str(e)}\n{traceback.format_exc()}"
            self.show_error_popup(error_message)
            return None  # Return None to prevent further crashes


if __name__ == "__main__":
    FeuerwehrApp().run()
