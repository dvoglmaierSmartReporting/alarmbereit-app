from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.screenmanager import Screen, SlideTransition
from kivy.metrics import dp

from helper.functions import (
    get_firetruck_abbreviations,
)
from helper.file_handling import (
    get_selected_city_state,
    load_app_version,
    update_config_firetruck,
)
from helper.aspect_image import get_city_image
from helper.strings import Strings, About_Text

from screens.screen_base import FontSizeMixin


strings = Strings()


class Start_Menu(FontSizeMixin, Screen):
    def __init__(self, **kwargs):
        super(Start_Menu, self).__init__(**kwargs)

        self.ids.all_cities_button.text = strings.BUTTON_STR_ALL_CITIES
        self.version = load_app_version()

    def on_pre_enter(self):
        self.selected_city, _ = get_selected_city_state()

        self.abbreviations = get_firetruck_abbreviations(self.selected_city)

        self.add_city_logo()

        # self.ids.score_button.text = strings.BUTTON_STR_SCORE
        self.add_mode_buttons()
        self.add_about_text()

    def on_enter(self):
        self.bind_font_scaling()

    def on_leave(self):
        self.unbind_font_scaling()

    def add_city_logo(self):
        self.ids.logo_layout.clear_widgets()
        self.ids.logo_layout.add_widget(get_city_image(self.selected_city))

    def add_mode_buttons(self):
        self.ids.content_layout.clear_widgets()
        self.clear_font_scaling_widgets()  # Clear previous widget references

        ### BUTTON Übung ###
        firetruck_training_btn = self.create_button(strings.BUTTON_STR_TRAINING)
        self.ids.content_layout.add_widget(firetruck_training_btn)

        ### BUTTON Zeitdruck ###
        firetruck_game_btn = self.create_button(strings.BUTTON_STR_GAME)
        self.ids.content_layout.add_widget(firetruck_game_btn)

        # ### BUTTON Stöbern ###
        # firetruck_browse_btn = self.create_button(strings.BUTTON_STR_BROWSE)
        # self.ids.content_layout.add_widget(firetruck_browse_btn)

        # ### BUTTON Bilder ###
        # firetruck_images_btn = self.create_button(strings.BUTTON_STR_IMAGES)
        # self.ids.content_layout.add_widget(firetruck_images_btn)

        # ### BUTTON Leistungsprüfung ###
        # firetruck_exam_btn = self.create_button(strings.BUTTON_STR_EXAM)
        # self.ids.content_layout.add_widget(firetruck_exam_btn)

        ### BUTTON Übung mit Bildern ###
        if self.selected_city in ["Hallein"]:
            firetruck_training_with_images_btn = self.create_button(
                strings.BUTTON_STR_TRAINING_WITH_IMAGES
            )
            self.ids.content_layout.add_widget(firetruck_training_with_images_btn)

        ### STATISTIK BUTTON ###
        score_btn = self.create_button(
            strings.BUTTON_STR_SCORE, target_screen="highscore_screen"
        )
        self.ids.content_layout.add_widget(score_btn)

    def create_button(
        self,
        button_text: str,
        disabled: bool = False,
        target_screen: str = "firetruck_menu",
    ) -> Button:
        base_font_size = 15  # 20
        font_scale = self.get_font_scale()
        font_size_pixels = dp(base_font_size) * font_scale
        font_size_half_pixels = dp(base_font_size) * font_scale // 2

        mapping = {
            strings.BUTTON_STR_TRAINING: "Lerne Gerätepositionen",
            strings.BUTTON_STR_TRAINING_WITH_IMAGES: "von Geräten und Räumen",
            strings.BUTTON_STR_GAME: "Teste dein Wissen unter Zeitdruck",
            strings.BUTTON_STR_SCORE: "Verfolge deinen Lernfortschritt",
        }

        subtitle = mapping.get(button_text, "")

        spacer_title = " " * 2
        spacer_subtitle = " " * 5
        btn = Button(
            pos_hint={"center_x": 0.5},
            text=f"{spacer_title}{button_text}[size={font_size_half_pixels}dp]\n{spacer_subtitle}{subtitle}[/size]",
            font_size=f"{font_size_pixels}dp",
            disabled=disabled,
            halign="left",
            text_size=(None, None),
            markup=True,
        )

        # Set text_size after button is created to enable text alignment
        def set_text_size(instance, size):
            instance.text_size = (size[0], None)

        btn.bind(size=set_text_size)

        # Register button for font scaling
        self.register_widget_for_font_scaling(btn, base_font_size)

        btn.bind(on_release=lambda instance: self.transit_screen(target_screen))
        btn.bind(
            on_release=lambda instance: update_config_firetruck({"mode": button_text})
        )

        return btn

    def add_about_text(self):
        base_font_size = 7

        about_label = Label(
            size_hint=(1, 1),
            text=About_Text(self.version).TEXT,
            halign="center",
        )

        # Register label for font scaling
        self.register_widget_for_font_scaling(about_label, base_font_size)

        self.ids.content_layout.add_widget(about_label)

    def transit_screen(self, menu_screen: str):
        self.manager.transition = SlideTransition(direction="left")
        self.manager.current = menu_screen
