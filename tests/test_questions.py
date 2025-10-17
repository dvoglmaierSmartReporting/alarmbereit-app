import sys
import os

# Allows simulated app to load packages
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../app")))


import pytest
import os
import shutil

from unittest.mock import patch

from kivy.app import App
from kivy.base import EventLoop
from kivy.clock import Clock
from kivy.uix.screenmanager import ScreenManager
from kivy.config import Config

from app.main import FeuerwehrApp
from app.screens.firetruck_training import Firetruck_Training
from app.screens.screen_base import BaseMethods
from app.helper.file_handling import (
    load_total_firetruck_storage,
)
from app.helper.settings import Settings

settings = Settings()


@pytest.fixture(scope="module")
def app():
    EventLoop.ensure_window()
    # Instantiate your Kivy app
    application = FeuerwehrApp()
    root_widget = application.build()
    application.root = root_widget
    # Register as the globally running app
    App._running_app = application
    yield application

    # Clean up after tests
    shutil.rmtree(application.user_data_dir, ignore_errors=True)
    App._running_app = None
    application.root = None


def test_root_is_screen_manager(app):
    assert app.root is not None, "app.root is None — build() likely failed"
    assert isinstance(
        app.root, ScreenManager
    ), f"Expected ScreenManager, got {type(app.root)}"


def test_user_data_dir_available(app):
    assert app.user_data_dir is not None


### HELPER FUNCTIONS ###


def set_graphics_config(to_update: dict) -> None:
    if not Config.has_section("graphics"):
        Config.add_section("graphics")
    for key, value in to_update.items():
        Config.set("graphics", key, value)


def set_graphics_defaults() -> None:
    set_graphics_config({"width": "600", "height": "1000", "min_state_time": ".035"})


def prepare_config_for_tests(city_name: str, mode: str):
    Config._sections.clear()
    Config.setdefaults("content", {"city": city_name, "state": "Salzburg"})
    Config.setdefaults("firetruck", {"mode": mode})
    set_graphics_defaults()


#### FIRETRUCK TRAINING ####

cities = ["Hallein", "Bad Dürrnberg", "Altenmarkt a.d. Alz"]


@pytest.mark.parametrize("city_name", cities)
def test_firetruck_training__select_firetruck(city_name):
    # need to be loaded in test, because function is
    # using get_running_app() methode, which is simulated above
    firetrucks = list(load_total_firetruck_storage(city_name).keys())

    prepare_config_for_tests(city_name, "Übung")

    settings.FIRETRUCK_TRAINING_FEEDBACK_SEC = 0.3

    class Instance:
        def __init__(self, text, background_color=(0, 0, 0, 0)):
            self.text = text
            self.background_color = background_color

    # Patch Clock.schedule_once to call the function immediately
    with patch("kivy.clock.Clock.schedule_once") as mock_schedule:
        mock_schedule.side_effect = lambda func, timeout: func(0.016)

        for firetruck in firetrucks:
            Config.set("firetruck", "selected_firetruck", firetruck)

            screen = Firetruck_Training(name="firetruck_training")
            try:
                screen.on_pre_enter()
                print(f"✅ Loaded firetruck_training '{firetruck}'")

                i = 0
                while True:
                    instance = Instance("Mannschaft")
                    screen.on_answer(instance)
                    if instance.background_color == (0, 0, 1, 1):
                        instance = Instance("G3")
                        screen.on_answer(instance)
                    print(f"Loaded successfully tool {i+1}: {screen.tool_label.text}")

                    i += 1

                    if i >= 200:
                        break

            except Exception as e:
                pytest.fail(f"❌ Failed to load firetruck_training '{firetruck}': {e}")
