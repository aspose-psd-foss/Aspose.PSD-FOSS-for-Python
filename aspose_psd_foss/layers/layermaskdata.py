from __future__ import annotations

import abc

from aspose_psd_foss.rectangle import Rectangle
from aspose_psd_foss.layer_mask_flags import LayerMaskFlags


class LayerMaskData(abc.ABC):
    """
    Defines the base class for PSD layer mask data.
    """

    def __init__(self) -> None:
        # Stores the layer mask image data.
        self._image_data: bytes = b""
        # Stores the layer mask rectangle.
        self._mask_rectangle: Rectangle = Rectangle()

        # Gets or sets the default layer mask color.
        self.default_color: int = 0
        # Gets or sets the layer mask flags.
        self.flags: LayerMaskFlags = LayerMaskFlags()

    @property
    def bottom(self) -> int:
        """
        Gets or sets the bottom layer mask position.
        """
        return self._mask_rectangle.bottom

    @bottom.setter
    def bottom(self, value: int) -> None:
        self._mask_rectangle.bottom = value

    @property
    def data_size(self) -> int:
        """
        Gets the size of the layer mask data.
        """
        return len(self._image_data)

    @property
    def image_data(self) -> bytes:
        """
        Gets or sets the layer mask image data.
        """
        return self._image_data

    @image_data.setter
    def image_data(self, value: bytes) -> None:
        if value is None:
            raise ValueError("image_data cannot be None")
        self._image_data = value

    @property
    def left(self) -> int:
        """
        Gets or sets the left layer mask position.
        """
        return self._mask_rectangle.left

    @left.setter
    def left(self, value: int) -> None:
        self._mask_rectangle.left = value

    @property
    def mask_rectangle(self) -> Rectangle:
        """
        Gets or sets the mask rectangle.
        """
        return self._mask_rectangle

    @mask_rectangle.setter
    def mask_rectangle(self, value: Rectangle) -> None:
        self._mask_rectangle = value

    @property
    def right(self) -> int:
        """
        Gets or sets the right layer mask position.
        """
        return self._mask_rectangle.right

    @right.setter
    def right(self, value: int) -> None:
        self._mask_rectangle.right = value

    @property
    def top(self) -> int:
        """
        Gets or sets the top layer mask position.
        """
        return self._mask_rectangle.top

    @top.setter
    def top(self, value: int) -> None:
        self._mask_rectangle.top = value
