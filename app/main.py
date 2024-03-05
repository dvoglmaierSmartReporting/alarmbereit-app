from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
import yaml
from kivy.clock import Clock
from random import shuffle

#
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.lang import Builder

#


# Define our different screens
class StartMenu(Screen):
    pass


class FahrzeugkundeMenu(Screen):
    def __init__(self, **kwargs):
        super(FahrzeugkundeMenu, self).__init__(**kwargs)
        # self.transition_callback = transition_callback

    #     self.load_firetrucks()

    # def load_firetrucks(self):
    #     with open("feuerwehr_tools_storage.yaml", "r") as f:
    #         try:
    #             self.tools_storage = yaml.safe_load(f)
    #             self.firetrucks_list = list(self.tools_storage.keys())
    #         except yaml.YAMLError as exc:
    #             print(exc)


class BewerbMenu(Screen):
    pass


class FeuerwehrGame(Screen):
    # def __init__(self, selected_firetruck, **kwargs):
    def __init__(self, **kwargs):
        super(FeuerwehrGame, self).__init__(**kwargs)
        # self.selected_firetruck = selected_firetruck
        self.selected_firetruck = "Rüst+Lösch"
        self.load_tools_from_firetruck()
        self.next_question()
        self.accept_answers = True  # Flag to indicate if answers should be processed

    def load_tools_from_firetruck(self):
        with open("feuerwehr_tools_storage.yaml", "r") as f:
            try:
                total_storage = yaml.safe_load(f)
                # self.firetruck_dict = total_storage[self.selected_firetruck]
                self.firetruck_dict = total_storage[self.selected_firetruck]
                self.rooms_list = self.firetruck_dict.keys()
                self.tools_list = [
                    tool for room in self.firetruck_dict.values() for tool in room
                ]
                self.tools_list = list(set(self.tools_list))
                shuffle(self.tools_list)
                self.tool_locations = self.invert_firetruck_equipment()
            except yaml.YAMLError as exc:
                print(exc)

    def invert_firetruck_equipment(self):
        tool_locations = {}
        for location, tools in self.firetruck_dict.items():
            for tool in tools:
                if tool in tool_locations:
                    tool_locations[tool].append(location)
                else:
                    tool_locations[tool] = [location]
        return tool_locations

    def next_question(self, *args):
        self.accept_answers = True  # Enable answer processing for the new question
        if not self.tools_list:
            self.load_tools_from_firetruck()

        self.current_tool = self.tools_list.pop()
        self.question_label.text = self.current_tool
        self.answers_layout.clear_widgets()
        self.mannschaftsraum_layout.clear_widgets()

        for storage in self.rooms_list:
            btn = Button(text=storage, font_size="32sp")
            btn.bind(on_press=self.on_answer)
            if storage == "Mannschaftsraum":
                self.mannschaftsraum_layout.add_widget(btn)
            else:
                self.answers_layout.add_widget(btn)

    def on_answer(self, instance):
        if not self.accept_answers:  # Check if answer processing is enabled
            return  # Ignore the button press if answer processing is disabled

        correct_storage = set(self.tool_locations[self.current_tool])

        if instance.text in correct_storage:
            instance.background_color = (0, 1, 0, 1)
        else:
            instance.background_color = (1, 0, 0, 1)
            # Identify and indicate the correct answer
            # for child in self.answers_layout.children:
            children = (
                self.answers_layout.children + self.mannschaftsraum_layout.children
            )
            for child in children:
                if child.text in correct_storage:
                    child.background_color = (0, 1, 0, 1)

        self.accept_answers = (
            False  # Disable answer processing after an answer is selected
        )
        Clock.schedule_once(self.next_question, 2)


class WindowManager(ScreenManager):
    pass


kv = Builder.load_file("feuerwehr.kv")


class FeuerwehrApp(App):
    def build(self):

        sm = ScreenManager()
        sm.add_widget(StartMenu())
        sm.add_widget(FahrzeugkundeMenu())
        sm.add_widget(BewerbMenu())
        sm.add_widget(FeuerwehrGame())
        return sm


if __name__ == "__main__":
    FeuerwehrApp().run()
