from kivy.uix.screenmanager import Screen


class Settings_Screen(Screen):
    # def __init__(self, **kwargs):
    #     super(Settings_Screen, self).__init__(**kwargs)
    pass


# TODO

# introduce:
#   - settings_screen.py + .kv
#   - main.cfg
#   - custom_scores.yaml and default_scores.yaml
#   - custom firetrucks and default firetrucks

# general logic:
# default files in read-only at app dir
# custom files in writeable dir
# update content according to main.cfg

# at start-up, if not exist, move main.cfg to writeable dir
# save current config in main.cfg at storeable location

# use default switch:
#   if true:
#       read default firetrucks
#       use default_scores.yaml
#   if false:
#       check if custom firetrucks are available
#       check if custom_scores.yaml is available, if not: create

# custom firetrucks:
# select file
# validate content
#   if false: display errors
#   if okay:
#       check if custom content already exists: -> overwrite custom firetruck...
#   with user confirmation:
#       upload file,
#       store at writeable dir, (overwrite if exist)
#       disable default_switch,
#       use custom firetrucks,
#       create custom_scores.yaml,
#       use custom_scores.yaml

# overwrite custom firetruck:
# selected, validated, uploaded
# warn user about irreversible steps
# if accepted:
#   replace custom firetruck file
#   replace custom_scores.yaml
