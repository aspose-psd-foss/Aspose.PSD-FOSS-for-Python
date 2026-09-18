from __future__ import annotations

from typing import Any, List

from ..bigendianwriter import BigEndianWriter
from ..layerandmasksectionwriter import LayerRecordWriter


class LayerAndMaskSection:
    raw_section_bytes: bytes = b""
    has_layer_collection_mutated: bool = False
    layers: List[Any] = []
    layer_count_raw: int = 0
    layer_channel_image_data_raw: bytes = b""
    layer_global_mask_and_tail_raw: bytes = b""

    def __init__(self):
        pass

    @staticmethod
    def save(instance: "LayerAndMaskSection", writer: BigEndianWriter, is_large_document: bool) -> None:
        if getattr(instance, "has_layer_collection_mutated", False):
            # Write layer count (signed 16‑bit for PSD, 32‑bit for PSB)
            if is_large_document:
                writer.write_int32(instance.layer_count_raw)
            else:
                writer.write_int16(instance.layer_count_raw)
            # Write each layer record
            for layer in getattr(instance, "layers", []):
                LayerRecordWriter.write(layer, writer, is_large_document)
            # Write remaining raw data
            writer.write(instance.layer_channel_image_data_raw)
            writer.write(instance.layer_global_mask_and_tail_raw)
        else:
            writer.write(instance.raw_section_bytes)
