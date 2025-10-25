from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.screenmanager import Screen, SlideTransition
from kivy.core.window import Window
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


strings = Strings()


class Start_Menu(Screen):
    def __init__(self, **kwargs):
        super(Start_Menu, self).__init__(**kwargs)

        self.ids.all_cities_button.text = strings.BUTTON_STR_ALL_CITIES
        self.version = load_app_version()

        self.dynamic_widgets = []

    def get_font_scale(self):
        return max(0.8, min(1.5, Window.width / dp(600)))

    def on_pre_enter(self):
        self.selected_city, _ = get_selected_city_state()

        self.abbreviations = get_firetruck_abbreviations(self.selected_city)

        self.add_city_logo()

        self.ids.score_button.text = strings.BUTTON_STR_SCORE
        self.add_mode_buttons()
        self.add_about_text()

    def on_enter(self):
        Window.bind(on_resize=self.update_font_sizes)

    def on_leave(self):
        Window.unbind(on_resize=self.update_font_sizes)

    def update_font_sizes(self, *args):
        font_scale = self.get_font_scale()

        # Update dynamically created buttons and labels
        for widget_info in self.dynamic_widgets:
            widget = widget_info["widget"]
            base_size = widget_info["base_size"]
            if hasattr(widget, "font_size"):
                widget.font_size = f"{dp(base_size) * font_scale}dp"

    def add_city_logo(self):
        self.ids.logo_layout.clear_widgets()
        self.ids.logo_layout.add_widget(get_city_image(self.selected_city))

    def add_mode_buttons(self):
        self.ids.content_layout.clear_widgets()
        self.dynamic_widgets.clear()  # Clear previous widget references

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
                strings.BUTTON_STR_TRAINING_NEW, disabled=False
            )
            self.ids.content_layout.add_widget(firetruck_training_with_images_btn)

    def create_button(self, button_text: str, disabled: bool = False) -> Button:
        font_scale = self.get_font_scale()
        base_font_size = 25

        btn = Button(
            pos_hint={"center_x": 0.5},
            text=button_text,
            font_size=f"{dp(base_font_size) * font_scale}dp",
            disabled=disabled,
        )

        # Store reference for dynamic font updates
        self.dynamic_widgets.append({"widget": btn, "base_size": base_font_size})

        btn.bind(on_release=lambda instance: self.transit_screen("firetruck_menu"))
        btn.bind(
            on_release=lambda instance: update_config_firetruck({"mode": button_text})
        )

        return btn

    def add_about_text(self):
        font_scale = self.get_font_scale()
        base_font_size = 10

        about_label = Label(
            size_hint=(1, 1),
            text=About_Text(self.version).TEXT,
            font_size=f"{dp(base_font_size) * font_scale}dp",
            halign="center",
        )

        # Store reference for dynamic font updates
        self.dynamic_widgets.append(
            {"widget": about_label, "base_size": base_font_size}
        )

        self.ids.content_layout.add_widget(about_label)

    def transit_screen(self, menu_screen: str):
        self.manager.transition = SlideTransition(direction="left")
        self.manager.current = menu_screen
