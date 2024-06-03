# version 0.7:
1. Globales string management in extra file
2. iOS Prototype erfolgreich gebaut
3. Stardardeinsatz Platzhalter hinzugefügt
4. Scrollview zur Ansicht von Bewerbsfragen
5.


-------------------------------------------------------------------------
# version 0.6:
1. Inhalte korrigiert (Rechtschreibfehler)
2. "Game" Modus überarbeitet

-------------------------------------------------------------------------
# version 0.5
1. Modus auswahl; nur erlaubte Kombinationen
2. Stöbern-Modus

Bekannte Fehler:
- Zeilenumbrüche in Stöbern-Modus
- Zeilenumbrüche und Textfelder in Bewerbs-Modus

-------------------------------------------------------------------------

# version 0.4
1. Game modus
2. Fahrer/GK und Mannschaft separiert

-------------------------------------------------------------------------

# version 0.3
1. Zug 1 Fahrzeuge

-------------------------------------------------------------------------

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

-------------------------------------------------------------------------

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

-------------------------------------------------------------------------

# backlog
- Game modus hinzufügen
    - 10 sec progress bar pro frage
    - punkte pro frage
    - 15 Fragen, ohne Antwortmöglichkeiten
    - Gesamtpunkte einmalig anzeigen
    - alle Fragen mit ID
- App design verbessern
- mehr Fahrzeuge
- Modus "alle Fahrzeuge"