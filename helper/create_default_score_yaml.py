import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# from app.screens.screen_base import BaseMethods
from app.helper.functions import get_ToolQuestion_instances


class Helper:
    def __init__(self):
        self.selected_city = "Hallein"
        self.selected_firetruck = "Kommando"

        (self.firetruck_rooms, self.default_tool_list) = get_ToolQuestion_instances(
            self.selected_firetruck, self.selected_city
        )
