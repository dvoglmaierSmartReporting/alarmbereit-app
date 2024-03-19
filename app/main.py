from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button

# import yaml
# from ruamel.yaml import YAML

from kivy.clock import Clock

from random import shuffle

#
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.lang import Builder

#


# Define our different screens
class StartMenu(Screen):
    pass


class FahrzeugkundeMenu(Screen):
    def __init__(self, **kwargs):
        super(FahrzeugkundeMenu, self).__init__(**kwargs)
        # self.transition_callback = transition_callback

    #     self.load_firetrucks()

    # def load_firetrucks(self):
    #     with open("feuerwehr_tools_storage.yaml", "r") as f:
    #         try:
    #             self.tools_storage = yaml.safe_load(f)
    #             self.firetrucks_list = list(self.tools_storage.keys())
    #         except yaml.YAMLError as exc:
    #             print(exc)


class BewerbMenu(Screen):
    pass


class FeuerwehrGame(Screen):
    # def __init__(self, selected_firetruck, **kwargs):
    def __init__(self, **kwargs):
        super(FeuerwehrGame, self).__init__(**kwargs)
        # self.selected_firetruck = selected_firetruck
        self.selected_firetruck = "Rüst+Lösch"
        self.load_tools_from_firetruck()
        self.next_question()
        self.accept_answers = True  # Flag to indicate if answers should be processed

    def load_total_storage(self):
        total_storage = {
            "Rüst+Lösch": {
                "Mannschaftsraum": [
                    "Winkerkelle",
                    "Handfunkgerät",
                    'Warnzeichen "Feuerwehr"',
                    "Rettungsleine",
                    "FW-Gurt",
                    "Notrettungsset",
                    "Feuerwehrauffanggurt",
                    "Basis Sichern/Auffangen",
                    "A2-Sanitätsrucksack",
                    "Einweghandschuhe",
                    "Alu-Rettungsdecke",
                    "Wolldecke",
                    "Pressluftatmer",
                    "Reserveflasche",
                    "Vollmaske f. Pressluftatmer",
                    "Totmannwarner",
                    "Brandfluchthauben",
                    "Wärmebildkamera",
                    "FW-Handschuhe",
                    "Hochsichtbare Warnbekleidung",
                    "Handlampe Adalite",
                    "Respihood",
                    "Kühlbox",
                    "Tragetuch",
                    "Leichensack",
                    "Trainingsanzug",
                    "Handtuch",
                    "Gasmessgerät",
                    "Nüssler Gefahrguthelfer",
                    "PAX-Meldertasche",
                    "Auto-Öffnungswerkzeug",
                    "Euro-Blitz Leuchte",
                ],
                "G1": [
                    "Spinboard",
                    "Schnittschutzhose",
                    "Arbeitsmesser",
                    "Bogensäge",
                    "Bolzenschneider",
                    "Hacke langstielig",
                    "Hacke kurzstielig",
                    "Vorschlaghammer 5 kg",
                    "Handfäustel 2 kg",
                    "Brechstange lang 1,5 m",
                    "Feuerwehraxt",
                    "Halligantool",
                    "Piassavabesen",
                    "Fassschaufel",
                    "Aluminium Randschaufel",
                    "Krampen",
                    "Feuerwehrsappel",
                    "Bindedraht verzinkt",
                    "Gerüstklammern verzinkt",
                    "Nägel",
                    "Schachthaken",
                    "Drahtseilkemmen",
                    "Drahtseil verzinkt 5 m",
                    "Drahtseil verzinkt 10 m",
                    "Reservekette f. Motorsäge",
                    "Rundschlinge 60 kN",
                    "Kette einsträngig 67 kN",
                    "Kette zweisträngig 56 kN",
                    "Schäkel 65 kN",
                    "Schäkel 120 kN",
                    "Aggregat f. hydr. Rettungssatz",
                    "Handpumpe",
                    "Hydraulischer Spreizer",
                    "Hydraulische Schere",
                    "Doppelwirkender Rettungszylinder",
                    "Pedalschneider",
                    "Akku Kombigerät",
                    "Schwellenaufsatz",
                    "Werkzeugsatz VU",
                    "Schutzdeckenset",
                    "Unterbauschiebeblock",
                    "Abstützsystem",
                    "Freilandverankerung",
                    "Greifzug",
                    "Greifzugseil",
                    "Umlenkrolle 100 kN",
                    "Kantenreiter",
                    "Umlenkrolle 140 kN",
                    "Winde 10 t",
                    "Motorsäge",
                    "Rettungssäge Stihl",
                    "Kombikanister f. Motorsäge",
                    "Ersatzkette Rettungssäge",
                    "Rauchfangtürschlüssel",
                ],
                "G2": [
                    "Schlagbohrmaschine mit Bohrersatz",
                    "Europa Absperrband",
                    "Absperrständer",
                    "Bodenteller f. Absperrständer",
                    "Verkehrsleitkegel",
                    "Blitzer LED",
                    "Erdungsspieß",
                    "Erdungszwingen",
                    "Erdungsschiene",
                    "Erdungslitzen",
                    "Lichtfluter",
                    "Stative",
                    "Aufnahmebrücke f. Fluter",
                    "Stromerzeuger",
                    "Abgasschlauch f. Stromerz.",
                    "Kraftstoffkanister f. Stromerz.",
                    "Einfüllstutzen",
                    "Verteilerkabeltrommel 30 m 400 V",
                    "Fixeingebaute Kabeltrommel",
                    "Kabeltrommel 230 V",
                    "Verlängerungskabel",
                    "Druckluftflasche f. Hebekissen",
                    "Hebekissensatz 8 bar",
                    "Druckbelüfter",
                    "Kraftstoffkanister",
                    "Ausgießstutzen",
                    "Markierleuchtenset",
                ],
                "G3": [
                    "Türöffnungsset",
                    "Schlauchtragekorb",
                    "Druckschlauch C",
                    "Hohlstrahlrohr C",
                    "D-Saugschlauch f. Zumischer",
                    "Schaummittelkanister",
                    "Zumischer Z2",
                    "Kombischaumrohr K2",
                    "Mobiler Rauchverschluss",
                    "Arbeitsleine",
                ],
                "G4": [
                    "Werkzeugsatz",
                    "Zurrgurt",
                    "Schnürleine",
                    "Unterlegkeil Seilwinde",
                    "Trennschleifer",
                    "Säbelsäge Akku",
                    "Akku f. Säbelsäge",
                    "Schutzbrille",
                    "Staubmaske",
                    "Doppelmembran Pumpe",
                    "Auffangtank 1500 l",
                    "Rolle Müllsäcke",
                    "Schuttwanne",
                    "Auffangplane 3x4 m",
                    "Auffangsack Spillpacks",
                    "Dichtkeil",
                    "Holzhammer",
                    "Dichtpfropfen",
                ],
                "G5": [
                    "Kupplungsschlüssel ABC",
                    "Druckschlauch B",
                    "Verbindungsschlauch B",
                    "Satz Schlauchbinden",
                    "Schlauchhalter",
                    "Hohlstrahlrohr C",
                    "Mehrzweckstrahlrohr B",
                    "Stützkrümmer B",
                    "Druckbegrenzungsventil B",
                    "Verteiler B-CBC",
                    "Sammelstück 2B-A",
                    "Übergangsstück A-B",
                    "Übergangsstück A125-A",
                    "Übergangsstück B-C",
                    "Überflurhydrantenschlüssel",
                    "C-Hydroschild",
                    "Tauchpumpen",
                    "Blindkupplungen f. Ölsperre",
                    "Druckschlauch C",
                ],
                "G6": [
                    "Schneekette",
                    "Kunststoffeimer",
                    "Löschdecke inkl. Beutel",
                    "CAFS Löscher 10 l",
                    "Trockenlöscher 12 kg",
                    "Kohlendioxidlöscher 5 kg",
                    "HD-Kupplungsschlüssel",
                    "Tragbarer Wasserwerfer",
                    "Unterlegsholz",
                    "Druckschlauch B",
                ],
                "Heck": [
                    "Handfunkgerät",
                    "Schlauchhaspel",
                    "Atemschutz- Außenüberwachung",
                    "Abschleppstange",
                ],
                "Dach": [
                    "Moosgummiplatte",
                    "Schlauchbrücke Paar Alu",
                    "Schiebeleiter 3-teilig",
                    "Steckleiter 4-teilig",
                    "Verbindungsteil Steckleiter",
                    "Chemieschutzstiefel",
                    "Chemieschutzhandschuhe",
                    "Chemieschutzanzug Stufe 2",
                    "Ausräumhaken",
                    "Heugabel",
                    "Einreißhaken",
                    "Kescher",
                    "Schachtabdeckung",
                ],
            },
            "Tank1": {"Mannschaftsraum": ["Handfunkgerät"], "G1": ["Handfunkgerät"]},
        }

        return total_storage

    def load_tools_from_firetruck(self):

        # yaml (PyYAML) approach
        # with open("feuerwehr_tools_storage.yaml", "r") as f:
        #     try:
        #         total_storage = yaml.safe_load(f)
        #         print(type(total_storage))
        #         # self.firetruck_dict = total_storage[self.selected_firetruck]
        #         self.firetruck_dict = total_storage[self.selected_firetruck]
        #         self.rooms_list = self.firetruck_dict.keys()
        #         self.tools_list = [
        #             tool for room in self.firetruck_dict.values() for tool in room
        #         ]
        #         self.tools_list = list(set(self.tools_list))
        #         shuffle(self.tools_list)
        #         self.tool_locations = self.invert_firetruck_equipment()
        #     except yaml.YAMLError as exc:
        #         print(exc)

        # # ruamel.yaml approach
        # yaml = YAML()
        # with open("feuerwehr_tools_storage.yaml", "r") as f:
        #     total_storage = yaml.load(f)
        #     print(type(total_storage))
        #     # self.firetruck_dict = total_storage[self.selected_firetruck]
        #     self.firetruck_dict = total_storage[self.selected_firetruck]
        #     self.rooms_list = self.firetruck_dict.keys()
        #     self.tools_list = [
        #         tool for room in self.firetruck_dict.values() for tool in room
        #     ]
        #     self.tools_list = list(set(self.tools_list))
        #     # shuffle(self.tools_list)
        #     self.tool_locations = self.invert_firetruck_equipment()

        # total_storage = {
        #     "Rüst+Lösch": {
        #         "Mannschaftsraum": [
        #             "Nüssler Gefahrguthelfer",
        #             "PAX-Meldertasche",
        #             "Auto-Öffnungswerkzeug",
        #             "Euro-Blitz Leuchte",
        #         ],
        #         "G1": [
        #             "Kombikanister f. Motorsäge",
        #             "Ersatzkette Rettungssäge",
        #             "Rauchfangtürschlüssel",
        #         ],
        #     },
        #     "Tank1": {"Mannschaftsraum": ["Handfunkgerät"], "G1": ["Handfunkgerät"]},
        # }

        total_storage = self.load_total_storage()

        # self.firetruck_dict = total_storage[self.selected_firetruck]
        self.firetruck_dict = total_storage[self.selected_firetruck]
        self.rooms_list = self.firetruck_dict.keys()
        self.tools_list = [
            tool for room in self.firetruck_dict.values() for tool in room
        ]
        self.tools_list = list(set(self.tools_list))
        shuffle(self.tools_list)
        self.tool_locations = self.invert_firetruck_equipment()

    def invert_firetruck_equipment(self):
        tool_locations = {}
        for location, tools in self.firetruck_dict.items():
            for tool in tools:
                if tool in tool_locations:
                    tool_locations[tool].append(location)
                else:
                    tool_locations[tool] = [location]
        return tool_locations

    def next_question(self, *args):
        self.accept_answers = True  # Enable answer processing for the new question
        if not self.tools_list:
            self.load_tools_from_firetruck()

        self.current_tool = self.tools_list.pop()
        self.question_label.text = self.current_tool
        self.answers_layout.clear_widgets()
        self.mannschaftsraum_layout.clear_widgets()

        for storage in self.rooms_list:
            btn = Button(text=storage, font_size="32sp")
            btn.bind(on_press=self.on_answer)
            if storage == "Mannschaftsraum":
                self.mannschaftsraum_layout.add_widget(btn)
            else:
                self.answers_layout.add_widget(btn)

    def on_answer(self, instance):
        if not self.accept_answers:  # Check if answer processing is enabled
            return  # Ignore the button press if answer processing is disabled

        correct_storage = set(self.tool_locations[self.current_tool])

        if instance.text in correct_storage:
            instance.background_color = (0, 1, 0, 1)
        else:
            instance.background_color = (1, 0, 0, 1)
            # Identify and indicate the correct answer
            # for child in self.answers_layout.children:
            children = (
                self.answers_layout.children + self.mannschaftsraum_layout.children
            )
            for child in children:
                if child.text in correct_storage:
                    child.background_color = (0, 1, 0, 1)

        self.accept_answers = (
            False  # Disable answer processing after an answer is selected
        )
        Clock.schedule_once(self.next_question, 2)


class WindowManager(ScreenManager):
    pass


kv = Builder.load_file("feuerwehr.kv")


class FeuerwehrApp(App):
    def build(self):

        sm = ScreenManager()
        sm.add_widget(StartMenu())
        sm.add_widget(FahrzeugkundeMenu())
        sm.add_widget(BewerbMenu())
        sm.add_widget(FeuerwehrGame())
        return sm


if __name__ == "__main__":
    FeuerwehrApp().run()
