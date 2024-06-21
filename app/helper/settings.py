class Settings:
    def __init__(self) -> None:
        # training
        self.FEEDBACK_TRAINING_SEC = round(2.0, 1)
        # game
        self.FEEDBACK_GAME_SEC = round(0.5, 1)
        self.INTERVAL_GAME_SEC = round(0.1, 1)
        self.START_TIME_GAME_SEC = round(1500.0, 1)
        self.PUNISHMENT_GAME_SEC = round(1.0, 1)
        self.REWARD_GAME_SEC = round(4.0, 1)


class Strings:
    def __init__(self) -> None:

        # Start_Menu mode names
        self.LABEL_STR_MODE = "Modus"
        self.LABEL_STR_QUESTIONS = "Inhalt"

        # Start_Menu button names
        self.BUTTON_STR_TRAINING = "Übung"
        self.BUTTON_STR_GAME = "Zeitdruck"
        self.BUTTON_STR_BROWSE = "Stöbern"
        self.BUTTON_STR_IMAGES = "Bilder"
        self.BUTTON_STR_FIRETRUCKS = "Fahrzeugkunde"
        self.BUTTON_STR_COMPETITIONS = "Bewerbsfragen"
        self.BUTTON_STR_STANDARDS = "Standard (coming soon)"  # Standardeinsatz

        # competition training
        self.BUTTON_STR_SOLUTION = "Lösung"
        self.BUTTON_STR_RANDOM_QUESTION = "Zufällig"
