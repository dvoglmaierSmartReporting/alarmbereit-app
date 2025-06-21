from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import Screen
from kivy.clock import Clock
from kivy.uix.togglebutton import ToggleButton

from helper.functions import change_screen_to
from helper.file_handling import read_main_cfg, update_main_cfg
from helper.settings import Strings


strings = Strings()


class Login(Screen):
    def __init__(self, **kwargs):
        super(Login, self).__init__(**kwargs)

        self.ids.login_label.text = strings.LABEL_STR_LOGIN

        self.ids.store_selection_button.text = strings.BUTTON_STR_STORE_SELECTION

        self.ids.store_selection_button.disabled = True

    def on_pre_enter(self):
        # Clear existing buttons
        self.ids.city_layout.clear_widgets()
        self.ids.store_selection_button.disabled = True

        self.cities = [
            ("Hallein", "Salzburg"),
            ("Bad Dürrnberg", "Salzburg"),
            ("Altenmarkt a.d. Alz", "Bayern"),
        ]

        for city, country in self.cities:
            btn = ToggleButton(
                text=f"{city}   ({country})",
                font_size="32sp",
                group="city",
                allow_no_selection=True,
                size_hint_y=None,
                height="150dp",
            )
            btn.bind(on_release=self.on_city_toggle)
            self.ids.city_layout.add_widget(btn)

    def on_city_toggle(self, instance):
        if instance.state == "down":
            self.selected_button = instance.text

            # deactivate others
            for btn in self.ids.city_layout.children:
                if btn != instance and btn.state == "down":
                    btn.state = "normal"

            self.ids.store_selection_button.disabled = False

        else:
            self.selected_button = ""
            self.ids.store_selection_button.disabled = True

    def store_selection(self):
        self.selected_country = self.selected_button.split("(")[1][:-1]

        if "Hallein" in self.selected_button:
            self.selected_city = "Hallein"
        elif "Dürrnberg" in self.selected_button:
            self.selected_city = "Bad Dürrnberg"
        elif "Altenmarkt" in self.selected_button:
            self.selected_city = "Altenmarkt a.d. Alz"

        main_cfg = read_main_cfg()
        main_cfg["content"]["city"] = self.selected_city
        main_cfg["content"]["country"] = self.selected_country

        update_main_cfg(main_cfg)

        change_screen_to("start_menu", transition_direction="left")
