from __future__ import annotations

import struct
from typing import BinaryIO

from aspose_psd_foss.coreexceptions.psdsaveexception import PsdSaveException


class BigEndianWriter:
    """Writes big-endian data to a stream.
    Used for writing PSD file format which uses big-endian byte order.
    """

    def __init__(self, stream: BinaryIO, leave_open: bool = False):
        self._stream = stream
        self._leave_open = leave_open
        self._disposed = False

    @property
    def position(self) -> int:
        return self._stream.tell()

    def seek(self, offset: int, origin: int = 0) -> None:
        """Seek to a position in the stream.
        origin follows the same convention as :py:meth:`io.IOBase.seek`.
        """
        self._stream.seek(offset, origin)

    def write_byte(self, value: int) -> None:
        """Write a single byte."""
        self._stream.write(bytes([value & 0xFF]))

    def write(self, buffer: bytes, offset: int | None = None, count: int | None = None) -> None:
        """Write bytes to the stream.
        If *offset* and *count* are provided, a slice of *buffer* is written.
        """
        if offset is None and count is None:
            self._stream.write(buffer)
        else:
            start = offset or 0
            end = start + (count if count is not None else len(buffer) - start)
            self._stream.write(buffer[start:end])

    def write_sbyte(self, value: int) -> None:
        """Write a signed byte."""
        self.write_byte(value)

    def write_int16(self, value: int) -> None:
        self._stream.write(struct.pack('>h', value))

    def write_uint16(self, value: int) -> None:
        self._stream.write(struct.pack('>H', value))

    def write_int32(self, value: int) -> None:
        self._stream.write(struct.pack('>i', value))

    def write_uint32(self, value: int) -> None:
        self._stream.write(struct.pack('>I', value))

    def write_int64(self, value: int) -> None:
        self._stream.write(struct.pack('>q', value))

    def write_uint64(self, value: int) -> None:
        self._stream.write(struct.pack('>Q', value))

    def write_pascal_string(self, value: str) -> None:
        self._write_pascal_string_aligned_to(value, boundary=4)

    def write_pascal_string_aligned_to_2(self, value: str) -> None:
        self._write_pascal_string_aligned_to(value, boundary=2)

    def write_pascal_string_aligned_to_4(self, value: str) -> None:
        self._write_pascal_string_aligned_to(value, boundary=4)

    @staticmethod
    def get_pascal_string_storage_length_aligned_to_4(value: str) -> int:
        length = len(value.encode('ascii')) if value else 0
        return 1 + length + BigEndianWriter._get_padding_length(length, boundary=4)

    def _write_pascal_string_aligned_to(self, value: str, boundary: int) -> None:
        data = value.encode('ascii')
        if len(data) > 0xFF:
            raise PsdSaveException(
                f"PSD Pascal string length {len(data)} exceeds the supported maximum {0xFF}."
            )
        self.write_byte(len(data))
        if data:
            self.write(data)
        padding = self._get_padding_length(len(data), boundary)
        if padding:
            self.write(bytes(padding))

    @staticmethod
    def _get_padding_length(payload_length: int, boundary: int) -> int:
        return (boundary - ((payload_length + 1) % boundary)) % boundary

    def write_all_bytes(self, data: bytes) -> None:
        self.write(data)

    def dispose(self) -> None:
        if self._disposed:
            return
        self._disposed = True
        if not self._leave_open:
            self._stream.close()

    def __enter__(self) -> "BigEndianWriter":
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        self.dispose()

