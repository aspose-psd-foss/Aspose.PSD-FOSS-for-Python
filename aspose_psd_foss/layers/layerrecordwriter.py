from aspose_psd_foss.big_endian_writer import BigEndianWriter
from aspose_psd_foss.layer import Layer


class LayerRecordWriter:
    _ADOBE_LAYER_SIGNATURE = 0x3842494D
    _LAYER_INVISIBLE_FLAG = 0x02
    _LAYER_RECORD_RESERVED_BYTE = 0

    @staticmethod
    def write(layer: Layer, writer: BigEndianWriter, is_large_document: bool):
        writer.write(layer.top)
        writer.write(layer.left)
        writer.write(layer.bottom)
        writer.write(layer.right)
        writer.write(len(layer.channel_info))

        for i in range(len(layer.channel_info)):
            writer.write(layer.channel_info[i].channel_id)
            if is_large_document:
                writer.write(layer.channel_info[i].data_length)
            else:
                writer.write(int(layer.channel_info[i].data_length))

        writer.write(LayerRecordWriter._ADOBE_LAYER_SIGNATURE)
        writer.write(layer.raw_blend_mode_key.encode('ascii'))
        writer.write(layer.opacity)
        writer.write(layer.clipping)
        writer.write(LayerRecordWriter._get_flags_for_write(layer))
        writer.write(LayerRecordWriter._LAYER_RECORD_RESERVED_BYTE)
        writer.write(LayerRecordWriter._get_extra_data_length(layer))
        writer.write(layer.raw_layer_mask_section.raw_data)
        writer.write(layer.raw_layer_blending_ranges_section.raw_data)
        writer.write_pascal_string_aligned_to4(layer.name)
        writer.write(layer.additional_layer_data)

    @staticmethod
    def _get_flags_for_write(layer: Layer) -> int:
        flags = layer.raw_flags
        return (
            (flags & ~LayerRecordWriter._LAYER_INVISIBLE_FLAG)
            if layer.is_visible
            else (flags | LayerRecordWriter._LAYER_INVISIBLE_FLAG)
        )

    @staticmethod
    def _get_extra_data_length(layer: Layer) -> int:
        return (
            len(layer.raw_layer_mask_section.raw_data)
            + len(layer.raw_layer_blending_ranges_section.raw_data)
            + BigEndianWriter.get_pascal_string_storage_length_aligned_to4(
                layer.name
            )
            + len(layer.additional_layer_data)
        )
