import io
import struct
from enum import IntEnum
from typing import Union

from aspose_psd_foss.coreexceptions.psdloadexception import PsdLoadException

class SeekOrigin(IntEnum):
    """Defines seek origin for reader."""
    BEGIN = 0
    CUR = 1
    END = 2

class BigEndianReader:
    """
    Reads big-endian data from a stream.
    Used for parsing PSD file format which uses big-endian byte order.
    """

    def __init__(self, stream: io.BufferedIOBase, leave_open: bool = False):
        self._stream = stream
        self._leave_open = leave_open

    @property
    def position(self) -> int:
        return self._stream.tell()

    @property
    def length(self) -> int:
        current = self._stream.tell()
        self._stream.seek(0, io.SEEK_END)
        length = self._stream.tell()
        self._stream.seek(current, io.SEEK_SET)
        return length

    def seek(self, offset: int, origin: int) -> None:
        self._stream.seek(offset, origin)

    def read_byte(self) -> int:
        b = self._stream.read(1)
        if len(b) == 0:
            raise EOFError()
        return b[0]

    def read_sbyte(self) -> int:
        b = self._stream.read(1)
        if len(b) == 0:
            raise EOFError()
        return struct.unpack('b', b)[0]

    def read_bytes(self, count: int) -> bytes:
        buffer = bytearray(count)
        view = memoryview(buffer)
        total_read = 0
        while total_read < count:
            read = self._stream.readinto(view[total_read:])
            if read == 0:
                raise EOFError()
            total_read += read
        return bytes(buffer)

    def read_int16(self) -> int:
        data = self.read_exactly(2)
        return int.from_bytes(data, byteorder='big', signed=True)

    def read_uint16(self) -> int:
        data = self.read_exactly(2)
        return int.from_bytes(data, byteorder='big', signed=False)

    def read_int32(self) -> int:
        data = self.read_exactly(4)
        return int.from_bytes(data, byteorder='big', signed=True)

    def read_uint32(self) -> int:
        data = self.read_exactly(4)
        return int.from_bytes(data, byteorder='big', signed=False)

    def read_int64(self) -> int:
        data = self.read_exactly(8)
        return int.from_bytes(data, byteorder='big', signed=True)

    def read_uint64(self) -> int:
        data = self.read_exactly(8)
        return int.from_bytes(data, byteorder='big', signed=False)

    def read_single(self) -> float:
        data = self.read_exactly(4)
        return struct.unpack('>f', data)[0]

    def read_double(self) -> float:
        data = self.read_exactly(8)
        return struct.unpack('>d', data)[0]

    def read_pascal_string(self, max_length: int = 256) -> str:
        return self._read_pascal_string_aligned_to(4, max_length)

    def read_pascal_string_aligned_to2(self, max_length: int = 255) -> str:
        return self._read_pascal_string_aligned_to(2, max_length)

    def read_pascal_string_aligned_to4(self, max_length: int = 255) -> str:
        return self._read_pascal_string_aligned_to(4, max_length)

    def _read_pascal_string_aligned_to(self, boundary: int, max_length: int) -> str:
        length = self.read_byte()
        if length > max_length:
            raise PsdLoadException(
                f"PSD Pascal string length {length} exceeds the supported maximum {max_length}."
            )

        result = ""
        if length > 0:
            bytes_data = self.read_bytes(length)
            result = bytes_data.decode("ascii")

        padding = self._get_padding_length(length, boundary)
        if padding > 0:
            self.read_bytes(padding)

        return result

    def read_exactly(self, size: int) -> bytes:
        buffer = bytearray(size)
        view = memoryview(buffer)
        total_read = 0
        while total_read < size:
            read = self._stream.readinto(view[total_read:])
            if read == 0:
                raise EOFError()
            total_read += read
        return bytes(buffer)

    @classmethod
    def _get_padding_length(cls, payload_length: int, boundary: int) -> int:
        return (boundary - ((payload_length + 1) % boundary)) % boundary

    def skip(self, count: int) -> None:
        self._stream.seek(count, io.SEEK_CUR)

    def dispose(self) -> None:
        if not self._leave_open:
            self._stream.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.dispose()

