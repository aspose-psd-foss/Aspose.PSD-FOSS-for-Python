from aspose_psd_foss.layers.layermaskdata import LayerMaskData


class LayerMaskDataShort(LayerMaskData):
    """Defines layer mask data for layers that have only a raster or vector mask."""

    def __init__(self):
        """Initializes a new instance of the <see cref="LayerMaskDataShort"/> class."""
        super().__init__()

    @property
    def padding(self) -> int:
        """Gets or sets the layer mask padding."""
        return self._padding

    @padding.setter
    def padding(self, value: int) -> None:
        self._padding = value
