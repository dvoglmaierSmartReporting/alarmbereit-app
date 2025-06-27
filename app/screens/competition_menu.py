from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.switch import Switch
from kivy.uix.label import Label
from kivy.uix.layout import Layout
from kivy.uix.screenmanager import Screen

from typing import cast

from helper.functions import mode_str2bool, change_screen_to
from helper.file_handling import (
    load_total_competition_questions,
    get_selected_city_state,
)
from helper.aspect_image import get_state_image
from helper.settings import Strings


strings = Strings()


class Bewerb_Menu(Screen):
    def __init__(self, **kwargs):
        super(Bewerb_Menu, self).__init__(**kwargs)
        # load available competitions
        total_competition_questions = load_total_competition_questions()
        self.total_competitions = list(total_competition_questions.keys())

        # update button strings
        # self.choose_mode_label.text = strings.BUTTON_STR_SOLUTION
        # self.ids.choose_mode_label.text = "Modus wählen"

        self.ids.mode_toggle_training.text = strings.BUTTON_STR_TRAINING
        self.ids.mode_toggle_game.text = strings.BUTTON_STR_GAME

        # training button selected by default
        self.ids.mode_toggle_training.state = "down"
        self.ids.mode_toggle_game.state = "normal"
        self.selected_mode = strings.BUTTON_STR_TRAINING

        # create button for all competitions
        for competitions in self.total_competitions:
            btn = Button(
                text=competitions,
                font_size="32sp",
                size_hint_y=None,
                height=150,
                size_hint_x=1,
            )
            btn.bind(on_release=self.on_button_release)
            self.ids.bewerbe_layout.add_widget(btn)

    def on_pre_enter(self):
        # Reset the scrollview to the top
        self.ids.bewerbe_layout_scrollview.scroll_y = 1

        # read from main.cfg
        self.selected_city, self.selected_state = get_selected_city_state()

        # update state logo
        self.ids.logo_layout.clear_widgets()
        self.ids.logo_layout.add_widget(get_state_image(self.selected_state))

    def on_mode_toggle(self, instance):
        if instance.state == "down":
            # Deselect all others
            for btn in self.ids.mode_toggle_layout.children:
                if btn != instance:
                    btn.state = "normal"
            self.selected_mode = instance.text
        else:
            self.selected_mode = ""

    def on_button_release(self, instance):
        self.mode_label = cast(Label, self.mode_label)
        # on question selection, read mode label text from current screen
        # mode = mode_str2bool(self.mode_label.text.strip())
        mode = mode_str2bool(self.selected_mode.strip())
        (
            mode_training,
            mode_training_new,
            mode_game,
            mode_browse,
            mode_images,
            mode_exam,
        ) = mode

        # bind competition selection
        app = App.get_running_app()

        if mode_training:
            # app.root.current = "bewerb_training"
            # app.root.transition.direction = "left"
            change_screen_to("bewerb_training", transition_direction="left")
            # continue game with selected competition
            bewerb_training_screen = app.root.get_screen("bewerb_training")
            bewerb_training_screen.select_competition(instance.text)
            bewerb_training_screen.play()

        if mode_game:
            # app.root.current = "bewerb_game"
            # app.root.transition.direction = "left"
            change_screen_to("bewerb_game", transition_direction="left")
            # continue game with selected competition
            bewerb_game_screen = app.root.get_screen("bewerb_game")
            bewerb_game_screen.select_city(self.selected_city)
            bewerb_game_screen.select_competition(instance.text)
            bewerb_game_screen.play()

        # adapt for competition
        # elif mode_browse:
        #     # change screen
        #     app.root.current = "fahrzeugkunde_browse"
        #     app.root.transition.direction = "left"
        #     # continue game with selected firetruck
        #     fahrzeugkunde_browse_screen = app.root.get_screen("fahrzeugkunde_browse")
        #     fahrzeugkunde_browse_screen.select_firetruck(instance.text)
        #     fahrzeugkunde_browse_screen.populate_list()

        # adapt for competition
        # elif mode_images:
        #     app.root.current = "fahrzeugkunde_images"
        #     app.root.transition.direction = "left"

    def go_back(self, *args) -> None:
        change_screen_to("start_menu")
