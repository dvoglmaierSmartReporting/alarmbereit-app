from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen

from typing import cast

from helper.settings import About_Text, Strings
from helper.functions import change_screen_to

about_text = About_Text().TEXT
strings = Strings()


class Info_Screen(Screen):
    def __init__(self, **kwargs):
        super(Info_Screen, self).__init__(**kwargs)
        self.header_label = cast(Label, self.header_label)
        self.about_label = cast(Label, self.about_label)

        self.header_label.text = strings.BUTTON_STR_INFO
        self.about_label.text = about_text

    def go_back(self, *args) -> None:
        change_screen_to("start_menu")
