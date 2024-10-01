from kivy.uix.button import Button
from kivy.properties import BooleanProperty
from kivy.uix.screenmanager import Screen
from kivy.clock import Clock


from random import shuffle
import yaml

from helper.functions import load_firetruck_storage
from helper.settings import Settings


settings = Settings()


class Fahrzeugkunde_Training(Screen):
    strike_label_visible = BooleanProperty(False)

    def select_firetruck(self, selected_firetruck: str):
        # troubleshooting: fix firetruck
        # self.selected_firetruck = "Tank1" "Rüst+Lösch"
        self.selected_firetruck = selected_firetruck
        self.firetruck_label.text = f"   {selected_firetruck}"  # type: ignore

    def forward_mode_2_fk_training(self, mode: tuple):
        self.mode_training: bool = mode[0]
        self.mode_game: bool = mode[1]
        self.mode_browse: bool = mode[2]
        self.mode_images: bool = mode[3]

    def update_strike(self):
        self.strike_label.text = f"{str(self.strike)}  "  # type: ignore

    def reset_strike(self):
        self.strike = 0
        self.update_strike()

    def increment_strike(self):
        self.strike += 1
        self.update_strike()

    def save_high_strike(self):
        # with open("./app/storage/high_strike.yaml", "w") as f:
        with open(
            "/".join(__file__.split("/")[:-2]) + "/storage/high_strike.yaml", "w"
        ) as f:
            yaml.dump({"high_strike": self.strike}, f)

    # def end_game(self):
    #     self.save_high_strike()

    #     app = App.get_running_app()
    #     app.root.current = "fahrzeugkunde_menu"
    #     app.root.transition.direction = "right"

    def reset_tool_list(self):
        (self.firetruck_rooms, self.tools, self.tools_locations) = (
            load_firetruck_storage(self.selected_firetruck)
        )

        shuffle(self.tools)

    def play(self):
        self.reset_tool_list()

        self.reset_strike()

        self.next_tool()

        self.accept_answers = True  # Flag to indicate if answers should be processed

    def next_tool(self, *args):
        self.accept_answers = True  # Enable answer processing for the new tool

        if len(self.tools) == 0:
            self.reset_tool_list()

        # troubleshooting: fix tool
        # self.current_tool = "Handfunkgerät"  # "Druckschlauch B"
        self.current_tool = self.tools.pop()

        self.correct_storage: set = set(self.tools_locations.get(self.current_tool))  # type: ignore

        self.correct_storage_multiple = list(self.correct_storage)

        tool_text = self.current_tool
        if len(tool_text) >= 29:
            tool_text_lst = tool_text[14:].split(" ")
            tool_text = (
                tool_text[:14] + tool_text_lst[0] + "\n" + " ".join(tool_text_lst[1:])
            )
        self.tool_label.text = tool_text  # type: ignore
        self.firetruck_rooms_layout.clear_widgets()  # type: ignore

        for storage in self.firetruck_rooms:
            btn = Button(text=storage, font_size="28sp")
            btn.bind(on_press=self.on_answer)  # type: ignore
            self.firetruck_rooms_layout.add_widget(btn)  # type: ignore

    def on_answer(self, instance):
        if not self.accept_answers:  # Check if answer processing is enabled
            return  # Ignore the button press if answer processing is disabled

        children = self.firetruck_rooms_layout.children  # type: ignore

        if instance.text in self.correct_storage_multiple:
            # correct answer
            self.increment_strike()

        else:
            # incorrect answer
            self.reset_strike()

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
                if self.tool_label.text[-7:] == "weitere":  # type: ignore
                    self.tool_label.text += " "  # type: ignore
                else:
                    self.tool_label.text += "\n"  # type: ignore
                self.tool_label.text += "weitere"  # type: ignore
                return

        self.accept_answers = (
            False  # Disable answer processing after an answer is selected
        )

        Clock.schedule_once(self.next_tool, settings.FEEDBACK_TRAINING_SEC)
