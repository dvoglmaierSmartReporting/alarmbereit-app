# next version

features:

- update modi: (see image from Lio) emoji, Modi, subtitle (add statistics to modi)

- daily strike

  - store last_access_date
  - add daily_strike to scores.yaml
  - calculate day difference from today to last_access_date
    - if 1, add +1
    - if >=2, subtract
    - lowest is 0
  - display difference in color
    - if 0 before, don't display
    - if adding, green
    - if subtracting, red
  - when to update last_access_date ???
  - where to display strike

# version 2.9.0

features:

- TODO: iPhone: move tools label

- menu texts and subtitles

- introduce running score, incremented by every game played

- update tool picking logic: play set of all tools, even when app was closed

- introduce percentage of correct answered tools per car and set

- display modi and truck names left aligned

- update highscore screen: display running score, high scores, and percentages

- display pop-up when at least one tools was played

- new pop-up texts

# version 2.8.0

new app title: Alarmbereit

update:

- remove team122 logos
- introduce BaseMethode to share common methods between screens
- introduce FontSizeMixin to share dynamic font size methods between screens
- upgrade to Android SPK = 35 (Android 15) and NDK = 28b (28.2.13676358)

fix:

- high strike updates correctly instead of using all correct answers from session
- font_size of labels are adjusted
- Filtermaske changed in Leiter, RüstLösch, and Tank

# version 2.7.0

features:

- adding "Übung mit Bildern" new mode
- prewarm images to avoid rendering delays
- update highscore display in screen

# version 2.6.2 (2.6.1 was forced to re-upload)

fix:

- correct app version displayed on screen

# version 2.6.0

features:

- remove competitions
- add Kommando truck
- add info popup when all and half the tools are trained
- introduce "Übung mit Bildern" button, but disabled

fixes:

- error found by Fehlerfinder

# version 2.5.1 (2.5.0 was forced to re-upload)

features:

- refactor info screen into highscore screen
- show impressum + version in start screen
- new LZ logo
- added supporter info text
- refactor highscore output text
- add custom font "Courier Prime"

fixes:

- tools of Hallein Tank1 + Leiter updated
- tool corrections

# version 2.4.1

- iOS only: file naming fixed

# version 2.4.0

features:

- choose your fire department in first screen
- only see the content of your department and state
- refactor scores storage
- scores migration from 2.3.2 to 2.4.0
- only display scores of your department
- change your department any time
- display logo of your fire department
- use "Fahrer / GF" in layout for German trucks
- use kivy.Config to store settings

fixes:

- error found by Fehlerfinder
- update tools of Hallein RüstLösch

# version 2.3.2

fixes:

- updated tools Tank 2
- errors found by Fehlerfinder
- tests independent of assets file paths

# version 2.3.1

features:

- adding tests against all questions and tools

fixes:

- errors found by Fehlerfinder

# version 2.3.0 (Announce for everyone to use!)

Idea: Hide optional features. Include them one by one in future releases.
features:

- Android return button is useable for screen navigation
- version tag in app displayed
- acknowledgements screen button invisible (easter egg)
- hide "Übung mit Bildern" button in training mode
- pytest to verify all screens are loading

fixes:

- progress bar exceeds with additional time

# version 2.2.1

known issues:

- extra time is hard -> 2 difficulties
- missing time limit/end screen
- missing info about number of tools
- competition game is too much text
- missing "return to previous tool" feature
- Google Play Console Recommondation: Remove resizability and orientation restrictions in your app to support large screen devices

fixes:

- show Leistungsprüfung modi
- add button for "Übung mit Bildern" but disable it

# version 2.2.0:

features:

- use Android return button for screen navigation

fixes: []

# version 2.2.0:

features:

- change feedback color to blue for multiple correct answers in firetruck training and game
- add clean firetruck layout background for firetruck training and game
- use custom types for type hints
- adding acknowledgements screen
- adding new Tank 2

fixes:

- competitions with lowest question_id > 1 are not crashing anymore
- cleaned pylint errors
- fixed some competition questions

# version 2.1.2:

Go live in Google Play Store!

Used this version for app testing with peer group:
(results...)

# version 2.1.1:

Go live in Apple App Store!

---

# some lazyness

---

# version 1.1:

1. browse modus with search text
2. use classes in truck game&training and competition game&training

# version 1.0:

known issues:

1. use classes in truck game&training and competition game&training
2. save strike and PB correctly (currently displayed incorrectly)
3. competition questions arrow behavior incorrect
4. competition allows to select questions out of range

# version 0.9:

fix issues of version 0.8

1. Persönlicher Highscore wird lokal bespeichert
2. Bilder aller Geräteräume für Zug 1
3. Update Zeitdruck modus gameplay
4. import & compile PyYaml pkg

to be fixed:

- app crash at end_game() func
- multi-answer: already selected answer results incorrect answer

new features:

- Bewerbsfragen mit Multiple Choice Antworten

---

# version 0.8 (alpha):

1. refactor main.py
2. Persönlicher Highscore wird lokal bespeichert
3. Bilder aller Geräteräume für Zug 1
4. Update Zeitdruck modus gameplay

---

# version 0.7:

1. Globales string management in extra file
2. iOS Prototype erfolgreich gebaut
3. Stardardeinsatz Platzhalter hinzugefügt
4. ScrollView zur Ansicht von Bewerbsfragen
5. Rüstfahrzeug hinzugefügt
6. Starte ScrollView immer von oben
7. mehrere Fragen korrigiert
8. Fragen vor und zurück Funktion

---

# version 0.6:

1. Inhalte korrigiert (Rechtschreibfehler)
2. "Game" Modus überarbeitet

---

# version 0.5

1. Modus auswahl; nur erlaubte Kombinationen
2. Stöbern-Modus

Bekannte Fehler:

- Zeilenumbrüche in Stöbern-Modus
- Zeilenumbrüche und Textfelder in Bewerbs-Modus

---

# version 0.4

1. Game modus
2. Fahrer/GK und Mannschaft separiert

---

# version 0.3

1. Zug 1 Fahrzeuge

---

# version 0.2

1. Hauptmenü mit App Titel
2. logo und bild
3. Tank1 hinzufügen, Fahrzeugname einblenden
   - technically: yaml is source of truth! (helper to create dict)
4. erster Teil Bewerbsfragen hinzufügen

bugfixes:

- mehrfach korrekte Antworten
- Abstand zw MR und G1&G2
- Zeilenumbruch bei FK Fragen string

---

# MVP (v0.1) - "FA1000"

1. Hauptmenü
2. Modus wählen
   - Training (alle Fragen random pick ohne zurücklegen, kein Zeitlimit, keine Punkte)
   - Moduswahl als single-select
3. Fragen
   - Fahrzeugkunde (Rüst+Lösch, oder alle)
4. Fragenseite
   - Zurück button "<"
   - Oben tool name
   - Unten multiple choice
   - Anklicken locked sofort ein
   - Wenn richtig, zeige alle weiteren richtigen grün an
   - Wenn falsch, Auswahl rot, alle richtigen grün
   - Restliche Felder unverändert
   - Nächste Frage nach 2 s cooldown
