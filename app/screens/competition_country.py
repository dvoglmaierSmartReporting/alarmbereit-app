from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import Screen

from typing import cast

from helper.functions import change_screen_to
from helper.settings import Strings


strings = Strings()


class Bewerb_Bundesland(Screen):
    def __init__(self, **kwargs):
        super(Bewerb_Bundesland, self).__init__(**kwargs)

        self.country_layout = cast(BoxLayout, self.country_layout)
        self.country_label = cast(Label, self.country_label)

        self.country_label.text = strings.LABEL_STR_COUNTRY

        # load available countries
        countries = [
            "Salzburg",
            "Burgenland",
            "Kärnten",
            "Steiermark",
            "Niederösterreich",
            "Oberösterreich",
            "Tirol",
            "Vorarlberg",
            "Wien",
        ]
        # create button for all countries
        for country in countries:
            btn = Button(
                text=country,
                font_size="32sp",
                size_hint_y=None,
                height=150,
                size_hint_x=1,
                disabled=country != "Salzburg",
            )
            btn.bind(on_release=self.on_button_release)
            self.country_layout.add_widget(btn)

    def on_enter(self):
        # Reset the scrollview to the top
        self.ids.country_scrollview.scroll_y = 1

    def on_button_release(self, instance):
        change_screen_to("bewerb_menu", transition_direction="left")

    def go_back(self, *args) -> None:
        change_screen_to("start_menu")
