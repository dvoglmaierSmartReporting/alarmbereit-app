from kivy.uix.screenmanager import Screen
from kivy.clock import Clock

from kivy.uix.image import Image


from random import shuffle


class Fahrzeugkunde_Images(Screen):
    # def __init__(self, **kwargs):
    #     super(Fahrzeugkunde_Images, self).__init__(**kwargs)

    def load_image(self):
        self.scatter.clear_widgets()  # type: ignore

        image = Image(
            source="assets/Rüst_G1_default-min.jpg",
            # allow_stretch=True,
            # keep_ratio=True,
            fit_mode="contain",
        )
        self.scatter.add_widget(image)  # type: ignore

        # Bind the size and position of the image to the scatter
        self.scatter.bind(size=self.update_image_size)  # type: ignore
        self.scatter.bind(pos=self.update_image_pos)  # type: ignore

    def update_image_size(self, instance, value):
        instance.children[0].size = instance.size

    def update_image_pos(self, instance, value):
        instance.children[0].pos = instance.pos

    def select_firetruck(self, selected_firetruck: str):
        # troubleshooting: fix firetruck
        # self.selected_firetruck = "Tank1" "Rüst+Lösch"
        self.selected_firetruck = selected_firetruck
        self.firetruck_label.text = f"   {selected_firetruck}"  # type: ignore
