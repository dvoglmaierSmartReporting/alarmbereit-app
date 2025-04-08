from kivy.uix.screenmanager import Screen
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.clock import Clock

from typing import cast

from helper.functions import change_screen_to


class Fahrzeugkunde_Images(Screen):
    # def load_image(self):
    #     self.scatter.clear_widgets()

    #     image = Image(
    #         source="assets/Rüst_G1_default-min.jpg",
    #         # allow_stretch=True,
    #         # keep_ratio=True,
    #         fit_mode="contain",
    #     )
    #     self.scatter.add_widget(image)

    #     # Bind the size and position of the image to the scatter
    #     self.scatter.bind(size=self.update_image_size)
    #     self.scatter.bind(pos=self.update_image_pos)

    # def update_image_size(self, instance, value):
    #     instance.children[0].size = instance.size

    # def update_image_pos(self, instance, value):
    #     instance.children[0].pos = instance.pos

    # def select_firetruck(self, selected_firetruck: str):
    #     # troubleshooting: fix firetruck
    #     # self.selected_firetruck = "Tank1" "Rüst+Lösch"
    #     self.selected_firetruck = selected_firetruck
    #     self.firetruck_label.text = selected_firetruck

    def select_firetruck(self, selected_firetruck: str):
        # troubleshooting: fix firetruck
        # self.selected_firetruck = "Tank1" "Rüst+Lösch"
        self.selected_firetruck = selected_firetruck

        self.firetruck_label = cast(Label, self.firetruck_label)
        self.firetruck_label.text = selected_firetruck

    def load_image(self):  # Called when screen is displayed
        self.populate_scroll()

    def populate_scroll(self):
        container = self.ids.scroll_container

        container.clear_widgets()

        # Example content (can be loaded from a list or data structure)
        content = [
            {"type": "label", "text": "G1"},
            {"type": "image", "source": "assets/truck_RL/g1_front.jpg"},
            {"type": "label", "text": "G1"},
            {"type": "image", "source": "assets/truck_RL/g1_door.jpg"},
            {"type": "label", "text": "G1"},
            {"type": "image", "source": "assets/truck_RL/g1_core.jpg"},
            {"type": "label", "text": "G3"},
            {"type": "image", "source": "assets/truck_RL/g3.jpg"},
            {"type": "label", "text": "G5"},
            {"type": "image", "source": "assets/truck_RL/g5_front.jpg"},
            {"type": "label", "text": "G5"},
            {"type": "image", "source": "assets/truck_RL/g5_door.jpg"},
            {"type": "label", "text": "G5"},
            {"type": "image", "source": "assets/truck_RL/g5_core.jpg"},
            {"type": "label", "text": "G7 / Heck"},
            {"type": "image", "source": "assets/truck_RL/g7.jpg"},
            {"type": "label", "text": "Dach"},
            {"type": "image", "source": "assets/truck_RL/roof_back.jpg"},
            {"type": "label", "text": "Dach"},
            {"type": "image", "source": "assets/truck_RL/roof_left.jpg"},
            {"type": "label", "text": "Dach"},
            {"type": "image", "source": "assets/truck_RL/roof_right.jpg"},
            {"type": "label", "text": "G6"},
            {"type": "image", "source": "assets/truck_RL/g6.jpg"},
            {"type": "label", "text": "G4"},
            {"type": "image", "source": "assets/truck_RL/g4.jpg"},
            {"type": "label", "text": "G2"},
            {"type": "image", "source": "assets/truck_RL/g2_front.jpg"},
            {"type": "label", "text": "G2"},
            {"type": "image", "source": "assets/truck_RL/g2_door.jpg"},
            {"type": "label", "text": "G2"},
            {"type": "image", "source": "assets/truck_RL/g2_core.jpg"},
            {"type": "label", "text": "Mannschaft"},
            {"type": "image", "source": "assets/truck_RL/in_right_backward.jpg"},
            {"type": "label", "text": "Mannschaft"},
            {"type": "image", "source": "assets/truck_RL/in_right_forward.jpg"},
            {"type": "label", "text": "Mannschaft"},
            {"type": "image", "source": "assets/truck_RL/in_core.jpg"},
            {"type": "label", "text": "Mannschaft"},
            {"type": "image", "source": "assets/truck_RL/in_top.jpg"},
        ]

        for item in content:
            if item["type"] == "label":
                lbl = Label(
                    text=item.get("text", ""),
                    font_size="20sp",
                    size_hint_y=None,
                    height="40dp",
                )
                container.add_widget(lbl)

            elif item["type"] == "image":
                container = self.ids.scroll_container
                img_widget = self.create_dynamic_image(item.get("source"), container)
                container.add_widget(img_widget)

    def create_dynamic_image(self, source_path, container):

        img = Image(
            source=source_path,
            size_hint=(1, None),  # Full width, dynamic height
            fit_mode="contain",
        )

        def set_height(*args):
            if img.texture:
                width = container.width
                tex_width, tex_height = img.texture_size
                aspect_ratio = tex_height / tex_width
                img.height = width * aspect_ratio

        # Wait for the image to finish loading & ensure container has a width
        def on_loaded(*_):
            Clock.schedule_once(set_height, 0)

        img.bind(texture=on_loaded)
        container.bind(width=lambda *_: set_height())

        return img

    def go_back(self, *args) -> None:
        change_screen_to("fahrzeugkunde_menu")
