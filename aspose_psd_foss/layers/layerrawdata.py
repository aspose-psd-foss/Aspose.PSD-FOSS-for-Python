from typing import ClassVar

from .rawlayermasksection import RawLayerMaskSection
from .rawlayerblendingrangessection import RawLayerBlendingRangesSection
from .layerchannelinfo import LayerChannelInfo


class LayerRawData:
    """
    Stores raw PSD layer record data required for byte‑preserving saves.
    """

    # Class level Empty placeholder; will be assigned after the class definition.
    Empty: ClassVar["LayerRawData"]

    def __init__(
        self,
        flags,
        blend_mode_key,
        channel_info,
        layer_mask_section,
        blending_ranges_section,
        additional_layer_data,
    ):
        """
        Initializes a new instance of LayerRawData.

        :param flags: The original PSD layer flags byte.
        :param blend_mode_key: The original 4‑byte PSD blend mode key.
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

    @property
    def flags(self):
        """Gets the original PSD layer flags byte."""
        return self._flags

    @flags.setter
    def flags(self, value):
        self._flags = value

    @property
    def blend_mode_key(self):
        """Gets the original 4‑byte PSD blend mode key."""
        return self._blend_mode_key

    @blend_mode_key.setter
    def blend_mode_key(self, value):
        self._blend_mode_key = value

    @property
    def channel_info(self):
        """Gets the parsed per‑channel metadata from the layer record."""
        return self._channel_info

    @channel_info.setter
    def channel_info(self, value):
        self._channel_info = value

    @property
    def layer_mask_section(self):
        """Gets the raw layer mask subsection including its length field."""
        return self._layer_mask_section

    @layer_mask_section.setter
    def layer_mask_section(self, value):
        self._layer_mask_section = value

    @property
    def blending_ranges_section(self):
        """Gets the raw blending ranges subsection including its length field."""
        return self._blending_ranges_section

    @blending_ranges_section.setter
    def blending_ranges_section(self, value):
        self._blending_ranges_section = value

    @property
    def additional_layer_data(self):
        """Gets all remaining additional layer data after the Pascal layer name."""
        return self._additional_layer_data

    @additional_layer_data.setter
    def additional_layer_data(self, value):
        self._additional_layer_data = value

    def with_blend_mode_key(self, blend_mode_key):
        """
        Creates a raw data copy with a replacement blend mode key.

        :param blend_mode_key: The replacement 4‑byte PSD blend mode key.
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


# Assign the Empty instance after the class definition.
LayerRawData.Empty = LayerRawData(
    0,
    b'norm',  # Default normal blend mode key
    [],
    RawLayerMaskSection(b""),
    RawLayerBlendingRangesSection(b""),
    [],
)
