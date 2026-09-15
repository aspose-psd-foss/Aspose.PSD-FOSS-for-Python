# Represents PSD layer blending ranges data.
from aspose_psd_foss.layers.blendrange import BlendRange


class LayerBlendingRangesData:
    # Stores the PSD blending-ranges subsection length prefix size.
    _LENGTH_FIELD_SIZE = 4  # sizeof(uint)

    def __init__(self):
        self.composite_blend_range = BlendRange()
        self.channel_blend_ranges = []
        self._length = 0

    @property
    def composite_blend_range(self):
        """Gets or sets the composite blend range."""
        return self._composite_blend_range

    @composite_blend_range.setter
    def composite_blend_range(self, value):
        self._composite_blend_range = value

    @property
    def channel_blend_ranges(self):
        """Gets or sets the per-channel blend ranges."""
        return self._channel_blend_ranges

    @channel_blend_ranges.setter
    def channel_blend_ranges(self, value):
        self._channel_blend_ranges = value

    @property
    def length(self):
        """Gets the blending ranges data length in bytes."""
        return self._length

    @classmethod
    def _from_raw_length(cls, length):
        """Creates public blending ranges data from a preserved raw subsection length."""
        instance = cls()
        instance._length = max(0, length - cls._LENGTH_FIELD_SIZE)
        return instance

    @classmethod
    def from_raw_length(cls, length):
        """Creates public blending ranges data from a preserved raw subsection length."""
        return cls._from_raw_length(length)


# Import after class definition to avoid circular imports if any.
#from aspose_psd_foss.blend_range import BlendRange
