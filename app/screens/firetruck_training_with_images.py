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
    TrainingText_AllTools,
    TrainingText_HalfTools,
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

        self.load_default_tool_list()

        self.load_score_content()

        self.check_tool_list()

        self.first_tool = True

        self.prewarm_room_images()

        self.reset_progress_bar()

        self.reset_score()

        self.next_tool()

    def prewarm_room_images(self):
        room_image_paths = set()
        for tool_question in self.default_tool_list:
            if tool_question.room_image_name and tool_question.room_image_name != "":
                room_image_paths.add(tool_question.room_image_name)

        # Start background loading for all unique room images
        for path in room_image_paths:
            if path not in self._img_proxies:
                self._img_proxies[path] = Loader.image(path)

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

        if len(self.current_tool_list) == 0:
            if not self.first_tool:
                self.percentages.append(self.current_percentage)

                # all tools have been trained
                info_popup = TextPopup(
                    message=TrainingText_AllTools(
                        self.tool_amount,
                        self.current_correct_answers,
                        self.current_percentage,
                    ).TEXT,
                    title=strings.TITLE_INFO_POPUP,
                    size_hint=(0.6, 0.6),
                )
                info_popup.open()

            self.save_score_percentage()

            self.reset_current_tool_list()

            self.update_score_labels()

        if len(self.current_tool_list) == self.tool_amount // 2:
            # half of tools have been trained
            info_popup = TextPopup(
                message=TrainingText_HalfTools(
                    self.tool_amount,
                    self.current_correct_answers,
                    self.current_percentage,
                ).TEXT,
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

        self.current_tool_name = self.current_tool_list.pop()

        self.current_tool_question = [
            item
            for item in self.default_tool_list
            if item.tool == self.current_tool_name
        ][0]

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

    def on_answer(self, instance):
        self.first_tool = False

        if not self.accept_answers:  # Check if answer processing is enabled
            return  # Ignore the button press if answer processing is disabled

        # do not accept identical answer
        if instance.text in self.current_tool_question.room_answered:
            return

        if len(self.current_tool_question.rooms_to_be_answered) <= 1:
            self.single_correct_answer = True
        else:
            self.single_correct_answer = False

        # process actual answer
        if instance.text in self.current_tool_question.rooms:
            # TODO if multiple correct answers possible, increment correct answer only once!
            self.correct_answer()
            self.answer_correct = True

        else:
            self.incorrect_answer()
            self.answer_correct = False

        self.update_score_labels()

        if self.color_layout(instance):
            return

        # document given answers in class instance
        self.current_tool_question.room_answered.append(instance.text)

        # Disable answer processing after an answer is selected
        self.accept_answers = False

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

        self.save_score_content()

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
