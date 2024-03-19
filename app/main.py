from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.lang import Builder
from kivy.clock import Clock

from random import shuffle

from helper.firetruck import load_total_storage


# Define our different screens
class StartMenu(Screen):
    pass


class FahrzeugkundeMenu(Screen):
    def __init__(self, **kwargs):
        super(FahrzeugkundeMenu, self).__init__(**kwargs)
        # self.transition_callback = transition_callback


class BewerbMenu(Screen):
    pass


class FeuerwehrGame(Screen):
    def __init__(self, **kwargs):
        super(FeuerwehrGame, self).__init__(**kwargs)

    def select_firetruck(self, selected_firetruck):
        # troubleshooting: fix firetruck
        # self.selected_firetruck = "Tank1" "Rüst+Lösch"
        self.selected_firetruck = selected_firetruck

    def play(self):
        self.load_tools_from_firetruck()
        self.next_question()
        self.accept_answers = True  # Flag to indicate if answers should be processed

    def load_tools_from_firetruck(self):
        total_storage = load_total_storage()
        self.firetruck_dict = total_storage[self.selected_firetruck]
        self.rooms_list = self.firetruck_dict.keys()
        self.tools_list = [
            tool for room in self.firetruck_dict.values() for tool in room
        ]
        self.tools_list = list(set(self.tools_list))
        shuffle(self.tools_list)
        self.tool_locations = self.invert_firetruck_equipment()

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

        # troubleshooting: fix question
        # self.current_tool = "Druckschlauch B"
        self.current_tool = self.tools_list.pop()

        tool_text = self.current_tool
        if len(tool_text) >= 29:
            tool_text_lst = tool_text[14:].split(" ")
            tool_text = (
                tool_text[:14] + tool_text_lst[0] + "\n" + " ".join(tool_text_lst[1:])
            )
        self.question_label.text = tool_text
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
        # Identify and indicate the correct answers
        children = self.answers_layout.children + self.mannschaftsraum_layout.children
        for child in children:
            if child.text in correct_storage:
                child.background_color = (0, 1, 0, 1)
        # Indicate if given answer was incorrect
        if instance.text not in correct_storage:
            instance.background_color = (1, 0, 0, 1)
        self.accept_answers = (
            False  # Disable answer processing after an answer is selected
        )
        # Clock.schedule_once(self.next_question, 2)
        Clock.schedule_once(self.next_question, 0)


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
