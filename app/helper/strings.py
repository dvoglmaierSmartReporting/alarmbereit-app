from helper.settings import Settings

settings = Settings()


class Strings:
    def __init__(self) -> None:

        # login
        self.LABEL_STR_LOGIN = "Wähle deine\nFeuerwehr"
        # self.BUTTON_STR_LOGIN = "Login"
        # self.LABEL_STR_CITY = "Freiwillige Feuerwehr"
        self.BUTTON_STR_STORE_SELECTION = "Speichern"

        # start_nenu
        self.LABEL_STR_QUESTIONS = "Mission"
        self.BUTTON_STR_ALL_CITIES = "Wähle deine\nFeuerwehr"
        self.BUTTON_STR_SCORE = "Statistiken"
        self.BUTTON_STR_INFO = "Info"
        self.BUTTON_STR_ACKNOWLEDGEMENT = "Dank"
        self.BUTTON_STR_SETTINGS = "Einst."
        self.BUTTON_STR_TRAINING = "Lernmodus"  # "Übung"  # "Lernen" # "Erkunden"
        self.BUTTON_STR_TRAINING_WITH_IMAGES = (
            "Bilder"  # f"{self.BUTTON_STR_TRAINING} mit Bildern"
        )
        self.BUTTON_STR_GAME = (
            "Quiz starten"  #  "Zeitdruck"  # "Herausfordern" # "Challengen"
        )
        self.BUTTON_STR_BROWSE = "Stöbern"
        self.BUTTON_STR_IMAGES = "Bilder (coming soon)"
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

        # highscore
        self.BUTTON_STR_SHARE = "Highscore via\nEmail senden"
        self.TEXT_STRIKE_CALCULATION = f"([i]Punkte aus '{self.BUTTON_STR_TRAINING}' werden mit\nFaktor {settings.FIRETRUCK_TRAINING_STRIKE_FACTOR} multipliziert[/i])"
        self.TEXT_STRIKE_IMAGE_CALCULATION = f"([i]Punkte aus '{self.BUTTON_STR_TRAINING_WITH_IMAGES}' werden mit\nFaktor {settings.FIRETRUCK_TRAINING_STRIKE_IMAGE_FACTOR} multipliziert[/i])"
        self.TEXT_SUM = "Summe"
        self.TEXT_POINTS = "Punkte"
        self.TEXT_TOTAL_POINTS = "Gesamtpunktzahl"
        self.COLUMN_FIRETRUCK = "FAHRZEUG"
        self.COLUMN_QUIZ = "QUIZ"
        self.COLUMN_TRAINING = "LERNMODUS"
        self.COLUMN_TRAINING_WITH_IMAGES = "BILDER"
        self.ROW_FACTOR = "FAKTOR"
        self.ROW_TOTAL = "GESAMT"
        self.ROW_RUNNING_SCORE = "RUNNING SCORE"
        self.ROW_HIGHSCORES = "HIGHSCORES"
        self.ROW_PROCENTAGE = "PROZENT"
        self.COLUMN_LAST_SET = "ZULETZT"
        self.COLUMN_BEST_SET = "BEST"
        self.ROW_AVERAGE = "Durchschnitt"

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

        # errors
        self.ERROR_IMAGE_NOT_FOUND = "Bild nicht verfügbar"


class TrainingText_AllTools:
    def __init__(
        self, tool_amount: int, correct_answers: int, percentage: float
    ) -> None:
        self.correct_answers = correct_answers
        self.TEXT = f"""

[b]Super![/b]

Du hast alle {tool_amount} Geräte des Fahrzeugs gelernt. {self.correct_answers} {self.is_plural()} {percentage} %.

Die Geräte werden neu geladen und weiterhin zufällig gezogen."""

    def is_plural(self) -> str:
        if self.correct_answers == 1:
            return "richtige Antwort entspricht"
        return "richtige Antworten entsprechen"


class TrainingText_HalfTools:
    def __init__(
        self, tool_amount: int, correct_answers: int, percentage: float
    ) -> None:
        self.correct_answers = correct_answers
        self.TEXT = f"""

[b]Bleib dran![/b]

Du hast bereits die Hälfte der {tool_amount} Geräte des Fahrzeugs gelernt. Mit {self.correct_answers} richtigen {self.is_plural()} liegst du aktuell bei {percentage} %."""

    def is_plural(self) -> str:
        if self.correct_answers == 1:
            return "Antwort"
        return "Antworten"


class Base:
    def is_plural(self) -> str:
        if self.answers_total > 1:
            return "Geräte"
        return "Gerät"

    def has_scored_in_training(self) -> str:
        if self.answers_correct > 0:
            return f"Deinem Running Score werden [b]{self.answers_correct * self.factor} Punkte[/b] hinzugefügt."
        return ""

    def has_scored_in_game(self) -> str:
        if self.answers_correct > 0:
            return (
                f"Deinem Running Score werden [b]{self.score} Punkte[/b] hinzugefügt."
            )
        return ""


class GameEndText(Base):
    def __init__(
        self,
        answers_total: int,
        answers_correct: int,
        score: int,
        is_new_highscore: bool,
    ) -> None:
        self.answers_total = answers_total
        self.answers_correct = answers_correct
        self.score = score
        self.is_new_highscore = is_new_highscore

        self.TEXT = f"""
[b]Spiel Ende![/b]

Du hast {self.answers_total} {self.is_plural()} gespielt, davon {self.answers_correct} richtig zugeordnet. {self.add_text()}\n\n{self.has_scored_in_game()}
"""

    def add_text(self) -> str:
        if self.is_new_highscore:
            return f"""

[b]Glückwunsch![/b]
Du hast deinen persönlichen Highscore an diesem Fahrzeug verbessert.

Neuer Highscore: {self.score}"""
        return f"""

Punktestand: {self.score}"""


class TrainingEndText(Base):
    def __init__(
        self,
        answers_total: int,
        answers_correct: int,
        factor: int,
    ) -> None:
        self.answers_total = answers_total
        self.answers_correct = answers_correct
        self.factor = factor

        self.TEXT = f"""
[b]Kurze Pause![/b]

Du hast {self.answers_total} {self.is_plural()} gelernt, davon {self.answers_correct} richtig zugeordnet.\n\n{self.has_scored_in_training()}
"""


class Info_Text:
    def __init__(self) -> None:
        self.TEXT = """Meine Feuerwehr fehlt noch!

In der derzeitigen Pilotphase fügen wir Standorte
kostenlos hinzu. Schicke deine Anfrage an
[b]d.voglmaier@feuerwehr-hallein.at[/b]"""


class About_Text:
    def __init__(self, version) -> None:
        self.TEXT = f"""
© 2025 Freiwillige Feuerwehr der Stadt Hallein
Idee und Entwicklung: Dominik Voglmaier
Support: d.voglmaier@feuerwehr-hallein.at
Version: {version}
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

• Für die Erstellung von Infoplakaten:
[b]Karina Tschematschar[/b]

• Für die tatkräftige Unterstützung bei der Erstellung der Beladelisten:
[b]Bereitschaft 1[/b]
[b]Dienstführer[/b]

• Für die Unterstützung bei den Geräteaufnahmen:
[b]David Reiterer[/b]
[b]Kilian Brüderl[/b]

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
