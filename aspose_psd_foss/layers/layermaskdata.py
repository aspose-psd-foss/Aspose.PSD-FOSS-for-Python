from __future__ import annotations

from abc import ABC
from typing import Any

from aspose_psd_foss.rectangle import Rectangle
from aspose_psd_foss.layers.layermaskflags import LayerMaskFlags

class LayerMaskData(ABC):
    """
    Defines the base class for PSD layer mask data.
    """

    def __init__(self) -> None:
        # Stores the layer mask image data.
        self._image_data: bytearray = bytearray()
        # Stores the layer mask rectangle.
        self._mask_rectangle: Rectangle = Rectangle()
        # Stores the default layer mask color.
        self._default_color: int = 0
        # Stores the layer mask flags.
        self._flags: LayerMaskFlags = LayerMaskFlags.NONE

    @property
    def bottom(self) -> int:
        """Gets or sets the bottom layer mask position."""
        return self._mask_rectangle.bottom

    @bottom.setter
    def bottom(self, value: int) -> None:
        self._mask_rectangle.bottom = value

    @property
    def data_size(self) -> int:
        """Gets the size of the layer mask data."""
        return len(self._image_data)

    @property
    def default_color(self) -> int:
        """Gets or sets the default layer mask color."""
        return self._default_color

    @default_color.setter
    def default_color(self, value: int) -> None:
        self._default_color = value

    @property
    def flags(self) -> LayerMaskFlags:
        """Gets or sets the layer mask flags."""
        return self._flags

    @flags.setter
    def flags(self, value: LayerMaskFlags) -> None:
        self._flags = value

    @property
    def image_data(self) -> bytearray:
        """Gets or sets the layer mask image data."""
        return self._image_data

    @image_data.setter
    def image_data(self, value: bytearray) -> None:
        if value is None:
            raise ValueError("value cannot be None")
        self._image_data = value

    @property
    def left(self) -> int:
        """Gets or sets the left layer mask position."""
        return self._mask_rectangle.left

    @left.setter
    def left(self, value: int) -> None:
        self._mask_rectangle.left = value

    @property
    def mask_rectangle(self) -> Rectangle:
        """Gets or sets the mask rectangle."""
        return self._mask_rectangle

    @mask_rectangle.setter
    def mask_rectangle(self, value: Rectangle) -> None:
        self._mask_rectangle = value

    @property
    def right(self) -> int:
        """Gets or sets the right layer mask position."""
        return self._mask_rectangle.right

    @right.setter
    def right(self, value: int) -> None:
        self._mask_rectangle.right = value

    @property
    def top(self) -> int:
        """Gets or sets the top layer mask position."""
        return self._mask_rectangle.top

    @top.setter
    def top(self, value: int) -> None:
        self._mask_rectangle.top = value
