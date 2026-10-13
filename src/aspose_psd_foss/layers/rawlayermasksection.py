from aspose_psd_foss.bigendianreader import BigEndianReader
from aspose_psd_foss.psdsectionreader import PsdSectionReader
from aspose_psd_foss.coreexceptions.psdloadexception import PsdLoadException
from typing import ClassVar

class RawLayerMaskSection:
    Empty: ClassVar["RawLayerMaskSection"]

    @classmethod
    def empty(cls):
        return cls(b'')

    def __init__(self, raw_data: bytes):
        self._raw_data = raw_data

    @property
    def raw_data(self) -> bytes:
        return self._raw_data

    @classmethod
    def load(cls, reader: BigEndianReader, section_end: int):
        length = reader.read_uint32()
        payload_length = PsdSectionReader.get_nested_memory_backed_length(
            reader, length, section_end, "Layer mask subsection"
        )
        if payload_length > (2**31 - 1) - 4:
            raise PsdLoadException(
                "Layer mask subsection is too large to preserve in memory with its length field."
            )

        raw_data = bytearray(4 + payload_length)
        cls._write_uint32_big_endian(raw_data, 0, length)
        if payload_length > 0:
            payload = reader.read_bytes(payload_length)
            raw_data[4:] = payload

        return cls(bytes(raw_data))

    @classmethod
    def _write_uint32_big_endian(cls, buffer: bytearray, offset: int, value: int):
        buffer[offset] = (value >> 24) & 0xFF
        buffer[offset + 1] = (value >> 16) & 0xFF
        buffer[offset + 2] = (value >> 8) & 0xFF
        buffer[offset + 3] = value & 0xFF


RawLayerMaskSection.Empty = RawLayerMaskSection(b'')
