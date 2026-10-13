import sys
from aspose_psd_foss.layers.blendrange import BlendRange


class LayerBlendingRangesData:
    """Represents PSD layer blending ranges data."""

    _LENGTH_FIELD_SIZE = 4  # size of uint in bytes

    def __init__(self):
        """Initializes a new instance of the LayerBlendingRangesData class."""
        self.composite_blend_range = BlendRange()
        self.channel_blend_ranges = []
        self._length = 0

    @property
    def length(self):
        """Gets the blending ranges data length in bytes."""
        return self._length

    @classmethod
    def from_raw_length(cls, length):
        """Creates public blending ranges data from a preserved raw subsection length.

        Args:
            length: The raw subsection length in bytes.

        Returns:
            The public blending ranges data.
        """
        instance = cls()
        instance._length = max(0, length - cls._LENGTH_FIELD_SIZE)
        return instance
