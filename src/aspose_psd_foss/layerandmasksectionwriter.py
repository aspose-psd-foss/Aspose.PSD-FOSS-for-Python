import io

from aspose_psd_foss.bigendianwriter import BigEndianWriter
from aspose_psd_foss.layers.layerrecordwriter import LayerRecordWriter
from aspose_psd_foss.sections.layerandmasksection import LayerAndMaskSection


class LayerAndMaskSectionWriter:
    """
    Writes PSD/PSB Layer and Mask Information sections.
    """

    @staticmethod
    def save(section: LayerAndMaskSection, writer: BigEndianWriter, is_large_document: bool) -> None:
        """
        Writes the section while preserving raw bytes for no-mutation saves.

        :param section: The section to write.
        :param writer: The destination writer.
        :param is_large_document: true for PSB-sized lengths; otherwise, false.
        """
        if (
            len(section.raw_section_bytes) > 0
            and not section.has_layer_collection_mutated
            and not any(layer.has_mutated for layer in section.layers)
        ):
            LayerAndMaskSectionWriter._write_section_length(
                writer, len(section.raw_section_bytes), is_large_document
            )
            writer.write(section.raw_section_bytes)
            return

        if len(section.layers) == 0:
            LayerAndMaskSectionWriter._write_section_length(writer, 0, is_large_document)
            return

        LayerAndMaskSectionWriter._write_layer_section_with_mutations(
            section, writer, is_large_document
        )

    @staticmethod
    def _write_layer_section_with_mutations(
        section: LayerAndMaskSection, writer: BigEndianWriter, is_large_document: bool
    ) -> None:
        """
        Rebuilds the layer info payload when at least one parsed layer has been mutated.

        :param section: The section being rebuilt.
        :param writer: The destination writer positioned at the Layer and Mask Information section.
        :param is_large_document: true for PSB-sized section lengths; otherwise, false.
        """
        layer_info_payload_stream = io.BytesIO()
        layer_info_payload_writer = BigEndianWriter(
            layer_info_payload_stream, leave_open=True
        )
        try:
            layer_count = (
                -len(section.layers)
                if section.layer_count_raw < 0
                else len(section.layers)
            )
            layer_info_payload_writer.write_int16(layer_count)

            for layer in section.layers:
                LayerRecordWriter.write(layer, layer_info_payload_writer, is_large_document)

            layer_info_payload_writer.write(section.layer_channel_image_data_raw)
            layer_info_payload = layer_info_payload_stream.getvalue()
        finally:
            layer_info_payload_writer.dispose()

        section_stream = io.BytesIO()
        section_writer = BigEndianWriter(section_stream, leave_open=True)
        try:
            if is_large_document:
                section_writer.write_long(len(layer_info_payload))
            else:
                section_writer.write_int32(len(layer_info_payload))

            section_writer.write(layer_info_payload)
            section_writer.write(
                LayerAndMaskSectionWriter._get_layer_global_mask_and_tail_bytes_for_write(section)
            )

            section_bytes = section_stream.getvalue()
            LayerAndMaskSectionWriter._write_section_length(
                writer, len(section_bytes), is_large_document
            )
            writer.write(section_bytes)
        finally:
            section_writer.dispose()

    @staticmethod
    def _get_layer_global_mask_and_tail_bytes_for_write(section: LayerAndMaskSection) -> bytearray:
        """
        Gets the global mask and trailing bytes to emit when rebuilding the layer section.

        :param section: The source section.
        :return: The preserved tail bytes, or an empty global mask block when the original section had no tail.
        """
        if len(section.layer_global_mask_and_tail_raw) > 0:
            return section.layer_global_mask_and_tail_raw
        return bytearray([0, 0, 0, 0])

    @staticmethod
    def _write_section_length(
        writer: BigEndianWriter, length: int, is_large_document: bool
    ) -> None:
        """
        Writes the outer Layer and Mask Information section length using PSD or PSB field size.

        :param writer: The destination writer.
        :param length: The section payload length to write.
        :param is_large_document: true to write an 8-byte PSB length; otherwise, false.
        """
        if is_large_document:
            writer.write_ulong(length)
        else:
            writer.write_uint32(length)