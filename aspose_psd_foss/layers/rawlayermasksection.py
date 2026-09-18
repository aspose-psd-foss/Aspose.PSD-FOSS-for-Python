from ..bigendianreader import BigEndianReader
from ..psdsectionreader import get_nested_memory_backed_length
from ..coreexceptions.psdloadexception import PsdLoadException
from typing import Optional


class RawLayerMaskSection:
    """
    Stores the raw layer mask subsection including its leading length field.
    """

    # Gets an empty layer mask subsection.
    EMPTY: Optional['RawLayerMaskSection'] = None  # will be initialized after the class definition

    def __init__(self, raw_data: bytes):
        """
        Initializes a new instance of the RawLayerMaskSection class.

        :param raw_data: The raw subsection bytes including the length field.
        """
        self._raw_data = raw_data

    @property
    def raw_data(self) -> bytes:
        """
        Gets the raw subsection bytes including the length field.
        """
        return self._raw_data

    @staticmethod
    def load(reader: BigEndianReader, section_end: int) -> 'RawLayerMaskSection':
        """
        Loads the layer mask subsection from the reader.

        :param reader: The reader positioned at the subsection length field.
        :param section_end: The byte position of the end of the enclosing layer extra data.
        :return: The loaded RawLayerMaskSection instance.
        """
        length = reader.read_uint32()
        payload_length = get_nested_memory_backed_length(
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
            raw_data[4:4 + payload_length] = payload

        return RawLayerMaskSection(bytes(raw_data))

    @staticmethod
    def _write_uint32_big_endian(buffer: bytearray, offset: int, value: int) -> None:
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


# Initialize the EMPTY static instance
RawLayerMaskSection.EMPTY = RawLayerMaskSection(b'')
