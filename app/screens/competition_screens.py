from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.screenmanager import Screen

from random import shuffle

from helper.functions import mode_str2bool, load_total_competition_questions
from helper.functions import mode_str2bool
from helper.settings import Strings

strings = Strings()


class Bewerb_Menu(Screen):
    def __init__(self, **kwargs):
        super(Bewerb_Menu, self).__init__(**kwargs)
        # load available competitions
        total_competition_questions = load_total_competition_questions()
        self.total_competitions = list(total_competition_questions.keys())
        # create button for all firetrucks
        for competitions in self.total_competitions:
            btn = Button(text=competitions, font_size="32sp")
            btn.bind(on_release=self.on_button_release)  # type: ignore
            self.bewerbe_layout.add_widget(btn)  # type: ignore

    def on_button_release(self, instance):
        # on question selection, read mode label text from current screen
        mode = mode_str2bool(self.mode_label.text.strip())  # type: ignore
        mode_training, mode_game, mode_browse, mode_images = mode

        # bind competition selection
        app = App.get_running_app()

        # if mode_training or mode_game:
        if mode_training:
            app.root.current = "bewerb_training"  # type: ignore
            app.root.transition.direction = "left"  # type: ignore
            # continue game with selected competition
            bewerb_training_screen = app.root.get_screen("bewerb_training")  # type: ignore
            bewerb_training_screen.select_competition(instance.text)
            bewerb_training_screen.play()
            # adapt for competition
            # fahrzeugkunde_tg_screen.forward_mode_2_fk_training_game(mode)

        # adapt for competition
        # elif mode_browse:
        #     # change screen
        #     app.root.current = "fahrzeugkunde_browse"
        #     app.root.transition.direction = "left"
        #     # continue game with selected firetruck
        #     fahrzeugkunde_browse_screen = app.root.get_screen("fahrzeugkunde_browse")
        #     fahrzeugkunde_browse_screen.select_firetruck(instance.text)
        #     fahrzeugkunde_browse_screen.populate_list()

        # adapt for competition
        # elif mode_images:
        #     app.root.current = "fahrzeugkunde_images"
        #     app.root.transition.direction = "left"


class Bewerb_Training(Screen):
    def __init__(self, **kwargs):
        super(Bewerb_Training, self).__init__(**kwargs)
        # update button strings
        self.solution_button.text = strings.BUTTON_STR_SOLUTION  # type: ignore
        self.random_question_button.text = strings.BUTTON_STR_RANDOM_QUESTION  # type: ignore

    def select_competition(self, selected_competition):
        # troubleshooting: fix competition
        # self.selected_competition = "Funk"
        self.selected_competition = selected_competition

    def load_competition_questions(self):
        total_questions = load_total_competition_questions()
        self.competition_dict = total_questions[self.selected_competition]

        self.question_ids = list(self.competition_dict.keys())
        # self.question_ids = [int(question_id) for question_id in list(self.competition_dict.keys())]
        shuffle(self.question_ids)  # moved to self.play()  # reverted!! needs to be executed each new load

        self.question_ids_min = str(min([int(x) for x in self.question_ids]))
        self.question_ids_max = str(max([int(x) for x in self.question_ids]))

    def play(self):
        self.load_competition_questions()

        # start with smallest question id, then shuffle list
        self.current_question_id = self.question_ids.pop(0)
        # shuffle(self.question_ids)  # moved to load_competition_questions()

        self.previous_question_button.disabled = True  # type: ignore
        self.next_question_button.disabled = False  # type: ignore

        self.process_question()

    def process_question(self):
        self.question_id_label.text = (  # type: ignore
            f"{self.current_question_id} von {self.question_ids_max}"
        )
        print(f"{self.current_question_id = }")
        print(f"{self.competition_dict.get(self.current_question_id) = }")
        print(f"{self.competition_dict.get(self.current_question_id).get("Q") = }")
        self.current_question = self.competition_dict.get(self.current_question_id).get(
            "Q"
        )
        self.question_label.text = self.current_question  # type: ignore

        self.current_answer = self.competition_dict.get(self.current_question_id).get(
            "A"
        )[0]

    def random_question(self):
        self.ids.question_scrollview.scroll_y = 1
        self.previous_question_button.disabled = False  # type: ignore
        self.next_question_button.disabled = False  # type: ignore
        self.solution_button.disabled = False  # type: ignore

        if len(self.question_ids) == 0:
            self.load_competition_questions()

        # troubleshooting: fix question
        # self.current_question_id = "22" # -> "Xaver"
        self.current_question_id = self.question_ids.pop()

        self.process_question()

    def next_question(self, previous: bool = False):
        self.previous_question_button.disabled = False  # type: ignore
        self.next_question_button.disabled = False  # type: ignore
        self.solution_button.disabled = False  # type: ignore

        if previous:
            # self.current_question_id = str(int(self.current_question_id) - 1)
            self.current_question_id = int(self.current_question_id) - 1
        else:
            # self.current_question_id = str(int(self.current_question_id) + 1)
            self.current_question_id = int(self.current_question_id) + 1

        if self.current_question_id == self.question_ids_min:
            self.previous_question_button.disabled = True  # type: ignore
        if self.current_question_id == self.question_ids_max:
            self.next_question_button.disabled = True  # type: ignore

        self.process_question()

    def reveal_answer(self):
        self.solution_button.disabled = True  # type: ignore

        self.question_label.text += "\n\n" + self.current_answer  # type: ignore
        self.ids.question_label.height = self.ids.question_label.texture_size[1]
