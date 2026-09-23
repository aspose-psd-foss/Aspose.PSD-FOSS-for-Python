from aspose_psd_foss.layers.layerblendmodemapper import LayerBlendModeMapper
from aspose_psd_foss.layers.rawlayermasksection import RawLayerMaskSection
from aspose_psd_foss.layers.rawlayerblendingrangessection import RawLayerBlendingRangesSection

class LayerRawData:
    """Stores raw PSD layer record data required for byte-preserving saves."""

    Empty = None

    def __init__(self, flags, blend_mode_key, channel_info, layer_mask_section, blending_ranges_section, additional_layer_data):
        """Initializes a new instance of the LayerRawData class.

        Args:
            flags: The original PSD layer flags byte.
            blend_mode_key: The original 4-byte PSD blend mode key.
            channel_info: The parsed layer channel metadata.
            layer_mask_section: The raw layer mask subsection.
            blending_ranges_section: The raw blending ranges subsection.
            additional_layer_data: The remaining additional layer data bytes.
        """
        self.Flags = flags
        self.BlendModeKey = blend_mode_key
        self.ChannelInfo = channel_info
        self.LayerMaskSection = layer_mask_section
        self.BlendingRangesSection = blending_ranges_section
        self.AdditionalLayerData = additional_layer_data

    @classmethod
    def empty_instance(cls):
        """Gets an empty raw layer data block."""
        if cls.Empty is None:
            cls.Empty = cls(
                0,
                LayerBlendModeMapper.normal_blend_mode_key,
                [],
                RawLayerMaskSection.Empty,
                RawLayerBlendingRangesSection.Empty,
                []
            )
        return cls.Empty

    @property
    def Flags(self):
        """Gets the original PSD layer flags byte."""
        return self._flags

    @Flags.setter
    def Flags(self, value):
        self._flags = value

    @property
    def BlendModeKey(self):
        """Gets the original 4-byte PSD blend mode key."""
        return self._blend_mode_key

    @BlendModeKey.setter
    def BlendModeKey(self, value):
        self._blend_mode_key = value

    @property
    def ChannelInfo(self):
        """Gets the parsed per-channel metadata from the layer record."""
        return self._channel_info

    @ChannelInfo.setter
    def ChannelInfo(self, value):
        self._channel_info = value

    @property
    def LayerMaskSection(self):
        """Gets the raw layer mask subsection including its length field."""
        return self._layer_mask_section

    @LayerMaskSection.setter
    def LayerMaskSection(self, value):
        self._layer_mask_section = value

    @property
    def BlendingRangesSection(self):
        """Gets the raw blending ranges subsection including its length field."""
        return self._blending_ranges_section

    @BlendingRangesSection.setter
    def BlendingRangesSection(self, value):
        self._blending_ranges_section = value

    @property
    def AdditionalLayerData(self):
        """Gets all remaining additional layer data after the Pascal layer name."""
        return self._additional_layer_data

    @AdditionalLayerData.setter
    def AdditionalLayerData(self, value):
        self._additional_layer_data = value

    def with_blend_mode_key(self, blend_mode_key):
        """Creates a raw data copy with a replacement blend mode key.

        Args:
            blend_mode_key: The replacement 4-byte PSD blend mode key.

        Returns:
            The updated raw layer data.
        """
        return LayerRawData(
            self.Flags,
            blend_mode_key,
            self.ChannelInfo,
            self.LayerMaskSection,
            self.BlendingRangesSection,
            self.AdditionalLayerData
        )
