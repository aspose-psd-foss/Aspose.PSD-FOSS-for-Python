from aspose_psd_foss.psdsectionreader import PsdSectionReader
from aspose_psd_foss.coreexceptions.psdloadexception import PsdLoadException
from typing import Optional


class RawLayerBlendingRangesSection:
    """Stores the raw blending ranges subsection including its leading length field."""

    Empty: Optional["RawLayerBlendingRangesSection"] = None

    def __init__(self, raw_data):
        """Initializes a new instance of the <see cref="RawLayerBlendingRangesSection"/> class."""
        self.RawData = raw_data

    @staticmethod
    def load(reader, section_end):
        """Loads the blending ranges subsection from the reader.

        :param reader: The reader positioned at the subsection length field.
        :param section_end: The byte position of the end of the layer extra data.
        :returns: The loaded <see cref="RawLayerBlendingRangesSection"/> instance.
        """
        length = reader.read_uint32()
        payload_length = PsdSectionReader.get_nested_memory_backed_length(reader, length, section_end, "Layer blending ranges subsection")
        if payload_length > int(2147483647) - 4:
            raise PsdLoadException("Layer blending ranges subsection is too large to preserve in memory with its length field.")

        raw_data = bytearray(4 + payload_length)
        RawLayerBlendingRangesSection._write_uint32_big_endian(raw_data, 0, length)
        if payload_length > 0:
            payload = reader.read_bytes(payload_length)
            raw_data[4:4 + payload_length] = payload

        return RawLayerBlendingRangesSection(bytes(raw_data))

    @staticmethod
    def _write_uint32_big_endian(buffer, offset, value):
        """Writes a 32-bit unsigned integer into a byte buffer in big-endian byte order.

        :param buffer: The target buffer.
        :param offset: The destination offset in the buffer.
        :param value: The value to encode.
        """
        buffer[offset] = (value >> 24) & 0xFF
        buffer[offset + 1] = (value >> 16) & 0xFF
        buffer[offset + 2] = (value >> 8) & 0xFF
        buffer[offset + 3] = value & 0xFF


RawLayerBlendingRangesSection.Empty = RawLayerBlendingRangesSection([])
