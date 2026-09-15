from __future__ import annotations

from typing import List, Optional, Any

from aspose_psd_foss.big_endian_reader import BigEndianReader
from aspose_psd_foss.big_endian_writer import BigEndianWriter
from aspose_psd_foss.rectangle import Rectangle
from aspose_psd_foss.blend_mode import BlendMode
from aspose_psd_foss.layer_raw_data import LayerRawData
from aspose_psd_foss.layer_blend_mode_mapper import LayerBlendModeMapper
from aspose_psd_foss.layer_record_reader import LayerRecordReader
from aspose_psd_foss.layer_record_writer import LayerRecordWriter
from aspose_psd_foss.channel_information import ChannelInformation
from aspose_psd_foss.psd_layer_channel_info import PsdLayerChannelInfo
from aspose_psd_foss.layer_mask_info import LayerMaskInfo
from aspose_psd_foss.layer_blending_ranges_info import LayerBlendingRangesInfo
from aspose_psd_foss.layer_mask_data import LayerMaskData
from aspose_psd_foss.layer_mask_data_short import LayerMaskDataShort
from aspose_psd_foss.layer_blending_ranges_data import LayerBlendingRangesData
from aspose_psd_foss.raw_layer_mask_section import RawLayerMaskSection
from aspose_psd_foss.raw_layer_blending_ranges_section import RawLayerBlendingRangesSection


class Layer:
    LAYER_TRAILER_SIZE = 16

    def __init__(self) -> None:
        self._name: str = ""
        self._is_visible: bool = True
        self._opacity: int = 255
        self._raw_data: LayerRawData = LayerRawData.empty()
        self._bounds: Rectangle = Rectangle(0, 0, 0, 0)
        self._clipping: int = 0
        self._blend_mode: BlendMode = BlendMode.NORMAL
        self._has_mutated: bool = False

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
                    self._bounds.left,
                    self._bounds.top,
                    self._bounds.right,
                    value,
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
                    self._bounds.left,
                    self._bounds.top,
                    value,
                    self._bounds.bottom,
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
        return len(self._channel_info)

    @property
    def channel_information(self) -> List[ChannelInformation]:
        return [ChannelInformation.from_layer_channel_info(ci) for ci in self._channel_info]

    @channel_information.setter
    def channel_information(self, value) -> None:
        raise NotImplementedError(
            "Changing layer channel information is not supported by this FOSS build."
        )

    @property
    def _channels(self) -> List[PsdLayerChannelInfo]:
        return [PsdLayerChannelInfo(ci.channel_id, ci.data_length) for ci in self._channel_info]

    @property
    def _has_mask_data(self) -> bool:
        return len(self._raw_data.layer_mask_section.raw_data) > 4

    @property
    def _has_blending_ranges_data(self) -> bool:
        return len(self._raw_data.blending_ranges_section.raw_data) > 4

    @property
    def _mask_info(self) -> LayerMaskInfo:
        return LayerMaskInfo(self._has_mask_data, len(self._raw_data.layer_mask_section.raw_data))

    @property
    def _blending_ranges_info(self) -> LayerBlendingRangesInfo:
        return LayerBlendingRangesInfo(
            self._has_blending_ranges_data,
            len(self._raw_data.blending_ranges_section.raw_data),
        )

    @property
    def _channel_info(self) -> List[Any]:
        return self._raw_data.channel_info

    @property
    def _raw_flags(self) -> int:
        return self._raw_data.flags

    @property
    def _raw_layer_mask_section(self) -> RawLayerMaskSection:
        return self._raw_data.layer_mask_section

    @property
    def _raw_layer_blending_ranges_section(self) -> RawLayerBlendingRangesSection:
        return self._raw_data.blending_ranges_section

    @property
    def layer_mask_data(self) -> Optional[LayerMaskData]:
        if not self._has_mask_data:
            return None
        return LayerMaskDataShort()

    @layer_mask_data.setter
    def layer_mask_data(self, value) -> None:
        raise NotImplementedError(
            "Changing layer mask data is not supported by this FOSS build."
        )

    @property
    def layer_blending_ranges_data(self) -> LayerBlendingRangesData:
        return LayerBlendingRangesData.from_raw_length(
            len(self._raw_data.blending_ranges_section.raw_data)
        )

    @layer_blending_ranges_data.setter
    def layer_blending_ranges_data(self, value) -> None:
        raise NotImplementedError(
            "Changing layer blending ranges data is not supported by this FOSS build."
        )

    @property
    def _additional_layer_data(self) -> bytes:
        return self._raw_data.additional_layer_data

    @property
    def _raw_blend_mode_key(self) -> str:
        return self._raw_data.blend_mode_key

    @property
    def _has_mutated(self) -> bool:
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
            self._raw_data = self._raw_data.with_blend_mode_key(
                LayerBlendModeMapper.get_blend_mode_key(blend_mode)
            )
            self._has_mutated = True

    @staticmethod
    def load(reader: BigEndianReader, is_large_document: bool) -> "Layer":
        return LayerRecordReader.load(reader, is_large_document)

    def write(self, writer: BigEndianWriter, is_large_document: bool) -> None:
        LayerRecordWriter.write(self, writer, is_large_document)

    @staticmethod
    def create_parsed(
        name: str,
        bounds: Rectangle,
        is_visible: bool,
        opacity: int,
        clipping: int,
        blend_mode: BlendMode,
        raw_data: LayerRawData,
    ) -> "Layer":
        layer = Layer()
        layer._name = name
        layer._bounds = bounds
        layer._is_visible = is_visible
        layer._opacity = opacity
        layer._clipping = clipping
        layer._blend_mode = blend_mode
        layer._raw_data = raw_data
        return layer
