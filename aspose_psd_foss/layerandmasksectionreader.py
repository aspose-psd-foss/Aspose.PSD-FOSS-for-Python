from typing import Optional
from .bigendianreader import BigEndianReader
from .psdsectionreader import PsdSectionReader
from .coreexceptions.psdloadexception import PsdLoadException
from .layers.layer import Layer
from .layers.layerrecordreader import LayerRecordReader
from .sections.layerandmasksection import LayerAndMaskSection


class LayerAndMaskSectionReader:
    @classmethod
    def load(cls, reader: BigEndianReader, is_large_document: bool) -> Optional[LayerAndMaskSection]:
        """
        Loads the section using PSD- or PSB-sized outer and layer-info lengths.
        """
        section_length = read_section_length(reader, is_large_document)
        if section_length == 0:
            # Return an empty LayerAndMaskSection instance when there is no data.
            return LayerAndMaskSection([], [], [], 0, [])

        raw_section_bytes = PsdSectionReader.read_bytes(
            reader,
            section_length,
            "Layer and Mask Information section",
        )
        mem_reader = BigEndianReader(raw_section_bytes, leave_open=True)

        layer_info_length = PsdSectionReader.validate_signed_length(
            mem_reader.read_int64() if is_large_document else mem_reader.read_int32(),
            "Layer Info section",
        )
        if layer_info_length > len(raw_section_bytes) - mem_reader.position:
            raise PsdLoadException(
                "Layer Info section length exceeds the enclosing Layer and Mask Information section."
            )

        layer_info_end = (8 if is_large_document else 4) + layer_info_length
        if layer_info_length == 0:
            tail = (
                raw_section_bytes[mem_reader.position :]
                if mem_reader.position < len(raw_section_bytes)
                else []
            )
            return LayerAndMaskSection(raw_section_bytes, [], tail, 0, [])

        if layer_info_length < 2:
            raise PsdLoadException(
                "Layer Info section is too short to contain the layer count field."
            )

        layer_count_raw = mem_reader.read_int16()
        layer_count = abs(layer_count_raw)
        layers = read_layers(
            mem_reader, layer_count, layer_info_end, is_large_document
        )

        channel_image_data_length = layer_info_end - mem_reader.position
        layer_channel_image_data_raw = (
            mem_reader.read_bytes(int(channel_image_data_length))
            if channel_image_data_length > 0
            else []
        )

        global_mask_and_tail_length = max(
            0, len(raw_section_bytes) - mem_reader.position
        )
        layer_global_mask_and_tail_raw = (
            mem_reader.read_bytes(global_mask_and_tail_length)
            if global_mask_and_tail_length > 0
            else []
        )

        return LayerAndMaskSection(
            raw_section_bytes,
            layer_channel_image_data_raw,
            layer_global_mask_and_tail_raw,
            layer_count_raw,
            layers,
        )


def read_layers(
    reader: BigEndianReader, layer_count: int, layer_info_end: int, is_large_document: bool
) -> list:
    """
    Reads layer records and validates the declared Layer Info boundary.
    """
    layers = []
    if layer_count > 0:
        layers = [
            LayerRecordReader.load(reader, is_large_document) for _ in range(layer_count)
        ]

    if reader.position > layer_info_end:
        raise PsdLoadException(
            "Layer records exceed the declared Layer Info section length."
        )

    return layers


def read_section_length(reader: BigEndianReader, is_large_document: bool) -> int:
    """
    Reads the outer Layer and Mask Information section length using PSD or PSB field size.
    """
    return reader.read_uint64() if is_large_document else reader.read_uint32()

