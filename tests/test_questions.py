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
        print(f"Loaded successfully question {screen.current_question.question_id}")

        while screen.next_question_button.disabled == False:
            screen.next_question()
            print(f"Loaded successfully question {screen.current_question.question_id}")
            screen.reveal_answer()

    except Exception as e:
        pytest.fail(
            f"select_competition('{competition_name}') raised an exception: {e}"
        )
