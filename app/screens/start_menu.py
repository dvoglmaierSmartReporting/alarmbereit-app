from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout

# from kivy.uix.image import Image
# from kivy.properties import StringProperty
from kivy.uix.layout import Layout
from kivy.uix.screenmanager import Screen, SlideTransition

from typing import cast

from helper.functions import change_screen_to, create_scores_text
from helper.file_handling import (
    read_scores_file,
    get_selected_city_state,
)
from helper.aspect_image import get_city_image
from helper.settings import Strings


strings = Strings()


# class AspectImage(Image):
#     source = StringProperty()

#     def __init__(self, **kwargs):
#         super().__init__(**kwargs)

#         self.bind(texture=self._on_texture, size=self._on_size)

#     def _on_texture(self, *args):
#         self._update_size()

#     def _on_size(self, *args):
#         self._update_size()

#     def _update_size(self):
#         if self.texture:
#             image_ratio = self.texture.width / self.texture.height
#             self.size_hint_x = None
#             self.width = self.height * image_ratio


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
        fahrzeuge_button.bind(
            on_release=lambda instance: change_screen_to("fahrzeugkunde_mode", "left")
        )

        bewerbe_button = Button(
            size_hint=(1, 1),
            text=strings.BUTTON_STR_COMPETITIONS,
            font_size="32sp",
        )

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
        info_text = create_scores_text(read_scores_file(), self.selected_city)

        info_text += "\n\n\n\n"

        self.manager.get_screen("info_screen").ids.info_text_label.text = info_text
