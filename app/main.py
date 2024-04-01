from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.lang import Builder
from kivy.clock import Clock

from random import shuffle

from helper.firetrucks import load_total_storage
from helper.competitions import load_total_competition_questions


class StartMenu(Screen):
    pass


class FahrzeugkundeMenu(Screen):
    def __init__(self, **kwargs):
        super(FahrzeugkundeMenu, self).__init__(**kwargs)

        # load available firetrucks
        total_storage = load_total_storage()
        self.total_firetrucks = list(total_storage.keys())

        # create button for all firetrucks
        for firetruck in self.total_firetrucks:
            btn = Button(text=firetruck, font_size="32sp")
            btn.bind(on_release=self.on_button_release)
            self.firetrucks_layout.add_widget(btn)

    def on_button_release(self, instance):
        # bind firetruck selection
        app = App.get_running_app()
        app.root.current = "fahrzeugkundegame"
        app.root.transition.direction = "left"

        # continue game with selected firetruck
        fahrzeugkundegame_screen = app.root.get_screen("fahrzeugkundegame")
        fahrzeugkundegame_screen.select_firetruck(instance.text)
        fahrzeugkundegame_screen.play()


class BewerbMenu(Screen):
    def __init__(self, **kwargs):
        super(BewerbMenu, self).__init__(**kwargs)

        # load available competitions
        total_competition_questions = load_total_competition_questions()
        self.total_competitions = list(total_competition_questions.keys())

        # create button for all firetrucks
        for competitions in self.total_competitions:
            btn = Button(text=competitions, font_size="32sp")
            btn.bind(on_release=self.on_button_release)
            self.bewerbe_layout.add_widget(btn)

    def on_button_release(self, instance):
        # bind competition selection
        app = App.get_running_app()
        app.root.current = "bewerbgame"
        app.root.transition.direction = "left"

        # continue game with selected firetruck
        bewerbgame_screen = app.root.get_screen("bewerbgame")
        bewerbgame_screen.select_competition(instance.text)
        bewerbgame_screen.play()


class FahrzeugkundeGame(Screen):
    def select_firetruck(self, selected_firetruck):
        # troubleshooting: fix firetruck
        # self.selected_firetruck = "Tank1" "Rüst+Lösch"
        self.selected_firetruck = selected_firetruck
        self.firetruck_label.text = selected_firetruck

    def play(self):
        self.load_firetruck_storage()
        self.next_tool()
        self.accept_answers = True  # Flag to indicate if answers should be processed

    def load_firetruck_storage(self):
        total_storage = load_total_storage()
        self.competition_dict = total_storage[self.selected_firetruck]
        self.rooms_list = self.competition_dict.keys()
        self.tools_list = [
            tool for room in self.competition_dict.values() for tool in room
        ]
        self.tools_list = list(set(self.tools_list))
        shuffle(self.tools_list)
        self.tool_locations = self.invert_firetruck_equipment()

    def invert_firetruck_equipment(self):
        tool_locations = {}
        for location, tools in self.competition_dict.items():
            for tool in tools:
                if tool in tool_locations:
                    tool_locations[tool].append(location)
                else:
                    tool_locations[tool] = [location]
        return tool_locations

    def next_tool(self, *args):
        self.accept_answers = True  # Enable answer processing for the new tool
        if not self.tools_list:
            self.load_firetruck_storage()

        # troubleshooting: fix tool
        # self.current_tool = "Handfunkgerät"  # "Druckschlauch B"
        self.current_tool = self.tools_list.pop()

        self.correct_storage = set(self.tool_locations.get(self.current_tool))

        if len(self.correct_storage) > 1:
            self.correct_storage_multiple = list(set(self.correct_storage))
        else:
            self.correct_storage_multiple = list()

        tool_text = self.current_tool
        if len(tool_text) >= 29:
            tool_text_lst = tool_text[14:].split(" ")
            tool_text = (
                tool_text[:14] + tool_text_lst[0] + "\n" + " ".join(tool_text_lst[1:])
            )
        self.tool_label.text = tool_text
        self.rooms_layout.clear_widgets()

        for storage in self.rooms_list:
            btn = Button(text=storage, font_size="28sp")
            btn.bind(on_press=self.on_answer)
            self.rooms_layout.add_widget(btn)

    def on_answer(self, instance):
        if not self.accept_answers:  # Check if answer processing is enabled
            return  # Ignore the button press if answer processing is disabled

        children = self.rooms_layout.children

        # one correct answer
        if len(self.correct_storage_multiple) <= 1:
            # Identify and indicate the correct answers
            for child in children:
                if child.text in self.correct_storage:
                    child.background_color = (0, 1, 0, 1)
            # Indicate if given answer was incorrect
            if instance.text not in self.correct_storage:
                instance.background_color = (1, 0, 0, 1)

        # multiple correct answers
        else:
            # Indicate if given answer was incorrect and close
            if instance.text not in self.correct_storage_multiple:
                instance.background_color = (1, 0, 0, 1)
                for child in children:
                    if child.text in self.correct_storage_multiple:
                        child.background_color = (0, 1, 0, 1)
                pass

            # answer was correct
            else:
                instance.background_color = (0, 1, 0, 1)
                # remove correct answer from set
                self.correct_storage_multiple.remove(instance.text)
                # display string "weitere"
                self.tool_label.text += "\nweitere"
                return

        self.accept_answers = (
            False  # Disable answer processing after an answer is selected
        )
        Clock.schedule_once(self.next_tool, 2)


class BewerbGame(Screen):
    def select_competition(self, selected_competition):
        # troubleshooting: fix competition
        # self.selected_competition = "Funk"
        self.selected_competition = selected_competition

    def play(self):
        self.load_competition_questions()
        self.next_question()
        self.accept_answers = True  # Flag to indicate if answers should be processed

    def load_competition_questions(self):
        total_questions = load_total_competition_questions()
        self.competition_dict = total_questions[self.selected_competition]

        self.question_ids = list(set(self.competition_dict.keys()))
        self.question_ids_total = len(self.question_ids)
        shuffle(self.question_ids)

    def break_lines(self, long_string: str) -> str:
        max_characters = 14
        words = long_string.split(" ")
        text = line = words[0]
        for word in words[1:]:
            if len(line) <= max_characters:
                text += " "
                line += " "
            else:
                text += "\n"
                line = ""
            text += word
            line += word
        return text

    def next_question(self):
        # self.accept_answers = True  # Enable answer processing for the new question
        if not self.question_ids:
            self.load_competition_questions()

        # troubleshooting: fix question
        # self.current_question_id = "22" # -> "Xaver"
        self.current_question_id = self.question_ids.pop()
        self.question_id_label.text = (
            f"{self.current_question_id} von {self.question_ids_total}"
        )

        self.current_question = self.competition_dict.get(self.current_question_id).get(
            "Q"
        )
        self.current_question = self.break_lines(self.current_question)
        self.question_label.text = self.current_question

        self.current_answer = self.competition_dict.get(self.current_question_id).get(
            "A"
        )[0]
        self.current_answer = self.break_lines(self.current_answer)
        self.answer_label.text = ""

    def reveal_answer(self):
        self.answer_label.text = self.current_answer


class WindowManager(ScreenManager):
    pass


class FeuerwehrApp(App):
    def build(self):

        sm = ScreenManager()
        sm.add_widget(StartMenu())
        sm.add_widget(FahrzeugkundeMenu())
        sm.add_widget(BewerbMenu())
        sm.add_widget(FahrzeugkundeGame())
        sm.add_widget(BewerbGame())
        return sm


if __name__ == "__main__":
    FeuerwehrApp().run()
