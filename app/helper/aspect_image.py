from kivy.uix.image import Image
from kivy.properties import StringProperty

from helper.file_handling import map_selected_city_2short_name, get_logo_file_path


class AspectImage(Image):
    source = StringProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.bind(texture=self._on_texture, size=self._on_size)

    def _on_texture(self, *args):
        self._update_size()

    def _on_size(self, *args):
        self._update_size()

    def _update_size(self):
        if self.texture:
            image_ratio = self.texture.width / self.texture.height
            self.size_hint_x = None
            self.width = self.height * image_ratio


def get_team122_image() -> AspectImage:
    return AspectImage(
        source=get_logo_file_path("team122"),
        # values are highly specific to used PNG
        size_hint=(0.35, 0.35),
        pos_hint={"center_x": 0.5, "center_y": 0.5},
    )


def get_team122_small_image() -> AspectImage:
    return AspectImage(
        source=get_logo_file_path("team122"),
        # values are highly specific to used PNG
        size_hint=(0.035, 0.035),
        pos_hint={"right": 0.98, "top": 0.96},
    )


def get_city_image(selected_city_long_name: str) -> AspectImage:
    selected_city = map_selected_city_2short_name(
        selected_city_long_name.strip("_small")
    )

    if selected_city == "Hallein":
        if "small" in selected_city_long_name:
            return AspectImage(
                source=get_logo_file_path(selected_city),
                # values are highly specific to used PNG
                size_hint=(1.05, 1.05),
                pos_hint={"x": -0.05, "y": -0.05},
            )
        else:
            return AspectImage(
                source=get_logo_file_path(selected_city),
                # values are highly specific to used PNG
                size_hint=(None, 0.21),
                pos_hint={"x": 0, "y": 0.79},
            )
    elif selected_city == "Dürrnberg":
        if "small" in selected_city_long_name:
            return AspectImage(
                source=get_logo_file_path(selected_city),
                # values are highly specific to used PNG
                size_hint=(1, 1),
                pos_hint={"x": 0, "y": 0},
            )
        else:
            return AspectImage(
                source=get_logo_file_path(selected_city),
                # values are highly specific to used PNG
                size_hint=(None, 0.205),
                pos_hint={"x": 0, "y": 0.795},
            )
    elif selected_city == "Altenmarkt":
        if "small" in selected_city_long_name:
            return AspectImage(
                source=get_logo_file_path(selected_city),
                # values are highly specific to used PNG
                size_hint=(None, 1.1),
                pos_hint={"x": -0.07, "y": -0.07},
            )
        else:
            return AspectImage(
                source=get_logo_file_path(selected_city),
                # values are highly specific to used PNG
                size_hint=(None, 0.215),
                pos_hint={"x": 0, "y": 0.788},
            )

    return AspectImage(source="")


def get_state_image(selected_state: str) -> AspectImage:
    if selected_state in ["Salzburg", "Bayern"]:
        return AspectImage(
            source=get_logo_file_path(selected_state),
            # values are highly specific to used PNG
            size_hint=(0.98, 0.98),
            pos_hint={"x": 0, "y": 0},
        )

    return AspectImage(source="")
