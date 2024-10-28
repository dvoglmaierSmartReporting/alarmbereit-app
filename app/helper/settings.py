class Settings:
    def __init__(self) -> None:
        # training
        self.FEEDBACK_TRAINING_SEC = 2.0
        # game
        self.FEEDBACK_GAME_SEC = 0.5
        self.INTERVAL_GAME_SEC = 0.1
        self.START_TIME_GAME_SEC = 15.0

        self.EXTRA_TIME = 10.0
        self.CORRECT_FOR_EXTRA_TIME = 5
        self.DISPLAY_EXTRA_TIME_LABEL = 2

        self.MAX_EXTRA_TIME_SEC = 5.0
        self.EXTRA_TIME_REDUCTION_SEC = 0.5
        # self.RENEW_EXTRA_TIME_INT = 25
        self.RENEW_EXTRA_TIME_INT = 15


class Strings:
    def __init__(self) -> None:

        # Start_Menu mode names
        self.LABEL_STR_MODE = "Modus"
        self.LABEL_STR_QUESTIONS = "Inhalt"

        # Start_Menu button names
        self.BUTTON_STR_TRAINING = "Übung"
        self.BUTTON_STR_GAME = "Zeitdruck"
        self.BUTTON_STR_BROWSE = "Stöbern"
        self.BUTTON_STR_IMAGES = "Bilder\n(coming soon)"
        self.BUTTON_STR_FIRETRUCKS = "Fahrzeugkunde"
        self.BUTTON_STR_COMPETITIONS = "Bewerbsfragen"
        self.BUTTON_STR_STANDARDS = "Standardeinsätze\n(coming soon)"  # Standardeinsatz

        # competition training
        self.BUTTON_STR_SOLUTION = "Lösung"
        self.BUTTON_STR_RANDOM_QUESTION = "Zufällig"

        self.trucks = {
            "TestTruck": "testing",
            "RüstLösch": "RLFA 2000",
            "Tank1": "TLF-A 3000",
            "Leiter": "DLA(K) 23-12",
            "Tank2": "TLF-A 4000",
            "Voraus": "VRFA-Tunnel",
            "Voraus+Ölanh.": "VRFA-Tunnel",
            "Pumpe": "LFA",
            "Rüst": "SRFK-A",
            "TankDürrnberg": "TLFA 3000",
        }
