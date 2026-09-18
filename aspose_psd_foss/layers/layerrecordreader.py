from typing import Any

class Layer:
    """
    Represents a PSD layer with basic properties such as name, bounds,
    visibility, opacity, and blend mode.
    """

    def __init__(self) -> None:
        self._name: str = ""
        self._bounds: Any = None
        self._visibility: bool = True
        self._opacity: int = 255
        self._blend_mode: Any = None

    def set_name(self, name: str) -> None:
        """Sets the layer's name."""
        self._name = name

    def set_bounds(self, bounds: Any) -> None:
        """Sets the layer's rectangular bounds."""
        self._bounds = bounds

    def set_visibility(self, visible: bool) -> None:
        """Sets the layer's visibility flag."""
        self._visibility = visible

    def set_opacity(self, opacity: int) -> None:
        """
        Sets the layer's opacity.

        Args:
            opacity: An integer in the range 0-255 where 255 is fully opaque.
        """
        self._opacity = opacity

    def set_blend_mode(self, blend_mode: Any) -> None:
        """Sets the layer's blend mode."""
        self._blend_mode = blend_mode

    # Optional getters for external use
    def get_name(self) -> str:
        return self._name

    def get_bounds(self) -> Any:
        return self._bounds

    def is_visible(self) -> bool:
        return self._visibility

    def get_opacity(self) -> int:
        return self._opacity

    def get_blend_mode(self) -> Any:
        return self._blend_mode
