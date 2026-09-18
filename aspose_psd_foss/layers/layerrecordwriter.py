from ..bigendianwriter import BigEndianWriter
from typing import Any

_ADOBE_LAYER_SIGNATURE = 0x3842494D
_LAYER_INVISIBLE_FLAG = 0x02
_LAYER_RECORD_RESERVED_BYTE = 0


def write(layer: Any, writer: BigEndianWriter, is_large_document: bool) -> None:
    bbox = layer.get_bbox()
    writer.write_int32(bbox.top)
    writer.write_int32(bbox.left)
    writer.write_int32(bbox.bottom)
    writer.write_int32(bbox.right)
    channel_info = layer.get_channels()
    writer.write_uint16(len(channel_info))

    for channel in channel_info:
        writer.write_int16(channel.channel_id)
        if is_large_document:
            writer.write_uint32(channel.data_length)
        else:
            writer.write_uint32(int(channel.data_length) & 0xFFFFFFFF)

    writer.write_uint32(_ADOBE_LAYER_SIGNATURE)
    writer.write(layer.get_blend_mode().encode("ascii"))
    writer.write_byte(layer.get_opacity())
    writer.write_byte(layer.get_clipping())
    writer.write_byte(_get_flags_for_write(layer))
    writer.write_byte(_LAYER_RECORD_RESERVED_BYTE)
    writer.write_uint32(_get_extra_data_length(layer))
    writer.write(layer.get_layer_mask().raw_data)
    writer.write(layer.get_layer_blend_ranges().raw_data)
    writer.write_pascal_string_aligned_to_4(layer.get_name())
    writer.write(layer.get_additional_info())


def _get_flags_for_write(layer: Any) -> int:
    flags = layer.get_flags()
    return (flags & ~_LAYER_INVISIBLE_FLAG) if layer.get_visible() else (flags | _LAYER_INVISIBLE_FLAG)


def _get_extra_data_length(layer: Any) -> int:
    return (
        len(layer.get_layer_mask().raw_data)
        + len(layer.get_layer_blend_ranges().raw_data)
        + BigEndianWriter.get_pascal_string_storage_length_aligned_to_4(layer.get_name())
        + len(layer.get_additional_info())
    )
