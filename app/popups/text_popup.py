from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView

from helper.settings import Strings


strings = Strings()


class TextPopup(Popup):
    def __init__(
        self,
        message: str,
        title: str,
        size_hint: tuple[float, float] = (0.8, 0.8),
        **kwargs
    ):
        super().__init__(**kwargs)
        self.title = title
        self.title_size = "23sp"
        self.size_hint = size_hint  # Adjust size as needed

        layout = BoxLayout(orientation="vertical", padding=10, spacing=10)

        # Scrollable container
        scroll_view = ScrollView(size_hint=(1, 1), do_scroll_x=False)

        # Uses the full width of the popup and wraps text
        self.text_label = Label(
            text=message,
            font_size="20sp",
            size_hint=(1, None),  # Full width, dynamic height
            text_size=(self.width - 40, None),  # Forces text wrapping
            halign="left",
            valign="top",
            markup=True,
        )
        self.text_label.bind(  # type: ignore[attr-defined]
            size=self._update_text_size, texture_size=self._adjust_label_height
        )

        # Add label inside ScrollView
        scroll_view.add_widget(self.text_label)

        # Close button
        close_button = Button(
            text=strings.BUTTON_CLOSE_POPUP,
            font_size="23sp",
            size_hint=(1, None),
            height=100,
        )
        close_button.bind(on_press=self.dismiss)  # type: ignore[attr-defined]

        layout.add_widget(scroll_view)
        layout.add_widget(close_button)

        self.content = layout

    def _update_text_size(self, instance, value):
        instance.text_size = (
            self.width - 100,
            None,
        )  # Adjust text wrapping dynamically

    def _adjust_label_height(self, instance, value):
        instance.height = value[1]  # Update height based on text content
