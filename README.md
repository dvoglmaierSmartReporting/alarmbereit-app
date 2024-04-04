# Feuerwehr App (cool name tbd)

## Goal
Goal is to create a software to train fire department specific knowledge. It is a quiz app with two main aspects: location of tools in firetrucks, and competition questions. Core feature is to make the app available for Android and iOS. That everyone can use it on their mobile devices whenever they have some leisure time to fill. In far future the quiz contain questions of all available competitions in Salzburg and all youth competition questions. Also, it shall include the option to customize the firetrucks to your local fire department individually. 
Later, if all other things already implemented, one can dream of a gamification with global database and highscore comparison...

## Framework
- Python, kivy package
- apk generation via buildozer

## Challenges
- compatibility with Android and iOS
- usage of imported python packages
- distribution via app store
- question content

## Repository content

### /app
Contains all necessary files to generate the Android package (.apk) via
`/app> buildozer -v android debug`

### /
Contains source-of-truth for competition questions:
`feuerwehr_competition_questions.yaml` (not complete)

Contains source-of-truth for tool storage locations:
`feuerwehr_tools_storage.yaml` (not complete)

As some python packages caused issues in the apk creation, for now its avoided to use imported packages (e.g. PyYAML). Workaround is to manually convert yaml into dict and import as function variable (e.g. `firetrucks.py`). Run
`/> ./yaml2json.py`
to update regarding files.

Another helper function is `pip_dependencies.py`. Its used to generate package dependency string used in `buildozer.spec`. E.g. run
`/> ./pip_dependencies.py kivy`
to receive a string of all dep-tree in hierarchie order, like
`Pygments==2.17.2,urllib3==2.1.0,idna==3.6,charset-normalizer==3.3.2,certifi==2023.11.17,requests==2.31.0,Kivy-Garden==0.1.5,docutils==0.20.1,Kivy==2.3.0`

### /app/assets
Contains logos and icons of Freiwillige Feuerwehr Hallein. Usage is only allowed in context of this application. Authorisation can be revoked anytime.
