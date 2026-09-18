"""Defines layer mask data for layers that have only a raster or vector mask."""

from .layermaskdata import LayerMaskData


class LayerMaskDataShort(LayerMaskData):
    """LayerMaskDataShort inherits from LayerMaskData and adds padding information."""

    def __init__(self):
        super().__init__()
        self._padding = 0

    @property
    def padding(self):
        """Gets or sets the layer mask padding."""
        return self._padding

    @padding.setter
    def padding(self, value):
        self._padding = int(value)
