from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.screenmanager import Screen
from kivy.clock import Clock


from random import shuffle

from helper.functions import load_total_storage, mode_str2bool


class Fahrzeugkunde_Menu(Screen):
    def __init__(self, **kwargs):
        super(Fahrzeugkunde_Menu, self).__init__(**kwargs)
        # load available firetrucks
        total_storage = load_total_storage()
        self.total_firetrucks = list(total_storage.keys())
        # create button for all firetrucks
        for firetruck in self.total_firetrucks:
            btn = Button(
                text=firetruck,
                font_size="32sp",
                size_hint_y=None,
                height=150,
                size_hint_x=1,
            )
            btn.bind(on_release=self.on_button_release)  # type: ignore
            self.firetrucks_layout.add_widget(btn)  # type: ignore

    def on_button_release(self, instance):
        # on question selection, read mode label text from current screen
        mode = mode_str2bool(self.mode_label.text.strip())  # type: ignore
        mode_training, mode_game, mode_browse, mode_images = mode

        # bind firetruck and mode selection
        app = App.get_running_app()

        if mode_training:
            app.root.current = "fahrzeugkunde_training"  # type: ignore
            app.root.transition.direction = "left"  # type: ignore
            # continue game with selected firetruck
            fahrzeugkunde_tg_screen = app.root.get_screen("fahrzeugkunde_training")  # type: ignore
            fahrzeugkunde_tg_screen.select_firetruck(instance.text)
            fahrzeugkunde_tg_screen.forward_mode_2_fk_training(mode)
            fahrzeugkunde_tg_screen.play()

        if mode_game:
            app.root.current = "fahrzeugkunde_game"  # type: ignore
            app.root.transition.direction = "left"  # type: ignore
            # continue game with selected firetruck  # type: ignore
            fahrzeugkunde_tg_screen = app.root.get_screen("fahrzeugkunde_game")  # type: ignore
            fahrzeugkunde_tg_screen.select_firetruck(instance.text)
            fahrzeugkunde_tg_screen.forward_mode_2_fk_game(mode)
            fahrzeugkunde_tg_screen.play()

        elif mode_browse:
            # change screen
            app.root.current = "fahrzeugkunde_browse"  # type: ignore
            app.root.transition.direction = "left"  # type: ignore
            # continue game with selected firetruck
            fahrzeugkunde_browse_screen = app.root.get_screen("fahrzeugkunde_browse")  # type: ignore
            fahrzeugkunde_browse_screen.select_firetruck(instance.text)
            fahrzeugkunde_browse_screen.display_all_tools()

        elif mode_images:
            app.root.current = "fahrzeugkunde_images"  # type: ignore
            app.root.transition.direction = "left"  # type: ignore

            fahrzeugkunde_images_screen = app.root.get_screen("fahrzeugkunde_images")  # type: ignore
            fahrzeugkunde_images_screen.select_firetruck(instance.text)
            fahrzeugkunde_images_screen.load_image()
