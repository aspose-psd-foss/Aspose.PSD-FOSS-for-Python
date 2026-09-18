# Defines the base class for PSD layer mask data.
import abc

from aspose_psd_foss.rectangle import Rectangle
from aspose_psd_foss.layers.layermaskflags import LayerMaskFlags


class LayerMaskData(abc.ABC):
    """Defines the base class for PSD layer mask data."""

    def __init__(self):
        # Stores the layer mask image data.
        self._image_data: bytes = b""

        # Stores the layer mask rectangle.
        self._mask_rectangle: Rectangle = Rectangle()

        # Gets or sets the default layer mask color.
        self.default_color: int = 0

        # Gets or sets the layer mask flags.
        self.flags: LayerMaskFlags = LayerMaskFlags(0)

    # Gets or sets the bottom layer mask position.
    @property
    def bottom(self) -> int:
        return self._mask_rectangle.bottom

    @bottom.setter
    def bottom(self, value: int) -> None:
        self._mask_rectangle.bottom = value

    # Gets the size of the layer mask data.
    @property
    def data_size(self) -> int:
        return len(self._image_data)

    # Gets or sets the default layer mask color.
    # (Already provided as public attribute `default_color`.)

    # Gets or sets the layer mask flags.
    # (Already provided as public attribute `flags`.)

    # Gets or sets the layer mask image data.
    @property
    def image_data(self) -> bytes:
        return self._image_data

    @image_data.setter
    def image_data(self, value: bytes) -> None:
        if value is None:
            raise ValueError("value cannot be None")
        self._image_data = value

    # Gets or sets the left layer mask position.
    @property
    def left(self) -> int:
        return self._mask_rectangle.left

    @left.setter
    def left(self, value: int) -> None:
        self._mask_rectangle.left = value

    # Gets or sets the mask rectangle.
    @property
    def mask_rectangle(self) -> Rectangle:
        return self._mask_rectangle

    @mask_rectangle.setter
    def mask_rectangle(self, value: Rectangle) -> None:
        self._mask_rectangle = value

    # Gets or sets the right layer mask position.
    @property
    def right(self) -> int:
        return self._mask_rectangle.right

    @right.setter
    def right(self, value: int) -> None:
        self._mask_rectangle.right = value

    # Gets or sets the top layer mask position.
    @property
    def top(self) -> int:
        return self._mask_rectangle.top

    @top.setter
    def top(self, value: int) -> None:
        self._mask_rectangle.top = value
