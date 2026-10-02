import io
from typing import TYPE_CHECKING

from aspose_psd_foss.bigendianwriter import BigEndianWriter

if TYPE_CHECKING:
    from ..layers.layer import Layer


class LayerAndMaskSection:
    def __init__(self, raw_section_bytes: bytes, layer_channel_image_data_raw: bytes, layer_global_mask_and_tail_raw: bytes, layer_count_raw: int, layers: list[Layer]):
        self.raw_section_bytes = raw_section_bytes
        self.layer_channel_image_data_raw = layer_channel_image_data_raw
        self.layer_global_mask_and_tail_raw = layer_global_mask_and_tail_raw
        self.layer_count_raw = layer_count_raw
        self.layers = layers

    @classmethod
    def empty(cls) -> "LayerAndMaskSection":
        return cls(b"", b"", b"", 0, [])

    @classmethod
    def Empty(cls) -> "LayerAndMaskSection":
        return cls.empty()


class LayerAndMaskSectionWriter:
    @staticmethod
    def save(section: 'LayerAndMaskSection', writer: BigEndianWriter, is_large_document: bool) -> None:
        """
        Serialize the given LayerAndMaskSection to the provided writer.

        Currently this method performs a minimal implementation that writes the raw
        section bytes if they are available. A full implementation should serialize
        all fields according to the PSD specification.

        :param section: The LayerAndMaskSection instance to serialize.
        :param writer: The BigEndianWriter used for writing binary data.
        :param is_large_document: Flag indicating whether the document uses large
                                  (64‑bit) offsets.
        """
        raw_bytes = getattr(section, 'raw_section_bytes', None)
        if raw_bytes:
            writer.write(raw_bytes)
