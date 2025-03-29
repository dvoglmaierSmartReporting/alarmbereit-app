from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.screenmanager import Screen
from kivy.uix.floatlayout import FloatLayout
from kivy.factory import Factory
from kivy.properties import ObjectProperty
from kivy.uix.popup import Popup

import os
import yaml
from typing import cast

from helper.file_handling import (
    update_main_cfg,
    copy_file_to_writable_dir,
    save_to_yaml,
    load_from_yaml,
    update_yaml_values,
)
from helper.functions import create_scores_content
from helper.settings import Strings


strings = Strings()


class LoadDialog(FloatLayout):
    load = ObjectProperty(None)
    cancel = ObjectProperty(None)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.load_button = cast(Button, self.load_button)
        self.load_button.disabled = True

    def on_selection(self, instance, value):
        self.load_button.disabled = not bool(value)


class Settings_Screen(Screen):
    text_output = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(Settings_Screen, self).__init__(**kwargs)

        self.ids.default_content_label.text = strings.SWITCH_STR_DEFAULT_CONTENT
        self.ids.select_file_button.text = strings.BUTTON_STR_SELECT_FILE
        self.ids.upload_confirm_button.text = strings.BUTTON_STR_CONFIRM_UPLOAD

        custom_file_path = os.path.join(
            App.get_running_app().user_data_dir,
            "custom_firetruck_tools.yaml",
        )
        custom_file_exists = os.path.exists(custom_file_path)

        main_cfg_file_path = os.path.join(
            App.get_running_app().user_data_dir,
            "main.cfg",
        )

        use_default = (
            load_from_yaml(main_cfg_file_path).get("content").get("use_default")
        )

        if not custom_file_exists and use_default:
            # keep at using default and disable switch as file is missing
            self.default_content_switch.active = True
            self.default_content_switch.disabled = True

        elif not custom_file_exists and not use_default:
            print(
                "Error: Custom firetruck file not found. Switch back to default instead."
            )
            # Change to using default and disable switch as file is missing
            self.default_content_switch.active = True
            self.default_content_switch.disabled = True

        elif custom_file_exists and use_default:
            # keep at using default and enable switch to allow user choice
            self.default_content_switch.active = True
            self.default_content_switch.disabled = False

        elif custom_file_exists and not use_default:
            # keep at using custom and enable switch to allow user choice
            self.default_content_switch.active = False
            self.default_content_switch.disabled = False

    def dismiss_popup(self):
        self._popup.dismiss()

    def show_load(self):
        content = LoadDialog(load=self.load, cancel=self.dismiss_popup)
        content.cancel_button.text = strings.BUTTON_DIALOG_POPUP_CANCEL
        content.load_button.text = strings.BUTTON_DIALOG_POPUP_CONFIRM
        self._popup = Popup(
            title=strings.TITLE_DIALOG_POPUP, content=content, size_hint=(0.9, 0.9)
        )
        self._popup.open()

    def preview_load(self) -> str:
        preview = (
            'Klicke "Bestätigen" um die Inhalte zu überschreiben.\nNeue Fahrzeuge:\n'
        )
        for truck in self.file_content.keys():
            preview += f"> {truck}\n"

        preview += "\nNeue Fahrzeuge und deren Geräteräume:"
        for truck in self.file_content.keys():
            preview += f"\n> {truck}\n"
            for room in self.file_content.get(truck).keys():
                preview += f" ---> {room}: {len(self.file_content.get(truck).get(room))} Werkzeuge\n"

        return preview

    def validate_load(self):
        errors_str = ""
        error_id = 1

        # validate 3 levels: dict > dict > list
        if not isinstance(self.file_content, dict):
            errors_str += f"Fehler {error_id}: Kein valides Format! Bitte den Beispielen folgen\nund unnötige und zusätzliche Einträge vermeiden.\n"
            error_id += 1
            return errors_str

        for truck in self.file_content:
            truck_content = self.file_content.get(truck)

            if not isinstance(truck_content, dict):
                errors_str += f"Fehler {error_id}: Geräteraum Ebene besteht nicht aus Objekt, sondern\n{type(truck_content)}, {truck_content}\n"
                error_id += 1
                continue

            # validate number of rooms [4,14]
            if not 3 < len(truck_content.keys()) < 12:
                errors_str += f"Fehler {error_id}: Anzahl an Geräteräumen (GR) ist ungültig (3 < GR < 12)\nlen={len(truck_content.keys())}, {truck}: {truck_content.keys()}\n"
                error_id += 1

            for room in truck_content:
                room_content = truck_content.get(room)
                if not isinstance(room_content, list):
                    errors_str += f"Fehler {error_id}: Geräte Ebene besteht nicht aus Liste, sondern\n{type(room_content)}, {room_content}\n"
                    error_id += 1
                    continue

                # validate length of room strings
                if not 1 < len(room) <= 30:
                    errors_str += f"Fehler {error_id}: Einzelner Geräteraum ist ungültig (1<Buchstaben<=30)\nlen={len(room)}, {room[:35]}\n"
                    error_id += 1

                # validate length of tool strings
                for tool in room_content:
                    if not 1 < len(tool) <= 100:
                        errors_str += f"Fehler {error_id}: Einzelnes Gerät ist ungültig (1<Buchstaben<=100)\nlen={len(tool)}, {tool[:35]}\n"
                        error_id += 1

        if len(errors_str) > 0:
            errors_str = "[b]Upload Validierung fehlgeschlagen:[/b]\n" + errors_str

        return errors_str

    def enable_upload_confirm_button(self):
        self.ids.upload_confirm_button.disabled = False

    def disable_upload_confirm_button(self):
        self.ids.upload_confirm_button.disabled = True

    def enable_default_content_switch(self):
        self.ids.default_content_switch.disabled = False

    def deactivate_default_content_switch(self):
        self.ids.default_content_switch.active = False

    def clear_text_output(self):
        self.ids.text_output = ""

    def load(self, path, filename):
        self.custom_tools_file_path = path
        self.custom_tools_file_name = filename[0]
        with open(os.path.join(path, filename[0])) as file:
            self.file_content = yaml.safe_load(file)

        error_str = self.validate_load()
        if not len(error_str) > 0:
            preview = self.preview_load()
            upload_error = False

        else:
            preview = error_str
            upload_error = True

        self.text_output.text = preview

        if not upload_error:
            self.enable_upload_confirm_button()

        self.dismiss_popup()

    def confirm_upload(self):

        self.enable_default_content_switch()
        self.deactivate_default_content_switch()

        update_main_cfg({"content": {"use_default": False}})

        # main.cfg is source-of-truth for custom firetruck and scores
        # custom-scores.yaml creation must be after update_main_cfg()

        # upload custom firetrucks
        copy_file_to_writable_dir(
            self.custom_tools_file_path,
            self.custom_tools_file_name,
            "custom_firetruck_tools.yaml",
        )

        # init custom scores yaml
        file_path = os.path.join(
            App.get_running_app().user_data_dir,
            "scores.yaml",
        )

        existing_content = load_from_yaml(file_path)
        new_content = create_scores_content()

        updated_comp_content = update_yaml_values(
            existing_content.get("competitions"),
            new_content.get("competitions"),
        )
        new_content["competitions"] = updated_comp_content

        custom_file_path = os.path.join(
            App.get_running_app().user_data_dir,
            "custom_scores.yaml",
        )
        save_to_yaml(custom_file_path, new_content)

        self.disable_upload_confirm_button()
        self.clear_text_output()

    def update_default_content_switch(self, switch, value):
        if value:
            update_main_cfg({"content": {"use_default": True}})

        else:
            update_main_cfg({"content": {"use_default": False}})


Factory.register("Settings_Screen", cls=Settings_Screen)
Factory.register("LoadDialog", cls=LoadDialog)
