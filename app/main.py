from kivy.config import Config

# Set width and height
Config.set("graphics", "width", "600")
Config.set("graphics", "height", "1000")

# Optional: Make the window non-resizable
Config.set("graphics", "resizable", "1")  # or '1' to allow resizing


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
from kivy.uix.layout import Layout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition
from kivy.clock import Clock

# from inspect import currentframe
import traceback

from screens.info_screen import Info_Screen

# from screens.settings_screen import Settings_Screen
from screens.firetruck_menu import Fahrzeugkunde_Menu
from screens.firetruck_training import Fahrzeugkunde_Training
from screens.firetruck_training_new import Fahrzeugkunde_Training_New
from screens.firetruck_game import Fahrzeugkunde_Game
from screens.firetruck_browse import Fahrzeugkunde_Browse
from screens.firetruck_images import Fahrzeugkunde_Images
from screens.competition_menu import Bewerb_Menu
from screens.competition_training import Bewerb_Training
from screens.competition_game import Bewerb_Game
from errors.error_popup import ErrorPopup

from helper.functions import load_total_storage, create_scores_text, mode_str2bool
from helper.file_handling import read_scores_file, transfer_file
from helper.settings import Strings

from typing import cast

strings = Strings()

# from helper.logging import log_and_call


class Start_Menu(Screen):
    # mode: tuple[bool, bool, bool, bool] = (
    #     True,  # training | default
    #     False,  # game
    #     False,  # browse
    #     False,  # images
    # )

    # @log_and_call("test")
    def __init__(self, **kwargs):
        super(Start_Menu, self).__init__(**kwargs)
        # Logger.info("Start_Menu: __init__")
        # Logger.info(f"Start_Menu: {__name__ = }")

        # this_function_name = currentframe().f_code.co_name
        # Logger.info(f"Start_Menu: {this_function_name = }")

        # type annotations
        self.info_button = cast(Button, self.info_button)
        self.content_layout = cast(Layout, self.content_layout)

        # update button strings
        self.info_button.text = strings.BUTTON_STR_INFO

        # Container where the additional widget will be displayed
        # Part of content_layout
        self.display_container = BoxLayout(
            size_hint=(1, 5), orientation="vertical", spacing="5dp", padding="20dp"
        )

        firetrucks_modi_widget = self.add_firetruck_modi_widget()

        competitions_modi_widget = self.add_competition_modi_widget()

        # Part of content_layout
        questions_label = Label(
            size_hint=(1, 0.5),
            text=strings.LABEL_STR_QUESTIONS,
            font_size="32sp",
            bold=True,
        )
        firetrucks_button = CustomContentToggleButton(
            size_hint=(1, 1),
            group="content_button",
            text=strings.BUTTON_STR_FIRETRUCKS,
            font_size="32sp",
            container=self.display_container,
            display_widget=firetrucks_modi_widget,
        )

        competitions_button = CustomContentToggleButton(
            size_hint=(1, 1),
            group="content_button",
            text=strings.BUTTON_STR_COMPETITIONS,
            font_size="32sp",
            container=self.display_container,
            display_widget=competitions_modi_widget,
        )

        # Add widgets to layout
        self.content_layout.add_widget(questions_label)
        self.content_layout.add_widget(firetrucks_button)
        self.content_layout.add_widget(competitions_button)
        self.content_layout.add_widget(self.display_container)

    def add_firetruck_modi_widget(self):
        firetrucks_modi_widget = BoxLayout(
            orientation="vertical",
            spacing="3dp",
        )

        firetrucks_modi_widget.add_widget(
            Label(
                size_hint=(1, 0.5),
                text=strings.LABEL_STR_MODE,
                font_size="32sp",
                bold=True,
            )
        )

        ### BUTTON 1 ###
        firetruck_btn1 = Button(
            pos_hint={"center_x": 0.5},
            text=f"{strings.BUTTON_STR_TRAINING} --->",
            font_size="32sp",
        )

        firetruck_btn1.bind(
            on_release=lambda instance: self.forward_mode2menu_manually(
                "fahrzeugkunde_menu", strings.BUTTON_STR_TRAINING
            )
        )

        firetruck_btn1.bind(
            on_release=lambda instance: self.update_firetruck_buttons(
                strings.BUTTON_STR_TRAINING
            )
        )

        firetrucks_modi_widget.add_widget(firetruck_btn1)

        ### BUTTON 2 ###
        firetruck_btn2 = Button(
            pos_hint={"center_x": 0.5},
            text=f"{strings.BUTTON_STR_GAME} --->",
            font_size="32sp",
        )

        firetruck_btn2.bind(
            on_release=lambda instance: self.forward_mode2menu_manually(
                "fahrzeugkunde_menu", strings.BUTTON_STR_GAME
            )
        )

        firetruck_btn2.bind(
            on_release=lambda instance: self.update_firetruck_buttons(
                strings.BUTTON_STR_GAME
            )
        )

        firetrucks_modi_widget.add_widget(firetruck_btn2)

        ### BUTTON 3 ###
        firetruck_btn3 = Button(
            pos_hint={"center_x": 0.5},
            text=f"{strings.BUTTON_STR_BROWSE} --->",
            font_size="32sp",
        )

        firetruck_btn3.bind(
            on_release=lambda instance: self.forward_mode2menu_manually(
                "fahrzeugkunde_menu", strings.BUTTON_STR_BROWSE
            )
        )

        firetruck_btn3.bind(
            on_release=lambda instance: self.update_firetruck_buttons(
                strings.BUTTON_STR_BROWSE
            )
        )

        firetrucks_modi_widget.add_widget(firetruck_btn3)

        ### BUTTON 4 ###
        firetruck_btn4 = Button(
            pos_hint={"center_x": 0.5},
            text=f"{strings.BUTTON_STR_IMAGES} --->",
            font_size="32sp",
        )

        firetruck_btn4.bind(
            on_release=lambda instance: self.forward_mode2menu_manually(
                "fahrzeugkunde_menu", strings.BUTTON_STR_IMAGES
            )
        )

        firetruck_btn4.bind(
            on_release=lambda instance: self.update_firetruck_buttons(
                strings.BUTTON_STR_IMAGES
            )
        )

        firetrucks_modi_widget.add_widget(firetruck_btn4)

        ### BUTTON 5 ###
        firetruck_btn5 = Button(
            pos_hint={"center_x": 0.5},
            text=f"{strings.BUTTON_STR_EXAM} --->",
            font_size="32sp",
        )

        firetruck_btn5.bind(
            on_release=lambda instance: self.forward_mode2menu_manually(
                "fahrzeugkunde_menu", strings.BUTTON_STR_EXAM
            )
        )

        firetruck_btn5.bind(
            on_release=lambda instance: self.update_firetruck_buttons(
                strings.BUTTON_STR_EXAM
            )
        )

        firetrucks_modi_widget.add_widget(firetruck_btn5)

        ### BUTTON 6 ###
        firetruck_btn6 = Button(
            pos_hint={"center_x": 0.5},
            text=f"{strings.BUTTON_STR_TRAINING_NEW} --->",
            font_size="32sp",
        )

        firetruck_btn6.bind(
            on_release=lambda instance: self.forward_mode2menu_manually(
                "fahrzeugkunde_menu", strings.BUTTON_STR_TRAINING_NEW
            )
        )

        firetruck_btn6.bind(
            on_release=lambda instance: self.update_firetruck_buttons(
                strings.BUTTON_STR_TRAINING_NEW
            )
        )

        firetrucks_modi_widget.add_widget(firetruck_btn6)

        return firetrucks_modi_widget

    def add_competition_modi_widget(self):
        ### WIDGET ###
        competitions_modi_widget = BoxLayout(
            orientation="vertical",
            spacing="3dp",
        )

        competitions_modi_widget.add_widget(
            Label(
                size_hint=(1, 0.5),
                text=strings.LABEL_STR_MODE,
                font_size="32sp",
                bold=True,
            )
        )

        ### BUTTON 1 ###
        competition_btn1 = Button(
            pos_hint={"center_x": 0.5},
            text=f"{strings.BUTTON_STR_TRAINING} --->",
            font_size="32sp",
        )

        competition_btn1.bind(
            on_release=lambda instance: self.forward_mode2menu_manually(
                "bewerb_menu", strings.BUTTON_STR_TRAINING
            )
        )

        competition_btn1.bind(
            on_release=lambda instance: self.update_firetruck_buttons(
                strings.BUTTON_STR_TRAINING
            )
        )

        competitions_modi_widget.add_widget(competition_btn1)

        ### BUTTON 2 ###
        competition_btn2 = Button(
            pos_hint={"center_x": 0.5},
            text=f"{strings.BUTTON_STR_GAME} --->",
            font_size="32sp",
        )

        competition_btn2.bind(
            on_release=lambda instance: self.forward_mode2menu_manually(
                "bewerb_menu", strings.BUTTON_STR_GAME
            )
        )

        competition_btn2.bind(
            on_release=lambda instance: self.update_firetruck_buttons(
                strings.BUTTON_STR_GAME
            )
        )

        competitions_modi_widget.add_widget(competition_btn2)

        ### BUTTON 3 ###
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

    def add_firetruck_button(self, firetruck: str):
        abbreviation = strings.trucks_hallein.get(firetruck, "")
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
            on_release=self.manager.get_screen("fahrzeugkunde_menu").on_button_release
        )

        # Add the button to the layout
        self.manager.get_screen("fahrzeugkunde_menu").ids.firetrucks_layout.add_widget(
            btn
        )

    def update_firetruck_buttons(self, mode_name: str):
        self.manager.get_screen(
            "fahrzeugkunde_menu"
        ).ids.firetrucks_scrollview.scroll_y = 1

        # load available firetrucks
        total_storage = load_total_storage()
        self.total_firetrucks = list(total_storage.keys())

        # create button for all firetrucks
        self.manager.get_screen(
            "fahrzeugkunde_menu"
        ).ids.firetrucks_layout.clear_widgets()

        mode = mode_str2bool(mode_name.strip())
        (
            mode_training,
            mode_training_new,
            mode_game,
            mode_browse,
            mode_images,
            mode_exam,
        ) = mode

        if mode_training or mode_game:
            excluded_firetrucks = ["BDLP-Tank1", "TestTruck"]

            for firetruck in self.total_firetrucks:

                if firetruck in excluded_firetrucks:
                    # skip BDLP and always add at the bottom of the list
                    continue

                self.add_firetruck_button(firetruck)

        elif mode_browse:
            for firetruck in self.total_firetrucks:
                self.add_firetruck_button(firetruck)

        elif mode_images:
            firetruck = "RüstLösch"
            self.add_firetruck_button(firetruck)

        elif mode_exam:
            # create button for BDLP-Tank1
            firetruck = "BDLP-Tank1"
            self.add_firetruck_button(firetruck)

        elif mode_training_new:
            # create button for BDLP-Tank1
            firetruck = "TestTruck"
            self.add_firetruck_button(firetruck)


class CustomContentToggleButton(ToggleButton):
    def __init__(self, container, display_widget, **kwargs):
        super().__init__(**kwargs)
        self.container = (
            container  # Reference to the container for displaying the widget
        )
        self.display_widget = display_widget  # The widget to show when selected
        self.scheduled_event = None  # To store the scheduled event for cancellation

    def on_touch_up(self, touch):
        super_result = super(CustomContentToggleButton, self).on_touch_up(touch)

        if self.collide_point(*touch.pos):  # Ensure the button was actually clicked
            if self.state == "down":
                # If there's a scheduled event, cancel it to avoid duplicate scheduling
                if self.scheduled_event:
                    Clock.unschedule(self.scheduled_event)

                self.container.clear_widgets()  # Remove any previous content

                # Schedule the widget appearance with a 0.5-second delay
                self.scheduled_event = Clock.schedule_once(self.show_widget, 0.3)
            else:
                # If button is deselected, cancel any scheduled event and remove the widget immediately
                if self.scheduled_event:
                    Clock.unschedule(self.scheduled_event)
                self.container.clear_widgets()

        return super_result

    def show_widget(self, dt):
        self.container.add_widget(self.display_widget)  # Add the new content


class FeuerwehrApp(App):
    def build(self):

        try:
            # path relative to app/helper/file_handling.py
            transfer_file("../storage", "scores.yaml")
            transfer_file("../storage", "main.cfg")

            sm = ScreenManager()
            sm.add_widget(Start_Menu())
            sm.add_widget(Info_Screen())
            # sm.add_widget(Settings_Screen())
            sm.add_widget(Fahrzeugkunde_Menu())
            sm.add_widget(Bewerb_Menu())
            sm.add_widget(Fahrzeugkunde_Training())
            sm.add_widget(Fahrzeugkunde_Training_New())
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
