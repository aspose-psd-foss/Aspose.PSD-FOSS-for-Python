import struct
from aspose_psd_foss.coreexceptions.psdsaveexception import PsdSaveException


class BigEndianWriter:
    def __init__(self, stream, leave_open=False):
        self._stream = stream
        self._leave_open = leave_open
        self._disposed = False

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.dispose()
        return False  # Don't suppress exceptions

    @property
    def position(self):
        return self._stream.tell()

    def seek(self, offset, origin):
        self._stream.seek(offset, origin)

    def write(self, value):
        if isinstance(value, int):
            # single byte or sbyte treated as byte
            self._stream.write(bytes([value & 0xFF]))
        elif isinstance(value, (bytes, bytearray)):
            self._stream.write(value)
        else:
            raise TypeError("Unsupported type for write")

    def write_bytes(self, buffer, offset=0, count=None):
        if count is None:
            count = len(buffer) - offset
        self._stream.write(buffer[offset:offset + count])

    def write_sbyte(self, value):
        self._stream.write(bytes([value & 0xFF]))

    def write_short(self, value):
        self._stream.write(struct.pack('>h', value))

    def write_ushort(self, value):
        self._stream.write(struct.pack('>H', value))

    def write_uint16(self, value: int) -> None:
        """Write an unsigned 16‑bit integer (big‑endian)."""
        self.write_ushort(value)

    def write_int(self, value):
        self._stream.write(struct.pack('>i', value))

    def write_int32(self, value: int) -> None:
        """Write a signed 32‑bit integer (big‑endian)."""
        self.write_int(value)

    def write_uint(self, value):
        self._stream.write(struct.pack('>I', value))

    def write_uint32(self, value: int) -> None:
        """Alias for writing a 32‑bit unsigned integer."""
        self.write_uint(value)

    def write_int16(self, value: int) -> None:
        """Alias for writing a signed 16‑bit integer (short)."""
        self.write_short(value)

    def write_uint8(self, value: int) -> None:
        """Alias for writing a single unsigned byte."""
        self.write(value)

    def write_long(self, value):
        self._stream.write(struct.pack('>q', value))

    def write_ulong(self, value):
        self._stream.write(struct.pack('>Q', value))

    def write_pascal_string(self, value):
        self._write_pascal_string_aligned_to(value, boundary=4)

    def write_pascal_string_aligned_to2(self, value):
        self._write_pascal_string_aligned_to(value, boundary=2)

    def write_pascal_string_aligned_to_2(self, value: str) -> None:
        """Alias for writing a Pascal string aligned to a 2‑byte boundary."""
        self.write_pascal_string_aligned_to2(value)

    def write_pascal_string_aligned_to4(self, value):
        self._write_pascal_string_aligned_to(value, boundary=4)

    @classmethod
    def get_pascal_string_storage_length_aligned_to4(cls, value):
        length = 0 if not value else len(value.encode('ascii'))
        return 1 + length + cls._get_padding_length(length, 4)

    def _write_pascal_string_aligned_to(self, value, boundary):
        bytes_value = value.encode('ascii')
        if len(bytes_value) > 0xFF:
            raise PsdSaveException(
                f"PSD Pascal string length {len(bytes_value)} exceeds the supported maximum {0xFF}."
            )
        self.write(len(bytes_value))
        if bytes_value:
            self.write(bytes_value)
        padding = self._get_padding_length(len(bytes_value), boundary)
        for _ in range(padding):
            self.write(0)

    @classmethod
    def _get_padding_length(cls, payload_length, boundary):
        return (boundary - ((payload_length + 1) % boundary)) % boundary

    def write_all_bytes(self, data):
        self.write(data)

    def dispose(self):
        if self._disposed:
            return
        self._disposed = True
        if not self._leave_open:
            self._stream.close()