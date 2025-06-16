from kivy.config import Config

# Set width and height
Config.set("graphics", "width", "600")
Config.set("graphics", "height", "1000")


from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.layout import Layout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition
from kivy.clock import Clock
from kivy.base import EventLoop
from kivy.lang import Builder


# from inspect import currentframe
import traceback
from typing import cast
import sys

from screens.info_screen import Info_Screen
from screens.acknowledgement_screen import Acknowledgement_Screen

# from screens.settings_screen import Settings_Screen
from screens.firetruck_login import Fahrzeugkunde_Login
from screens.firetruck_mode import Fahrzeugkunde_Mode
from screens.firetruck_menu import Fahrzeugkunde_Menu
from screens.firetruck_training import Fahrzeugkunde_Training

# from screens.firetruck_training_new import Fahrzeugkunde_Training_New
from screens.firetruck_game import Fahrzeugkunde_Game
from screens.firetruck_browse import Fahrzeugkunde_Browse
from screens.firetruck_images import Fahrzeugkunde_Images

from screens.competition_country import Bewerb_Bundesland
from screens.competition_menu import Bewerb_Menu
from screens.competition_training import Bewerb_Training
from screens.competition_game import Bewerb_Game
from errors.error_popup import ErrorPopup

from helper.functions import (
    load_total_storage,
    create_scores_text,
    mode_str2bool,
    change_screen_to,
)
from helper.file_handling import read_scores_file, transfer_file
from helper.settings import Strings


strings = Strings()


if "pytest" in sys.modules:
    Builder.load_file("app/feuerwehr.kv")


class Start_Menu(Screen):
    def __init__(self, **kwargs):
        super(Start_Menu, self).__init__(**kwargs)

    def on_kv_post(self, base_widget):
        # type annotations
        self.info_button = cast(Button, self.info_button)
        # self.acknowledgement_button = cast(Button, self.acknowledgement_button)
        self.content_layout = cast(Layout, self.content_layout)

        # update button strings
        self.info_button.text = strings.BUTTON_STR_INFO
        # self.acknowledgement_button.text = strings.BUTTON_STR_ACKNOWLEDGEMENT

        # Container where the additional widget will be displayed
        # Part of content_layout
        self.display_container = BoxLayout(
            size_hint=(1, 3), orientation="vertical", spacing="5dp", padding="20dp"
        )

        fahrzeuge_button = Button(
            size_hint=(1, 1),
            text=strings.BUTTON_STR_FIRETRUCKS,
            font_size="32sp",
        )
        # if selection is stored
        if True:
            # transition to login screen
            fahrzeuge_button.bind(
                on_release=lambda instance: change_screen_to(
                    "fahrzeugkunde_login", "left"
                )
            )
        else:
            fahrzeuge_button.bind(
                on_release=lambda instance: change_screen_to(
                    "fahrzeugkunde_menu", "left"
                )
            )

        bewerbe_button = Button(
            size_hint=(1, 1),
            text=strings.BUTTON_STR_COMPETITIONS,
            font_size="32sp",
        )

        # if selection is stored
        if True:
            # transition to countries screen
            bewerbe_button.bind(
                on_release=lambda instance: change_screen_to(
                    "bewerb_bundesland", "left"
                )
            )
        else:
            bewerbe_button.bind(
                on_release=lambda instance: change_screen_to("bewerb_menu", "left")
            )

        placeholder1 = Label(
            size_hint=(1, 1),
        )

        # Add widgets to layout
        self.content_layout.add_widget(fahrzeuge_button)
        self.content_layout.add_widget(bewerbe_button)
        self.content_layout.add_widget(placeholder1)

    def add_competition_modi_widget(self):
        ### WIDGET ###
        competitions_modi_widget = BoxLayout(
            orientation="vertical",
            spacing="3dp",
        )

        ### BUTTON Übung ###
        competition_btn1 = Button(
            pos_hint={"center_x": 0.5},
            text=strings.BUTTON_STR_TRAINING,
            font_size="32sp",
        )

        competition_btn1.bind(  # type: ignore[attr-defined]
            on_release=lambda instance: self.forward_mode2menu_manually(
                "bewerb_menu", strings.BUTTON_STR_TRAINING
            )
        )

        competitions_modi_widget.add_widget(competition_btn1)

        ### BUTTON Zeitdruck ###
        competition_btn2 = Button(
            pos_hint={"center_x": 0.5},
            text=strings.BUTTON_STR_GAME,
            font_size="32sp",
        )

        competition_btn2.bind(  # type: ignore[attr-defined]
            on_release=lambda instance: self.forward_mode2menu_manually(
                "bewerb_menu", strings.BUTTON_STR_GAME
            )
        )

        competitions_modi_widget.add_widget(competition_btn2)

        ### BUTTON Placeholder ###
        competitions_modi_widget.add_widget(
            Label(  # placeholder
                size_hint=(1, 1),
                font_size="32sp",
            )
        )

        return competitions_modi_widget

    def forward_mode2menu_manually(self, menu_screen: str, mode: str):
        self.manager.transition = SlideTransition(direction="left")
        self.manager.current = menu_screen
        self.manager.get_screen(menu_screen).ids.mode_label.text = mode

    def update_info_text(self):
        info_text = create_scores_text(read_scores_file())

        info_text += "\n\n\n\n"

        self.manager.get_screen("info_screen").ids.info_text_label.text = info_text




class FeuerwehrApp(App):
    def build(self):

        try:
            # path relative to app/helper/file_handling.py
            transfer_file("../storage", "scores.yaml")
            transfer_file("../storage", "main.cfg")

            self.sm = ScreenManager()
            self.sm.add_widget(Start_Menu())
            self.sm.add_widget(Info_Screen())
            self.sm.add_widget(Acknowledgement_Screen())
            # self.sm.add_widget(Settings_Screen())
            self.sm.add_widget(Fahrzeugkunde_Login())
            self.sm.add_widget(Fahrzeugkunde_Mode())
            self.sm.add_widget(Fahrzeugkunde_Menu())
            self.sm.add_widget(Fahrzeugkunde_Training())
            # self.sm.add_widget(Fahrzeugkunde_Training_New())
            self.sm.add_widget(Fahrzeugkunde_Game())
            self.sm.add_widget(Fahrzeugkunde_Browse())
            self.sm.add_widget(Fahrzeugkunde_Images())
            self.sm.add_widget(Bewerb_Bundesland())
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

    # test
    def show_error_popup(self, message="An unknown error occurred!"):
        popup = ErrorPopup(message)
        popup.open()

    # Android return button
    def on_android_back_button(self, window, key, *args):
        try:
            if key == 27:  # 27 is the Android back button key code
                current = self.sm.current
                if current == "start_menu":
                    self.stop()  # exit the app
                    return True

                elif current in [
                    "info_screen",
                    "acknowledgement_screen",
                    "settings_screen",
                    "fahrzeugkunde_login",
                    "bewerb_country",
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
                    "bewerb_menu",
                ]:
                    if True:  # add logic to save country
                        self.sm.transition.direction = "right"
                        self.sm.current = "bewerb_country"
                    else:
                        self.sm.transition.direction = "right"
                        self.sm.current = "start_menu"
                    return True

                elif current in [
                    "fahrzeugkunde_mode",
                ]:
                    if True:  # add logic to save login
                        self.sm.transition.direction = "right"
                        self.sm.current = "fahrzeugkunde_login"
                    else:
                        self.sm.transition.direction = "right"
                        self.sm.current = "start_menu"
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
