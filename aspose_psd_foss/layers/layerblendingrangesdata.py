from aspose_psd_foss.layers.blendrange import BlendRange


class LayerBlendingRangesData:
    LENGTH_FIELD_SIZE = 4

    def __init__(self, length: int = 0):
        self._length: int = length
        self.composite_blend_range: BlendRange = BlendRange()
        self.channel_blend_ranges: list[BlendRange] = []

    @property
    def length(self) -> int:
        return self._length

    @classmethod
    def from_raw_length(cls, length: int):
        return cls(max(0, length - cls.LENGTH_FIELD_SIZE))
