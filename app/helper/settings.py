class Settings:
    def __init__(self) -> None:
        ## firetruck
        self.FIRETRUCK_TRAINING_FEEDBACK_SEC = 2.0
        self.FIRETRUCK_TRAINING_NEW_FEEDBACK_SEC = 2.5
        self.FIRETRUCK_TRAINING_CORRECT_POINTS = 1
        self.FIRETRUCK_TRAINING_STRIKE_FACTOR = 50
        self.FIRETRUCK_GAME_INTERVAL_SEC = 0.1
        self.FIRETRUCK_GAME_DISPLAY_EXTRA_TIME_SEC = 2
        self.FIRETRUCK_GAME_START_TIME_SEC = 15.0
        self.FIRETRUCK_GAME_EXTRA_TIME_SEC = 10.0
        self.FIRETRUCK_GAME_FEEDBACK_SEC = 0.5
        self.FIRETRUCK_GAME_CORRECT_FOR_EXTRA_TIME = 5
        self.FIRETRUCK_GAME_CORRECT_POINTS = 100
        ## competition
        self.COMPETITION_GAME_INTERVAL_SEC = 0.1
        self.COMPETITION_GAME_DISPLAY_EXTRA_TIME_SEC = 2
        self.COMPETITION_GAME_START_TIME_SEC = 90.0
        self.COMPETITION_GAME_EXTRA_TIME_SEC = 60.0
        self.COMPETITION_GAME_FEEDBACK_SEC = 1.5
        self.COMPETITION_GAME_CORRECT_FOR_EXTRA_TIME = 4
        self.COMPETITION_GAME_CORRECT_POINTS = 100


class Strings:
    def __init__(self) -> None:

        # Start_Menu mode names
        self.LABEL_STR_QUESTIONS = "Mission"
        self.LABEL_STR_MODE = "Lernpfad"

        # Start_Menu button names
        self.BUTTON_STR_INFO = "Info"
        self.BUTTON_STR_ACKNOWLEDGEMENT = "Dank"
        self.BUTTON_STR_SETTINGS = "Einst."
        self.BUTTON_STR_TRAINING = "Übung"  # "Lernen" # "Erkunden"
        self.BUTTON_STR_TRAINING_NEW = (
            f"{self.BUTTON_STR_TRAINING} mit Bildern\n(bald verfügbar)"
        )
        self.BUTTON_STR_GAME = "Zeitdruck"  # "Herausfordern" # "Testen" # "Challengen"
        self.BUTTON_STR_BROWSE = "Stöbern"
        self.BUTTON_STR_IMAGES = "Bilder"
        self.BUTTON_STR_EXAM = "Leistungsprüfung"
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

        # firetruck login
        self.LABEL_STR_LOGIN = "Login"
        self.BUTTON_STR_LOGIN = "Login"
        self.LABEL_STR_DEPARTMENT = "Freiwillige Feuerwehr"

        # firetruck modes
        self.LABEL_STR_MODES = "Inhalte"

        # firetruck training
        self.HINT_STR_MULTIPLE_ANSWERS = "Wo noch?"

        # competition country
        self.LABEL_STR_COUNTRY = "Bundesland"

        # competition training
        self.BUTTON_STR_SOLUTION = "Lösung"
        self.BUTTON_STR_RANDOM_QUESTION = "Zufällig"

        # browse screen
        self.BUTTON_STR_FILTER = "Filtern"

        # error popup
        self.TITLE_ERROR_POPUP = "Fehlermeldung"
        self.BUTTON_CLOSE_POPUP = "Schließen"

        # TODO: move this to firetruck.yaml into truck key-value pair
        # in screen, read from firetruck.yaml
        self.trucks_hallein = {
            "TestTruck": "testing",
            "RüstLösch": "RLFA 2000",
            "Tank1": "TLF-A 3000",
            "BDLP-Tank1": "TLF-A 3000",
            "Leiter": "DLA(K) 23-12",
            "Tank2": "TLF-A 4000",
            "Voraus": "VRFA-Tunnel",
            "Voraus+Ölanh.": "VRFA-Tunnel",
            "Pumpe": "LFA",
            "Rüst": "SRFK-A",
            "TankDürrnberg": "TLF-A 3000",
            "PumpeDürrnberg": "LFA",
        }


class About_Text:
    def __init__(self) -> None:
        self.TEXT = """
© 2025 Freiwillige Feuerwehr der Stadt Hallein

Idee und Entwicklung: Dominik Voglmaier

Support: d.voglmaier@feuerwehr-hallein.at

"""


class Acknowledgements_Text:
    def __init__(self) -> None:
        self.TEXT = """
Herzlichen Dank an alle Unterstützerinnen und Unterstützer dieses Projekts!

• Für hilfreiche Diskussionen und Finanzierung:
[b]OFK Sebastian Wass[/b]

• Für ihren Einsatz als System-Tester der ersten Stunde:
[b]Kilian Brüderl[/b]
[b]Martin Reisaus[/b]
[b]Thomas Herbst[/b]

• Für die tatkräftige Unterstützung bei der Erstellung der Beladelisten:
[b]Bereitschaft 1[/b]
[b]Dienstführer[/b]

• Für konstruktives Feedback und intensive Belastungstests der Beta-Version:
[b]Bereitschaft 5[/b]

• Danke an alle Fehler-Finder:
[b]Manuel Promock[/b]
[b]Michael Nocker[/b]
[b]Julian Marx[/b]
[b]Jürgen Jung (4x)[/b]
"""
