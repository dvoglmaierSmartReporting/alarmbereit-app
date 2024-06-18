from kivy.app import App
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.screenmanager import ScreenManager, Screen

from random import shuffle

from screens.firetruck_screens import (
    Fahrzeugkunde_Menu,
    Fahrzeugkunde_Training,
    Fahrzeugkunde_Game,
    Fahrzeugkunde_Browse,
    Fahrzeugkunde_Images,
)
from screens.competition_screens import Bewerb_Menu, Bewerb_Training

from helper.functions import mode_str2bool, mode_bool2str
from helper.settings import Strings

strs = Strings()


class Start_Menu(Screen):
    mode: tuple[bool, bool, bool, bool] = (
        True,  # training | default
        False,  # game
        False,  # browse
        False,  # images
    )

    def __init__(self, **kwargs):
        super(Start_Menu, self).__init__(**kwargs)
        # update button strings
        self.training_button.text = strs.BUTTON_STR_TRAINING
        self.game_button.text = strs.BUTTON_STR_GAME
        self.browse_button.text = strs.BUTTON_STR_BROWSE
        self.images_button.text = strs.BUTTON_STR_IMAGES
        self.firetrucks_button.text = strs.BUTTON_STR_FIRETRUCKS
        self.competitions_button.text = strs.BUTTON_STR_COMPETITIONS
        self.standards_button.text = strs.BUTTON_STR_STANDARDS
        # update label strings
        self.mode_label.text = strs.LABEL_STR_MODE
        self.questions_label.text = strs.LABEL_STR_QUESTIONS

        self.standards_button.disabled = True

    def on_button_release(self):
        # if mode change, read mode label from current selection
        self.mode = mode_str2bool(self.find_down_toggle_button(self))

        # disable not existing combinations
        self.firetrucks_button.disabled = False
        self.competitions_button.disabled = False
        # self.standards_button.disabled = False
        mode_training, mode_game, mode_browse, mode_images = self.mode
        # if mode_images:
        #     self.firetrucks_button.disabled = True
        if mode_game or mode_images or mode_browse:
            # if mode_game or mode_images:
            self.competitions_button.disabled = True
        # if mode_training or mode_game or mode_images or mode_browse:
        #     self.standards_button.disabled = True

    def forward_mode2menu(self, menu_screen: str):
        selected_mode = mode_bool2str(self.mode)
        self.manager.current = menu_screen
        self.manager.get_screen(menu_screen).ids.mode_label.text = f"{selected_mode}   "

    # def find_down_toggle_button(self, widget, selected_mode=None):
    def find_down_toggle_button(self, widget):
        # Recursively search for a ToggleButton in the 'down' state.
        if isinstance(widget, ToggleButton) and widget.state == "down":
            return widget.text
        for child in widget.children:
            result = self.find_down_toggle_button(child)
            if result:  # If a 'down' ToggleButton is found, return its text
                return result
        return None  # if no 'down' ToggleButton is found


class CustomToggleButton(ToggleButton):  # used in feuerwehr.kv
    def on_touch_up(self, touch):
        # Call the superclass method to ensure standard behavior is preserved
        super_result = super(CustomToggleButton, self).on_touch_up(touch)
        if self.state == "normal":  # Check if the button was just released
            # Force it back to 'down' state if no other buttons are down
            if not any(btn.state == "down" for btn in self.get_widgets(self.group)):
                self.state = "down"
        return super_result


class Feuerwehr_App(App):
    def build(self):

        sm = ScreenManager()
        sm.add_widget(Start_Menu())
        sm.add_widget(Fahrzeugkunde_Menu())
        sm.add_widget(Bewerb_Menu())
        sm.add_widget(Fahrzeugkunde_Training())
        sm.add_widget(Fahrzeugkunde_Game())
        sm.add_widget(Fahrzeugkunde_Browse())
        sm.add_widget(Fahrzeugkunde_Images())
        sm.add_widget(Bewerb_Training())
        return sm


if __name__ == "__main__":
    FeuerwehrApp().run()
