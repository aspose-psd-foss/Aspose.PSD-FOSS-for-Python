from __future__ import annotations

from typing import List

from aspose_psd_foss.layers.layerchannelinfo import LayerChannelInfo
from aspose_psd_foss.layers.rawlayerblendingrangessection import RawLayerBlendingRangesSection
from aspose_psd_foss.layers.rawlayermasksection import RawLayerMaskSection


class LayerRawData:
    """
    Stores raw PSD layer record data required for byte-preserving saves.
    """

    EMPTY: "LayerRawData"

    def __init__(
        self,
        flags: int,
        blend_mode_key: str,
        channel_info: List[LayerChannelInfo],
        layer_mask_section: RawLayerMaskSection,
        blending_ranges_section: RawLayerBlendingRangesSection,
        additional_layer_data: bytes,
    ):
        """
        Initializes a new instance of the LayerRawData class.

        :param flags: The original PSD layer flags byte.
        :param blend_mode_key: The original 4-byte PSD blend mode key.
        :param channel_info: The parsed layer channel metadata.
        :param layer_mask_section: The raw layer mask subsection.
        :param blending_ranges_section: The raw blending ranges subsection.
        :param additional_layer_data: The remaining additional layer data bytes.
        """
        self.flags = flags
        self.blend_mode_key = blend_mode_key
        self.channel_info = channel_info
        self.layer_mask_section = layer_mask_section
        self.blending_ranges_section = blending_ranges_section
        self.additional_layer_data = additional_layer_data

    def with_blend_mode_key(self, blend_mode_key: str) -> "LayerRawData":
        """
        Creates a raw data copy with a replacement blend mode key.

        :param blend_mode_key: The replacement 4-byte PSD blend mode key.
        :return: The updated raw layer data.
        """
        return LayerRawData(
            self.flags,
            blend_mode_key,
            self.channel_info,
            self.layer_mask_section,
            self.blending_ranges_section,
            self.additional_layer_data,
        )


# Initialize the static EMPTY instance
LayerRawData.EMPTY = LayerRawData(
    0,
    LayerBlendModeMapper.NormalBlendModeKey,
    [],
    RawLayerMaskSection.Empty,
    RawLayerBlendingRangesSection.Empty,
    b"",
)
