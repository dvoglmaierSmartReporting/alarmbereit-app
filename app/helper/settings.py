class Settings:
    def __init__(self) -> None:
        # training
        self.FEEDBACK_TRAINING_SEC = 2
        # game
        self.FEEDBACK_GAME_SEC = 0.5
        self.INTERVAL_GAME_SEC = 0.1
        self.START_TIME_GAME_SEC = 15
        self.PUNISHMENT_GAME_SEC = 1  # to be replaced by extra_time
        self.REWARD_GAME_SEC = 4  # to be replaced by extra_time
        self.MAX_EXTRA_TIME_SEC = 5
        self.EXTRA_TIME_REDUCTION_SEC = 0.5

        # 15      +  5 + 4.5 + 4 + ... = 42.5
        # 15 - 8  +  4 + 3.5 + 3 + ... = 25.0
        # self.RENEW_EXTRA_TIME_INT = 25
        self.RENEW_EXTRA_TIME_INT = 10


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
