from kivy.uix.screenmanager import Screen

from kivy.clock import Clock
from kivy.config import Config

from helper.strings import Strings
from helper.functions import change_screen_to, create_scores_text
from helper.file_handling import (
    get_selected_city_state,
    map_selected_city_2long_name,
    read_scores_file,
)

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
    def on_pre_enter(self):
        self.update_city_label()

        self.update_info_text()

    def update_city_label(self):
        self.selected_city, _ = get_selected_city_state()
        self.selected_city = map_selected_city_2long_name(self.selected_city)

        if self.selected_city == "Hallein":
            selected_city_displayed = "Stadt Hallein"
        else:
            selected_city_displayed = self.selected_city
        self.ids.city_label.text = selected_city_displayed

    def update_info_text(self):
        info_text = (
            create_scores_text(read_scores_file(), self.selected_city) + "\n\n\n\n"
        )

        self.ids.score_text_label.text = info_text

    def go_back(self, *args) -> None:
        change_screen_to("start_menu")

    # Not used currently
    # idea: in internal competitions, use button to create image of highscore screen
    # to be able to share the whole values
    #
    # This won't be needed, if online highscore is implemented

    # def capture_scrollview(self):
    #     content = self.ids.score_text_label  # Layout inside ScrollView
    #     filename = os.path.join(self.get_save_path(), "scrollview_capture.png")

    #     # Schedule to wait one frame, so layout has time to render
    #     def do_capture(dt):
    #         content.export_to_png(filename)
    #         print(f"Captured ScrollView content to {filename}")

    #     Clock.schedule_once(do_capture, 0.1)

    # def get_save_path(self):
    #     if platform == "android":
    #         from android.storage import app_storage_path

    #         return app_storage_path()
    #     else:
    #         return os.path.expanduser("~")
