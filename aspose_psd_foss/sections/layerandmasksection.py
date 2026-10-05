"""
Python port of Aspose.PSD.FileFormats.Psd.LayerAndMaskSection

Represents the PSD/PSB Layer and Mask Information section and its
raw-preserved save state.
"""

from __future__ import annotations

from typing import List

from aspose_psd_foss.bigendianreader import BigEndianReader
from aspose_psd_foss.bigendianwriter import BigEndianWriter
from aspose_psd_foss.layers.layer import Layer


class LayerAndMaskSection:
    """
    Represents the PSD/PSB Layer and Mask Information section and its
    raw-preserved save state.
    """

    def __init__(
        self,
        raw_section_bytes: bytes,
        layer_channel_image_data_raw: bytes,
        layer_global_mask_and_tail_raw: bytes,
        layer_count_raw: int,
        layers: List[Layer],
        has_layer_collection_mutated: bool = False,
    ):
        """
        Initializes a new instance of the :class:`LayerAndMaskSection` class.

        :param raw_section_bytes:
            The raw section payload without the outer length field.
        :param layer_channel_image_data_raw:
            The raw channel image data payload after layer records.
        :param layer_global_mask_and_tail_raw:
            The raw global mask and trailing section bytes.
        :param layer_count_raw:
            The original signed layer count value.
        :param layers:
            The parsed layer records.
        :param has_layer_collection_mutated:
            True when the public layer collection was replaced; otherwise, False.
        """
        self._raw_section_bytes = raw_section_bytes
        self._layer_channel_image_data_raw = layer_channel_image_data_raw
        self._layer_global_mask_and_tail_raw = layer_global_mask_and_tail_raw
        self._layer_count_raw = layer_count_raw
        self._layers = layers
        self._has_layer_collection_mutated = has_layer_collection_mutated

    # -- Static: Empty ------------------------------------------------------

    _empty_instance: "LayerAndMaskSection | None" = None

    @classmethod
    def empty(cls) -> "LayerAndMaskSection":
        """
        Gets an empty Layer and Mask Information section.

        Mirrors the C# ``static LayerAndMaskSection Empty { get; }``.
        """
        if cls._empty_instance is None:
            cls._empty_instance = cls(b"", b"", b"", 0, [])
        return cls._empty_instance

    # -- Properties ---------------------------------------------------------

    @property
    def raw_section_bytes(self) -> bytes:
        """Gets the raw section payload without the outer length field."""
        return self._raw_section_bytes

    @property
    def layer_channel_image_data_raw(self) -> bytes:
        """Gets the raw layer channel image data payload after layer records."""
        return self._layer_channel_image_data_raw

    @property
    def layer_global_mask_and_tail_raw(self) -> bytes:
        """Gets the raw global mask info and trailing section bytes."""
        return self._layer_global_mask_and_tail_raw

    @property
    def layer_count_raw(self) -> int:
        """
        Gets the original signed layer count so transparency-protected layers
        can preserve sign.
        """
        return self._layer_count_raw

    @property
    def layers(self) -> List[Layer]:
        """Gets the parsed layer records."""
        return self._layers

    @property
    def has_layer_collection_mutated(self) -> bool:
        """Gets whether the public layer collection was replaced."""
        return self._has_layer_collection_mutated

    # -- Loading / saving ---------------------------------------------------

    @staticmethod
    def load(reader: BigEndianReader, is_large_document: bool) -> "LayerAndMaskSection":
        from aspose_psd_foss.layerandmasksectionreader import LayerAndMaskSectionReader
        """
        Loads the section using PSD- or PSB-sized outer and layer-info lengths.

        :param reader: The reader positioned at the outer section length field.
        :param is_large_document: True for PSB-sized lengths; otherwise, False.
        :return: The loaded section.
        """
        return LayerAndMaskSectionReader.load(reader, is_large_document)

    def save(self, writer: BigEndianWriter, is_large_document: bool) -> None:
        from aspose_psd_foss.layerandmasksectionwriter import LayerAndMaskSectionWriter
        """
        Writes the section while preserving raw bytes for no-mutation saves.

        :param writer: The destination writer.
        :param is_large_document: True for PSB-sized lengths; otherwise, False.
        """
        LayerAndMaskSectionWriter.save(self, writer, is_large_document)

    # -- Copy helpers -------------------------------------------------------

    def with_layers(self, layers: List[Layer]) -> "LayerAndMaskSection":
        """
        Creates a section copy with a replaced layer collection and marks it
        for rewriting on save.

        :param layers: The replacement layer collection.
        :return: The section copy.
        """
        return LayerAndMaskSection(
            self._raw_section_bytes,
            self._layer_channel_image_data_raw,
            self._layer_global_mask_and_tail_raw,
            self._layer_count_raw,
            list(layers),
            has_layer_collection_mutated=True,
        )