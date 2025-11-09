from kivy.uix.screenmanager import Screen

from tabulate import tabulate

from helper.settings import Settings
from helper.strings import Strings
from helper.file_handling import (
    get_selected_city_state,
    map_selected_city_2long_name,
    read_scores_file,
    map_selected_city_2short_name,
)
from helper.custom_types import *

from screens.screen_base import BaseMethods


strings = Strings()
settings = Settings()


# TODO:
# enable and display button again, in
#  - .kv file + ids
#  - .py __init__
# save PNG in tempfile instead of file
# configure FileProvider xml
#  - .xml file with permissions
#  - in buildozer file
# open default email app and prepare email

# from kivy.utils import platform
# from kivy.clock import Clock
# import os


class Highscore(Screen, BaseMethods):
    def on_pre_enter(self):
        self.current_screen = self.get_current_screen()

        self.update_city_label()

        self.prepare_table()

        self.update_info_text()

    def update_city_label(self):
        self.selected_city, _ = get_selected_city_state()
        self.selected_city = map_selected_city_2long_name(self.selected_city)

        if self.selected_city == "Hallein":
            selected_city_displayed = "Stadt Hallein"
        else:
            selected_city_displayed = self.selected_city
        self.ids.city_label.text = selected_city_displayed

    def update_info_text(self):
        info_text = self.create_scores_text() + "\n\n\n\n"

        self.ids.score_text_label.text = info_text

    def prepare_table(self):
        city = map_selected_city_2short_name(self.selected_city)
        self.third_column = True if city == "Hallein" else False

        self.running_score = read_scores_file().get(city, {}).get("running_score")
        self.truck_scores = read_scores_file().get(city, {}).get("firetrucks")

        self.empty_line = ["", "", ""] + ([""] if self.third_column else [])
        self.em_dash1column = ["—" * 13, "", ""] + ([""] if self.third_column else [])
        self.em_dash2column = ["—" * 13, "—" * 10, ""] + (
            [""] if self.third_column else []
        )
        self.em_dash3column = ["—" * 13, "—" * 10, "—" * 7] + (
            [""] if self.third_column else []
        )
        self.em_dash4column = ["—" * 13, "—" * 10, "—" * 7] + (
            ["—" * 9] if self.third_column else []
        )

    def create_scores_text(self) -> str:
        table = list()

        # print running score table
        for row in self.build_running_score_table():
            table.append(row)
        table.append(self.empty_line)

        # print highscore table
        for row in self.build_highscore_table():
            table.append(row)
        table.append(self.empty_line)
        table.append(self.empty_line)

        # print percentage table
        for row in self.build_percentage_table():
            table.append(row)

        colalign = ["right", "right", "right"] + (
            ["right"] if self.third_column else []
        )

        return tabulate(
            table,
            tablefmt="rounded_outline",
            colalign=colalign,
        )

    def separate(self, string: str) -> str:
        # every 3rd character from the end, insert a underscore
        reversed_string = string[::-1]
        parts = [reversed_string[i : i + 3] for i in range(0, len(reversed_string), 3)]
        return "_".join(parts)[::-1]

    def build_highscore_table(self) -> list[list[str]]:
        factor = settings.FIRETRUCK_TRAINING_STRIKE_FACTOR
        factor_image = settings.FIRETRUCK_TRAINING_STRIKE_IMAGE_FACTOR

        rows = list()
        total_score = 0
        total_strike = 0
        total_strike_image = 0

        for truck, data in self.truck_scores.items():
            score = data.get("high_score", 0)
            total_score += score

            strike = data.get("high_strike", 0)
            total_strike += strike

            if truck == "Leiter":
                strike_image = data.get("high_strike_image", 0)
                total_strike_image += strike_image
                strike_image = str(strike_image)
            else:
                strike_image = ""

            rows.append(
                [truck, self.separate(str(score)), str(strike)]
                + ([strike_image] if self.third_column else [])
            )

        factor_line = [
            strings.ROW_FACTOR,
            "-",
            f"x {factor}",
        ] + ([f"x {factor_image}"] if self.third_column else [])

        total = [
            strings.ROW_TOTAL,
            self.separate(
                str(
                    total_score
                    + (total_strike * factor)
                    + (total_strike_image * factor_image)
                )
            ),
            "",
        ] + ([""] if self.third_column else [])

        header_row = [
            strings.COLUMN_FIRETRUCK,
            strings.COLUMN_QUIZ,
            strings.COLUMN_TRAINING,
        ] + ([strings.COLUMN_TRAINING_WITH_IMAGES] if self.third_column else [])

        title_row = [strings.ROW_HIGHSCORES, "", ""] + (
            [""] if self.third_column else []
        )

        table = list()
        table.append(self.em_dash1column)
        table.append(title_row)
        table.append(self.em_dash1column)
        table.append(header_row)
        table.append(self.empty_line)
        for row in rows:
            table.append(row)
        table.append(self.empty_line)
        table.append(factor_line)
        table.append(self.em_dash4column)
        table.append(total)

        return table

    def build_running_score_table(self) -> list[list[str]]:
        running_score_line = [
            strings.ROW_RUNNING_SCORE,
            self.separate(str(self.running_score)),
            "",
        ]

        table = list()
        table.append(self.em_dash1column)
        table.append(running_score_line)
        table.append(self.em_dash1column)

        return table

    def build_percentage_table(self) -> list[list[str]]:
        rows = list()
        total_last_percentage = 0
        total_best_percentage = 0

        for truck, data in self.truck_scores.items():
            percentages = data.get("percentages", [])
            if len(percentages) == 0:
                last_percentage = None
                best_percentage = None
            else:
                last_percentage = percentages[-1]
                total_last_percentage += last_percentage

                best_percentage = max(percentages)
                total_best_percentage += best_percentage

            rows.append(
                [truck]
                + ([f"{last_percentage:.1f} %"] if last_percentage else ["- %"])
                + ([f"{best_percentage:.1f} %"] if best_percentage else ["- %"])
                + ([""] if self.third_column else [])
            )

        average_line = [
            strings.ROW_AVERAGE,
            f"{total_last_percentage/len(self.truck_scores) if len(self.truck_scores) > 0 else 0:.1f} %",
            f"{total_best_percentage/len(self.truck_scores) if len(self.truck_scores) > 0 else 0:.1f} %",
        ] + ([""] if self.third_column else [])

        header_row = [
            strings.COLUMN_FIRETRUCK,
            strings.COLUMN_LAST_SET,
            strings.COLUMN_BEST_SET,
        ] + ([""] if self.third_column else [])

        title_row = [strings.ROW_PROCENTAGE, "", ""] + (
            [""] if self.third_column else []
        )

        table = list()
        table.append(self.em_dash1column)
        table.append(title_row)
        table.append(self.em_dash1column)
        table.append(header_row)
        table.append(self.empty_line)
        for row in rows:
            table.append(row)
        table.append(self.empty_line)
        table.append(self.em_dash3column)
        table.append(average_line)

        return table

    # Not used currently

    # idea: in internal competitions, use button to create image of highscore screen
    # to be able to share the whole values
    #
    # This won't be needed, if online highscore is implemented

    # def capture_scrollview(self):
    #     content = self.ids.score_text_label  # Layout inside ScrollView
    #     filename = os.path.join(self.get_save_path(), "scrollview_capture.png")

    #     # Schedule to wait one frame, so layout has time to render
    #     def do_capture(dt):
    #         content.export_to_png(filename)
    #         print(f"Captured ScrollView content to {filename}")

    #     Clock.schedule_once(do_capture, 0.1)

    # def get_save_path(self):
    #     if platform == "android":
    #         from android.storage import app_storage_path

    #         return app_storage_path()
    #     else:
    #         return os.path.expanduser("~")
