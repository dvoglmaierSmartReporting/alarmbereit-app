from kivy.app import App
from kivy.clock import Clock
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen
from kivy.core.window import Window
from kivy.metrics import dp
from kivy.utils import platform

from dataclasses import dataclass
from random import shuffle

from helper.settings import Settings
from helper.strings import TrainingEndText
from helper.functions import *
from helper.file_handling import *

from popups.text_popup import TextPopup


settings = Settings()


@dataclass
class FontSizeMixin:
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.dynamic_widgets = []

    def get_font_scale(self):
        return max(0.8, min(1.5, Window.width / dp(600)))

    def register_widget_for_font_scaling(self, widget, base_font_size):
        self.dynamic_widgets.append({"widget": widget, "base_size": base_font_size})

        # Apply initial font size
        if hasattr(widget, "font_size"):
            font_scale = self.get_font_scale()
            widget.font_size = f"{dp(base_font_size) * font_scale}dp"

    def update_font_sizes(self, *args):
        font_scale = self.get_font_scale()

        for widget_info in self.dynamic_widgets:
            widget = widget_info["widget"]
            base_size = widget_info["base_size"]
            if hasattr(widget, "font_size"):
                widget.font_size = f"{dp(base_size) * font_scale}dp"

    def bind_font_scaling(self):
        Window.bind(on_resize=self.update_font_sizes)

    def unbind_font_scaling(self):
        Window.unbind(on_resize=self.update_font_sizes)

    def clear_font_scaling_widgets(self):
        self.dynamic_widgets.clear()


@dataclass
class BaseMethods(FontSizeMixin):
    def on_enter(self):
        self.bind_font_scaling()

    def on_leave(self):
        self.unbind_font_scaling()

    def load_score_content(self):
        score_content = read_scores_file()

        self.selected_city_short = map_selected_city_2short_name(self.selected_city)

        score_truck = (
            score_content.get(self.selected_city_short)
            .get("firetrucks")
            .get(self.selected_firetruck)
        )

        self.current_correct_answers = score_truck.get("current").get("correct_answers")
        self.current_tool_list = score_truck.get("current").get("tool_list")
        self.high = score_truck.get(self.get_scores_key())
        self.percentages = score_truck.get("percentages", [])
        # self.tool_amount = score_truck.get("tool_amount")

    def save_score_content(self):
        truck_content = {
            "current": {
                "correct_answers": self.current_correct_answers,
                "tool_list": self.current_tool_list,
            },
            self.get_scores_key(): self.high,
            # "percentages": ([] if self.percentages == None else self.percentages),
            "tool_amount": self.tool_amount,
        }

        scores_file_path = os.path.join(
            get_user_data_dir(),
            "scores.yaml",
        )

        score_content = read_scores_file()

        score_truck_content = score_content[self.selected_city_short]["firetrucks"][
            self.selected_firetruck
        ]

        score_truck_content.update(truck_content)

        score_content[self.selected_city_short]["firetrucks"][
            self.selected_firetruck
        ] = score_truck_content

        save_to_yaml(scores_file_path, score_content)

    def save_score_percentage(self):
        scores_file_path = os.path.join(
            get_user_data_dir(),
            "scores.yaml",
        )

        score_content = read_scores_file()

        score_content[self.selected_city_short]["firetrucks"][self.selected_firetruck][
            "percentages"
        ] = self.percentages

        save_to_yaml(scores_file_path, score_content)

    def update_score_labels(self):
        self.update_score_label()
        self.update_high_score_label()
        self.update_tool_number_label()
        self.update_percentage_label()

    def update_score_label(self):
        self.ids.score_label.text = str(self.game.score)

    def update_high_score_label(self):
        self.ids.high_score_label.text = f"Best: {str(self.high)}"

    def update_tool_number_label_ios(self):
        # Clear only existing label widgets, keep other widgets
        widgets_to_remove = []
        for widget in self.ids.firetruck_layout.children:
            if widget.text.startswith("⚒"):
                widgets_to_remove.append(widget)

        for widget in widgets_to_remove:
            self.ids.firetruck_layout.remove_widget(widget)

        font_scale = self.get_font_scale()

        lbl = Label(
            size_hint_y=1,
            text=f"⚒ {self.answered_tools} / {self.tool_amount}",
            font_name="DejaVuSans",
            font_size=f"{17 * font_scale}dp",
            halign="left",
            valign="middle",
        )
        # Bind text_size to the label's size for proper alignment
        lbl.bind(size=lambda instance, size: setattr(instance, "text_size", size))

        self.ids.firetruck_layout.add_widget(lbl)

        self.ids.tool_number_label.text = ""

    def update_tool_number_label(self):
        self.answered_tools = self.tool_amount - len(self.current_tool_list)

        if platform == "ios":
            self.update_tool_number_label_ios()

        else:
            self.ids.tool_number_label.text = (
                f"⚒ {self.answered_tools} / {self.tool_amount}"
            )
            self.ids.tool_number_label.font_name = (
                "DejaVuSans"  # or "Roboto" if available
            )

    def update_percentage_label(self):
        if self.tool_amount - len(self.current_tool_list) == 0:
            self.current_percentage = "-"

        else:
            self.current_percentage = round(
                (
                    self.current_correct_answers
                    / (self.tool_amount - len(self.current_tool_list))
                    * 100
                ),
                1,
            )

        self.ids.percentage_label.markup = True
        self.ids.percentage_label.text = (
            f"[color=00b300][size=65]✓[/size][/color] {self.current_percentage:.1f} %"
            if self.current_percentage != "-"
            else self.current_percentage
        )
        self.ids.percentage_label.font_name = "DejaVuSans"  # or "Roboto" if available

    def reset_score(self, *arg):
        self.game.score = 0
        self.update_score_labels()

    def increment_score(self):
        self.game.score += self.get_scores_value()
        self.update_score_label()

    def load_default_tool_list(self):
        (self.firetruck_rooms, self.default_tool_list) = get_ToolQuestion_instances(
            self.selected_firetruck, self.selected_city
        )
        self.tool_amount = len(self.default_tool_list)

    def get_current_tool_list(self):
        self.current_tool_list = self.get_truck_data("set", current=True)

    def reset_current_tool_list(self):
        # default_tool_list stores answered rooms in game_class instances
        # take sure classes are re-created
        self.load_default_tool_list()

        self.current_tool_list = [item.tool for item in self.default_tool_list]
        shuffle(self.current_tool_list)

        self.current_correct_answers = 0

    def check_tool_list(self):
        current = set(self.current_tool_list)
        # ToolQuestion is unhashable, so we extract tool names
        default = set([item.tool for item in self.default_tool_list])

        if current.issubset(default):
            return

        # Keep only items that are in both lists, preserving original order
        self.current_tool_list = [
            item for item in self.current_tool_list if item in default
        ]

    def hide_label(self, *args):
        self.ids.extra_time_label.opacity = 0

    def reset_progress_bar(self):
        self.ids.progress_bar_answer.max = (
            settings.FIRETRUCK_TRAINING_WITH_IMAGES_FEEDBACK_SEC - 0.3
        )
        self.ids.progress_bar_answer.value = 0

    def update_progress_bar(self):
        self.progress_bar.value = self.time_left

    def reset_timer(self):
        self.time_left = settings.FIRETRUCK_GAME_START_TIME_SEC

        self.ids.progress_bar.max = settings.FIRETRUCK_GAME_START_TIME_SEC

    def add_time(self):
        self.time_left = round(
            self.time_left + settings.FIRETRUCK_GAME_EXTRA_TIME_SEC, 1
        )

        # avoid that remaining time (add time) can exceed max progress bar
        if self.time_left > self.progress_bar.max:
            self.progress_bar.max = self.time_left

        self.ids.extra_time_label.text = f"+ {settings.FIRETRUCK_GAME_EXTRA_TIME_SEC} s"

        self.extra_time_label.opacity = 1

        Clock.schedule_once(
            self.hide_label,
            settings.FIRETRUCK_GAME_DISPLAY_EXTRA_TIME_SEC,
        )

    def update_timer(self, *args):
        self.update_progress_bar()

        if self.time_left > 0.0:
            self.time_left = round(
                self.time_left - settings.FIRETRUCK_GAME_INTERVAL_SEC, 1
            )

        else:
            self.end_game()
            pass

    def get_current_screen(self):
        app = App.get_running_app()
        return app.root.current

    def _screen_name(self):
        # Prefer the instance's own Screen.name if present
        if isinstance(self, Screen) and getattr(self, "name", None):
            return self.name

        # Fall back to the running app's ScreenManager current
        try:
            app = App.get_running_app()
            if app and app.root:
                return app.root.current
        except Exception:
            pass
        return None

    def get_scores_key(self):
        current_screen = self._screen_name()

        mapping = {
            "firetruck_training": "high_strike",
            "firetruck_training_with_images": "high_strike_image",
            "firetruck_game": "high_score",
        }
        try:
            return mapping[current_screen]
        except KeyError:
            raise NotImplementedError("scores.yaml key not defined!")

    def get_scores_value(self):
        current_screen = self._screen_name()

        mapping = {
            "firetruck_training": settings.FIRETRUCK_TRAINING_CORRECT_POINTS,
            "firetruck_training_with_images": settings.FIRETRUCK_TRAINING_CORRECT_POINTS,
            "firetruck_exam": settings.FIRETRUCK_TRAINING_CORRECT_POINTS,
            "firetruck_game": settings.FIRETRUCK_GAME_CORRECT_POINTS,
        }
        try:
            return mapping[current_screen]
        except KeyError:
            raise NotImplementedError("self.current_screen not defined!")

    def correct_answer(self):
        self.increment_score()

        self.game.answers_correct += 1

        # increment if all tool answers are correct
        if self.single_correct_answer:
            self.current_correct_answers += 1

        if self.game.score > self.high:
            self.high = self.game.score

            self.update_high_score_label()

        self.feedback_green = True

    def incorrect_answer(self):
        self.feedback_green = False

        Clock.schedule_once(self.reset_score, settings.FIRETRUCK_TRAINING_FEEDBACK_SEC)

    def color_layout(self, instance):
        float_layout = self.ids.firetruck_rooms_layout.children[
            0
        ]  # children is reversed

        # indicate if correct or incorrect answer
        # for single correct answer
        if self.single_correct_answer:
            # always identify and indicate the correct answer
            # for child in children:
            for child in float_layout.children:
                if isinstance(child, Button):
                    if child.text in self.current_tool_question.rooms:
                        child.background_color = (0, 1, 0, 1)  # green
            # if, indicate incorrect answer
            if instance.text not in self.current_tool_question.rooms:
                instance.background_color = (1, 0, 0, 1)  # red

        # for multiple correct answers
        else:
            # document given answers in class instance
            self.current_tool_question.room_answered.append(instance.text)

            if instance.text not in self.current_tool_question.rooms:
                # if, indicate incorrect and all correct answers and close
                instance.background_color = (1, 0, 0, 1)  # red
                # for child in children:
                for child in float_layout.children:
                    if isinstance(child, Button):
                        if child.text in self.current_tool_question.rooms:
                            child.background_color = (0, 1, 0, 1)  # green

            else:
                # answer in correct answers
                instance.background_color = (0, 0, 1, 1)  # blue

                if self.current_screen == "firetruck_training_with_images":
                    self.tool_label.text += "\n"
                    self.tool_label.text += strings.HINT_STR_MULTIPLE_ANSWERS
                else:
                    self.ids.tool_label.text += "\n"
                    self.ids.tool_label.text += strings.HINT_STR_MULTIPLE_ANSWERS

                return True

        return False  # pass

    def end_game(self, factor: int) -> None:
        add2running_score(
            city=self.selected_city,
            to_add=int(self.game.answers_correct * factor),
        )

        if not self.first_tool:
            message = TrainingEndText(
                answers_total=self.game.questions_len,
                answers_correct=self.game.answers_correct,
                factor=factor,
            ).TEXT

            info_popup = TextPopup(
                message=message,
                title=strings.TITLE_INFO_POPUP,
                size_hint=(0.6, 0.6),
            )
            info_popup.open()

    def go_back(self, *args) -> None:
        if self.current_screen in [
            "firetruck_browse",
            "firetruck_images",
        ]:
            change_screen_to("firetruck_menu")

        elif self.current_screen == "firetruck_training":
            self.end_game(factor=settings.FIRETRUCK_TRAINING_STRIKE_FACTOR)
            change_screen_to("firetruck_menu")

        elif self.current_screen == "firetruck_training_with_images":
            self.end_game(factor=settings.FIRETRUCK_TRAINING_STRIKE_IMAGE_FACTOR)
            change_screen_to("firetruck_menu")

        elif self.current_screen == "firetruck_game":
            self.end_game()

        elif self.current_screen in [
            "highscore_screen",
            "acknowledgement_screen",
            "firetruck_menu",
        ]:
            change_screen_to("start_menu")

        else:
            raise NotImplementedError("go_back() not implemented for this screen!")

    # TESTING
    def set_first_tool(self, tool_name: str):
        for idx, tool in enumerate(self.tool_questions):
            if tool.tool == tool_name:
                # move to end of list, so it is picked next
                self.tool_questions.append(self.tool_questions.pop(idx))
                return
