from __future__ import annotations

from aspose_psd_foss.bigendianwriter import BigEndianWriter
from aspose_psd_foss.layers.layer import Layer


class LayerRecordWriter:
    _ADOBE_LAYER_SIGNATURE = 0x3842494D
    _LAYER_INVISIBLE_FLAG = 0x02
    _LAYER_RECORD_RESERVED_BYTE = 0

    @classmethod
    def write(cls, layer: Layer, writer: BigEndianWriter, is_large_document: bool) -> None:
        writer.write(layer.top)
        writer.write(layer.left)
        writer.write(layer.bottom)
        writer.write(layer.right)
        writer.write_uint16(len(layer.channel_info))

        for channel in layer.channel_info:
            writer.write(channel.channel_id)
            if is_large_document:
                writer.write(channel.data_length)
            else:
                writer.write_uint32(channel.data_length)

        writer.write_uint32(cls._ADOBE_LAYER_SIGNATURE)
        writer.write_bytes(layer.raw_blend_mode_key.encode('ascii'))
        writer.write(layer.opacity)
        writer.write(layer.clipping)
        writer.write(cls._get_flags_for_write(layer))
        writer.write_uint8(cls._LAYER_RECORD_RESERVED_BYTE)
        writer.write_uint32(cls._get_extra_data_length(layer))
        writer.write_bytes(layer.raw_layer_mask_section.raw_data)
        writer.write_bytes(layer.raw_layer_blending_ranges_section.raw_data)
        writer.write_pascal_string_aligned_to4(layer.name)
        writer.write_bytes(layer.additional_layer_data)

    @classmethod
    def _get_flags_for_write(cls, layer: Layer) -> int:
        flags = layer.raw_flags
        return (flags & ~cls._LAYER_INVISIBLE_FLAG) if layer.is_visible else (flags | cls._LAYER_INVISIBLE_FLAG)

    @classmethod
    def _get_extra_data_length(cls, layer: Layer) -> int:
        return (
            len(layer.raw_layer_mask_section.raw_data)
            + len(layer.raw_layer_blending_ranges_section.raw_data)
            + BigEndianWriter.get_pascal_string_storage_length_aligned_to4(layer.name)
            + len(layer.additional_layer_data)
        )
