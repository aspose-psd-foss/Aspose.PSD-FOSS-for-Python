"""
Python port of Aspose.PSD.FileFormats.Psd.LayerAndMaskSectionWriter

Writes PSD/PSB Layer and Mask Information sections.
"""

from __future__ import annotations

import io

from aspose_psd_foss.bigendianwriter import BigEndianWriter
from aspose_psd_foss.layers.layerrecordwriter import LayerRecordWriter
from aspose_psd_foss.sections.layerandmasksection import LayerAndMaskSection


class LayerAndMaskSectionWriter:
    """
    Writes PSD/PSB Layer and Mask Information sections.
    """

    @staticmethod
    def save(section: LayerAndMaskSection,
             writer: BigEndianWriter,
             is_large_document: bool) -> None:
        """
        Writes the section while preserving raw bytes for no-mutation saves.

        :param section: The section to write.
        :param writer: The destination writer.
        :param is_large_document: True for PSB-sized lengths; otherwise, False.
        """
        if (len(section.raw_section_bytes) > 0
                and not section.has_layer_collection_mutated
                and not any(layer.has_mutated for layer in section.layers)):
            LayerAndMaskSectionWriter._write_section_length(
                writer, len(section.raw_section_bytes), is_large_document
            )
            writer.write(section.raw_section_bytes)
            return

        if len(section.layers) == 0:
            LayerAndMaskSectionWriter._write_section_length(
                writer, 0, is_large_document
            )
            return

        LayerAndMaskSectionWriter._write_layer_section_with_mutations(
            section, writer, is_large_document
        )

    # ------------------------------------------------------------------
    # Private helpers
    # ------------------------------------------------------------------

    @staticmethod
    def _write_layer_section_with_mutations(
        section: LayerAndMaskSection,
        writer: BigEndianWriter,
        is_large_document: bool,
    ) -> None:
        """
        Rebuilds the layer info payload when at least one parsed layer
        has been mutated.
        """
        # Build the layer info payload in memory.
        with io.BytesIO() as layer_info_payload_stream:
            with BigEndianWriter(layer_info_payload_stream, leave_open=True) as layer_info_payload_writer:
                # Preserve sign of the original layer count when negative.
                if section.layer_count_raw < 0:
                    layer_count = -len(section.layers)
                else:
                    layer_count = len(section.layers)

                # C# writes a ``short`` here (2 bytes, big-endian).
                # Wrap through 16-bit signed arithmetic to match C# behavior.
                layer_count = LayerAndMaskSectionWriter._to_int16(layer_count)
                layer_info_payload_writer.write(layer_count)

                for layer in section.layers:
                    LayerRecordWriter.write(
                        layer, layer_info_payload_writer, is_large_document
                    )

                layer_info_payload_writer.write(section.layer_channel_image_data_raw)

            layer_info_payload = layer_info_payload_stream.getvalue()

        # Build the section payload in memory.
        with io.BytesIO() as section_stream:
            with BigEndianWriter(section_stream, leave_open=True) as section_writer:
                if is_large_document:
                    # C# writes a ``long`` (8 bytes, big-endian).
                    section_writer.write(len(layer_info_payload))
                else:
                    # C# writes an ``int`` (4 bytes, big-endian).
                    section_writer.write(len(layer_info_payload))

                section_writer.write(layer_info_payload)
                section_writer.write(
                    LayerAndMaskSectionWriter._get_layer_global_mask_and_tail_bytes_for_write(section)
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
        """
        Gets the global mask and trailing bytes to emit when rebuilding
        the layer section.

        :return: The preserved tail bytes, or an empty global mask block
                 when the original section had no tail.
        """
        if len(section.layer_global_mask_and_tail_raw) > 0:
            return section.layer_global_mask_and_tail_raw
        return bytes([0, 0, 0, 0])

    @staticmethod
    def _write_section_length(
        writer: BigEndianWriter,
        length: int,
        is_large_document: bool,
    ) -> None:
        """
        Writes the outer Layer and Mask Information section length using
        PSD or PSB field size.

        :param writer: The destination writer.
        :param length: The section payload length to write.
        :param is_large_document: True to write an 8-byte PSB length;
                                  otherwise, False.
        """
        if is_large_document:
            # C# writes a ``ulong`` (8 bytes, big-endian).
            writer.write(length & 0xFFFFFFFFFFFFFFFF)
        else:
            # C# writes a ``uint`` (4 bytes, big-endian).
            writer.write(length & 0xFFFFFFFF)

    @staticmethod
    def _to_int16(value: int) -> int:
        """
        Wrap an integer into 16-bit signed range, mirroring C#'s ``(short)`` cast.
        """
        value &= 0xFFFF
        return value - 0x10000 if value >= 0x8000 else value