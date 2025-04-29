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

from helper.functions import load_total_storage, create_scores_text, mode_str2bool
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

        ### BUTTON Übung ###
        firetruck_btn1 = Button(
            pos_hint={"center_x": 0.5},
            text=f"{strings.BUTTON_STR_TRAINING} --->",
            font_size="32sp",
        )

        firetruck_btn1.bind(  # type: ignore[attr-defined]
            on_release=lambda instance: self.forward_mode2menu_manually(
                "fahrzeugkunde_menu", strings.BUTTON_STR_TRAINING
            )
        )

        firetruck_btn1.bind(  # type: ignore[attr-defined]
            on_release=lambda instance: self.update_firetruck_buttons(
                strings.BUTTON_STR_TRAINING
            )
        )

        firetrucks_modi_widget.add_widget(firetruck_btn1)

        ### BUTTON Zeitdruck ###
        firetruck_btn2 = Button(
            pos_hint={"center_x": 0.5},
            text=f"{strings.BUTTON_STR_GAME} --->",
            font_size="32sp",
        )

        firetruck_btn2.bind(  # type: ignore[attr-defined]
            on_release=lambda instance: self.forward_mode2menu_manually(
                "fahrzeugkunde_menu", strings.BUTTON_STR_GAME
            )
        )

        firetruck_btn2.bind(  # type: ignore[attr-defined]
            on_release=lambda instance: self.update_firetruck_buttons(
                strings.BUTTON_STR_GAME
            )
        )

        firetrucks_modi_widget.add_widget(firetruck_btn2)

        # ### BUTTON Stöbern ###
        # firetruck_btn3 = Button(
        #     pos_hint={"center_x": 0.5},
        #     text=f"{strings.BUTTON_STR_BROWSE} --->",
        #     font_size="32sp",
        # )

        # firetruck_btn3.bind(   # type: ignore[attr-defined]
        #     on_release=lambda instance: self.forward_mode2menu_manually(
        #         "fahrzeugkunde_menu", strings.BUTTON_STR_BROWSE
        #     )
        # )

        # firetruck_btn3.bind(   # type: ignore[attr-defined]
        #     on_release=lambda instance: self.update_firetruck_buttons(
        #         strings.BUTTON_STR_BROWSE
        #     )
        # )

        # firetrucks_modi_widget.add_widget(firetruck_btn3)

        # ### BUTTON Bilder ###
        # firetruck_btn4 = Button(
        #     pos_hint={"center_x": 0.5},
        #     text=f"{strings.BUTTON_STR_IMAGES} --->",
        #     font_size="32sp",
        # )

        # firetruck_btn4.bind(   # type: ignore[attr-defined]
        #     on_release=lambda instance: self.forward_mode2menu_manually(
        #         "fahrzeugkunde_menu", strings.BUTTON_STR_IMAGES
        #     )
        # )

        # firetruck_btn4.bind(   # type: ignore[attr-defined]
        #     on_release=lambda instance: self.update_firetruck_buttons(
        #         strings.BUTTON_STR_IMAGES
        #     )
        # )

        # firetrucks_modi_widget.add_widget(firetruck_btn4)

        # ### BUTTON Leistungsprüfung ###
        # firetruck_btn5 = Button(
        #     pos_hint={"center_x": 0.5},
        #     text=f"{strings.BUTTON_STR_EXAM} --->",
        #     font_size="32sp",
        # )

        # firetruck_btn5.bind(  # type: ignore[attr-defined]
        #     on_release=lambda instance: self.forward_mode2menu_manually(
        #         "fahrzeugkunde_menu", strings.BUTTON_STR_EXAM
        #     )
        # )

        # firetruck_btn5.bind(  # type: ignore[attr-defined]
        #     on_release=lambda instance: self.update_firetruck_buttons(
        #         strings.BUTTON_STR_EXAM
        #     )
        # )

        # firetrucks_modi_widget.add_widget(firetruck_btn5)

        # ### BUTTON Übung mit Bildern ###
        # firetruck_btn6 = Button(
        #     pos_hint={"center_x": 0.5},
        #     text=f"{strings.BUTTON_STR_TRAINING_NEW} --->",
        #     font_size="32sp",
        #     # Modus not ready yet
        #     disabled=True,
        # )

        # firetruck_btn6.bind(  # type: ignore[attr-defined]
        #     on_release=lambda instance: self.forward_mode2menu_manually(
        #         "fahrzeugkunde_menu", strings.BUTTON_STR_TRAINING_NEW
        #     )
        # )

        # firetruck_btn6.bind(  # type: ignore[attr-defined]
        #     on_release=lambda instance: self.update_firetruck_buttons(
        #         strings.BUTTON_STR_TRAINING_NEW
        #     )
        # )

        # firetrucks_modi_widget.add_widget(firetruck_btn6)

        ### BUTTON Placeholder ###
        firetrucks_modi_widget.add_widget(
            Label(  # placeholder
                size_hint=(1, 1),
                font_size="32sp",
            )
        )

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

        ### BUTTON Übung ###
        competition_btn1 = Button(
            pos_hint={"center_x": 0.5},
            text=f"{strings.BUTTON_STR_TRAINING} --->",
            font_size="32sp",
        )

        competition_btn1.bind(  # type: ignore[attr-defined]
            on_release=lambda instance: self.forward_mode2menu_manually(
                "bewerb_menu", strings.BUTTON_STR_TRAINING
            )
        )

        competition_btn1.bind(  # type: ignore[attr-defined]
            on_release=lambda instance: self.update_firetruck_buttons(
                strings.BUTTON_STR_TRAINING
            )
        )

        competitions_modi_widget.add_widget(competition_btn1)

        ### BUTTON Zeitdruck ###
        competition_btn2 = Button(
            pos_hint={"center_x": 0.5},
            text=f"{strings.BUTTON_STR_GAME} --->",
            font_size="32sp",
        )

        competition_btn2.bind(  # type: ignore[attr-defined]
            on_release=lambda instance: self.forward_mode2menu_manually(
                "bewerb_menu", strings.BUTTON_STR_GAME
            )
        )

        competition_btn2.bind(  # type: ignore[attr-defined]
            on_release=lambda instance: self.update_firetruck_buttons(
                strings.BUTTON_STR_GAME
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

    def add_firetruck_button(self, firetruck: str, disabled: bool = False):
        abbreviation = strings.trucks_hallein.get(firetruck, "")
        # Create a button with two strings, one centered and one at the bottom right
        btn = Button(
            text=f"{firetruck}{' '*3}[size=30]{abbreviation}[/size]",
            font_size="32sp",
            markup=True,  # Enable markup for custom text positioning
            size_hint_y=None,
            height=150,
            size_hint_x=1,
            disabled=disabled,
        )
        btn.bind(  # type: ignore[attr-defined]
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
            # excluded_firetrucks = ["BDLP-Tank1", "TestTruck"]
            excluded_firetrucks = ["BDLP-Tank1"]
            disabled_firetrucks = []  # ["Tank2"]

            for firetruck in self.total_firetrucks:

                if firetruck in excluded_firetrucks:
                    # skip BDLP and always add at the bottom of the list
                    continue

                if firetruck in disabled_firetrucks:
                    self.add_firetruck_button(firetruck, disabled=True)
                else:
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

            self.sm = ScreenManager()
            self.sm.add_widget(Start_Menu())
            self.sm.add_widget(Info_Screen())
            self.sm.add_widget(Acknowledgement_Screen())
            # self.sm.add_widget(Settings_Screen())
            self.sm.add_widget(Fahrzeugkunde_Menu())
            self.sm.add_widget(Bewerb_Menu())
            self.sm.add_widget(Fahrzeugkunde_Training())
            # self.sm.add_widget(Fahrzeugkunde_Training_New())
            self.sm.add_widget(Fahrzeugkunde_Game())
            self.sm.add_widget(Fahrzeugkunde_Browse())
            self.sm.add_widget(Fahrzeugkunde_Images())
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
                    "fahrzeugkunde_menu",
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
