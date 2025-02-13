from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen


from helper.functions import load_total_storage
from helper.settings import Strings


strings = Strings()


class Fahrzeugkunde_Browse(Screen):
    def __init__(self, **kwargs):
        super(Fahrzeugkunde_Browse, self).__init__(**kwargs)

        self.ids.filter_button.text = strings.BUTTON_STR_FILTER

    def select_firetruck(self, selected_firetruck: str):
        # troubleshooting: fix firetruck
        # self.selected_firetruck = "Tank1" "Rüst+Lösch"
        self.selected_firetruck = selected_firetruck
        self.firetruck_label.text = f"{selected_firetruck}   "  # type: ignore

    def load_firetruck(self):
        total_storage = load_total_storage()
        self.firetruck: dict = total_storage[self.selected_firetruck]
        self.firetruck_rooms: list = list(self.firetruck.keys())

    def give_room_label(self, label_text: str):
        label = Label(
            text=f"[b]{str(label_text)}[/b]",
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
        return label

    def give_item_label(self, label_text: str = ""):
        if label_text != "":
            label_text = f"   -  {str(label_text)}"

        label = Label(
            text=label_text,
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
        return label

    def add_items(self, truck: dict):
        self.ids.browse_scrollview.scroll_y = 1
        label_container = self.ids.label_list
        label_container.clear_widgets()

        for room in truck.keys():
            label_container.add_widget(self.give_room_label(room))

            for tool in truck.get(room):  # type: ignore
                label_container.add_widget(self.give_item_label(tool))

        # exceed list by empty entry
        label_container.add_widget(self.give_item_label())

    def display_all_tools(self):
        self.load_firetruck()
        self.add_items(self.firetruck)

    def filter_list(self):
        filter_text = self.filter_text.text

        # Dictionary comprehension with case-insensitive filtering
        filtered_dict = {
            key: [item for item in value if filter_text.lower() in item.lower()]
            for key, value in self.firetruck.items()
        }

        self.add_items(filtered_dict)
