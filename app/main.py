from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.clock import Clock

from random import shuffle

from helper.firetrucks import load_total_storage
from helper.competitions import load_total_competition_questions
from helper.functions import load_firetruck_storage, mode_str2bool


class StartMenu(Screen):
    # current_choice = "Training"  # default

    def forward_mode(self):
        selected_mode = self.find_down_toggle_button(self)
        if selected_mode:
            self.manager.current = "fahrzeugkundemenu"
            self.manager.get_screen("fahrzeugkundemenu").ids.mode_label.text = (
                f"{selected_mode}   "
            )

    def find_down_toggle_button(self, widget, selected_mode=None):
        # Recursively search for a ToggleButton in the 'down' state.
        if isinstance(widget, ToggleButton) and widget.state == "down":
            return widget.text
        for child in widget.children:
            result = self.find_down_toggle_button(child)
            if result:  # If a 'down' ToggleButton is found, return its text
                return result
        return selected_mode  # Return None if no 'down' ToggleButton is found


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

        mode = mode_str2bool(self.mode_label.text.strip())
        mode_training, mode_game, mode_browse, mode_images = mode

        # bind firetruck and mode selection
        app = App.get_running_app()

        if mode_training or mode_game:
            app.root.current = "fahrzeugkunde_training_game"
            app.root.transition.direction = "left"

            # continue game with selected firetruck
            fahrzeugkunde_tg_screen = app.root.get_screen("fahrzeugkunde_training_game")
            fahrzeugkunde_tg_screen.select_firetruck(instance.text)
            # fahrzeugkunde_training_screen.forward_mode_str(self.mode_label.text)
            # fahrzeugkunde_tg_screen.forward_mode(
            #     mode_str2bool(self.mode_label.text.strip())
            # )
            fahrzeugkunde_tg_screen.forward_mode(mode)
            fahrzeugkunde_tg_screen.play()

        elif mode_browse:
            app.root.current = "fahrzeugkunde_browse"
            app.root.transition.direction = "left"

        elif mode_images:
            app.root.current = "fahrzeugkunde_images"
            app.root.transition.direction = "left"


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


class FahrzeugkundeTrainingGame(Screen):
    def select_firetruck(self, selected_firetruck: str):
        # troubleshooting: fix firetruck
        # self.selected_firetruck = "Tank1" "Rüst+Lösch"
        self.selected_firetruck = selected_firetruck
        self.firetruck_label.text = f"   {selected_firetruck}"

    def forward_mode(self, mode: tuple):
        self.mode_training: bool = mode[0]
        self.mode_game: bool = mode[1]
        self.mode_browse: bool = mode[2]
        self.mode_images: bool = mode[3]

    def play(self):
        # training mode
        print(f"{self.mode_training = }, {self.mode_game = }")
        if self.mode_training or self.mode_game:
            # self.load_firetruck_storage()
            rooms, tools, tools_locations = load_firetruck_storage(
                self.selected_firetruck
            )
            self.rooms: list = rooms
            self.tools: list = tools
            self.tools_locations: dict = tools_locations

            shuffle(self.tools)

        self.next_tool()
        self.accept_answers = True  # Flag to indicate if answers should be processed

    def next_tool(self, *args):
        self.accept_answers = True  # Enable answer processing for the new tool

        # training mode
        if not self.tools:
            self.load_firetruck_storage()
            shuffle(self.tools)

        # troubleshooting: fix tool
        # self.current_tool = "Handfunkgerät"  # "Druckschlauch B"
        self.current_tool = self.tools.pop()

        self.correct_storage = set(self.tools_locations.get(self.current_tool))

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

        for storage in self.rooms:
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
                if self.tool_label.text[-7:] == "weitere":
                    self.tool_label.text += " "
                else:
                    self.tool_label.text += "\n"
                self.tool_label.text += "weitere"
                return

        self.accept_answers = (
            False  # Disable answer processing after an answer is selected
        )
        # Clock.schedule_once(self.next_tool, 2)
        Clock.schedule_once(self.next_tool, 0.2)


class FahrzeugkundeBrowse(Screen):
    pass


class FahrzeugkundeImages(Screen):
    pass


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


class CustomToggleButton(ToggleButton):
    def on_touch_up(self, touch):
        # Call the superclass method to ensure standard behavior is preserved
        super_result = super(CustomToggleButton, self).on_touch_up(touch)
        if self.state == "normal":  # Check if the button was just released
            # Force it back to 'down' state if no other buttons are down
            if not any(btn.state == "down" for btn in self.get_widgets(self.group)):
                self.state = "down"
        return super_result


class FeuerwehrApp(App):
    def build(self):

        sm = ScreenManager()
        sm.add_widget(StartMenu())
        sm.add_widget(FahrzeugkundeMenu())
        sm.add_widget(BewerbMenu())
        sm.add_widget(FahrzeugkundeTrainingGame())
        sm.add_widget(FahrzeugkundeBrowse())
        sm.add_widget(FahrzeugkundeImages())
        sm.add_widget(BewerbGame())
        return sm


if __name__ == "__main__":
    FeuerwehrApp().run()
