from kivy.uix.screenmanager import Screen

from kivy.clock import Clock

import os

from helper.strings import Strings
from helper.functions import change_screen_to
from helper.file_handling import get_user_data_dir

strings = Strings()


# TODO:
# enable and display button again, in
#  - .kv file + ids
#  - .py __init__
# save PNG in tempfile instead of file
# configure FileProvider xml
#  - .xml file with permissions
#  - in buildozer file
# open default email app and prepare email

from kivy.utils import platform
from kivy.clock import Clock
import os


class Highscore(Screen):
    # def __init__(self, **kwargs):
    #     super(Highscore, self).__init__(**kwargs)
    #     self.ids.share_button.text = strings.BUTTON_STR_SHARE

    def capture_scrollview(self):
        content = self.ids.score_text_label  # Layout inside ScrollView
        filename = os.path.join(self.get_save_path(), "scrollview_capture.png")

        # Schedule to wait one frame, so layout has time to render
        def do_capture(dt):
            content.export_to_png(filename)
            print(f"Captured ScrollView content to {filename}")

        Clock.schedule_once(do_capture, 0.1)

    def get_save_path(self):
        if platform == "android":
            from android.storage import app_storage_path

            return app_storage_path()
        else:
            return os.path.expanduser("~")




    def go_back(self, *args) -> None:
        change_screen_to("start_menu")
