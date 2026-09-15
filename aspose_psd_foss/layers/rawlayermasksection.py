"""Stores the raw layer mask subsection including its leading length field."""

from aspose_psd_foss.big_endian_reader import BigEndianReader
from aspose_psd_foss.psd_section_reader import PsdSectionReader
from aspose_psd_foss.core_exceptions.psd_load_exception import PsdLoadException


class RawLayerMaskSection:
    """Represents a raw layer mask subsection."""

    EMPTY = None

    def __init__(self, raw_data):
        self.raw_data = raw_data

    @staticmethod
    def load(reader: BigEndianReader, section_end: int):
        """Loads the layer mask subsection from the reader."""
        length = reader.read_uint32()
        payload_length = PsdSectionReader.get_nested_memory_backed_length(
            reader, length, section_end, "Layer mask subsection"
        )
        if payload_length > (2**31 - 1) - 4:
            raise PsdLoadException(
                "Layer mask subsection is too large to preserve in memory with its length field."
            )

        raw_data = bytearray(4 + payload_length)
        RawLayerMaskSection._write_uint32_big_endian(raw_data, 0, length)
        if payload_length > 0:
            payload = reader.read_bytes(payload_length)
            raw_data[4 : 4 + payload_length] = payload

        return RawLayerMaskSection(raw_data)

    @staticmethod
    def _write_uint32_big_endian(buffer, offset: int, value: int):
        """Writes a 32-bit unsigned integer into a byte buffer in big-endian order."""
        buffer[offset] = (value >> 24) & 0xFF
        buffer[offset + 1] = (value >> 16) & 0xFF
        buffer[offset + 2] = (value >> 8) & 0xFF
        buffer[offset + 3] = value & 0xFF


# Initialize static empty instance
RawLayerMaskSection.EMPTY = RawLayerMaskSection(bytearray())
