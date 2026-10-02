from aspose_psd_foss.layers.layerchannelinfo import LayerChannelInfo
from aspose_psd_foss.layers.rawlayermasksection import RawLayerMaskSection
from aspose_psd_foss.layers.rawlayerblendingrangessection import RawLayerBlendingRangesSection
from aspose_psd_foss.layers.layerblendmodemapper import LayerBlendModeMapper


class LayerRawData:
    Empty: "LayerRawData" = None  # type: ignore

    @classmethod
    def empty(cls) -> "LayerRawData":
        return cls(
            0,
            LayerBlendModeMapper.NORMAL_BLEND_MODE_KEY,
            [],
            RawLayerMaskSection.empty(),
            RawLayerBlendingRangesSection.empty(),
            []
        )

    def __init__(
        self,
        flags,
        blend_mode_key,
        channel_info,
        layer_mask_section,
        blending_ranges_section,
        additional_layer_data
    ):
        self.flags = flags
        self.blend_mode_key = blend_mode_key
        self.channel_info = channel_info
        self.layer_mask_section = layer_mask_section
        self.blending_ranges_section = blending_ranges_section
        self.additional_layer_data = additional_layer_data

    def with_blend_mode_key(self, blend_mode_key):
        return LayerRawData(
            self.flags,
            blend_mode_key,
            self.channel_info,
            self.layer_mask_section,
            self.blending_ranges_section,
            self.additional_layer_data
        )

    # Alias to match C# naming
    def WithBlendModeKey(self, blend_mode_key):
        return self.with_blend_mode_key(blend_mode_key)


# Assign the static Empty instance after class definition
LayerRawData.Empty = LayerRawData.empty()

