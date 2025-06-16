from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import Screen

from typing import cast

from helper.functions import change_screen_to
from helper.settings import Strings


strings = Strings()


class Fahrzeugkunde_Login(Screen):
    def __init__(self, **kwargs):
        super(Fahrzeugkunde_Login, self).__init__(**kwargs)

        self.login_label = cast(Label, self.login_label)
        # self.login_button = cast(Button, self.login_button)
        # self.city_label = cast(Label, self.city_label)
        self.city_layout = cast(BoxLayout, self.city_layout)

        self.login_label.text = strings.LABEL_STR_LOGIN
        # self.login_button.text = strings.BUTTON_STR_LOGIN
        # self.city_label.text = strings.LABEL_STR_DEPARTMENT

        # load available departments
        departments = [
            "Hallein",
            "Bad Dürrnberg",
            "Altenmarkt a.d. Alz",
            "Kuchl",
            "Elsbethen",
        ]
        departments_disabled = ["Kuchl", "Elsbethen"]

        # create button for all countries
        for department in departments:
            btn = Button(
                text=department,
                font_size="32sp",
                size_hint_y=None,
                height=150,
                size_hint_x=1,
                disabled=department in departments_disabled,
            )
            btn.bind(on_release=self.on_button_release)
            self.city_layout.add_widget(btn)

    def on_button_release(self, instance):
        change_screen_to("fahrzeugkunde_mode", transition_direction="left")

        app = App.get_running_app()
        app_root = app.root

        # forward city selection to mode screen for content loading
        screen = app_root.get_screen("fahrzeugkunde_mode")
        screen.select_city(instance.text)

    def go_back(self, *args) -> None:
        change_screen_to("start_menu")
