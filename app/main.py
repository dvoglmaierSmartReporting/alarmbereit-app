from kivy.config import Config

# Set a default window size for development (will be ignored on mobile)
Config.set("graphics", "width", "600")
Config.set("graphics", "height", "1000")

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, NoTransition
from kivy.clock import Clock
from kivy.base import EventLoop
from kivy.lang import Builder
from kivy.core.text import LabelBase
from kivy.core.window import Window
from kivy.metrics import dp


import traceback
import sys

from screens.start_menu import Start_Menu
from screens.login_screen import Login

from screens.highscore_screen import Highscore
from screens.acknowledgement_screen import Acknowledgment
from screens.firetruck_menu import Firetruck_Menu
from screens.firetruck_training import Firetruck_Training
from screens.firetruck_training_with_images import Firetruck_Training_With_Images
from screens.firetruck_game import Firetruck_Game

# from screens.firetruck_browse import Firetruck_Browse
# from screens.firetruck_images import Firetruck_Images

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
        # Bind to window size changes for responsive behavior
        Window.bind(on_resize=self.on_window_resize)

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
            self.sm.add_widget(Firetruck_Menu())
            self.sm.add_widget(Firetruck_Training())
            self.sm.add_widget(Firetruck_Training_With_Images())
            self.sm.add_widget(Firetruck_Game())
            # self.sm.add_widget(Firetruck_Browse())
            # self.sm.add_widget(Firetruck_Images())

            # Android return button
            # Bind keyboard handler after window is initialized
            EventLoop.window.bind(on_keyboard=self.on_android_back_button)

            # Schedule initial layout update to ensure correct initial layout
            Clock.schedule_once(self.force_layout_update, 0.1)

            return self.sm

        except Exception as e:
            error_message = f"An error occurred:\n{str(e)}\n{traceback.format_exc()}"
            print(error_message)
            self.show_error_popup(error_message)
            return None  # Return None to prevent further crashes

    def force_layout_update(self, dt):
        """Force a layout update to ensure correct initial layout"""
        # Trigger a fake resize event to update all layouts
        self.on_window_resize(Window, Window.width, Window.height)

        # Also trigger canvas updates for all screens
        if hasattr(self, "sm"):
            for screen in self.sm.screens:
                try:
                    screen.canvas.ask_update()
                except:
                    pass

    def on_window_resize(self, instance, width, height):
        # Trigger layout updates for all screens
        if hasattr(self, "sm"):
            for screen in self.sm.screens:
                if hasattr(screen, "update_layout"):
                    screen.update_layout()
                # Force canvas update for immediate visual changes
                try:
                    screen.canvas.ask_update()
                except:
                    pass

    def on_start(self):
        # Force another layout update after app fully starts
        Clock.schedule_once(self.force_layout_update, 0.2)

        # Avoid app crash at first installation, when Config is not added yet
        if "content" in Config.sections() and Config.has_option("content", "city"):
            if Config.get("content", "city"):
                # Delay screen switch until app is fully initialized
                Clock.schedule_once(self.jump_to_start_menu, 0.3)

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
                    "highscore_screen",
                    "acknowledgement_screen",
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

            return False

        except Exception as e:
            error_message = f"Android return button {key = }\nAn error occurred:\n{str(e)}\n{traceback.format_exc()}"
            self.show_error_popup(error_message)
            return None  # Return None to prevent further crashes


if __name__ == "__main__":
    FeuerwehrApp().run()
