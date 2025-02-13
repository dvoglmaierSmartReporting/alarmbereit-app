class Settings:
    def __init__(self) -> None:
        # training
        self.FEEDBACK_TRAINING_SEC = 2.0
        # game
        self.INTERVAL_GAME_SEC = 0.1
        self.DISPLAY_EXTRA_TIME_LABEL_SEC = 2
        ## firetruck
        self.FIRETRUCK_START_TIME_SEC = 15.0
        self.FIRETRUCK_EXTRA_TIME_SEC = 10.0
        self.FIRETRUCK_FEEDBACK_GAME_SEC = 0.5
        self.FIRETRUCK_CORRECT_FOR_EXTRA_TIME = 5
        self.FIRETRUCK_CORRECT_POINTS = 100
        self.FIRETRUCK_STRIKE_POINTS = 1
        self.FIRETRUCK_STRIKE_FACTOR = 25
        ## competition
        self.COMPETITION_START_TIME_SEC = 90.0
        self.COMPETITION_EXTRA_TIME_SEC = 60.0
        self.COMPETITION_FEEDBACK_GAME_SEC = 1.5
        self.COMPETITION_CORRECT_FOR_EXTRA_TIME = 4
        self.COMPETITION_CORRECT_POINTS = 100


class Strings:
    def __init__(self) -> None:

        # Start_Menu mode names
        self.LABEL_STR_MODE = "Modus"
        self.LABEL_STR_QUESTIONS = "Inhalt"

        # Start_Menu button names
        self.BUTTON_STR_INFO = "Info"
        self.BUTTON_STR_SETTINGS = "Einst."
        self.BUTTON_STR_TRAINING = "Übung"
        self.BUTTON_STR_GAME = "Zeitdruck"
        self.BUTTON_STR_BROWSE = "Stöbern"
        self.BUTTON_STR_IMAGES = "Bilder\n(coming soon)"
        self.BUTTON_STR_FIRETRUCKS = "Fahrzeugkunde"
        self.BUTTON_STR_COMPETITIONS = "Bewerbsfragen"
        self.BUTTON_STR_STANDARDS = "Standardeinsätze\n(coming soon)"  # Standardeinsatz
        self.BUTTON_STR_YOUTH = "Jugend\n(coming soon)"  # Wissenstest/-spiel

        # settings screen
        self.SWITCH_STR_DEFAULT_CONTENT = "Standardinhalte"
        self.BUTTON_STR_SELECT_FILE = "Eigene Fahrzeuge laden"
        self.BUTTON_STR_CONFIRM_UPLOAD = "Bestätigen"
        self.TITLE_DIALOG_POPUP = "Datei auswählen"
        self.BUTTON_DIALOG_POPUP_CANCEL = "Abbrechen"
        self.BUTTON_DIALOG_POPUP_CONFIRM = "Auswählen"

        # competition training
        self.BUTTON_STR_SOLUTION = "Lösung"
        self.BUTTON_STR_RANDOM_QUESTION = "Zufällig"

        # browse screen
        self.BUTTON_STR_FILTER = "Filtern"

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
            "PumpeDürrnberg": "LFA",
        }


class Info_Screen_Text:
    def __init__(self) -> None:
        self.TEXT = """
        © 2025 Freiwillige Feuerwehr der Stadt Hallein

        Idee und Entwicklung: Dominik Voglmaier
        
        Support: d.voglmaier@feuerwehr-hallein.at
        """
