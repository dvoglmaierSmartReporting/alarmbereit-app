from typing import cast

from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen

from helper.settings import About_Text


about_text = About_Text().TEXT


class Info_Screen(Screen):
    def __init__(self, **kwargs):
        super(Info_Screen, self).__init__(**kwargs)

        self.about_label = cast(Label, self.about_label)
        self.about_label.text = about_text
