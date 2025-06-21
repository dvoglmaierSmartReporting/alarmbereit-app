from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import Screen, SlideTransition

from helper.functions import (
    load_total_storage,
    mode_str2bool,
    change_screen_to,
    get_firetruck_abbreviation_values,
)
from helper.file_handling import get_selected_city_country, get_logo_file_path
from helper.settings import Strings


strings = Strings()


class Fahrzeugkunde_Mode(Screen):
    def __init__(self, **kwargs):
        super(Fahrzeugkunde_Mode, self).__init__(**kwargs)

        self.ids.modes_label.text = strings.LABEL_STR_MODES

    def on_kv_post(self, base_widget):
        self.ids.modes_layout.add_widget(self.add_firetruck_modi_widget())

    def on_pre_enter(self):
        # read from main.cfg
        self.selected_city, _ = get_selected_city_country()
        self.abbreviations = get_firetruck_abbreviation_values(self.selected_city)

        # update city logo
        self.ids.logo_layout.source = get_logo_file_path(self.selected_city)

    def add_firetruck_modi_widget(self):
        firetrucks_modi_widget = BoxLayout(
            orientation="vertical",
            spacing="5dp",
        )

        ### BUTTON Übung ###
        firetruck_btn1 = Button(
            pos_hint={"center_x": 0.5},
            text=strings.BUTTON_STR_TRAINING,
            font_size="32sp",
        )

        firetruck_btn1.bind(
            on_release=lambda instance: self.forward_mode2menu_manually(
                "fahrzeugkunde_menu", strings.BUTTON_STR_TRAINING
            )
        )

        firetruck_btn1.bind(
            on_release=lambda instance: self.update_firetruck_buttons(
                strings.BUTTON_STR_TRAINING
            )
        )

        firetrucks_modi_widget.add_widget(firetruck_btn1)

        ### BUTTON Zeitdruck ###
        firetruck_btn2 = Button(
            pos_hint={"center_x": 0.5},
            text=strings.BUTTON_STR_GAME,
            font_size="32sp",
        )

        firetruck_btn2.bind(
            on_release=lambda instance: self.forward_mode2menu_manually(
                "fahrzeugkunde_menu", strings.BUTTON_STR_GAME
            )
        )

        firetruck_btn2.bind(
            on_release=lambda instance: self.update_firetruck_buttons(
                strings.BUTTON_STR_GAME
            )
        )

        firetrucks_modi_widget.add_widget(firetruck_btn2)

        # ### BUTTON Stöbern ###
        # firetruck_btn3 = Button(
        #     pos_hint={"center_x": 0.5},
        #     text=f"{strings.BUTTON_STR_BROWSE} --->",
        #     font_size="32sp",
        # )

        # firetruck_btn3.bind(
        #     on_release=lambda instance: self.forward_mode2menu_manually(
        #         "fahrzeugkunde_menu", strings.BUTTON_STR_BROWSE
        #     )
        # )

        # firetruck_btn3.bind(
        #     on_release=lambda instance: self.update_firetruck_buttons(
        #         strings.BUTTON_STR_BROWSE
        #     )
        # )

        # firetrucks_modi_widget.add_widget(firetruck_btn3)

        # ### BUTTON Bilder ###
        # firetruck_btn4 = Button(
        #     pos_hint={"center_x": 0.5},
        #     text=f"{strings.BUTTON_STR_IMAGES} --->",
        #     font_size="32sp",
        # )

        # firetruck_btn4.bind(
        #     on_release=lambda instance: self.forward_mode2menu_manually(
        #         "fahrzeugkunde_menu", strings.BUTTON_STR_IMAGES
        #     )
        # )

        # firetruck_btn4.bind(
        #     on_release=lambda instance: self.update_firetruck_buttons(
        #         strings.BUTTON_STR_IMAGES
        #     )
        # )

        # firetrucks_modi_widget.add_widget(firetruck_btn4)

        # ### BUTTON Leistungsprüfung ###
        # firetruck_btn5 = Button(
        #     pos_hint={"center_x": 0.5},
        #     text=f"{strings.BUTTON_STR_EXAM} --->",
        #     font_size="32sp",
        # )

        # firetruck_btn5.bind(
        #     on_release=lambda instance: self.forward_mode2menu_manually(
        #         "fahrzeugkunde_menu", strings.BUTTON_STR_EXAM
        #     )
        # )

        # firetruck_btn5.bind(
        #     on_release=lambda instance: self.update_firetruck_buttons(
        #         strings.BUTTON_STR_EXAM
        #     )
        # )

        # firetrucks_modi_widget.add_widget(firetruck_btn5)

        # ### BUTTON Übung mit Bildern ###
        # firetruck_btn6 = Button(
        #     pos_hint={"center_x": 0.5},
        #     text=f"{strings.BUTTON_STR_TRAINING_NEW} --->",
        #     font_size="32sp",
        #     # Modus not ready yet
        #     disabled=True,
        # )

        # firetruck_btn6.bind(
        #     on_release=lambda instance: self.forward_mode2menu_manually(
        #         "fahrzeugkunde_menu", strings.BUTTON_STR_TRAINING_NEW
        #     )
        # )

        # firetruck_btn6.bind(
        #     on_release=lambda instance: self.update_firetruck_buttons(
        #         strings.BUTTON_STR_TRAINING_NEW
        #     )
        # )

        # firetrucks_modi_widget.add_widget(firetruck_btn6)

        ### BUTTON Placeholder ###
        firetrucks_modi_widget.add_widget(
            Label(  # placeholder
                size_hint=(1, 1),
                font_size="32sp",
            )
        )

        return firetrucks_modi_widget

    def forward_mode2menu_manually(self, menu_screen: str, mode: str):
        self.manager.transition = SlideTransition(direction="left")
        self.manager.current = menu_screen
        self.manager.get_screen(menu_screen).ids.mode_label.text = mode

    def update_firetruck_buttons(self, mode_name: str):
        self.manager.get_screen(
            "fahrzeugkunde_menu"
        ).ids.firetrucks_scrollview.scroll_y = 1

        # load available firetrucks
        total_storage = load_total_storage(self.selected_city)
        self.total_firetrucks = list(total_storage.keys())

        # create button for all firetrucks
        self.manager.get_screen(
            "fahrzeugkunde_menu"
        ).ids.firetrucks_layout.clear_widgets()

        mode = mode_str2bool(mode_name.strip())
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
            excluded_firetrucks = ["BDLP-Tank1"]
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
            firetruck = "TestTruck"
            self.add_firetruck_button(firetruck)

    def add_firetruck_button(self, firetruck: str, disabled: bool = False):

        abbreviation = self.abbreviations.get(firetruck, "")
        # Create a button with two strings, one centered and one at the bottom right
        btn = Button(
            text=f"{firetruck}{' '*3}[size=30]{abbreviation}[/size]",
            font_size="32sp",
            markup=True,  # Enable markup for custom text positioning
            size_hint_y=None,
            height=200,
            size_hint_x=1,
            disabled=disabled,
        )
        btn.bind(
            on_release=self.manager.get_screen("fahrzeugkunde_menu").on_button_release
        )

        # Add the button to the layout
        self.manager.get_screen("fahrzeugkunde_menu").ids.firetrucks_layout.add_widget(
            btn
        )

    def go_back(self, *args) -> None:
        change_screen_to("start_menu")
