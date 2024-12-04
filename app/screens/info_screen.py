from kivy.uix.screenmanager import Screen

from helper.settings import Info_Screen_Text


info_content = Info_Screen_Text()


class Info_Screen(Screen):
    def __init__(self, **kwargs):
        super(Info_Screen, self).__init__(**kwargs)

        self.ids.info_label.text = info_content.TEXT