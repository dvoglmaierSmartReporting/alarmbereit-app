from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.layout import Layout
from kivy.uix.screenmanager import Screen

from helper.functions import mode_str2bool
from helper.file_handling import load_total_competition_questions
from helper.settings import Strings

from typing import cast

strings = Strings()


class Bewerb_Menu(Screen):
    def __init__(self, **kwargs):
        super(Bewerb_Menu, self).__init__(**kwargs)
        # load available competitions
        total_competition_questions = load_total_competition_questions()
        self.total_competitions = list(total_competition_questions.keys())

        self.bewerbe_layout = cast(Layout, self.bewerbe_layout)

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
            self.bewerbe_layout.add_widget(btn)

    def on_button_release(self, instance):
        self.mode_label = cast(Label, self.mode_label)
        # on question selection, read mode label text from current screen
        mode = mode_str2bool(self.mode_label.text.strip())
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
            app.root.current = "bewerb_training"
            app.root.transition.direction = "left"
            # continue game with selected competition
            bewerb_training_screen = app.root.get_screen("bewerb_training")
            bewerb_training_screen.select_competition(instance.text)
            bewerb_training_screen.play()

        if mode_game:
            app.root.current = "bewerb_game"
            app.root.transition.direction = "left"
            # continue game with selected competition
            bewerb_game_screen = app.root.get_screen("bewerb_game")
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
