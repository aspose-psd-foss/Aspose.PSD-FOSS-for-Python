class LayerBlendingRangesData:
    """
    Represents PSD layer blending ranges data.
    """

    _length_field_size = 4

    def __init__(self):
        """
        Initializes a new instance of the <see cref="LayerBlendingRangesData"/> class.
        """
        self._composite_blend_range = None
        self._channel_blend_ranges = None
        self._length = 0

    @property
    def composite_blend_range(self):
        """
        Gets or sets the composite blend range.
        """
        if self._composite_blend_range is None:
            from aspose_psd_foss.layers.blendrange import BlendRange
            self._composite_blend_range = BlendRange()
        return self._composite_blend_range

    @composite_blend_range.setter
    def composite_blend_range(self, value):
        self._composite_blend_range = value

    @property
    def channel_blend_ranges(self):
        """
        Gets or sets the per-channel blend ranges.
        """
        if self._channel_blend_ranges is None:
            self._channel_blend_ranges = []
        return self._channel_blend_ranges

    @channel_blend_ranges.setter
    def channel_blend_ranges(self, value):
        self._channel_blend_ranges = value

    @property
    def length(self):
        """
        Gets the blending ranges data length in bytes.
        """
        return self._length

    @classmethod
    def from_raw_length(cls, length):
        """
        Creates public blending ranges data from a preserved raw subsection length.
        """
        return cls._from_raw_length_internal(max(0, length - cls._length_field_size))

    @classmethod
    def _from_raw_length_internal(cls, length):
        instance = cls()
        instance._length = length
        return instance
