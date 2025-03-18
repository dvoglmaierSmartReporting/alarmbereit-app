from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView

from helper.settings import Strings


strings = Strings()


class ErrorPopup(Popup):
    def __init__(self, message, **kwargs):
        super().__init__(**kwargs)
        self.title = strings.TITLE_ERROR_POPUP
        self.size_hint = (0.8, 0.8)  # Adjust size as needed

        # layout = BoxLayout(orientation="vertical")
        # layout.add_widget(Label(text=message))

        # close_button = Button(text=strings.BUTTON_CLOSE_POPUP, size_hint=(1, 0.3))
        # close_button.bind(on_press=self.dismiss)

        # layout.add_widget(close_button)
        # self.content = layout

        layout = BoxLayout(orientation="vertical", padding=10, spacing=10)

        # Scrollable container
        scroll_view = ScrollView(size_hint=(1, 1), do_scroll_x=False)

        # Error Label: Uses the full width of the popup and wraps text
        self.error_label = Label(
            text=message,
            size_hint=(1, None),  # Full width, dynamic height
            text_size=(self.width - 40, None),  # Forces text wrapping
            halign="left",
            valign="top",
        )
        self.error_label.bind(
            size=self._update_text_size, texture_size=self._adjust_label_height
        )

        # Add label inside ScrollView
        scroll_view.add_widget(self.error_label)

        # Close button
        close_button = Button(
            text=strings.BUTTON_CLOSE_POPUP, size_hint=(1, None), height=100
        )
        close_button.bind(on_press=self.dismiss)

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
