from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.layout import Layout
from kivy.uix.screenmanager import Screen, SlideTransition

from typing import cast

from helper.functions import change_screen_to, create_scores_text
from helper.file_handling import (
    read_scores_file,
    get_selected_city_state,
)
from helper.aspect_image import get_city_image
from helper.settings import Strings, About_Text


strings = Strings()


class Start_Menu(Screen):
    def __init__(self, **kwargs):
        super(Start_Menu, self).__init__(**kwargs)
        
        self.ids.all_cities_button.text = strings.BUTTON_STR_ALL_CITIES

    def on_pre_enter(self):
        self.selected_city, _ = get_selected_city_state()

        # update city logo
        self.ids.logo_layout.clear_widgets()
        self.ids.logo_layout.add_widget(get_city_image(self.selected_city))

    def on_kv_post(self, base_widget):
        # type annotations
        self.score_button = cast(Button, self.score_button)
        # self.acknowledgement_button = cast(Button, self.acknowledgement_button)
        self.content_layout = cast(Layout, self.content_layout)

        # update button strings
        self.score_button.text = strings.BUTTON_STR_SCORE
        # self.acknowledgement_button.text = strings.BUTTON_STR_ACKNOWLEDGEMENT

        # Container where the additional widget will be displayed
        # Part of content_layout
        self.display_container = BoxLayout(
            size_hint=(1, 3), orientation="vertical", spacing="5dp", padding="20dp"
        )

        # FIRETRUCKS BUTTON
        fahrzeuge_button = Button(
            size_hint=(1, 1),
            text=strings.BUTTON_STR_FIRETRUCKS,
            font_size="32sp",
        )
        fahrzeuge_button.bind(
            on_release=lambda instance: change_screen_to("fahrzeugkunde_mode", "left")
        )

        # COMPETITIONS BUTTON
        bewerbe_button = Button(
            size_hint=(1, 1),
            text=strings.BUTTON_STR_COMPETITIONS,
            font_size="32sp",
        )

        bewerbe_button.bind(
            on_release=lambda instance: change_screen_to("bewerb_menu", "left")
        )

        about_label = Label(
            size_hint=(1, 1),
            text=About_Text().TEXT,
            font_size="15sp",
            halign="center",
        )

        # Add widgets to layout
        self.content_layout.add_widget(fahrzeuge_button)
        self.content_layout.add_widget(bewerbe_button)
        self.content_layout.add_widget(about_label)

    def forward_mode2menu_manually(self, menu_screen: str, mode: str):
        self.manager.transition = SlideTransition(direction="left")
        self.manager.current = menu_screen
        self.manager.get_screen(menu_screen).ids.mode_label.text = mode

    def update_info_text(self):
        info_text = (
            create_scores_text(read_scores_file(), self.selected_city) + "\n\n\n\n"
        )

        self.manager.get_screen("punkte_screen").ids.score_text_label.text = info_text
