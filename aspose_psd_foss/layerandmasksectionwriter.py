import io

from aspose_psd_foss.sections.layerandmasksection import LayerAndMaskSection
from aspose_psd_foss.bigendianwriter import BigEndianWriter
from aspose_psd_foss.layers.layer import Layer
from aspose_psd_foss.layers.layerrecordwriter import LayerRecordWriter


class LayerAndMaskSectionWriter:
    """Writes PSD/PSB Layer and Mask Information sections."""

    @staticmethod
    def save(section: LayerAndMaskSection, writer: BigEndianWriter, is_large_document: bool):
        """Writes the section while preserving raw bytes for no‑mutation saves."""
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
    ):
        """Rebuilds the layer info payload when at least one parsed layer has been mutated."""
        layer_info_payload_stream = io.BytesIO()
        layer_info_payload_writer = BigEndianWriter(
            layer_info_payload_stream, leave_open=True
        )

        if section.layer_count_raw < 0:
            layer_count = -len(section.layers)
        else:
            layer_count = len(section.layers)
        layer_info_payload_writer.write(layer_count)

        for layer in section.layers:
            LayerRecordWriter.write(layer, layer_info_payload_writer, is_large_document)

        layer_info_payload_writer.write(section.layer_channel_image_data_raw)
        layer_info_payload = layer_info_payload_stream.getvalue()

        section_stream = io.BytesIO()
        section_writer = BigEndianWriter(section_stream, leave_open=True)

        # Length field size depends on document type, but both branches write the same value.
        section_writer.write(len(layer_info_payload))

        section_writer.write(layer_info_payload)
        section_writer.write(
            LayerAndMaskSectionWriter._get_layer_global_mask_and_tail_bytes_for_write(
                section
            )
        )

        section_bytes = section_stream.getvalue()
        LayerAndMaskSectionWriter._write_section_length(
            writer, len(section_bytes), is_large_document
        )
        writer.write(section_bytes)

    @staticmethod
    def _get_layer_global_mask_and_tail_bytes_for_write(
        section: LayerAndMaskSection,
    ) -> bytes:
        """Returns the preserved tail bytes, or an empty global mask block if none."""
        return (
            section.layer_global_mask_and_tail_raw
            if len(section.layer_global_mask_and_tail_raw) > 0
            else bytes([0, 0, 0, 0])
        )

    @staticmethod
    def _write_section_length(
        writer: BigEndianWriter, length: int, is_large_document: bool
    ):
        """Writes the outer Layer and Mask Information section length using PSD or PSB field size."""
        writer.write(length)  # Length is written as 8‑byte for large docs, 4‑byte otherwise.
