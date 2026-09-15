# Stores the raw blending ranges subsection including its leading length field.
class RawLayerBlendingRangesSection:
    """Stores the raw blending ranges subsection including its leading length field."""

    # Gets an empty blending ranges subsection.
    Empty = None

    def __init__(self, raw_data):
        """Initializes a new instance of the RawLayerBlendingRangesSection class.

        Args:
            raw_data: The raw subsection bytes including the length field.
        """
        self.raw_data = raw_data

    @property
    def raw_data(self):
        """Gets the raw subsection bytes including the length field."""
        return self._raw_data

    @raw_data.setter
    def raw_data(self, value):
        self._raw_data = value

    @staticmethod
    def load(reader, section_end):
        """Loads the blending ranges subsection from the reader.

        Args:
            reader: The reader positioned at the subsection length field.
            section_end: The byte position of the end of the enclosing layer extra data.

        Returns:
            The loaded RawLayerBlendingRangesSection instance.
        """
        from aspose_psd_foss.big_endian_reader import BigEndianReader
        from aspose_psd_foss.psd_section_reader import PsdSectionReader
        from aspose_psd_foss.core_exceptions.psd_load_exception import PsdLoadException

        length = reader.read_uint32()
        payload_length = PsdSectionReader.get_nested_memory_backed_length(
            reader,
            length,
            section_end,
            "Layer blending ranges subsection"
        )
        if payload_length > (2**31 - 1) - 4:
            raise PsdLoadException(
                "Layer blending ranges subsection is too large to preserve in memory "
                "with its length field."
            )

        raw_data = bytearray(4 + payload_length)
        RawLayerBlendingRangesSection._write_uint32_big_endian(
            raw_data, 0, length
        )
        if payload_length > 0:
            payload = reader.read_bytes(payload_length)
            raw_data[4:4 + payload_length] = payload

        return RawLayerBlendingRangesSection(raw_data)

    @staticmethod
    def _write_uint32_big_endian(buffer, offset, value):
        """Writes a 32-bit unsigned integer into a byte buffer in big-endian byte order.

        Args:
            buffer: The target buffer.
            offset: The destination offset in the buffer.
            value: The value to encode.
        """
        buffer[offset] = (value >> 24) & 0xFF
        buffer[offset + 1] = (value >> 16) & 0xFF
        buffer[offset + 2] = (value >> 8) & 0xFF
        buffer[offset + 3] = value & 0xFF


# Initialize the Empty static member
RawLayerBlendingRangesSection.Empty = RawLayerBlendingRangesSection(b'')
