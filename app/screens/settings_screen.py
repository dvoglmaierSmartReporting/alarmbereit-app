from kivy.uix.screenmanager import Screen

import os
from typing import cast

from helper.file_handling import (
    update_main_cfg,
    load_from_yaml,
    get_user_data_dir,
)
from helper.functions import change_screen_to
from helper.settings import Strings


strings = Strings()


class Settings_Screen(Screen):

    def __init__(self, **kwargs):
        super(Settings_Screen, self).__init__(**kwargs)

        main_cfg_file_path = os.path.join(
            get_user_data_dir(),
            "main.cfg",
        )

        use_default = (
            load_from_yaml(main_cfg_file_path).get("content").get("use_default")
        )


    def update_default_content_switch(self, switch, value):
        if value:
            update_main_cfg({"content": {"use_default": True}})

        else:
            update_main_cfg({"content": {"use_default": False}})

    def reset_city(self):
        pass

    def reset_country(self):
        pass

    def go_back(self, *args) -> None:
        change_screen_to("start_menu")
