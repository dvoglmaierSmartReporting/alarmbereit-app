from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen
from kivy.clock import Clock


from random import shuffle

from helper.functions import load_total_storage


class Fahrzeugkunde_Browse(Screen):
    def select_firetruck(self, selected_firetruck: str):
        # troubleshooting: fix firetruck
        # self.selected_firetruck = "Tank1" "Rüst+Lösch"
        self.selected_firetruck = selected_firetruck
        self.firetruck_label.text = f"{selected_firetruck}   "  # type: ignore

    def load_firetruck(self):
        total_storage = load_total_storage()
        self.firetruck: dict = total_storage[self.selected_firetruck]
        self.firetruck_rooms: list = list(self.firetruck.keys())

    def populate_list(self):
        self.load_firetruck()
        self.ids.browse_scrollview.scroll_y = 1
        label_container = self.ids.label_list
        label_container.clear_widgets()

        for room in self.firetruck_rooms:
            label = Label(
                text=f"[b]{str(room)}[/b]",
                markup=True,
                size_hint_y=None,
                font_size="24sp",
                height=90,
                halign="left",
                text_size=(self.width, None),
            )
            label.bind(  # type: ignore
                size=label.setter("text_size")  # type: ignore
            )  # Update text_size on label size change
            label_container.add_widget(label)

            for tool in self.firetruck.get(room):  # type: ignore
                label = Label(
                    text=f"   -  {str(tool)}",
                    size_hint_y=None,
                    size_hint_x=1,
                    font_size="22sp",
                    height=70,
                    halign="left",
                    valign="middle",
                )
                label.text_size = (label.width, None)
                label.bind(  # type: ignore
                    width=lambda instance, value: setattr(
                        instance, "text_size", (value, None)
                    )
                )

                label_container.add_widget(label)

        # exceed list by empty entry
        label = Label(
            text="",
            size_hint_y=None,
            size_hint_x=1,
            font_size="22sp",
            height=70,
            halign="left",
            valign="middle",
        )
        label.text_size = (label.width, None)
        label.bind(  # type: ignore
            width=lambda instance, value: setattr(instance, "text_size", (value, None))
        )

        label_container.add_widget(label)
