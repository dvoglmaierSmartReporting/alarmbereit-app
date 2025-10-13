from kivy.uix.screenmanager import Screen

from helper.strings import Strings, Acknowledgements_Text
from helper.functions import change_screen_to

strings = Strings()
acknowledgement_text = Acknowledgements_Text().TEXT


class Acknowledgment(Screen):
    def __init__(self, **kwargs):
        super(Acknowledgment, self).__init__(**kwargs)

        self.ids.header_label.text = strings.BUTTON_STR_ACKNOWLEDGEMENT

        self.ids.acknowledgement_label.text = acknowledgement_text + "\n\n\n"

    def go_back(self, *args) -> None:
        change_screen_to("start_menu")
