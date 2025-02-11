from kivy.logger import Logger

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
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.screenmanager import ScreenManager, Screen

from inspect import currentframe

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

from helper.functions import (
    load_total_storage,
    mode_str2bool,
    mode_bool2str,
    create_scores_text,
)
from helper.file_handling import (
    copy_file_to_writable_dir,
    read_scores_file,
    transfer_file,
)
from helper.settings import Strings


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
        Logger.info("Start_Menu: __init__")
        Logger.info(f"Start_Menu: {__name__ = }")

        this_function_name = currentframe().f_code.co_name  # type: ignore
        Logger.info(f"Start_Menu: {this_function_name = }")

        # update button strings
        self.info_button.text = strings.BUTTON_STR_INFO  # type: ignore
        self.settings_button.text = strings.BUTTON_STR_SETTINGS  # type: ignore
        self.training_button.text = strings.BUTTON_STR_TRAINING  # type: ignore
        self.game_button.text = strings.BUTTON_STR_GAME  # type: ignore
        self.browse_button.text = strings.BUTTON_STR_BROWSE  # type: ignore
        # self.images_button.text = strings.BUTTON_STR_IMAGES  # type: ignore
        self.firetrucks_button.text = strings.BUTTON_STR_FIRETRUCKS  # type: ignore
        self.competitions_button.text = strings.BUTTON_STR_COMPETITIONS  # type: ignore
        # self.standards_button.text = strings.BUTTON_STR_STANDARDS  # type: ignore

        # update label strings
        self.mode_label.text = strings.LABEL_STR_MODE  # type: ignore
        self.questions_label.text = strings.LABEL_STR_QUESTIONS  # type: ignore

        # self.standards_button.disabled = True  # type: ignore

    def on_button_release2(self):
        # if mode change, read mode label from current selection
        self.mode = mode_str2bool(self.find_down_toggle_button(self))  # type: ignore

        # disable not existing combinations
        self.firetrucks_button.disabled = False  # type: ignore
        self.competitions_button.disabled = False  # type: ignore
        # self.standards_button.disabled = False  # type: ignore
        mode_training, mode_game, mode_browse, mode_images = self.mode
        if mode_images:
            self.firetrucks_button.disabled = True  # type: ignore
        # if mode_game or mode_images or mode_browse:
        if mode_images or mode_browse:
            # if mode_game or mode_images:
            self.competitions_button.disabled = True  # type: ignore
        # if mode_training or mode_game or mode_images or mode_browse:
        #     self.standards_button.disabled = True  # type: ignore

    def forward_mode2menu(self, menu_screen: str):
        selected_mode = mode_bool2str(self.mode)
        self.manager.current = menu_screen
        self.manager.get_screen(menu_screen).ids.mode_label.text = f"{selected_mode}   "

    # def find_down_toggle_button(self, widget, selected_mode=None):
    def find_down_toggle_button(self, widget):
        # Recursively search for a ToggleButton in the 'down' state.
        if isinstance(widget, ToggleButton) and widget.state == "down":
            return widget.text
        for child in widget.children:
            result = self.find_down_toggle_button(child)
            if result:  # If a 'down' ToggleButton is found, return its text
                return result
        return None  # if no 'down' ToggleButton is found

    def update_info_scores(self):
        scores = read_scores_file()
        # self.ids.scores_label.text = create_scores_text(scores)
        self.manager.get_screen("info_screen").ids.scores_label.text = (
            create_scores_text(scores)
        )

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
            btn.bind(  # type: ignore
                on_release=self.manager.get_screen(
                    "fahrzeugkunde_menu"
                ).on_button_release
            )

            # Add the button to the layout
            self.manager.get_screen(
                "fahrzeugkunde_menu"
            ).ids.firetrucks_layout.add_widget(
                btn
            )  # type: ignore


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

        # path relative to app/helper/file_handling.py
        # copy_file_to_writable_dir("../storage", "scores.yaml")
        # copy_file_to_writable_dir("../storage", "main.cfg")
        transfer_file("../storage", "scores.yaml")
        transfer_file("../storage", "main.cfg")

        # lookup_firetruck_files_at_writable_dir()
        # validate_firetruck_files()

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


if __name__ == "__main__":
    FeuerwehrApp().run()
