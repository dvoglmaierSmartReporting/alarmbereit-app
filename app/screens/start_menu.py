from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.screenmanager import Screen, SlideTransition

from helper.functions import (
    create_scores_text,
    load_total_storage,
    mode_str2bool,
    get_firetruck_abbreviations,
)
from helper.file_handling import (
    read_scores_file,
    get_selected_city_state,
)
from helper.aspect_image import get_city_image, get_team122_image
from helper.strings import Strings, About_Text


strings = Strings()


class Start_Menu(Screen):
    def __init__(self, **kwargs):
        super(Start_Menu, self).__init__(**kwargs)

        self.ids.all_cities_button.text = strings.BUTTON_STR_ALL_CITIES

    def on_pre_enter(self):
        self.selected_city, _ = get_selected_city_state()
        self.abbreviations = get_firetruck_abbreviations(self.selected_city)

        # update city logo
        self.ids.logo_layout.clear_widgets()
        self.ids.logo_layout.add_widget(get_city_image(self.selected_city))

        self.ids.score_button.text = strings.BUTTON_STR_SCORE

        self.content_layout.clear_widgets()

        # ### BUTTON Übung ###
        firetruck_training_btn = self.create_button(strings.BUTTON_STR_TRAINING)
        self.content_layout.add_widget(firetruck_training_btn)

        # ### BUTTON Zeitdruck ###
        firetruck_game_btn = self.create_button(strings.BUTTON_STR_GAME)
        self.content_layout.add_widget(firetruck_game_btn)

        # ### BUTTON Stöbern ###
        # firetruck_browse_btn = self.create_button(strings.BUTTON_STR_BROWSE)
        # self.content_layout.add_widget(firetruck_browse_btn)

        # ### BUTTON Bilder ###
        # firetruck_images_btn = self.create_button(strings.BUTTON_STR_IMAGES)
        # self.content_layout.add_widget(firetruck_images_btn)

        # ### BUTTON Leistungsprüfung ###
        # firetruck_exam_btn = self.create_button(strings.BUTTON_STR_EXAM)
        # self.content_layout.add_widget(firetruck_exam_btn)

        ### BUTTON Übung mit Bildern ###
        if self.selected_city in ["Hallein"]:
            firetruck_training_with_images_btn = self.create_button(
                strings.BUTTON_STR_TRAINING_NEW, disabled=True
            )
            self.content_layout.add_widget(firetruck_training_with_images_btn)

        # ABOUT TEXT / IMPRESSUM
        about_label = Label(
            size_hint=(1, 1),
            text=About_Text().TEXT,
            font_size="13sp",
            halign="center",
        )
        self.content_layout.add_widget(about_label)

        # TEAM122 LOGO
        team122_logo = get_team122_image()
        self.content_layout.add_widget(team122_logo)

    def create_button(self, button_text: str, disabled: bool = False) -> Button:
        btn = Button(
            pos_hint={"center_x": 0.5},
            text=button_text,
            font_size="32sp",
            disabled=disabled,
        )

        btn.bind(
            on_release=lambda instance: self.forward_mode2menu_manually(
                "firetruck_menu", button_text
            )
        )

        btn.bind(on_release=lambda instance: self.update_firetruck_buttons(button_text))
        return btn

    def create_placeholder(self) -> Label:
        return Label(
            size_hint=(1, 1),
            font_size="32sp",
        )

    def forward_mode2menu_manually(self, menu_screen: str, mode: str):
        self.manager.transition = SlideTransition(direction="left")
        self.manager.current = menu_screen
        self.manager.get_screen(menu_screen).ids.mode_label.text = mode

    def update_firetruck_buttons(self, mode_name: str):
        self.manager.get_screen("firetruck_menu").ids.firetrucks_scrollview.scroll_y = 1

        # load available firetrucks
        total_storage = load_total_storage(self.selected_city)
        self.total_firetrucks = list(total_storage.keys())

        # create button for all firetrucks
        self.manager.get_screen("firetruck_menu").ids.firetrucks_layout.clear_widgets()

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
            firetruck = "TestTruck"
            self.add_firetruck_button(firetruck)

    def add_firetruck_button(self, firetruck: str, disabled: bool = False):

        abbreviation = self.abbreviations.get(firetruck, "")
        # Create a button with two strings, one centered and one at the bottom right
        btn = Button(
            text=f"{firetruck}{' '*3}[size=30]{abbreviation}[/size]",
            markup=True,  # Enable markup for custom text positioning
            font_size="32sp",
            size_hint_y=None,
            height=200,
            size_hint_x=1,
            disabled=disabled,
        )
        btn.bind(on_release=self.manager.get_screen("firetruck_menu").on_button_release)

        # Add the button to the layout
        self.manager.get_screen("firetruck_menu").ids.firetrucks_layout.add_widget(btn)

    def update_info_text(self):
        info_text = (
            create_scores_text(read_scores_file(), self.selected_city) + "\n\n\n\n"
        )

        self.manager.get_screen("highscore_screen").ids.score_text_label.text = (
            info_text
        )
