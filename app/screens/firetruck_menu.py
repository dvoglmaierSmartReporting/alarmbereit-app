from kivy.uix.button import Button
from kivy.uix.screenmanager import Screen

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


strings = Strings()


class Firetruck_Menu(Screen):
    def on_pre_enter(self):
        self.update_mode_label()

        self.update_city_logo()

        self.abbreviations = get_firetruck_abbreviations(self.selected_city)

        self.update_firetruck_buttons()

    def update_mode_label(self):
        self.selected_mode = get_selected_mode()
        self.ids.mode_label.text = self.selected_mode

    def update_city_logo(self):
        self.selected_city, _ = get_selected_city_state()
        self.ids.logo_layout.clear_widgets()
        self.ids.logo_layout.add_widget(get_city_image(f"{self.selected_city}_small"))

    def on_button_release(self, instance):
        update_config_firetruck(
            {
                "selected_firetruck": instance.text.split(" ")[0],
            }
        )

        mode = mode_str2bool(self.selected_mode)
        (
            mode_training,
            mode_training_new,
            mode_game,
            mode_browse,
            mode_images,
            mode_exam,
        ) = mode

        if mode_training:
            next_screen = "firetruck_training"

        elif mode_training_new:
            next_screen = "firetruck_training_with_images"

        elif mode_game:
            next_screen = "firetruck_game"

        # elif mode_browse:
        #     next_screen = "firetruck_browse"

        # elif mode_images:
        #     next_screen = "firetruck_images"

        # elif mode_exam:
        #     next_screen = "firetruck_exam"

        change_screen_to(next_screen, transition_direction="left")

    def update_firetruck_buttons(self):
        self.ids.firetrucks_scrollview.scroll_y = 1

        # load available firetrucks
        total_storage = load_total_storage(self.selected_city)
        self.total_firetrucks = list(total_storage.keys())

        # create button for all firetrucks
        self.ids.firetrucks_layout.clear_widgets()

        mode = mode_str2bool(self.selected_mode)
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
            firetruck = "Leiter"
            self.add_firetruck_button(firetruck)

    def add_firetruck_button(self, firetruck: str, disabled: bool = False):
        abbreviation = self.abbreviations.get(firetruck, "")
        # Create a button with two strings, one centered and one at the bottom right

        if self.selected_city == "Hallein":
            button_height = 200
        else:
            button_height = 350

        btn = Button(
            text=f"{firetruck}{' '*3}[size=30]{abbreviation}[/size]",
            markup=True,  # Enable markup for custom text positioning
            font_size="32sp",
            size_hint_y=None,
            height=button_height,
            size_hint_x=1,
            disabled=disabled,
        )
        btn.bind(on_release=self.on_button_release)

        # Add the button to the layout
        self.ids.firetrucks_layout.add_widget(btn)

    def go_back(self, *args) -> None:
        # change_screen_to("firetruck_mode")
        change_screen_to("start_menu")
