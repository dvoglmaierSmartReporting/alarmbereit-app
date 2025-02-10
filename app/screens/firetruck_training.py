from kivy.uix.button import Button
from kivy.properties import BooleanProperty
from kivy.uix.screenmanager import Screen
from kivy.clock import Clock


from random import shuffle

from helper.functions import get_firetruck_storage, break_tool_name
from helper.file_handling import save_to_scores_file, get_scores_key
from helper.settings import Settings
from helper.game_class import GameCore, ToolQuestion


settings = Settings()


class Fahrzeugkunde_Training(Screen):
    strike_label_visible = BooleanProperty(False)

    def select_firetruck(self, selected_firetruck: str):
        # troubleshooting: fix firetruck
        # self.selected_firetruck = "Tank1" "Rüst+Lösch"
        self.selected_firetruck = selected_firetruck
        self.firetruck_label.text = f"   {selected_firetruck}"  # type: ignore

    # def forward_mode_2_fk_training(self, mode: tuple):
    #     self.mode_training: bool = mode[0]
    #     self.mode_game: bool = mode[1]
    #     self.mode_browse: bool = mode[2]
    #     self.mode_images: bool = mode[3]

    def update_strike_label(self):
        self.strike_label.text = f"{str(self.game.answers_correct_strike)}  "  # type: ignore

    def update_high_strike_label(self):
        self.high_strike_label.text = f"Best: {str(self.current_high_strike)}  "  # type: ignore

    def reset_strike(self, *arg):
        self.game.answers_correct_strike = 0
        self.update_strike_label()

    def increment_strike(self):
        self.game.answers_correct_strike += 1
        self.update_strike_label()

    # def end_game(self):
    #     self.save_high_strike()

    #     app = App.get_running_app()
    #     app.root.current = "fahrzeugkunde_menu"
    #     app.root.transition.direction = "right"

    def reset_tool_list(self):
        (self.firetruck_rooms, self.tools, self.tools_locations) = (
            get_firetruck_storage(self.selected_firetruck)
        )

        shuffle(self.tools)

    def play(self):
        # init GameCore class instance
        self.game = GameCore()

        # (re)set game specific elements
        self.reset_tool_list()

        self.reset_strike()

        self.current_high_strike = get_scores_key(
            self.selected_firetruck, "high_strike"
        )

        self.update_high_strike_label()

        # NEXT: when to update high_strike???
        # todo: display best strike!

        self.next_tool()

    def next_tool(self, *args):
        self.accept_answers = True  # Enable answer processing for the new tool

        if len(self.tools) == 0:
            self.reset_tool_list()

        # troubleshooting: fix tool
        # self.current_tool = "Handfunkgerät"  # "Druckschlauch B"
        current_tool = self.tools.pop()

        self.current_question = ToolQuestion(
            firetruck=self.selected_firetruck,
            tool=current_tool,
            rooms=list(set(self.tools_locations.get(current_tool))),  # type: ignore
        )

        self.tool_label.text = break_tool_name(current_tool)  # type: ignore

        self.firetruck_rooms_layout.clear_widgets()  # type: ignore

        for storage in self.firetruck_rooms:
            btn = Button(text=storage, font_size="28sp", disabled=storage == "")
            btn.bind(on_press=self.on_answer)  # type: ignore
            self.firetruck_rooms_layout.add_widget(btn)  # type: ignore

    def correct_answer(self):
        self.increment_strike()

        self.game.answers_correct_total += 1

        if self.game.answers_correct_strike > self.current_high_strike:
            self.current_high_strike = self.game.answers_correct_strike
            self.update_high_strike_label()
            save_to_scores_file(
                self.selected_firetruck, "high_strike", self.game.answers_correct_strike
            )

    def incorrect_answer(self):
        # self.reset_strike()
        Clock.schedule_once(self.reset_strike, settings.FEEDBACK_TRAINING_SEC)

        # todo: check for PB score!

    def on_answer(self, instance):
        if not self.accept_answers:  # Check if answer processing is enabled
            return  # Ignore the button press if answer processing is disabled

        # do not accept identical answer
        if instance.text in self.current_question.room_answered:
            return

        # process actual answer
        if instance.text in self.current_question.rooms:
            self.correct_answer()

        else:
            self.incorrect_answer()

        children = self.firetruck_rooms_layout.children  # type: ignore

        # indicate if correct or incorrect answer
        # for single correct answer
        if len(self.current_question.rooms_to_be_answered) <= 1:
            # always identify and indicate the correct answer
            for child in children:
                if child.text in self.current_question.rooms:
                    child.background_color = (0, 1, 0, 1)
            # if, indicate incorrect answer
            if instance.text not in self.current_question.rooms:
                instance.background_color = (1, 0, 0, 1)

        # for multiple correct answers
        else:
            # document given answers in class instance
            self.current_question.room_answered.append(instance.text)

            if instance.text not in self.current_question.rooms:
                # if, indicate incorrect and all correct answers and close
                instance.background_color = (1, 0, 0, 1)
                for child in children:
                    if child.text in self.current_question.rooms:
                        child.background_color = (0, 1, 0, 1)
                pass

            else:
                # answer in correct answers
                instance.background_color = (0, 1, 0, 1)

                # display string "weitere"
                if self.tool_label.text[-7:] == "weitere":  # type: ignore
                    self.tool_label.text += " "  # type: ignore
                else:
                    self.tool_label.text += "\n"  # type: ignore
                self.tool_label.text += "weitere"  # type: ignore
                return

        # document given answers in class instance
        self.current_question.room_answered.append(instance.text)

        self.accept_answers = (
            False  # Disable answer processing after an answer is selected
        )

        # tool ends here. document tool and given answers in question history
        self.game.questions.append(self.current_question)

        Clock.schedule_once(self.next_tool, settings.FEEDBACK_TRAINING_SEC)
