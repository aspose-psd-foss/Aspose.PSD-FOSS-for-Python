from ..bigendianreader import BigEndianReader
from ..coreexceptions.psdloadexception import PsdLoadException
from ..psdsectionreader import get_nested_memory_backed_length
from typing import Optional


class RawLayerBlendingRangesSection:
    """
    Stores the raw blending ranges subsection including its leading length field.
    """

    # Gets an empty blending ranges subsection.
    Empty: Optional["RawLayerBlendingRangesSection"] = None  # will be set after class definition

    def __init__(self, raw_data: bytes):
        """
        Initializes a new instance of the RawLayerBlendingRangesSection class.

        :param raw_data: The raw subsection bytes including the length field.
        """
        self.raw_data = raw_data

    @staticmethod
    def load(reader: BigEndianReader, section_end: int):
        """
        Loads the blending ranges subsection from the reader.

        :param reader: The reader positioned at the subsection length field.
        :param section_end: The byte position of the end of the enclosing layer extra data.
        :return: The loaded RawLayerBlendingRangesSection instance.
        """
        length = reader.read_uint32()
        payload_length = get_nested_memory_backed_length(
            reader, length, section_end, "Layer blending ranges subsection"
        )
        if payload_length > (2**31 - 1) - 4:
            raise PsdLoadException(
                "Layer blending ranges subsection is too large to preserve in memory with its length field."
            )

        raw_data = bytearray(4 + payload_length)
        RawLayerBlendingRangesSection._write_uint32_big_endian(raw_data, 0, length)
        if payload_length > 0:
            payload = reader.read_bytes(payload_length)
            raw_data[4 : 4 + payload_length] = payload

        return RawLayerBlendingRangesSection(bytes(raw_data))

    @staticmethod
    def _write_uint32_big_endian(buffer: bytearray, offset: int, value: int):
        """
        Writes a 32-bit unsigned integer into a byte buffer in big-endian byte order.

        :param buffer: The target buffer.
        :param offset: The destination offset in the buffer.
        :param value: The value to encode.
        """
        buffer[offset] = (value >> 24) & 0xFF
        buffer[offset + 1] = (value >> 16) & 0xFF
        buffer[offset + 2] = (value >> 8) & 0xFF
        buffer[offset + 3] = value & 0xFF


# Initialize the Empty static instance
RawLayerBlendingRangesSection.Empty = RawLayerBlendingRangesSection(b'')
