from kivy.uix.image import Image
from kivy.graphics import Color, Rectangle
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen
from kivy.clock import Clock
from kivy.loader import Loader

from random import shuffle
from typing import cast

from popups.text_popup import TextPopup

from helper.functions import (
    get_ToolQuestion_instances,
    change_screen_to,
    get_firetruck_layouts,
    break_tool_name,
)
from helper.file_handling import (
    save_to_scores_file,
    get_score_value,
    tool_image_file_exists,
)
from helper.settings import Settings
from helper.strings import (
    Strings,
    Firetruck_TrainingText_AllTools,
    Firetruck_TrainingText_HalfTools,
)
from helper.game_class import GameCore
from helper.firetruck_layouts import build_answer_layout


settings = Settings()
strings = Strings()


class Firetruck_Training_With_Images(Screen):
    def __init__(self, **kwargs):
        super(Firetruck_Training_With_Images, self).__init__(**kwargs)

        # do this once (e.g., in App.build or your Screen __init__)
        Loader.num_workers = 2  # tweak 2–8 depending on cores
        self._img_proxies = {}  # path -> ProxyImage

    def prewarm_images(self, paths):
        # kick off background loads and keep references so cache isn't GC'd
        for p in paths:
            self._img_proxies[p] = self._img_proxies.get(p) or Loader.image(p)

    def add_image(self, layout, path, usage: str = "tool"):
        # get (or start) the background load
        proxy = self._img_proxies.get(path) or Loader.image(path)
        self._img_proxies[path] = proxy

        # make the widget now
        if usage == "tool":
            image = Image(
                fit_mode="contain",
                size_hint_y=3,
            )
        elif usage == "room":
            image = Image(
                fit_mode="contain",
            )
        layout.add_widget(image)

        # when the background load finishes, assign the texture on the main thread
        def _apply_texture(_=None):
            if proxy.image and proxy.image.texture:
                # schedule is extra-safe to ensure we're on the UI thread
                Clock.schedule_once(
                    lambda dt: setattr(image, "texture", proxy.image.texture), 0
                )

        # if it's already warm, set immediately; otherwise bind to on_load
        if proxy.image:
            _apply_texture()
        else:
            proxy.bind(on_load=_apply_texture)

        return image

    def select_city(self, selected_city: str):
        self.selected_city = selected_city

    def select_firetruck(self, selected_firetruck: str):
        # troubleshooting: fix firetruck
        # self.selected_firetruck = "Tank1" "Rüst+Lösch"
        self.selected_firetruck = selected_firetruck

        self.firetruck_label = cast(Label, self.firetruck_label)
        self.firetruck_label.text = selected_firetruck

        self.room_layout = get_firetruck_layouts(selected_firetruck, self.selected_city)

    def update_strike_label(self):
        self.strike_label = cast(Label, self.strike_label)
        self.strike_label.text = str(self.game.answers_correct_strike)

    def update_high_strike_label(self):
        self.high_strike_label = cast(Label, self.high_strike_label)
        self.high_strike_label.text = f"Best: {str(self.current_high_strike)}"

    def reset_strike(self, *arg):
        self.game.answers_correct_strike = 0
        self.update_strike_label()

    def increment_strike(self):
        self.game.answers_correct_strike += settings.FIRETRUCK_TRAINING_CORRECT_POINTS
        self.update_strike_label()

    def reset_tool_list(self):
        (self.firetruck_rooms, self.tool_questions) = get_ToolQuestion_instances(
            self.selected_firetruck, self.selected_city
        )
        self.tool_amount = len(self.tool_questions)

        shuffle(self.tool_questions)

    def reset_progress_bar(self):
        self.ids.progress_bar_answer.max = (
            settings.FIRETRUCK_TRAINING_WITH_IMAGES_FEEDBACK_SEC - 0.3
        )
        self.ids.progress_bar_answer.value = 0

    def play(self):
        # init GameCore class instance
        self.game = GameCore()

        # (re)set game specific elements
        self.reset_tool_list()

        # init prewarm var for next question
        self.prewarmed_question = []

        self.reset_progress_bar()

        self.reset_strike()

        # TODO: high_strike already used!
        # decide on wether overwriting or introducing a new variable
        # or replacing regular training mode
        self.current_high_strike = get_score_value(
            city=self.selected_city,
            questions="firetrucks",
            truck_or_comp=self.selected_firetruck,
            key="high_strike_image",
        )

        self.update_high_strike_label()

        self.next_tool()

    def next_tool(self, *args):
        self.accept_answers = True

        if len(self.tool_questions) == 0:
            self.reset_tool_list()

            # all tools have been trained
            info_popup = TextPopup(
                message=Firetruck_TrainingText_AllTools(self.tool_amount).TEXT,
                title=strings.TITLE_INFO_POPUP,
                size_hint=(0.6, 0.6),
            )
            info_popup.open()

        if len(self.tool_questions) == self.tool_amount // 2:
            # half of tools have been trained
            info_popup = TextPopup(
                message=Firetruck_TrainingText_HalfTools(self.tool_amount).TEXT,
                title=strings.TITLE_INFO_POPUP,
                size_hint=(0.6, 0.6),
            )
            info_popup.open()

        # Reset image boxes
        self.ids.firetruck_rooms_layout.clear_widgets()
        self.ids.tool_image_layout.clear_widgets()

        layout = self.ids.tool_image_layout
        layout.clear_widgets()
        layout.canvas.before.clear()

        # first tool will be rendered without prewarm
        # then prewarm next tool image
        if self.prewarmed_question:
            self.current_tool_question = self.prewarmed_question
            tool_image_prewarmed = True
        else:
            # troubleshooting: fix tool
            # self.current_tool = "Handfunkgerät"  # "Druckschlauch B"
            self.current_tool_question = self.tool_questions.pop()
            tool_image_prewarmed = False

        # always prewarm room image
        self.prewarm_images([self.current_tool_question.room_image_name])

        self.tool_label = Label(
            text=self.current_tool_question.tool,
            size_hint_y=1,
            font_size="28sp",
        )
        self.ids.tool_image_layout.add_widget(self.tool_label)

        # display image if available
        # tool image file name is either tag or name of tool + ".jpg"
        # if not self.current_tool_question.tool_image_name == "":
        try:
            if not tool_image_file_exists(self.current_tool_question.tool_image_name):
                raise FileNotFoundError()

            # first tool will be created and rendered without prewarm
            # then prewarm next tool image
            if tool_image_prewarmed:
                self.add_image(
                    self.ids.tool_image_layout,
                    self.current_tool_question.tool_image_name,
                )

            else:
                tool_image = Image(
                    source=self.current_tool_question.tool_image_name,
                    fit_mode="contain",
                    size_hint_y=3,
                )
                self.ids.tool_image_layout.add_widget(tool_image)

        except Exception as e:
            print(
                f"Tool image load failed. Error: {e}, Tool file: {self.current_tool_question.tool_image_name}"
            )
            placeholder = Label(text=strings.ERROR_IMAGE_NOT_FOUND, size_hint_y=3)
            self.ids.tool_image_layout.add_widget(placeholder)

        # display background and buttons
        float = build_answer_layout(self.room_layout, "firetruck_training_with_images")

        self.ids.firetruck_rooms_layout.add_widget(float)

        # pick and prewarm upcoming tool question
        self.prewarmed_question = self.tool_questions.pop()
        self.prewarm_images([self.prewarmed_question.tool_image_name])

    def correct_answer(self):
        self.increment_strike()

        self.game.answers_correct_total += settings.FIRETRUCK_TRAINING_CORRECT_POINTS

        if self.game.answers_correct_strike > self.current_high_strike:
            self.current_high_strike = self.game.answers_correct_strike
            self.update_high_strike_label()
            save_to_scores_file(
                city=self.selected_city,
                questions="firetrucks",
                truck_or_comp=self.selected_firetruck,
                key="high_strike_image",
                value=self.game.answers_correct_strike,
            )

        self.feedback_green = True

    def incorrect_answer(self):
        self.feedback_green = False

        Clock.schedule_once(self.reset_strike, settings.FIRETRUCK_TRAINING_FEEDBACK_SEC)

    def on_answer(self, instance):
        if not self.accept_answers:  # Check if answer processing is enabled
            return  # Ignore the button press if answer processing is disabled

        # do not accept identical answer
        if instance.text in self.current_tool_question.room_answered:
            return

        # process actual answer
        if instance.text in self.current_tool_question.rooms:
            self.correct_answer()

        else:
            self.incorrect_answer()

        float_layout = self.ids.firetruck_rooms_layout.children[
            0
        ]  # children is reversed

        # indicate if correct or incorrect answer
        # for single correct answer
        if len(self.current_tool_question.rooms_to_be_answered) <= 1:
            # always identify and indicate the correct answer
            # for child in children:
            for child in float_layout.children:
                if isinstance(child, Button):
                    if child.text in self.current_tool_question.rooms:
                        child.background_color = (0, 1, 0, 1)
            # if, indicate incorrect answer
            if instance.text not in self.current_tool_question.rooms:
                instance.background_color = (1, 0, 0, 1)

        # for multiple correct answers
        else:
            # document given answers in class instance
            self.current_tool_question.room_answered.append(instance.text)

            if instance.text not in self.current_tool_question.rooms:
                # if, indicate incorrect and all correct answers and close
                instance.background_color = (1, 0, 0, 1)
                # for child in children:
                for child in float_layout.children:
                    if isinstance(child, Button):
                        if child.text in self.current_tool_question.rooms:
                            child.background_color = (0, 1, 0, 1)
                pass

            else:
                # answer in correct answers
                instance.background_color = (0, 0, 1, 1)

                self.tool_label.text += "\n"
                self.tool_label.text += strings.HINT_STR_MULTIPLE_ANSWERS

                return

        # document given answers in class instance
        self.current_tool_question.room_answered.append(instance.text)

        self.accept_answers = (
            False  # Disable answer processing after an answer is selected
        )

        # tool ends here. document tool and given answers in question history
        self.game.questions.append(self.current_tool_question)

        self.show_feedback_image()

    def show_feedback_image(self):
        # Show location image during cooldown if available
        # self.ids.image_box_answer.clear_widgets()
        #
        # room image file name is either tag or name of room + ".jpg"
        #
        # multiple rooms are ignored for now
        if not self.current_tool_question.room_image_name == "":
            layout = self.ids.tool_image_layout
            layout.clear_widgets()
            layout.canvas.before.clear()

            # Set background color only on the layout
            with layout.canvas.before:
                if self.feedback_green:
                    Color(0, 0.5, 0, 1)  # Green
                else:
                    Color(0.5, 0, 0, 1)  # Red
                layout.rect = Rectangle(pos=layout.pos, size=layout.size)

            # Bind layout's pos/size to update the background rectangle
            layout.bind(pos=self.update_rect, size=self.update_rect)

            # # tool name Label
            # # tool + " in " + room
            # tool_answer = f"{self.current_tool_question.tool} in {', '.join(self.current_tool_question.rooms)}"
            # tool_label_answer = Label(
            #     text=break_tool_name(tool_answer, 35),
            #     size_hint_y=1,
            #     font_size="20sp",  # "28sp"
            # )
            # layout.add_widget(tool_label_answer)

            # progress bar
            interval = settings.FIRETRUCK_TRAINING_WITH_IMAGES_FEEDBACK_SEC / 50

            self.ids.progress_bar_answer.value = (
                settings.FIRETRUCK_TRAINING_WITH_IMAGES_FEEDBACK_SEC
            )

            Clock.schedule_interval(self.update_progress_bar, interval)

            # room image
            try:
                ###
                # room_image = Image(
                #     # source=self.current_tool_question.room_image_name,
                #     fit_mode="contain",
                # )
                # layout.add_widget(room_image)
                self.add_image(
                    layout, self.current_tool_question.room_image_name, usage="room"
                )
                ###

            except Exception as e:
                print(f"Room image load failed: {e}")
                # Add a placeholder label if the image is not found
                placeholder = Label(
                    text=strings.ERROR_IMAGE_NOT_FOUND, size_hint=(1, 1)
                )
                layout.add_widget(placeholder)

            # add invincible overlay float button
            # if clicked, skip cooldown
            # overlay button shall span the whole screen except the top bar

            self.root_layer = self.ids.root_layer

            self.overlay_button = Button(
                size_hint=(1, 1),
                pos_hint={"center_x": 0.5, "center_y": 0.5},
                background_color=(0, 0, 0, 0),  # Invisible
            )
            self.overlay_button.bind(
                on_release=lambda *_: self.on_overlay_button_release()
            )

            self.root_layer.add_widget(self.overlay_button)

    def on_overlay_button_release(self):
        self.root_layer.remove_widget(self.overlay_button)

        self.progress_bar_answer.value = -5

    def update_rect(self, *args):
        layout = self.ids.tool_image_layout
        if hasattr(layout, "rect"):
            layout.rect.pos = layout.pos
            layout.rect.size = layout.size

    def update_progress_bar(self, dt):
        interval = settings.FIRETRUCK_TRAINING_WITH_IMAGES_FEEDBACK_SEC / 50
        self.progress_bar_answer.value = max(
            0, self.progress_bar_answer.value - interval
        )

        if self.progress_bar_answer.value <= 0:
            Clock.unschedule(
                self.update_progress_bar
            )  # Stop the timer when it reaches 0

            self.root_layer.remove_widget(self.overlay_button)

            self.next_tool()

    def go_back(self, *args) -> None:
        change_screen_to("firetruck_menu")
