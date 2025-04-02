# FahrzeugkundeApp

## Goal
Goal is to create a software to train fire department specific knowledge. It is a quiz app with two main aspects: location of tools in firetrucks, and competition questions. Core feature is to make the app available for Android and iOS. That everyone can use it on their mobile devices whenever they have some leisure time to fill. In far future the quiz contain questions of all available competitions in Salzburg and all youth competition questions. Also, it shall include the option to customize the firetrucks to your local fire department individually. 
Later, if all other things already implemented, one can dream of a gamification with global database and highscore comparison...

## Ziel
Das Ziel ist: Es muss Spaß machen, Fahrzeugkunde zu betreiben!
Der Fokus liegt daher auf den features der App, die Fahrzeugkunde vermitteln ("Übung" und "Zeitdruck"). Diese Modi sollen den User motivieren, die eigenen High-Scores zu verbessern und die App regelmäßig zu verwenden. Denn nur die regelmäßige Wiederholung der Fahrzeugbeladung festigt das Wissen und bring den erwünschten Mehrwert im Einsatzfall. Vor allem für Fahrzeuge, die schwierig zu lernen sind (z.B. Rüst).

## Framework
- Python, kivy package
- aab generation via buildozer

## Challenges
- compatibility with Android and iOS
- usage of imported python packages
- distribution via app store
- question content

## Build Android package (.apk/.aab)
```
/app> buildozer -v android debug
/app> buildozer -v android release
```

## Run locally
```
/app> python3 main.py
```

## Build iOS package (.ipa)

1. duplicate the repository to "iOS-build" proxy folder
2. open Xcode project
3. build and archive the package