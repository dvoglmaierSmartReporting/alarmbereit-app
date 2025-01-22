from kivy.uix.screenmanager import Screen
from kivy.uix.floatlayout import FloatLayout
from kivy.factory import Factory
from kivy.properties import ObjectProperty
from kivy.uix.popup import Popup

import os
import yaml

from helper.file_handling import update_main_cfg, copy_file_to_writable_dir
from helper.functions import create_scores_content


class LoadDialog(FloatLayout):
    load = ObjectProperty(None)
    cancel = ObjectProperty(None)


class Settings_Screen(Screen):
    text_output = ObjectProperty(None)

    def dismiss_popup(self):
        self._popup.dismiss()

    def show_load(self):
        content = LoadDialog(load=self.load, cancel=self.dismiss_popup)
        self._popup = Popup(title="Load file", content=content, size_hint=(0.9, 0.9))
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
            for room in self.file_content.get(truck).keys():  # type: ignore
                preview += f" ---> {room}: {len(self.file_content.get(truck).get(room))} Werkzeuge\n"  # type: ignore

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
        # upload custom scores yaml
        # todo
        # create_scores_content()
        # copy_file_to_writable_dir()

        self.disable_upload_confirm_button()
        self.clear_text_output()

    # def default_content_switch


Factory.register("Settings_Screen", cls=Settings_Screen)
Factory.register("LoadDialog", cls=LoadDialog)

# TODO

# introduce:
#   - settings_screen.py + .kv
#   - main.cfg
#   - custom_scores.yaml and default_scores.yaml
#   - custom firetrucks and default firetrucks

# general logic:
# default files in read-only at app dir
# custom files in writeable dir
# update content according to main.cfg

# at start-up, if not exist, move main.cfg to writeable dir
# save current config in main.cfg at storeable location

# use default switch:
#   if true:
#       read default firetrucks
#       use default_scores.yaml
#   if false:
#       check if custom firetrucks are available
#       check if custom_scores.yaml is available, if not: create

# custom firetrucks:
# select file
# validate content
#   if false: display errors
#   if okay:
#       check if custom content already exists: -> overwrite custom firetruck...
#   with user confirmation:
#       upload file,
#       store at writeable dir, (overwrite if exist)
#       disable default_switch,
#       use custom firetrucks,
#       create custom_scores.yaml,
#       use custom_scores.yaml

# overwrite custom firetruck:
# selected, validated, uploaded
# warn user about irreversible steps
# if accepted:
#   replace custom firetruck file
#   replace custom_scores.yaml
