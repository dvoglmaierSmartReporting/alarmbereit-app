from kivy.uix.screenmanager import Screen

from typing import cast

from helper.settings import About_Text, Strings
from helper.functions import change_screen_to

about_text = About_Text().TEXT
strings = Strings()


class Highscore(Screen):
    def go_back(self, *args) -> None:
        change_screen_to("start_menu")
