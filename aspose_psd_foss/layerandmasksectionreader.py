import io

from aspose_psd_foss.sections.layer_and_mask_section import LayerAndMaskSection
from aspose_psd_foss.big_endian_reader import BigEndianReader
from aspose_psd_foss.psd_section_reader import PsdSectionReader
from aspose_psd_foss.core_exceptions.psd_load_exception import PsdLoadException
from aspose_psd_foss.layers.layer import Layer
from aspose_psd_foss.layers.layer_record_reader import LayerRecordReader


class LayerAndMaskSectionReader:
    @staticmethod
    def load(reader: BigEndianReader, is_large_document: bool) -> LayerAndMaskSection:
        section_length = LayerAndMaskSectionReader._read_section_length(reader, is_large_document)
        if section_length == 0:
            return LayerAndMaskSection.empty()

        raw_section_bytes = PsdSectionReader.read_bytes(
            reader, section_length, "Layer and Mask Information section"
        )
        mem_reader = BigEndianReader(io.BytesIO(raw_section_bytes), leave_open=True)

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
                if len(raw_section_bytes) > mem_reader.position
                else b""
            )
            return LayerAndMaskSection(
                raw_section_bytes, b"", tail, 0, []
            )

        if layer_info_length < 2:
            raise PsdLoadException(
                "Layer Info section is too short to contain the layer count field."
            )

        layer_count_raw = mem_reader.read_int16()
        layer_count = -layer_count_raw if layer_count_raw < 0 else layer_count_raw
        layers = LayerAndMaskSectionReader._read_layers(
            mem_reader, layer_count, layer_info_end, is_large_document
        )

        channel_image_data_length = int(layer_info_end - mem_reader.position)
        layer_channel_image_data_raw = (
            mem_reader.read_bytes(channel_image_data_length)
            if channel_image_data_length > 0
            else b""
        )

        global_mask_and_tail_length = max(
            0, len(raw_section_bytes) - int(mem_reader.position)
        )
        layer_global_mask_and_tail_raw = (
            mem_reader.read_bytes(global_mask_and_tail_length)
            if global_mask_and_tail_length > 0
            else b""
        )

        return LayerAndMaskSection(
            raw_section_bytes,
            layer_channel_image_data_raw,
            layer_global_mask_and_tail_raw,
            layer_count_raw,
            layers,
        )

    @staticmethod
    def _read_layers(
        reader: BigEndianReader,
        layer_count: int,
        layer_info_end: int,
        is_large_document: bool,
    ) -> list[Layer]:
        layers: list[Layer] = []
        if layer_count > 0:
            layers = [None] * layer_count
            for i in range(layer_count):
                layers[i] = LayerRecordReader.load(reader, is_large_document)

        if reader.position > layer_info_end:
            raise PsdLoadException(
                "Layer records exceed the declared Layer Info section length."
            )
        return layers

    @staticmethod
    def _read_section_length(reader: BigEndianReader, is_large_document: bool) -> int:
        return reader.read_uint64() if is_large_document else reader.read_uint32()

