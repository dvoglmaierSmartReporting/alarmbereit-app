import os

# Get absolute path to the layouts asset folder
ASSETS_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "assets", "layouts")
)


from kivy.app import App
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout

from helper.custom_types import *


def get_7_rooms_layout() -> floatButtons:
    return [
        ("Fahrer / GK", 0.5, 0.15, 0.25, 1),
        ("Mannschaft", 0.5, 0.16, 0.25, 0.85),
        ("G1", 0.27, 0.175, 0.085, 0.68),
        ("G3", 0.205, 0.175, 0.15, 0.505),
        ("G5", 0.27, 0.175, 0.085, 0.33),
        ("G2", 0.27, 0.175, 0.65, 0.68),
        ("G4", 0.205, 0.175, 0.65, 0.505),
        ("G6", 0.27, 0.175, 0.65, 0.33),
        ("G7 / Heck", 0.4, 0.145, 0.3, 0.145),
        ("Dach", 0.2, 0.4, 0.4, 0.61),
    ]


def get_5_rooms_layout() -> floatButtons:
    return [
        ("Fahrer / GK", 0.5, 0.15, 0.25, 1),
        ("Mannschaft", 0.5, 0.16, 0.25, 0.85),
        ("G1", 0.27, 0.175, 0.085, 0.68),
        ("G3", 0.205, 0.35, 0.15, 0.505),
        ("G2", 0.27, 0.175, 0.65, 0.68),
        ("G4", 0.205, 0.35, 0.65, 0.505),
        ("G5 / Heck", 0.4, 0.145, 0.3, 0.145),
        ("Dach", 0.2, 0.4, 0.4, 0.61),
    ]


def get_leiter_layout() -> floatButtons:
    return [
        ("Korb", 0.3, 0.13, 0.35, 1),
        ("Mannschaft", 0.55, 0.155, 0.225, 0.86),
        ("G1", 0.27, 0.2, 0.085, 0.68),
        ("G3", 0.185, 0.185, 0.085, 0.45),
        ("G5", 0.185, 0.125, 0.085, 0.14),
        ("G2", 0.27, 0.2, 0.65, 0.68),
        ("G4", 0.185, 0.185, 0.735, 0.45),
        ("G6", 0.185, 0.125, 0.735, 0.14),
        ("Dach", 0.34, 0.42, 0.33, 0.45),
    ]


def get_voraus_layout() -> floatButtons:
    return [
        ("Fahrer / GK", 0.55, 0.13, 0.225, 0.90),
        ("Mannschaft", 0.55, 0.13, 0.225, 0.75),
        ("G1", 0.22, 0.415, 0.18, 0.61),
        ("G1\ntief", 0.1, 0.155, 0.08, 0.35),
        ("G2", 0.22, 0.415, 0.605, 0.61),
        ("G2\ntief", 0.1, 0.155, 0.825, 0.35),
        ("G3", 0.4, 0.185, 0.3, 0.19),
    ]


def get_ruest_layout() -> floatButtons:
    return [
        ("Mannschaft", 0.55, 0.13, 0.225, 0.99),
        ("G1\nlinks", 0.15, 0.22, 0.08, 0.81),
        ("G1\ninnen", 0.15, 0.45, 0.23, 0.81),
        ("G1\nrechts", 0.15, 0.22, 0.08, 0.58),
        ("G3", 0.23, 0.265, 0.15, 0.355),
        ("G2\nrechts", 0.15, 0.22, 0.77, 0.81),
        ("G2\ninnen", 0.15, 0.45, 0.62, 0.81),
        ("G2\nlinks", 0.15, 0.22, 0.77, 0.58),
        ("G4", 0.23, 0.265, 0.62, 0.355),
        ("G5 / Heck", 0.4, 0.08, 0.3, 0.085),
        ("Dach", 0.2, 0.4, 0.4, 0.61),
    ]


def build_answer_layout(room_layout: str, calling_screen: str) -> FloatLayout:
    # display background and buttons
    float = FloatLayout(size_hint=(1, 1))

    if room_layout in ["7-Raum"]:
        bgd_image = os.path.join(ASSETS_DIR, "truck.jpg")
        buttons = get_7_rooms_layout()

    elif room_layout in ["5-Raum"]:
        bgd_image = os.path.join(ASSETS_DIR, "truck.jpg")
        buttons = get_5_rooms_layout()

    elif room_layout in ["Leiter"]:
        bgd_image = os.path.join(ASSETS_DIR, "leiter.jpg")
        buttons = get_leiter_layout()

    elif room_layout in ["Rüst", "Ruest"]:
        bgd_image = os.path.join(ASSETS_DIR, "ruest.jpg")
        buttons = get_ruest_layout()

    elif room_layout in ["Voraus"]:
        bgd_image = os.path.join(ASSETS_DIR, "voraus.jpg")
        buttons = get_voraus_layout()

    else:
        raise NotImplementedError

    background = Image(
        source=bgd_image,
        fit_mode="fill",
        size_hint=(1, 1),
        pos_hint={"center_x": 0.5, "center_y": 0.5},
    )
    float.add_widget(background)

    screen = App.get_running_app().root.get_screen(calling_screen)
    for text, w, h, x, top in buttons:
        btn = Button(
            text=text,
            font_size="25sp",
            background_color=(0.7, 0.7, 0.7, 0.7),
            size_hint=(w, h),
            pos_hint={"x": x, "top": top},
        )
        # btn.bind(on_press=self.on_answer)
        btn.bind(on_press=screen.on_answer)
        float.add_widget(btn)

    return float
