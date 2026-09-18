import io
import struct
from aspose_psd_foss.coreexceptions.psdloadexception import PsdLoadException


class BigEndianReader:
    """Reads big-endian data from a stream.
    Used for parsing PSD file format which uses big-endian byte order.
    """

    # Stores the underlying source stream.
    # Indicates whether disposing the reader should leave the stream open.
    def __init__(self, stream: io.BufferedIOBase, leave_open: bool = False):
        self._stream = stream
        self._leave_open = leave_open

    # Gets the current position within the stream.
    @property
    def position(self) -> int:
        return self._stream.tell()

    # Gets the total length of the stream.
    @property
    def length(self) -> int:
        current = self._stream.tell()
        self._stream.seek(0, io.SEEK_END)
        length = self._stream.tell()
        self._stream.seek(current, io.SEEK_SET)
        return length

    # Seeks to a position in the stream.
    def seek(self, offset: int, origin: int):
        self._stream.seek(offset, origin)

    # Reads a single byte from the stream.
    def read_byte(self) -> int:
        b = self._stream.read(1)
        if len(b) == 0:
            raise EOFError()
        return b[0]

    # Reads a signed byte (sbyte) from the stream.
    def read_sbyte(self) -> int:
        b = self._stream.read(1)
        if len(b) == 0:
            raise EOFError()
        return int.from_bytes(b, byteorder='big', signed=True)

    # Reads a specified number of bytes from the stream.
    def read_bytes(self, count: int) -> bytes:
        buffer = bytearray(count)
        total_read = 0
        while total_read < count:
            chunk = self._stream.read(count - total_read)
            if not chunk:
                raise EOFError()
            buffer[total_read:total_read + len(chunk)] = chunk
            total_read += len(chunk)
        return bytes(buffer)

    # Reads a 16-bit signed integer in big-endian format.
    def read_int16(self) -> int:
        buffer = self._read_exactly(2)
        return int.from_bytes(buffer, byteorder='big', signed=True)

    # Reads a 16-bit unsigned integer in big-endian format.
    def read_uint16(self) -> int:
        buffer = self._read_exactly(2)
        return int.from_bytes(buffer, byteorder='big', signed=False)

    # Reads a 32-bit signed integer in big-endian format.
    def read_int32(self) -> int:
        buffer = self._read_exactly(4)
        return int.from_bytes(buffer, byteorder='big', signed=True)

    # Reads a 32-bit unsigned integer in big-endian format.
    def read_uint32(self) -> int:
        buffer = self._read_exactly(4)
        return int.from_bytes(buffer, byteorder='big', signed=False)

    # Reads a 64-bit signed integer in big-endian format.
    def read_int64(self) -> int:
        buffer = self._read_exactly(8)
        return int.from_bytes(buffer, byteorder='big', signed=True)

    # Reads a 64-bit unsigned integer in big-endian format.
    def read_uint64(self) -> int:
        buffer = self._read_exactly(8)
        return int.from_bytes(buffer, byteorder='big', signed=False)

    # Reads a 32-bit floating-point number in big-endian format.
    def read_single(self) -> float:
        buffer = self._read_exactly(4)
        return struct.unpack('>f', buffer)[0]

    # Reads a 64-bit floating-point number in big-endian format.
    def read_double(self) -> float:
        buffer = self._read_exactly(8)
        return struct.unpack('>d', buffer)[0]

    # Reads a PSD Pascal string whose length byte and payload are padded to a 4-byte boundary.
    def read_pascal_string(self, max_length: int = 256) -> str:
        return self.read_pascal_string_aligned_to_4(max_length)

    # Reads a PSD resource Pascal string whose length byte and payload are padded to a 2-byte boundary.
    def read_pascal_string_aligned_to_2(self, max_length: int = 255) -> str:
        return self._read_pascal_string_aligned_to(2, max_length)

    # Reads a PSD layer Pascal string whose length byte and payload are padded to a 4-byte boundary.
    def read_pascal_string_aligned_to_4(self, max_length: int = 255) -> str:
        return self._read_pascal_string_aligned_to(4, max_length)

    # Reads a Pascal string and consumes alignment padding according to the enclosing PSD structure.
    def _read_pascal_string_aligned_to(self, boundary: int, max_length: int) -> str:
        length = self.read_byte()
        if length > max_length:
            raise PsdLoadException(f"PSD Pascal string length {length} exceeds the supported maximum {max_length}.")
        result = ''
        if length > 0:
            bytes_data = self.read_bytes(length)
            result = bytes_data.decode('ascii')
        padding = self._get_padding_length(length, boundary)
        if padding > 0:
            self.read_bytes(padding)
        return result

    # Reads exactly the requested number of bytes into a stack or array span.
    def _read_exactly(self, size: int) -> bytes:
        buffer = bytearray(size)
        view = memoryview(buffer)
        total_read = 0
        while total_read < size:
            read = self._stream.readinto(view[total_read:])
            if read == 0:
                raise EOFError()
            total_read += read
        return bytes(buffer)

    # Calculates padding after a Pascal string length byte and payload.
    @staticmethod
    def _get_padding_length(payload_length: int, boundary: int) -> int:
        return (boundary - ((payload_length + 1) % boundary)) % boundary

    # Skips the specified number of bytes in the stream.
    def skip(self, count: int):
        self._stream.seek(count, io.SEEK_CUR)

    # Releases the stream resources.
    def close(self):
        if not self._leave_open:
            self._stream.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

