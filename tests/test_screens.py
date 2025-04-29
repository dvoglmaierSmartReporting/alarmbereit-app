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

from app.main import FeuerwehrApp
from app.screens.competition_menu import Bewerb_Menu
from app.screens.competition_training import Bewerb_Training
from app.screens.competition_game import Bewerb_Game
from app.screens.firetruck_menu import Fahrzeugkunde_Menu
from app.screens.firetruck_training import Fahrzeugkunde_Training
from app.screens.firetruck_game import Fahrzeugkunde_Game
from app.helper.file_handling import (
    load_total_competition_questions,
    load_total_firetruck_storage,
)


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

    for screen_name in screen_names:
        screen_manager.current = screen_name

        def check(dt):
            screen = screen_manager.get_screen(screen_name)
            assert screen is not None, f"Screen '{screen_name}' not found"
            assert screen.name == screen_name

        Clock.schedule_once(check, 0)
        EventLoop.idle()


#### COMPETITION MENU ####


@pytest.mark.parametrize("mode", ["Übung", "Zeitdruck"])
def test_competition_menu__select_mode(mode):
    screen = Bewerb_Menu(name="bewerb_menu")
    try:
        screen.mode_label = mode
        print(f"competition_menu loaded successfully for mode {mode}.")
    except Exception as e:
        pytest.fail(f"Mode ('{mode}') raised an exception: {e}")


#### FIRETRUCK MENU ####


@pytest.mark.parametrize("mode", ["Übung", "Zeitdruck"])
def test_firetruck_menu__select_mode(mode):
    screen = Fahrzeugkunde_Menu(name="firetruck_menu")
    try:
        screen.mode_label = mode
        print(f"firetruck_menu loaded successfully for mode {mode}.")
    except Exception as e:
        pytest.fail(f"Mode ('{mode}') raised an exception: {e}")


#### COMPETITION TRAINING ####

competitions = list(load_total_competition_questions().keys())


@pytest.mark.parametrize("competition_name", competitions)
def test_competition_training__select_competition(competition_name):
    screen = Bewerb_Training(name="bewerb_training")
    try:
        screen.select_competition(competition_name)
        screen.play()
        print(
            f"competition_training loaded successfully for competition {competition_name}."
        )
    except Exception as e:
        pytest.fail(
            f"select_competition('{competition_name}') raised an exception: {e}"
        )


def test_competition_training__select_invalid_competition__should_fail():
    screen = Bewerb_Training(name="bewerb_training")
    invalid_competition = "Blub - not exists"
    with pytest.raises(Exception):
        screen.select_competition(invalid_competition)
        screen.play()


#### COMPETITION GAME ####


@pytest.mark.parametrize("competition_name", competitions)
def test_competition_game__select_competition(competition_name):
    screen = Bewerb_Game(name="bewerb_game")
    try:
        screen.select_competition(competition_name)
        screen.play()
        print(
            f"competition_game loaded successfully for competition {competition_name}."
        )
    except Exception as e:
        pytest.fail(
            f"select_competition('{competition_name}') raised an exception: {e}"
        )


def test_competition_game__select_invalid_competition__should_fail():
    screen = Bewerb_Game(name="bewerb_game")
    invalid_competition = "Blub - not exists"
    with pytest.raises(Exception):
        screen.select_competition(invalid_competition)
        screen.play()


#### FIRETRUCK TRAINING ####


def test_firetruck_training__select_firetruck():
    # need to be loaded in test, because
    # fct is using get_running_app() methode, which is simulated above
    firetrucks = list(load_total_firetruck_storage().keys())

    for firetruck_name in firetrucks:
        screen = Fahrzeugkunde_Training(name="fahrzeugkunde_training")
        try:
            screen.select_firetruck(firetruck_name)
            screen.play()
            print(f"✅ Loaded firetruck_training '{firetruck_name}'")
        except Exception as e:
            pytest.fail(f"❌ Failed to load firetruck_training '{firetruck_name}': {e}")


def test_firetruck_training__select_invalid_firetruck__should_fail():
    screen = Fahrzeugkunde_Training(name="fahrzeugkunde_training")
    invalid_firetruck = "Tank300"
    with pytest.raises(Exception):
        screen.select_firetruck(invalid_firetruck)
        screen.play()


#### FIRETRUCK GAME ####


def test_firetruck_game__select_firetruck():
    # need to be loaded in test, because
    # fct is using get_running_app() methode, which is simulated above
    firetrucks = list(load_total_firetruck_storage().keys())

    for firetruck_name in firetrucks:
        screen = Fahrzeugkunde_Game(name="fahrzeugkunde_game")
        try:
            screen.select_firetruck(firetruck_name)
            screen.play()
            print(f"✅ Loaded firetruck_game '{firetruck_name}'")
        except Exception as e:
            pytest.fail(f"❌ Failed to load firetruck_game '{firetruck_name}': {e}")


def test_firetruck_game__select_invalid_firetruck__should_fail():
    screen = Fahrzeugkunde_Game(name="fahrzeugkunde_game")
    invalid_firetruck = "Tank300"
    with pytest.raises(Exception):
        screen.select_firetruck(invalid_firetruck)
        screen.play()
