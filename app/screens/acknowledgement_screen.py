from typing import cast

from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen

from helper.settings import Strings, Acknowledgements_Text


strings = Strings()
acknowledgement_text = Acknowledgements_Text().TEXT


class Acknowledgement_Screen(Screen):
    def __init__(self, **kwargs):
        super(Acknowledgement_Screen, self).__init__(**kwargs)
        self.header_label = cast(Label, self.header_label)
        self.acknowledgement_label = cast(Label, self.acknowledgement_label)

        self.header_label.text = strings.BUTTON_STR_ACKNOWLEDGEMENT
        self.acknowledgement_label.text = acknowledgement_text
