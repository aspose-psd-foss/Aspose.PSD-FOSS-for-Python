import io
import struct
from typing import BinaryIO, Optional


class BigEndianWriter:
    def __init__(self, stream: BinaryIO, leave_open: bool = False) -> None:
        self._stream = stream
        self._leave_open = leave_open

    def close(self) -> None:
        if not self._leave_open:
            self._stream.close()

    def write(self, data: bytes) -> None:
        self._stream.write(data)

    def write_int16(self, value: int) -> None:
        self._stream.write(struct.pack(">h", value))

    def write_uint16(self, value: int) -> None:
        self._stream.write(struct.pack(">H", value))

    def write_int32(self, value: int) -> None:
        self._stream.write(struct.pack(">i", value))

    def write_uint32(self, value: int) -> None:
        self._stream.write(struct.pack(">I", value))

    def write_int64(self, value: int) -> None:
        self._stream.write(struct.pack(">q", value))

    def write_uint64(self, value: int) -> None:
        """Write an unsigned 64‑bit integer in big‑endian order."""
        self._stream.write(struct.pack(">Q", value))

    def write_float(self, value: float) -> None:
        self._stream.write(struct.pack(">f", value))

    def write_double(self, value: float) -> None:
        self._stream.write(struct.pack(">d", value))

    def write_bytes(self, data: bytes) -> None:
        self._stream.write(data)

    def flush(self) -> None:
        self._stream.flush()

    @property
    def position(self) -> int:
        return self._stream.tell()

    @position.setter
    def position(self, pos: int) -> None:
        self._stream.seek(pos)
