from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.core.window import Window
from kivy.utils import platform


class FirstScreen(Screen):
    pass


class SecondScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation="vertical")
        self.back_button = Button(text="Go Back")
        self.back_button.bind(on_press=self.go_back)
        layout.add_widget(self.back_button)
        self.add_widget(layout)

    def go_back(self, *args):
        print("Going back to first screen...")
        self.manager.current = "first"  # Use the screen manager to switch back


class MyApp(App):
    def build(self):
        self.sm = ScreenManager()
        self.first = FirstScreen(name="first")
        self.second = SecondScreen(name="second")

        self.sm.add_widget(self.first)
        self.sm.add_widget(self.second)

        if platform == "android":
            Window.bind(on_keyboard=self.on_android_back)

        return self.sm

    def on_android_back(self, window, key, *args):
        if key == 27:
            current_screen = self.sm.current_screen
            if isinstance(current_screen, SecondScreen):
                # Call the same method as the button
                current_screen.go_back()
                return True
        return False


if __name__ == "__main__":
    MyApp().run()
