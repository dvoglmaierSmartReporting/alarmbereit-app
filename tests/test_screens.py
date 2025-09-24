import sys
import os

# Allows simulated app to load packages
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../app")))


import pytest
import os
import shutil

from kivy.app import App
from kivy.base import EventLoop
from kivy.clock import Clock
from kivy.uix.screenmanager import ScreenManager
from kivy.config import Config

from app.main import FeuerwehrApp
from app.screens.firetruck_menu import Firetruck_Menu
from app.screens.firetruck_training import Firetruck_Training
from app.screens.firetruck_game import Firetruck_Game
from app.helper.file_handling import load_total_firetruck_storage


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


#### ALL SCREENS ####


def test_all_screens_load(app):
    screen_manager = app.root
    screen_names = screen_manager.screen_names

    Config._sections.clear()
    Config.setdefaults("content", {"city": "Hallein", "state": "Salzburg"})
    Config.setdefaults("graphics", {"width": "600", "height": "1000"})
    Config.setdefaults("graphics", {"min_state_time": ".035"})

    for screen_name in screen_names:
        screen_manager.current = screen_name

        def check(dt):
            screen = screen_manager.get_screen(screen_name)
            assert screen is not None, f"Screen '{screen_name}' not found"
            assert screen.name == screen_name

        Clock.schedule_once(check, 0)
        EventLoop.idle()


### FIRETRUCK TRAINING ####

cities = ["Hallein", "Bad Dürrnberg", "Altenmarkt a.d. Alz"]


@pytest.mark.parametrize("city_name", cities)
def test_firetruck_training__select_firetruck(city_name):
    # need to be loaded in test, because function is
    # using get_running_app() methode, which is simulated above
    firetrucks = list(load_total_firetruck_storage(city_name).keys())

    for firetruck_name in firetrucks:
        screen = Firetruck_Training(name="firetruck_training")
        try:
            screen.select_city(city_name)
            screen.select_firetruck(firetruck_name)
            screen.play()
            print(f"✅ Loaded firetruck_training '{firetruck_name}'")
        except Exception as e:
            pytest.fail(f"❌ Failed to load firetruck_training '{firetruck_name}': {e}")


@pytest.mark.parametrize("city_name", cities)
def test_firetruck_training__select_invalid_firetruck__should_fail(city_name):
    screen = Firetruck_Training(name="firetruck_training")
    invalid_firetruck = "Tank300"
    with pytest.raises(Exception):
        screen.select_city(city_name)
        screen.select_firetruck(invalid_firetruck)
        screen.play()


#### FIRETRUCK GAME ####


@pytest.mark.parametrize("city_name", cities)
def test_firetruck_game__select_firetruck(city_name):
    # need to be loaded in test, because function is
    # using get_running_app() methode, which is simulated above
    firetrucks = list(load_total_firetruck_storage(city_name).keys())

    for firetruck_name in firetrucks:
        screen = Firetruck_Game(name="firetruck_game")
        try:
            screen.select_city(city_name)
            screen.select_firetruck(firetruck_name)
            screen.play()
            print(f"✅ Loaded firetruck_game '{firetruck_name}'")
        except Exception as e:
            pytest.fail(f"❌ Failed to load firetruck_game '{firetruck_name}': {e}")


@pytest.mark.parametrize("city_name", cities)
def test_firetruck_game__select_invalid_firetruck__should_fail(city_name):
    screen = Firetruck_Game(name="firetruck_game")
    invalid_firetruck = "Tank300"
    with pytest.raises(Exception):
        screen.select_city(city_name)
        screen.select_firetruck(invalid_firetruck)
        screen.play()
