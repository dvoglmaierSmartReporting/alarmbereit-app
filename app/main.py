# from kivy.logger import Logger

# from kivy.config import Config

# Config.read("/".join(__file__.split("/")[:-1]) + "/kivy.config")
# Config.set("kivy", "log_dir", "/".join(__file__.split("/")[:-1]) + "/logs")
# Config.set("kivy", "log_level", "info")
# # Config.set("kivy", "log_name", "fa1006_%y-%m-%d_%_.log")
# # Config.set("kivy", "log_enable", 1)
# # Config.write()

# # from kivy.logger import Logger
# import logging
# from kivy.logger import FileHandler


# # Define a custom FileHandler
# class CustomFileHandler(FileHandler):
#     def _write_message(self, record):
#         # Custom behavior for writing message
#         record.msg = f"Custom log message: {record.msg}"
#         super()._write_message(record)


# # Function to replace the existing FileHandler
# def replace_file_handler(logger, new_handler):
#     # Remove existing FileHandlers
#     for handler in logger.handlers:
#         if isinstance(handler, FileHandler):
#             logger.removeHandler(handler)

#     # Add the new custom FileHandler
#     logger.addHandler(new_handler)


# # Create and configure the custom file handler
# custom_file_handler = CustomFileHandler(level=logging.INFO)
# formatter = logging.Formatter("teeest - %(asctime)s - %(name)s - %(levelname)s - %(message)s")
# custom_file_handler.setFormatter(formatter)

# # Replace the existing file handler in the Kivy logger
# replace_file_handler(Logger, custom_file_handler)

# # Test logging
# Logger.info("This is an info message")
# Logger.debug("This is a debug message")
# Logger.error("This is an error message")


###

from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.screenmanager import ScreenManager, Screen

# from inspect import currentframe
import traceback

from screens.info_screen import Info_Screen
from screens.settings_screen import Settings_Screen
from screens.firetruck_menu import Fahrzeugkunde_Menu
from screens.firetruck_training import Fahrzeugkunde_Training
from screens.firetruck_game import Fahrzeugkunde_Game
from screens.firetruck_browse import Fahrzeugkunde_Browse
from screens.firetruck_images import Fahrzeugkunde_Images
from screens.competition_menu import Bewerb_Menu
from screens.competition_training import Bewerb_Training
from screens.competition_game import Bewerb_Game
from screens.error_popup import ErrorPopup

from helper.functions import (
    load_total_storage,
    mode_str2bool,
    mode_bool2str,
    create_scores_text,
)
from helper.file_handling import (
    read_scores_file,
    transfer_file,
)
from helper.settings import Strings

from typing import cast

strings = Strings()

# from helper.logging import log_and_call


class Start_Menu(Screen):
    mode: tuple[bool, bool, bool, bool] = (
        True,  # training | default
        False,  # game
        False,  # browse
        False,  # images
    )

    # @log_and_call("test")
    def __init__(self, **kwargs):
        super(Start_Menu, self).__init__(**kwargs)
        # Logger.info("Start_Menu: __init__")
        # Logger.info(f"Start_Menu: {__name__ = }")

        # this_function_name = currentframe().f_code.co_name
        # Logger.info(f"Start_Menu: {this_function_name = }")

        # type annotations
        self.info_button = cast(Button, self.info_button)
        # self.settings_button = cast(Button, self.settings_button)
        self.training_button = cast(Button, self.training_button)
        self.game_button = cast(Button, self.game_button)
        self.browse_button = cast(Button, self.browse_button)
        # self.images_button = cast(Button, self.images_button)
        self.firetrucks_button = cast(Button, self.firetrucks_button)
        self.competitions_button = cast(Button, self.competitions_button)
        # self.standards_button = cast(Button, self.standards_button)
        self.mode_label = cast(Label, self.mode_label)
        self.questions_label = cast(Label, self.questions_label)

        # update button strings
        self.info_button.text = strings.BUTTON_STR_INFO
        # self.settings_button.text = strings.BUTTON_STR_SETTINGS
        self.training_button.text = strings.BUTTON_STR_TRAINING
        self.game_button.text = strings.BUTTON_STR_GAME
        self.browse_button.text = strings.BUTTON_STR_BROWSE
        # self.images_button.text = strings.BUTTON_STR_IMAGES
        self.firetrucks_button.text = strings.BUTTON_STR_FIRETRUCKS
        self.competitions_button.text = strings.BUTTON_STR_COMPETITIONS
        # self.standards_button.text = strings.BUTTON_STR_STANDARDS

        # update label strings
        self.mode_label.text = strings.LABEL_STR_MODE
        self.questions_label.text = strings.LABEL_STR_QUESTIONS

        # self.standards_button.disabled = True

    def on_button_release2(self):
        # if mode change, read mode label from current selection
        self.mode = mode_str2bool(self.find_down_toggle_button(self))

        # disable not existing combinations
        self.firetrucks_button.disabled = False
        self.competitions_button.disabled = False
        # self.standards_button.disabled = False
        mode_training, mode_game, mode_browse, mode_images = self.mode
        if mode_images:
            self.firetrucks_button.disabled = True
        # if mode_game or mode_images or mode_browse:
        if mode_images or mode_browse:
            # if mode_game or mode_images:
            self.competitions_button.disabled = True
        # if mode_training or mode_game or mode_images or mode_browse:
        #     self.standards_button.disabled = True

    def forward_mode2menu(self, menu_screen: str):
        selected_mode = mode_bool2str(self.mode)
        self.manager.current = menu_screen
        self.manager.get_screen(menu_screen).ids.mode_label.text = f"{selected_mode}   "

    # def find_down_toggle_button(self, widget, selected_mode=None):
    def find_down_toggle_button(self, widget) -> str:
        # Recursively search for a ToggleButton in the 'down' state.
        if isinstance(widget, ToggleButton) and widget.state == "down":
            return widget.text
        for child in widget.children:
            result = self.find_down_toggle_button(child)
            if result:  # If a 'down' ToggleButton is found, return its text
                return result
        return ""  # if no 'down' ToggleButton is found

    def update_info_text(self):
        info_text = create_scores_text(read_scores_file())

        info_text += "\n\n\n\n"

        self.manager.get_screen("info_screen").ids.info_text_label.text = info_text

    def update_firetruck_buttons(self):
        # load available firetrucks
        total_storage = load_total_storage()
        self.total_firetrucks = list(total_storage.keys())

        # create button for all firetrucks
        self.manager.get_screen(
            "fahrzeugkunde_menu"
        ).ids.firetrucks_layout.clear_widgets()
        for firetruck in self.total_firetrucks:

            abbreviation = strings.trucks.get(firetruck)
            # Create a button with two strings, one centered and one at the bottom right
            btn = Button(
                text=f"{firetruck}{' '*3}[size=30]{abbreviation}[/size]",
                font_size="32sp",
                markup=True,  # Enable markup for custom text positioning
                size_hint_y=None,
                height=150,
                size_hint_x=1,
            )
            btn.bind(
                on_release=self.manager.get_screen(
                    "fahrzeugkunde_menu"
                ).on_button_release
            )

            # Add the button to the layout
            self.manager.get_screen(
                "fahrzeugkunde_menu"
            ).ids.firetrucks_layout.add_widget(btn)


class CustomToggleButton(ToggleButton):  # used in feuerwehr.kv
    def on_touch_up(self, touch):
        # Call the superclass method to ensure standard behavior is preserved
        super_result = super(CustomToggleButton, self).on_touch_up(touch)
        if self.state == "normal":  # Check if the button was just released
            # Force it back to 'down' state if no other buttons are down
            if not any(btn.state == "down" for btn in self.get_widgets(self.group)):
                self.state = "down"
        return super_result


class FeuerwehrApp(App):
    def build(self):

        try:
            # path relative to app/helper/file_handling.py
            transfer_file("../storage", "scores.yaml")
            transfer_file("../storage", "main.cfg")

            sm = ScreenManager()
            sm.add_widget(Start_Menu())
            sm.add_widget(Info_Screen())
            sm.add_widget(Settings_Screen())
            sm.add_widget(Fahrzeugkunde_Menu())
            sm.add_widget(Bewerb_Menu())
            sm.add_widget(Fahrzeugkunde_Training())
            sm.add_widget(Fahrzeugkunde_Game())
            sm.add_widget(Fahrzeugkunde_Browse())
            sm.add_widget(Fahrzeugkunde_Images())
            sm.add_widget(Bewerb_Training())
            sm.add_widget(Bewerb_Game())

            return sm

        except Exception as e:
            error_message = f"An error occurred:\n{str(e)}\n{traceback.format_exc()}"
            self.show_error_popup(error_message)
            return None  # Return None to prevent further crashes

    # test
    def show_error_popup(self, message="An unknown error occurred!"):
        popup = ErrorPopup(message)
        popup.open()


if __name__ == "__main__":
    FeuerwehrApp().run()
