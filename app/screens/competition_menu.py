from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.screenmanager import Screen

from random import shuffle

from helper.functions import mode_str2bool
from helper.file_handling import load_total_competition_questions
from helper.settings import Strings

strings = Strings()


class Bewerb_Menu(Screen):
    def __init__(self, **kwargs):
        super(Bewerb_Menu, self).__init__(**kwargs)
        # load available competitions
        total_competition_questions = load_total_competition_questions()
        self.total_competitions = list(total_competition_questions.keys())
        # create button for all competitions
        for competitions in self.total_competitions:
            btn = Button(
                text=competitions,
                font_size="32sp",
                size_hint_y=None,
                height=150,
                size_hint_x=1,
            )
            btn.bind(on_release=self.on_button_release)  # type: ignore
            self.bewerbe_layout.add_widget(btn)  # type: ignore

    def on_button_release(self, instance):
        # on question selection, read mode label text from current screen
        mode = mode_str2bool(self.mode_label.text.strip())  # type: ignore
        mode_training, mode_game, mode_browse, mode_images = mode

        # bind competition selection
        app = App.get_running_app()

        if mode_training:
            app.root.current = "bewerb_training"  # type: ignore
            app.root.transition.direction = "left"  # type: ignore
            # continue game with selected competition
            bewerb_training_screen = app.root.get_screen("bewerb_training")  # type: ignore
            bewerb_training_screen.select_competition(instance.text)
            bewerb_training_screen.play()

        if mode_game:
            app.root.current = "bewerb_game"  # type: ignore
            app.root.transition.direction = "left"  # type: ignore
            # continue game with selected competition
            bewerb_game_screen = app.root.get_screen("bewerb_game")  # type: ignore
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
