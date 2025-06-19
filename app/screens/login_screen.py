from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import Screen
from kivy.clock import Clock

from typing import cast

from helper.functions import change_screen_to
from helper.file_handling import read_main_cfg, update_main_cfg
from helper.settings import Strings


strings = Strings()


class Login(Screen):
    def __init__(self, **kwargs):
        super(Login, self).__init__(**kwargs)

        self.login_label = cast(Label, self.login_label)
        # self.login_button = cast(Button, self.login_button)
        # self.city_label = cast(Label, self.city_label)
        self.city_layout = cast(BoxLayout, self.city_layout)

        self.login_label.text = strings.LABEL_STR_LOGIN
        # self.login_button.text = strings.BUTTON_STR_LOGIN
        # self.city_label.text = strings.LABEL_STR_CITY

        # load available cities
        cities = [
            ("Hallein", "Salzburg"),
            ("Bad Dürrnberg", "Salzburg"),
            ("Altenmarkt a.d. Alz", "Bayern"),
            ("Adnet", "Salzburg"),
            ("Elsbethen", "Salzburg"),
        ]
        cities_disabled = ["Adnet", "Elsbethen"]

        # TODO: CustomToggleButton group with only one selected Button a time
        # no selection possible

        # create button for all cities
        for city, country in cities:
            btn = Button(
                text=f"{city} ({country})",
                font_size="32sp",
                size_hint_y=None,
                height=150,
                size_hint_x=1,
                disabled=city in cities_disabled,
            )
            self.city_layout.add_widget(btn)

        # TODO: if selection, enable store_selection_button
        # if no selection, disable store_selection_button
        self.ids.store_selection_button.text = strings.BUTTON_STR_STORE_SELECTION

    def get_down_button(self):
        raise NotImplementedError

    def store_selection(self):
        # TODO: get down button from CustomToggleButton group

        city, country = self.get_down_button()

        main_cfg = read_main_cfg()
        main_cfg["content"]["city"] = city
        main_cfg["content"]["country"] = country

        update_main_cfg(main_cfg)

        change_screen_to("start_menu", transition_direction="left")

    def on_enter(self):
        main_cfg = read_main_cfg()

        selected_city = main_cfg["content"]["city"]
        selected_country = main_cfg["content"]["country"]

        print(f"{selected_city = }")

        if selected_city:
            # TODO: fix error!
            change_screen_to("start_menu", "left")

            # TODO: forward selected_city/country to following screens
