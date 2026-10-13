from __future__ import annotations

from typing import List, Optional

from ..bigendianreader import BigEndianReader
from ..bigendianwriter import BigEndianWriter
from ..coreexceptions.notsupportedexception import NotSupportedException
from ..rectangle import Rectangle
from .blendmode import BlendMode
from .layerblendmodemapper import LayerBlendModeMapper
from .layerblendingrangesdata import LayerBlendingRangesData
from .layerblendingrangesinfo import LayerBlendingRangesInfo
from .layermaskdatashort import LayerMaskDataShort
from .layermaskinfo import LayerMaskInfo
from .layerrawdata import LayerRawData
from .channelinformation import ChannelInformation
from .psdlayerchannelinfo import PsdLayerChannelInfo


class Layer:
    # Gets the fixed-size byte count of the layer record trailer fields.
    LAYER_TRAILER_SIZE = 16
    LayerTrailerSize = 16

    # Stores the current layer name.
    _name: str = ""
    # Stores the current layer visibility flag.
    _is_visible: bool = True
    # Stores the current layer opacity value.
    _opacity: int = 255
    # Stores raw PSD layer record data required for byte-preserving saves.
    _raw_data: LayerRawData = LayerRawData.empty()
    # Stores the current layer bounds in document coordinates.
    _bounds: Rectangle = Rectangle(0, 0, 0, 0)
    # Stores the PSD clipping value for the layer.
    _clipping: int = 0
    # Stores the PSD blend mode exposed by the layer record.
    _blend_mode: BlendMode = BlendMode.NORMAL
    # Indicates whether the layer has a pending in-memory mutation.
    _has_mutated: bool = False

    def __init__(self):
        pass

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, value: str) -> None:
        if self._name != value:
            self._name = value
            self._has_mutated = True

    @property
    def bounds(self) -> Rectangle:
        return Rectangle(0, 0, self._bounds.width, self._bounds.height)

    @property
    def width(self) -> int:
        return self._bounds.width

    @property
    def height(self) -> int:
        return self._bounds.height

    @property
    def top(self) -> int:
        return self._bounds.top

    @top.setter
    def top(self, value: int) -> None:
        if self._bounds.top != value:
            self._set_bounds(
                Rectangle.from_ltrb(
                    self._bounds.left, value, self._bounds.right, self._bounds.bottom
                )
            )

    @property
    def left(self) -> int:
        return self._bounds.left

    @left.setter
    def left(self, value: int) -> None:
        if self._bounds.left != value:
            self._set_bounds(
                Rectangle.from_ltrb(
                    value, self._bounds.top, self._bounds.right, self._bounds.bottom
                )
            )

    @property
    def bottom(self) -> int:
        return self._bounds.bottom

    @bottom.setter
    def bottom(self, value: int) -> None:
        if self._bounds.bottom != value:
            self._set_bounds(
                Rectangle.from_ltrb(
                    self._bounds.left, self._bounds.top, self._bounds.right, value
                )
            )

    @property
    def right(self) -> int:
        return self._bounds.right

    @right.setter
    def right(self, value: int) -> None:
        if self._bounds.right != value:
            self._set_bounds(
                Rectangle.from_ltrb(
                    self._bounds.left, self._bounds.top, value, self._bounds.bottom
                )
            )

    @property
    def is_visible(self) -> bool:
        return self._is_visible

    @is_visible.setter
    def is_visible(self, value: bool) -> None:
        if self._is_visible != value:
            self._is_visible = value
            self._has_mutated = True

    @property
    def IsVisible(self) -> bool:
        return self.is_visible

    @IsVisible.setter
    def IsVisible(self, value: bool) -> None:
        self.is_visible = value

    @property
    def opacity(self) -> int:
        return self._opacity

    @opacity.setter
    def opacity(self, value: int) -> None:
        if self._opacity != value:
            self._opacity = value
            self._has_mutated = True

    @property
    def clipping(self) -> int:
        return self._clipping

    @clipping.setter
    def clipping(self, value: int) -> None:
        if self._clipping != value:
            self._clipping = value
            self._has_mutated = True

    @property
    def blend_mode_key(self) -> BlendMode:
        return self._blend_mode

    @blend_mode_key.setter
    def blend_mode_key(self, value: BlendMode) -> None:
        self._set_blend_mode_key(value)

    @property
    def channels_count(self) -> int:
        return len(self.channel_info)

    @property
    def channel_information(self) -> List[ChannelInformation]:
        return [
            ChannelInformation.from_layer_channel_info(ci) for ci in self.channel_info
        ]

    @channel_information.setter
    def channel_information(self, value):
        raise NotSupportedException(
            "Changing layer channel information is not supported by this FOSS build."
        )

    @property
    def channels(self) -> List[PsdLayerChannelInfo]:
        return [
            PsdLayerChannelInfo(ci.channel_id, ci.data_length) for ci in self.channel_info
        ]

    @property
    def has_mask_data(self) -> bool:
        return len(self._raw_data.layer_mask_section.raw_data) > 4

    @property
    def has_blending_ranges_data(self) -> bool:
        return len(self._raw_data.blending_ranges_section.raw_data) > 4

    @property
    def _has_mask_data(self) -> bool:
        return self.has_mask_data

    @property
    def _has_blending_ranges_data(self) -> bool:
        return self.has_blending_ranges_data

    @property
    def mask_info(self) -> LayerMaskInfo:
        return LayerMaskInfo(
            self.has_mask_data, len(self._raw_data.layer_mask_section.raw_data)
        )

    @property
    def blending_ranges_info(self) -> LayerBlendingRangesInfo:
        return LayerBlendingRangesInfo(
            self.has_blending_ranges_data,
            len(self._raw_data.blending_ranges_section.raw_data),
        )

    @property
    def channel_info(self) -> List:
        return self._raw_data.channel_info

    @property
    def raw_flags(self) -> int:
        return self._raw_data.flags

    @property
    def raw_layer_mask_section(self):
        return self._raw_data.layer_mask_section

    @property
    def raw_layer_blending_ranges_section(self):
        return self._raw_data.blending_ranges_section

    @property
    def layer_mask_data(self) -> Optional[LayerMaskDataShort]:
        if not self.has_mask_data:
            return None
        return LayerMaskDataShort()

    @layer_mask_data.setter
    def layer_mask_data(self, value):
        raise NotSupportedException(
            "Changing layer mask data is not supported by this FOSS build."
        )

    @property
    def layer_blending_ranges_data(self) -> LayerBlendingRangesData:
        return LayerBlendingRangesData.from_raw_length(
            len(self._raw_data.blending_ranges_section.raw_data)
        )

    @layer_blending_ranges_data.setter
    def layer_blending_ranges_data(self, value):
        raise NotSupportedException(
            "Changing layer blending ranges data is not supported by this FOSS build."
        )

    @property
    def additional_layer_data(self) -> bytes:
        return self._raw_data.additional_layer_data

    @property
    def raw_blend_mode_key(self) -> str:
        return self._raw_data.blend_mode_key

    @property
    def has_mutated(self) -> bool:
        return self._has_mutated

    def mark_mutated(self) -> None:
        self._has_mutated = True

    def _set_bounds(self, bounds: Rectangle) -> None:
        if self._bounds != bounds:
            self._bounds = bounds
            self._has_mutated = True

    def _set_blend_mode_key(self, blend_mode: BlendMode) -> None:
        if self._blend_mode != blend_mode:
            self._blend_mode = blend_mode
            key = LayerBlendModeMapper.get_blend_mode_key(blend_mode)
            self._raw_data = self._raw_data.with_blend_mode_key(key)
            self._has_mutated = True

    @classmethod
    def load(cls, reader: BigEndianReader, is_large_document: bool) -> "Layer":
        from .layerrecordreader import LayerRecordReader
        return LayerRecordReader.load(reader, is_large_document)

    def write(self, writer: BigEndianWriter, is_large_document: bool) -> None:
        from .layerrecordwriter import LayerRecordWriter
        LayerRecordWriter.write(self, writer, is_large_document)

    @classmethod
    def create_parsed(
        cls,
        name: str,
        bounds: Rectangle,
        is_visible: bool,
        opacity: int,
        clipping: int,
        blend_mode: BlendMode,
        raw_data: LayerRawData,
    ) -> "Layer":
        layer = cls()
        layer._name = name
        layer._bounds = bounds
        layer._is_visible = is_visible
        layer._opacity = opacity
        layer._clipping = clipping
        layer._blend_mode = blend_mode
        layer._raw_data = raw_data
        layer._has_mutated = False
        return layer
