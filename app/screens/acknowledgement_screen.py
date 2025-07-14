from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen

from typing import cast

from helper.settings import Strings, Acknowledgements_Text
from helper.functions import change_screen_to


strings = Strings()
acknowledgement_text = Acknowledgements_Text().TEXT


class Acknowledgment(Screen):
    def __init__(self, **kwargs):
        super(Acknowledgment, self).__init__(**kwargs)
        self.header_label = cast(Label, self.header_label)
        self.acknowledgement_label = cast(Label, self.acknowledgement_label)

        self.header_label.text = strings.BUTTON_STR_ACKNOWLEDGEMENT
        self.acknowledgement_label.text = acknowledgement_text + "\n\n\n"

    def go_back(self, *args) -> None:
        change_screen_to("start_menu")
