import sys
from aspose_psd_foss.bigendianreader import BigEndianReader
from aspose_psd_foss.psdsectionreader import PsdSectionReader
from aspose_psd_foss.coreexceptions.psdloadexception import PsdLoadException


class RawLayerBlendingRangesSection:
    @classmethod
    def empty(cls):
        return cls(b'')

    def __init__(self, raw_data):
        self._raw_data = raw_data

    @property
    def raw_data(self):
        return self._raw_data

    @classmethod
    def load(cls, reader, section_end):
        length = reader.read_uint32()
        payload_length = PsdSectionReader.get_nested_memory_backed_length(
            reader, length, section_end, "Layer blending ranges subsection"
        )
        if payload_length > (2**31 - 1 - 4):
            raise PsdLoadException(
                "Layer blending ranges subsection is too large to preserve in memory with its length field."
            )

        raw_data = bytearray(4 + payload_length)
        cls._write_uint32_big_endian(raw_data, 0, length)
        if payload_length > 0:
            payload = reader.read_bytes(payload_length)
            raw_data[4:4 + payload_length] = payload

        return cls(bytes(raw_data))

    @classmethod
    def _write_uint32_big_endian(cls, buffer, offset, value):
        buffer[offset] = (value >> 24) & 0xFF
        buffer[offset + 1] = (value >> 16) & 0xFF
        buffer[offset + 2] = (value >> 8) & 0xFF
        buffer[offset + 3] = value & 0xFF
