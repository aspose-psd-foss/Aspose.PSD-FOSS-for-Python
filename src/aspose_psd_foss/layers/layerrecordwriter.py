from aspose_psd_foss.bigendianwriter import BigEndianWriter
from aspose_psd_foss.layers.layer import Layer


class LayerRecordWriter:
    """
    Writes PSD/PSB layer records from the in-memory Layer model.
    """

    # Stores the Adobe layer record signature value "8BIM".
    ADOBE_LAYER_SIGNATURE = 0x3842494D

    # Stores the PSD flag bit that marks a layer as hidden when set.
    LAYER_INVISIBLE_FLAG = 0x02

    # Stores the reserved trailing byte in the fixed layer record fields.
    LAYER_RECORD_RESERVED_BYTE = 0

    @staticmethod
    def write(layer: Layer, writer: BigEndianWriter, is_large_document: bool) -> None:
        """
        Writes one layer record using PSD- or PSB-sized channel lengths.

        :param layer: The layer to write.
        :param writer: The destination writer.
        :param is_large_document: true for PSB-sized layer channel lengths; otherwise, false.
        """
        writer.write_int32(layer.top)
        writer.write_int32(layer.left)
        writer.write_int32(layer.bottom)
        writer.write_int32(layer.right)
        writer.write_uint16(len(layer.channel_info))

        for i in range(len(layer.channel_info)):
            writer.write_int16(layer.channel_info[i].channel_id)
            if is_large_document:
                writer.write_long(layer.channel_info[i].data_length)
            else:
                writer.write_uint32(layer.channel_info[i].data_length)

        writer.write_uint32(LayerRecordWriter.ADOBE_LAYER_SIGNATURE)
        writer.write(layer.raw_blend_mode_key.encode("ascii"))
        writer.write_uint8(layer.opacity)
        writer.write_uint8(layer.clipping)
        writer.write_uint8(LayerRecordWriter._get_flags_for_write(layer))
        writer.write_uint8(LayerRecordWriter.LAYER_RECORD_RESERVED_BYTE)
        writer.write_int32(LayerRecordWriter._get_extra_data_length(layer))
        writer.write(layer.raw_layer_mask_section.raw_data)
        writer.write(layer.raw_layer_blending_ranges_section.raw_data)
        writer.write_pascal_string_aligned_to4(layer.name)
        writer.write(layer.additional_layer_data)

    @staticmethod
    def _get_flags_for_write(layer: Layer) -> int:
        """
        Combines the original layer flags with the current public visibility state.

        :param layer: The layer whose flags should be written.
        :return: The PSD layer flags byte to write.
        """
        flags = layer.raw_flags
        if layer.is_visible:
            return flags & ~LayerRecordWriter.LAYER_INVISIBLE_FLAG
        return flags | LayerRecordWriter.LAYER_INVISIBLE_FLAG

    @staticmethod
    def _get_extra_data_length(layer: Layer) -> int:
        """
        Calculates the layer extra data byte count written after the fixed layer record fields.

        :param layer: The layer whose extra data should be measured.
        :return: The extra data byte count.
        """
        return (
            len(layer.raw_layer_mask_section.raw_data)
            + len(layer.raw_layer_blending_ranges_section.raw_data)
            + BigEndianWriter.get_pascal_string_storage_length_aligned_to4(layer.name)
            + len(layer.additional_layer_data)
        )