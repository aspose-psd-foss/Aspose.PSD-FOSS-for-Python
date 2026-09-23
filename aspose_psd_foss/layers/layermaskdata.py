from aspose_psd_foss.rectangle import Rectangle
from aspose_psd_foss.layers.layermaskflags import LayerMaskFlags


class LayerMaskData:
    """
    Defines the base class for PSD layer mask data.
    """

    def __init__(self):
        self._image_data = []
        self._mask_rectangle = Rectangle()

    @property
    def bottom(self):
        """
        Gets or sets the bottom layer mask position.
        """
        return self._mask_rectangle.bottom

    @bottom.setter
    def bottom(self, value):
        self._mask_rectangle.bottom = value

    @property
    def data_size(self):
        """
        Gets the size of the layer mask data.
        """
        return len(self._image_data)

    @property
    def default_color(self):
        """
        Gets or sets the default layer mask color.
        """
        return self._default_color

    @default_color.setter
    def default_color(self, value):
        self._default_color = value

    @property
    def flags(self):
        """
        Gets or sets the layer mask flags.
        """
        return self._flags

    @flags.setter
    def flags(self, value):
        self._flags = value

    @property
    def image_data(self):
        """
        Gets or sets the layer mask image data.
        """
        return self._image_data

    @image_data.setter
    def image_data(self, value):
        if value is None:
            raise ValueError("Value cannot be None")
        self._image_data = value

    @property
    def left(self):
        """
        Gets or sets the left layer mask position.
        """
        return self._mask_rectangle.left

    @left.setter
    def left(self, value):
        self._mask_rectangle.left = value

    @property
    def mask_rectangle(self):
        """
        Gets or sets the mask rectangle.
        """
        return self._mask_rectangle

    @mask_rectangle.setter
    def mask_rectangle(self, value):
        self._mask_rectangle = value

    @property
    def right(self):
        """
        Gets or sets the right layer mask position.
        """
        return self._mask_rectangle.right

    @right.setter
    def right(self, value):
        self._mask_rectangle.right = value

    @property
    def top(self):
        """
        Gets or sets the top layer mask position.
        """
        return self._mask_rectangle.top

    @top.setter
    def top(self, value):
        self._mask_rectangle.top = value
