from __future__ import annotations

import io
from typing import List, Any

from .bigendianwriter import BigEndianWriter


class LayerRecordWriter:
    @staticmethod
    def write(layer: Any, writer: BigEndianWriter, is_large_document: bool) -> None:
        # Placeholder implementation
        pass


class LayerAndMaskSection:
    raw_section_bytes: bytes = b""
    has_layer_collection_mutated: bool = False
    layers: List[Any] = []
    layer_count_raw: int = 0
    layer_channel_image_data_raw: bytes = b""
    layer_global_mask_and_tail_raw: bytes = b""


def save(section: LayerAndMaskSection, writer: BigEndianWriter, is_large_document: bool) -> None:
    """Writes the section while preserving raw bytes for no‑mutation saves."""
    if (
        len(section.raw_section_bytes) > 0
        and not section.has_layer_collection_mutated
        and not any(layer.has_mutated for layer in section.layers)
    ):
        _write_section_length(writer, len(section.raw_section_bytes), is_large_document)
        writer.write(section.raw_section_bytes)
        return

    if len(section.layers) == 0:
        _write_section_length(writer, 0, is_large_document)
        return

    _write_layer_section_with_mutations(section, writer, is_large_document)


def _write_layer_section_with_mutations(
    section: LayerAndMaskSection, writer: BigEndianWriter, is_large_document: bool
) -> None:
    """Rebuilds the layer info payload when at least one parsed layer has been mutated."""
    layer_info_payload_stream = io.BytesIO()
    layer_info_payload_writer = BigEndianWriter(layer_info_payload_stream, leave_open=True)

    layer_count: int = (
        -len(section.layers)
        if section.layer_count_raw < 0
        else len(section.layers)
    )
    layer_info_payload_writer.write_int16(layer_count)

    for layer in section.layers:
        LayerRecordWriter.write(layer, layer_info_payload_writer, is_large_document)

    layer_info_payload_writer.write(section.layer_channel_image_data_raw)
    layer_info_payload = layer_info_payload_stream.getvalue()

    section_stream = io.BytesIO()
    section_writer = BigEndianWriter(section_stream, leave_open=True)

    if is_large_document:
        section_writer.write_uint64(len(layer_info_payload))
    else:
        section_writer.write_uint32(len(layer_info_payload))

    section_writer.write(layer_info_payload)
    section_writer.write(_get_layer_global_mask_and_tail_bytes_for_write(section))

    section_bytes = section_stream.getvalue()
    _write_section_length(writer, len(section_bytes), is_large_document)
    writer.write(section_bytes)


def _get_layer_global_mask_and_tail_bytes_for_write(section: LayerAndMaskSection) -> bytes:
    """Gets the global mask and trailing bytes to emit when rebuilding the layer section."""
    return (
        section.layer_global_mask_and_tail_raw
        if len(section.layer_global_mask_and_tail_raw) > 0
        else bytes([0, 0, 0, 0])
    )


def _write_section_length(writer: BigEndianWriter, length: int, is_large_document: bool) -> None:
    """Writes the outer Layer and Mask Information section length using PSD or PSB field size."""
    if is_large_document:
        writer.write_uint64(length)
    else:
        writer.write_uint32(length)
