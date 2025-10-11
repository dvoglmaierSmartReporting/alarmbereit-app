from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen

from typing import cast

from helper.strings import Strings
from helper.functions import change_screen_to

strings = Strings()


class Info(Screen):
    def __init__(self, **kwargs):
        super(Info, self).__init__(**kwargs)
        self.header_label = cast(Label, self.header_label)
        self.header_label.text = strings.BUTTON_STR_INFO

    def go_back(self, *args) -> None:
        change_screen_to("start_menu")
