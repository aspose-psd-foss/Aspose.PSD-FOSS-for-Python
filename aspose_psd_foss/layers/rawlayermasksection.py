from aspose_psd_foss.psdsectionreader import PsdSectionReader
from aspose_psd_foss.coreexceptions.psdloadexception import PsdLoadException


class RawLayerMaskSection:
    """Stores the raw layer mask subsection including its leading length field."""

    Empty: "RawLayerMaskSection"

    def __init__(self, raw_data):
        """
        Initializes a new instance of the <see cref="RawLayerMaskSection"/> class.
        :param raw_data: The raw subsection bytes including the length field.
        """
        self._raw_data = raw_data

    @property
    def raw_data(self):
        """Gets the raw subsection bytes including the length field."""
        return self._raw_data

    @staticmethod
    def load(reader, section_end):
        """
        Loads the layer mask subsection from the reader.
        :param reader: The reader positioned at the subsection length field.
        :param section_end: The byte position of the end of the enclosing layer extra data.
        :return: The loaded <see cref="RawLayerMaskSection"/> instance.
        """
        length = reader.read_uint32()
        payload_length = PsdSectionReader.get_nested_memory_backed_length(reader, length, section_end, "Layer mask subsection")
        if payload_length > 2147483647 - 4:  # int.MaxValue - sizeof(uint)
            raise PsdLoadException("Layer mask subsection is too large to preserve in memory with its length field.")

        raw_data = bytearray(4 + payload_length)
        raw_data[0] = ((length >> 24) & 0xFF)
        raw_data[1] = ((length >> 16) & 0xFF)
        raw_data[2] = ((length >> 8) & 0xFF)
        raw_data[3] = (length & 0xFF)
        if payload_length > 0:
            payload = reader.read_bytes(payload_length)
            raw_data[4:4 + payload_length] = payload

        return RawLayerMaskSection(bytes(raw_data))

    @staticmethod
    def _write_uint32_big_endian(buffer, offset, value):
        """
        Writes a 32-bit unsigned integer into a byte buffer in big-endian byte order.
        :param buffer: The target buffer.
        :param offset: The destination offset in the buffer.
        :param value: The value to encode.
        """
        buffer[offset] = ((value >> 24) & 0xFF)
        buffer[offset + 1] = ((value >> 16) & 0xFF)
        buffer[offset + 2] = ((value >> 8) & 0xFF)
        buffer[offset + 3] = (value & 0xFF)


# Initialize static Empty field after class definition
RawLayerMaskSection.Empty = RawLayerMaskSection(b"")
