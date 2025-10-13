from kivy.uix.image import Image
from kivy.graphics import Color, Rectangle
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen
from kivy.clock import Clock
from kivy.loader import Loader

from popups.text_popup import TextPopup

from helper.functions import get_firetruck_layouts
from helper.file_handling import (
    tool_image_file_exists,
    get_selected_city_state,
    get_selected_firetruck,
)
from helper.settings import Settings
from helper.strings import (
    Strings,
    Firetruck_TrainingText_AllTools,
    Firetruck_TrainingText_HalfTools,
)
from helper.game_class import GameCore
from helper.firetruck_layouts import build_answer_layout

from screens.screen_base import BaseMethods


settings = Settings()
strings = Strings()


class Firetruck_Training_With_Images(Screen, BaseMethods):
    def __init__(self, **kwargs):
        super(Firetruck_Training_With_Images, self).__init__(**kwargs)

        # do this once (e.g., in App.build or your Screen __init__)
        Loader.num_workers = 2  # tweak 2–8 depending on cores
        self._img_proxies = {}  # path -> ProxyImage

    def on_pre_enter(self):
        self.selected_city, _ = get_selected_city_state()

        self.selected_firetruck = get_selected_firetruck()

        self.current_screen = self.get_current_screen()

        self.ids.firetruck_label.text = self.selected_firetruck

        self.room_layout = get_firetruck_layouts(
            self.selected_firetruck, self.selected_city
        )

        self.play()

    def play(self):
        self.game = GameCore()

        self.reset_tool_list()

        self.prewarmed_question = []

        self.reset_progress_bar()

        self.load_high_score()

        self.reset_score()

        self.next_tool()

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
            # troubleshooting: fix first popped tool
            # self.set_first_tool("Unterlegplatte")  # for testing
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

    def on_answer(self, instance):
        if not self.accept_answers:  # Check if answer processing is enabled
            return  # Ignore the button press if answer processing is disabled

        # do not accept identical answer
        if instance.text in self.current_tool_question.room_answered:
            return

        # process actual answer
        if instance.text in self.current_tool_question.rooms:
            self.correct_answer()
            self.answer_correct = True

        else:
            self.incorrect_answer()
            self.answer_correct = False

        if self.color_layout(instance):
            return

        # document given answers in class instance
        self.current_tool_question.room_answered.append(instance.text)

        self.accept_answers = (
            False  # Disable answer processing after an answer is selected
        )

        # tool ends here. document tool and given answers in question history
        self.game.questions.append(self.current_tool_question)

        self.show_feedback_image()

    def incorrect_answer(self):
        self.feedback_green = False

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
                self.add_image(
                    layout, self.current_tool_question.room_image_name, usage="room"
                )

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

            if not self.answer_correct:
                self.reset_score()

            self.root_layer.remove_widget(self.overlay_button)

            self.next_tool()
