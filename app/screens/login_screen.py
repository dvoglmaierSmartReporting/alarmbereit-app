from kivy.uix.label import Label
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.screenmanager import Screen
from kivy.clock import Clock

from helper.functions import change_screen_to
from helper.file_handling import update_config, map_selected_city_2long_name
from helper.aspect_image import get_city_image, get_team122_small_image
from helper.strings import Strings, Info_Text


strings = Strings()


class Login(Screen):
    def __init__(self, **kwargs):
        super(Login, self).__init__(**kwargs)
        self.ids.login_label.text = strings.LABEL_STR_LOGIN
        self.ids.store_selection_button.text = strings.BUTTON_STR_STORE_SELECTION
        self.ids.store_selection_button.disabled = True

    def on_pre_enter(self):
        # Logo Hallein
        self.ids.logo_hallein_layout.clear_widgets()
        self.ids.logo_hallein_layout.add_widget(get_city_image("Hallein"))

        # Logo Team122
        self.ids.logo_team122_layout.clear_widgets()
        self.ids.logo_team122_layout.add_widget(get_team122_small_image())

        # Clear existing buttons
        self.ids.city_layout.clear_widgets()
        self.ids.store_selection_button.disabled = True

        self.cities = [
            ("Hallein", "Salzburg"),
            ("Bad Dürrnberg", "Salzburg"),
            ("Altenmarkt a.d. Alz", "Bayern"),
        ]

        for city, state in self.cities:
            btn = ToggleButton(
                text=f"{city}\n[size=35]{state}[/size]",
                markup=True,
                font_size="32sp",
                group="city",
                allow_no_selection=True,
                size_hint_y=None,
                height="150dp",
            )
            btn.bind(on_release=self.on_city_toggle)
            self.ids.city_layout.add_widget(btn)

        lbl = Label(
            text=Info_Text().TEXT,
            markup=True,
            font_size="17sp",
            size_hint_y=None,
            height="150dp",
        )
        self.ids.city_layout.add_widget(lbl)

    def on_city_toggle(self, instance):
        if instance.state == "down":
            self.selected_button = instance.text

            # deactivate others ToggleButtons
            for child in self.ids.city_layout.children:
                # ignore Label
                if isinstance(child, ToggleButton):
                    if child != instance and child.state == "down":
                        child.state = "normal"

            self.ids.store_selection_button.disabled = False

        else:
            self.selected_button = ""
            self.ids.store_selection_button.disabled = True

    def store_selection(self):
        state = self.selected_button.split("\n")[1]
        self.selected_state = state[9:-7]
        self.selected_city = map_selected_city_2long_name(self.selected_button)

        update_config(
            {
                "city": self.selected_city,
                "state": self.selected_state,
            }
        )

        change_screen_to("start_menu", transition_direction="left")
