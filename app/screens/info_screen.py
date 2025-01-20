from kivy.app import App
from kivy.uix.screenmanager import Screen

from helper.settings import Info_Screen_Text
from helper.file_handling import read_scores_file
from helper.functions import create_scores_text


info_content = Info_Screen_Text()


class Info_Screen(Screen):
    def __init__(self, **kwargs):
        super(Info_Screen, self).__init__(**kwargs)

        # init screen with about text
        self.ids.about_label.text = info_content.TEXT

        # update scores text at every call; done in main.py Start_Menu screen