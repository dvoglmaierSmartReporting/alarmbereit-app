from kivy.uix.button import Button
from kivy.uix.screenmanager import Screen
from kivy.core.window import Window
from kivy.metrics import dp

from helper.functions import (
    load_total_storage,
    mode_str2bool,
    change_screen_to,
    get_firetruck_abbreviations,
)
from helper.file_handling import (
    get_selected_city_state,
    get_selected_mode,
    update_config_firetruck,
)
from helper.aspect_image import get_city_image
from helper.strings import Strings

from screens.screen_base import FontSizeMixin


strings = Strings()


class Firetruck_Menu(FontSizeMixin, Screen):
    def on_pre_enter(self):
        self.update_mode_label()

        self.update_city_logo()

        self.abbreviations = get_firetruck_abbreviations(self.selected_city)

        self.update_firetruck_buttons()

    def on_enter(self):
        self.bind_font_scaling()

    def on_leave(self):
        self.unbind_font_scaling()

    def update_mode_label(self):
        self.selected_mode = get_selected_mode()
        self.ids.mode_label.text = self.selected_mode

    def update_city_logo(self):
        self.selected_city, _ = get_selected_city_state()
        self.ids.logo_layout.clear_widgets()
        self.ids.logo_layout.add_widget(get_city_image(f"{self.selected_city}_small"))

    def on_button_release(self, instance):
        for substring in [" ", "[size="]:
            truck_name = instance.text.strip().split(substring)[0]
            truck_name = truck_name.strip()

        update_config_firetruck(
            {
                "selected_firetruck": truck_name,
            }
        )

        mode = mode_str2bool(self.selected_mode)
        (
            mode_training,
            mode_training_with_images,
            mode_game,
            mode_browse,
            mode_images,
            mode_exam,
        ) = mode

        if mode_training:
            next_screen = "firetruck_training"

        elif mode_training_with_images:
            next_screen = "firetruck_training_with_images"

        elif mode_game:
            next_screen = "firetruck_game"

        change_screen_to(next_screen, transition_direction="left")

    def update_firetruck_buttons(self):
        self.ids.firetrucks_scrollview.scroll_y = 1

        # load available firetrucks
        total_storage = load_total_storage(self.selected_city)
        self.total_firetrucks = list(total_storage.keys())

        # create button for all firetrucks
        self.ids.firetrucks_layout.clear_widgets()
        self.dynamic_widgets.clear()  # Clear previous widget references

        mode = mode_str2bool(self.selected_mode)
        (
            mode_training,
            mode_training_with_images,
            mode_game,
            mode_browse,
            mode_images,
            mode_exam,
        ) = mode

        if mode_training or mode_game:
            # excluded_firetrucks = ["BDLP-Tank1", "TestTruck"]
            excluded_firetrucks = ["BDLP-Tank1", "TestTruck", "TestTruck2"]
            disabled_firetrucks = []  # ["Tank2"]

            for firetruck in self.total_firetrucks:

                if firetruck in excluded_firetrucks:
                    # skip BDLP and always add at the bottom of the list
                    continue

                if firetruck in disabled_firetrucks:
                    self.add_firetruck_button(firetruck, disabled=True)
                else:
                    self.add_firetruck_button(firetruck)

        elif mode_training_with_images:
            firetruck = "Leiter"
            self.add_firetruck_button(firetruck)

    def add_firetruck_button(self, firetruck: str, disabled: bool = False):
        abbreviation = self.abbreviations.get(firetruck, "")
        font_scale = self.get_font_scale()
        base_font_size = 15  # 20
        font_size_pixels = dp(base_font_size) * font_scale
        font_size_half_pixels = dp(base_font_size) * font_scale // 2

        if self.selected_city == "Hallein":
            button_height = 200
        else:
            button_height = 350

        spacer_title = " " * 6
        spacer_subtitle = " " * 13
        btn = Button(
            text=f"{spacer_title}{firetruck}[size={font_size_half_pixels}dp]\n{spacer_subtitle}{abbreviation}[/size]",
            markup=True,
            font_size=f"{font_size_pixels}dp",
            size_hint_y=None,
            height=button_height,
            size_hint_x=1,
            disabled=disabled,
            halign="left",
            text_size=(None, None),
        )

        # Set text_size after button is created to enable text alignment
        def set_text_size(instance, size):
            instance.text_size = (size[0], None)

        btn.bind(size=set_text_size)

        # Register button for font scaling
        self.register_widget_for_font_scaling(btn, base_font_size)

        btn.bind(on_release=self.on_button_release)
        self.ids.firetrucks_layout.add_widget(btn)

    def go_back(self, *args) -> None:
        change_screen_to("start_menu")
