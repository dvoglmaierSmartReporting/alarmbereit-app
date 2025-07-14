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

        # login
        self.LABEL_STR_LOGIN = "meine Feuerwehr\nwählen"
        # self.BUTTON_STR_LOGIN = "Login"
        # self.LABEL_STR_CITY = "Freiwillige Feuerwehr"
        self.BUTTON_STR_STORE_SELECTION = "Speichern"

        # start_nenu
        self.LABEL_STR_QUESTIONS = "Mission"
        self.BUTTON_STR_ALL_CITIES = "Wähle deine\nFeuerwehr"
        self.BUTTON_STR_SCORE = "Highscore"
        self.BUTTON_STR_INFO = "Info"
        self.BUTTON_STR_ACKNOWLEDGEMENT = "Dank"
        self.BUTTON_STR_SETTINGS = "Einst."
        self.BUTTON_STR_TRAINING = "Übung"  # "Lernen" # "Erkunden"
        self.BUTTON_STR_TRAINING_NEW = (
            f"{self.BUTTON_STR_TRAINING} mit Bildern"
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

        # firetruck modes
        self.LABEL_STR_MODES = "Lernpfad"

        # firetruck training
        self.HINT_STR_MULTIPLE_ANSWERS = "Wo noch?"

        # competition state
        self.LABEL_STR_STATE = "Bundesland"

        # competition training
        self.BUTTON_STR_SOLUTION = "Lösung"
        self.BUTTON_STR_RANDOM_QUESTION = "Zufällig"

        # browse screen
        self.BUTTON_STR_FILTER = "Filtern"

        # popup
        self.TITLE_ERROR_POPUP = "Fehlermeldung"
        self.TITLE_INFO_POPUP = "Info"
        self.BUTTON_CLOSE_POPUP = "Schließen"


class Firetruck_TrainingText_AllTools:
    def __init__(self, tool_amount: int) -> None:
        self.TEXT = f"""

[b]Super![/b]

Du hast alle {tool_amount} Geräte des Fahrzeugs gelernt.

Die Geräte werden neu geladen und weiterhin zufällig gezogen."""


class Firetruck_TrainingText_HalfTools:
    def __init__(self, tool_amount: int) -> None:
        self.TEXT = f"""

[b]Bleib dran![/b]

Du hast bereits die Hälfte der {tool_amount} Geräte des Fahrzeugs gelernt."""


class Firetruck_GameEndText:
    def __init__(
        self,
        answers_total: int,
        answers_correct: int,
        score: int,
        is_new_highscore: bool,
    ) -> None:
        self.TEXT = f"""
[b]Spiel Ende![/b]

Du hast {answers_total} {self.is_plural(answers_total>1)} gespielt, davon {answers_correct} richtig zugeordnet. {self.add_text(score,is_new_highscore)}
"""

    def add_text(self, score: int, is_new_highscore: bool) -> str:
        if is_new_highscore:
            return f"""

Glückwunsch!
Du hast deinen persönlichen Highscore an diesem Fahrzeug verbessert.

Neuer Highscore: {score}"""
        return f"""

Punktestand: {score}"""

    def is_plural(self, is_plural: bool) -> str:
        if is_plural:
            return "Geräte"
        return "Gerät"


class Competition_GameEndText:
    def __init__(
        self,
        answers_total: int,
        answers_correct: int,
        score: int,
        is_new_highscore: bool,
    ) -> None:
        self.TEXT = f"""
[b]Spiel Ende![/b]

Du hast {answers_total} {self.is_plural(answers_total > 1)} gespielt, davon {answers_correct} richtig zugeordnet.

{self.is_new_highscore(score, is_new_highscore)}
"""

    def is_new_highscore(self, score: int, is_new_highscore: bool) -> str:
        if is_new_highscore:
            return f"""[b]Glückwunsch![/b]
Du hast deinen persönlichen Highscore in diesem Bewerb verbessert.

Neuer Highscore: {score}"""
        return f"\n\nPunktestand: {score}"

    def is_plural(self, is_plural: bool) -> str:
        if is_plural:
            return "Fragen"
        return "Frage"


class Info_Text:
    def __init__(self) -> None:
        self.TEXT = """Meine Feuerwehr fehlt noch!

Standorte können kostenlos hinzugefügt
werden. Schicke deine Anfrage an
[b]d.voglmaier@feuerwehr-hallein.at[/b]"""


class About_Text:
    def __init__(self) -> None:
        self.TEXT = """
© 2025 Freiwillige Feuerwehr der Stadt Hallein

Idee und Entwicklung: Dominik Voglmaier

Support: d.voglmaier@feuerwehr-hallein.at

Version: 2.5.1
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
[b]Rudolf Wessely[/b]



[b]WERDE SELBST AKTIVER UNTERSTÜTZER DIESES PROJEKTS[/b]

• Bewirb die FahrzeugkundeApp in deiner Feuerwehr

• Schreibe eine positive Bewertung im App Store

• Unterstütze die Entwicklung mit einer freiwilligen Spende:
  Dominik Voglmaier
  DE26 1203 0000 1055 3765 43
"""
