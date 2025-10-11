from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.screenmanager import Screen, SlideTransition
from kivy.config import Config

from helper.functions import (
    get_firetruck_abbreviations,
)
from helper.file_handling import (
    get_selected_city_state,
    load_app_version,
    update_config_firetruck,
)
from helper.aspect_image import get_city_image, get_team122_image
from helper.strings import Strings, About_Text


strings = Strings()


class Start_Menu(Screen):
    def __init__(self, **kwargs):
        super(Start_Menu, self).__init__(**kwargs)

        self.ids.all_cities_button.text = strings.BUTTON_STR_ALL_CITIES

        self.version = load_app_version()

    def on_pre_enter(self):
        self.selected_city, _ = get_selected_city_state()

        self.abbreviations = get_firetruck_abbreviations(self.selected_city)

        self.add_city_logo()

        self.ids.score_button.text = strings.BUTTON_STR_SCORE

        self.add_mode_buttons()

        self.add_about_text()

        self.add_team122_logo()

    def add_city_logo(self):
        self.ids.logo_layout.clear_widgets()
        self.ids.logo_layout.add_widget(get_city_image(self.selected_city))

    def add_mode_buttons(self):
        self.ids.content_layout.clear_widgets()

        ### BUTTON Übung ###
        firetruck_training_btn = self.create_button(strings.BUTTON_STR_TRAINING)
        self.ids.content_layout.add_widget(firetruck_training_btn)

        ### BUTTON Zeitdruck ###
        firetruck_game_btn = self.create_button(strings.BUTTON_STR_GAME)
        self.ids.content_layout.add_widget(firetruck_game_btn)

        # ### BUTTON Stöbern ###
        # firetruck_browse_btn = self.create_button(strings.BUTTON_STR_BROWSE)
        # self.ids.content_layout.add_widget(firetruck_browse_btn)

        # ### BUTTON Bilder ###
        # firetruck_images_btn = self.create_button(strings.BUTTON_STR_IMAGES)
        # self.ids.content_layout.add_widget(firetruck_images_btn)

        # ### BUTTON Leistungsprüfung ###
        # firetruck_exam_btn = self.create_button(strings.BUTTON_STR_EXAM)
        # self.ids.content_layout.add_widget(firetruck_exam_btn)

        ### BUTTON Übung mit Bildern ###
        if self.selected_city in ["Hallein"]:
            firetruck_training_with_images_btn = self.create_button(
                strings.BUTTON_STR_TRAINING_NEW, disabled=False
            )
            self.ids.content_layout.add_widget(firetruck_training_with_images_btn)

    def create_button(self, button_text: str, disabled: bool = False) -> Button:
        btn = Button(
            pos_hint={"center_x": 0.5},
            text=button_text,
            font_size="32sp",
            disabled=disabled,
        )

        btn.bind(on_release=lambda instance: self.transit_screen("firetruck_menu"))

        btn.bind(
            on_release=lambda instance: update_config_firetruck({"mode": button_text})
        )

        return btn

    def add_about_text(self):
        about_label = Label(
            size_hint=(1, 1),
            text=About_Text(self.version).TEXT,
            font_size="13sp",
            halign="center",
        )
        self.ids.content_layout.add_widget(about_label)

    def add_team122_logo(self):
        team122_logo = get_team122_image()
        self.ids.content_layout.add_widget(team122_logo)

    def transit_screen(self, menu_screen: str):
        self.manager.transition = SlideTransition(direction="left")
        self.manager.current = menu_screen
