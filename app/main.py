from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.togglebutton import ToggleButton
from kivy.properties import BooleanProperty
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.clock import Clock

from kivy.uix.boxlayout import BoxLayout

from random import shuffle

from helper.firetrucks import load_total_storage
from helper.competitions import load_total_competition_questions
from helper.functions import load_firetruck_storage, mode_str2bool, mode_bool2str


class StartMenu(Screen):
    mode: tuple[bool, bool, bool, bool] = (
        True,  # training | default
        False,  # game
        False,  # browse
        False,  # images
    )

    def on_button_release(self):
        # if mode change, read mode label from current selection
        self.mode = mode_str2bool(self.find_down_toggle_button(self))

        # # disable not existing combinations
        # self.firetrucks_button.disabled = False
        # self.competition_button.disabled = False
        # mode_training, mode_game, mode_browse, mode_images = self.mode
        # if mode_images:
        #     self.firetrucks_button.disabled = True
        # if mode_game or mode_images or mode_browse:
        #     self.competition_button.disabled = True
        # disable not existing combinations
        self.firetrucks_button.enabled = True
        self.competition_button.enabled = True
        mode_training, mode_game, mode_browse, mode_images = self.mode
        if not mode_images:
            self.firetrucks_button.enabled = False
        if not (mode_game or mode_images or mode_browse):
            self.competition_button.enabled = False

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
        # on question selection, read mode label text from current screen
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
            fahrzeugkunde_tg_screen.forward_mode_2_fk_training_game(mode)
            fahrzeugkunde_tg_screen.play()

        elif mode_browse:
            # change screen
            app.root.current = "fahrzeugkunde_browse"
            app.root.transition.direction = "left"
            # continue game with selected firetruck
            fahrzeugkunde_browse_screen = app.root.get_screen("fahrzeugkunde_browse")
            fahrzeugkunde_browse_screen.select_firetruck(instance.text)
            fahrzeugkunde_browse_screen.populate_list()

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
        app.root.current = "bewerbtraining"
        app.root.transition.direction = "left"

        # continue game with selected firetruck
        bewerbtraining_screen = app.root.get_screen("bewerbtraining")
        bewerbtraining_screen.select_competition(instance.text)
        bewerbtraining_screen.play()


class FahrzeugkundeTrainingGame(Screen):
    strike_label_visible = BooleanProperty(False)
    timer_label_visible = BooleanProperty(False)
    timer_change_label_visible = BooleanProperty(False)
    timer_change_add = BooleanProperty(True)

    def select_firetruck(self, selected_firetruck: str):
        # troubleshooting: fix firetruck
        # self.selected_firetruck = "Tank1" "Rüst+Lösch"
        self.selected_firetruck = selected_firetruck
        self.firetruck_label.text = f"   {selected_firetruck}"

    def forward_mode_2_fk_training_game(self, mode: tuple):
        self.mode_training: bool = mode[0]
        self.mode_game: bool = mode[1]
        self.mode_browse: bool = mode[2]
        self.mode_images: bool = mode[3]

    def display_strike_label(self, display: bool = True):
        if display:
            self.strike_label_visible = True
        else:
            self.strike_label_visible = False

    def update_strike(self):
        self.strike_label.text = f"{str(self.strike)}  "

    def reset_strike(self):
        self.strike = 0
        self.update_strike()

    def increment_strike(self):
        self.strike += 1
        self.update_strike()

    def display_timer_label(self, display: bool = True):
        if display:
            self.timer_label_visible = True
        else:
            self.timer_label_visible = False

    def display_timer_change_label(self, *args):
        # state switch between True and False
        self.timer_change_label_visible = not self.timer_change_label_visible

    def display_timer_change_add(self):
        self.timer_change_add = not self.timer_change_add

    def reset_timer(self):
        self.time_left = 15  # seconds
        self.timer_label.text = f"{str(self.time_left)} s  "

    def add_time(self):
        time_extra = 4
        self.time_left += time_extra
        # todo: display time addition, green "+3"

    def subtract_time(self):
        time_punishment = 1
        self.time_left = max(
            0, self.time_left - time_punishment
        )  # Subtract 5 seconds, ensuring time doesn't go negative

    def update_time(self, *args):
        if self.time_left > 0:
            self.time_left -= 1
            if not self.time_left == 0:
                self.timer_label.text = f"{str(self.time_left)} s  "
            else:
                self.timer_label.text = "Ende  "
                # todo: disable buttons between game end and menu screen animation
        else:
            Clock.unschedule(self.update_time)  # Stop the timer when it reaches 0
            self.end_game()

    def update_score(self):
        self.score_label.text = f"{str(self.score)}  "

    def reset_score(self):
        self.score = 0
        self.update_score()

    def increment_score(self, add: int = 100):
        self.score += add
        self.update_score()

    def end_game(self):
        app = App.get_running_app()
        app.root.current = "fahrzeugkundemenu"
        app.root.transition.direction = "right"

    def reset_tool_list(self):
        rooms, tools, tools_locations = load_firetruck_storage(self.selected_firetruck)
        self.rooms: list = rooms
        self.tools: list = tools
        self.tools_locations: dict = tools_locations

        shuffle(self.tools)

    def play(self):
        # training mode
        if self.mode_training or self.mode_game:
            self.reset_tool_list()

        if self.mode_training:
            # disable timer and enable strike counter
            self.display_timer_label(display=False)
            self.reset_strike()
            self.display_strike_label()

        if self.mode_game:
            # disable strike and enable timer and score
            self.display_strike_label(display=False)
            self.reset_timer()
            self.display_timer_label()
            # Schedule the timer update every second
            Clock.schedule_interval(self.update_time, 1)
            # total score
            self.reset_score()

        self.next_tool()
        self.accept_answers = True  # Flag to indicate if answers should be processed

    def next_tool(self, *args):
        self.accept_answers = True  # Enable answer processing for the new tool

        if len(self.tools) == 0:
            self.reset_tool_list()

        # troubleshooting: fix tool
        # self.current_tool = "Handfunkgerät"  # "Druckschlauch B"
        self.current_tool = self.tools.pop()

        self.correct_storage: set = set(self.tools_locations.get(self.current_tool))

        self.correct_storage_multiple = list(self.correct_storage)

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

    def correct_answer(self):
        if self.mode_training:
            self.increment_strike()
        elif self.mode_game:
            self.increment_score()
            if not self.timer_change_add:
                # if False, switch to True
                self.display_timer_change_add()
            self.display_timer_change_label()
            Clock.schedule_once(self.display_timer_change_label, 2)

            self.add_time()
        # todo: pause timer until next tool (?)

    def incorrect_answer(self):
        if self.mode_training:
            self.reset_strike()
        elif self.mode_game:
            if self.timer_change_add:
                # if True, switch to False
                self.display_timer_change_add()
            self.display_timer_change_label()
            Clock.schedule_once(self.display_timer_change_label, 2)

            self.subtract_time()
        # todo: pause timer until next tool (?)

    def on_answer(self, instance):
        if not self.accept_answers:  # Check if answer processing is enabled
            return  # Ignore the button press if answer processing is disabled

        children = self.rooms_layout.children

        if instance.text in self.correct_storage_multiple:
            # correct answer
            self.correct_answer()
        else:
            # incorrect answer
            self.incorrect_answer()

        # indicate if correct or incorrect answer
        # for single correct answer
        if len(self.correct_storage_multiple) <= 1:
            # always identify and indicate the correct answer
            for child in children:
                if child.text in self.correct_storage:
                    child.background_color = (0, 1, 0, 1)
            # if, indicate incorrect answer
            if instance.text not in self.correct_storage:
                instance.background_color = (1, 0, 0, 1)

        # for multiple correct answers
        else:
            if instance.text not in self.correct_storage_multiple:
                # if, indicate incorrect and all correct answers and close
                instance.background_color = (1, 0, 0, 1)
                for child in children:
                    if child.text in self.correct_storage_multiple:
                        child.background_color = (0, 1, 0, 1)
                pass

            else:
                # answer in correct answers
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

        timer_pause = 2
        if self.mode_game:
            timer_pause = 0.5

        Clock.schedule_once(self.next_tool, timer_pause)
        # Clock.schedule_once(self.next_tool, 0.2)


class FahrzeugkundeBrowse(Screen):
    def select_firetruck(self, selected_firetruck: str):
        # troubleshooting: fix firetruck
        # self.selected_firetruck = "Tank1" "Rüst+Lösch"
        self.selected_firetruck = selected_firetruck
        self.firetruck_label.text = f"{selected_firetruck}   "

    def load_firetruck(self):
        total_storage = load_total_storage()
        self.firetruck: dict = total_storage[self.selected_firetruck]
        self.rooms: list = list(self.firetruck.keys())

    def populate_list(self):
        self.load_firetruck()
        container = self.ids.container
        container.clear_widgets()

        for room in self.rooms:
            label = Label(
                text=f"[b]{str(room)}[/b]",
                markup=True,
                size_hint_y=None,
                font_size="24sp",
                height=90,
                halign="left",
                text_size=(self.width, None),
            )
            label.bind(
                size=label.setter("text_size")
            )  # Update text_size on label size change
            container.add_widget(label)

            for tool in self.firetruck.get(room):
                label = Label(
                    text=f"   -  {str(tool)}",
                    size_hint_y=None,
                    size_hint_x=1,
                    font_size="22sp",
                    height=70,
                    halign="left",
                    valign="middle",
                )
                label.text_size = (label.width, None)
                label.bind(
                    width=lambda instance, value: setattr(
                        instance, "text_size", (value, None)
                    )
                )

                container.add_widget(label)


class Container(BoxLayout):
    pass


class FahrzeugkundeImages(Screen):
    pass


class BewerbTraining(Screen):
    def select_competition(self, selected_competition):
        # troubleshooting: fix competition
        # self.selected_competition = "Funk"
        self.selected_competition = selected_competition

    def play(self):
        self.load_competition_questions()
        self.next_question()

    def load_competition_questions(self):
        total_questions = load_total_competition_questions()
        self.competition_dict = total_questions[self.selected_competition]

        self.question_ids = list(set(self.competition_dict.keys()))
        shuffle(self.question_ids)

        self.question_ids_total = max([int(x) for x in self.question_ids])

    def next_question(self):
        if len(self.question_ids) == 0:
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
        self.question_label.text = self.current_question

        self.current_answer = self.competition_dict.get(self.current_question_id).get(
            "A"
        )[0]

    def reveal_answer(self):
        self.question_label.text += "\n\n" + self.current_answer


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
        sm.add_widget(BewerbTraining())
        return sm


if __name__ == "__main__":
    FeuerwehrApp().run()
