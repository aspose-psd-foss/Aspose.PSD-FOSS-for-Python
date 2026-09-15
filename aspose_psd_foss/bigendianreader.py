import struct

from aspose_psd_foss.core_exceptions.psd_load_exception import PsdLoadException


class BigEndianReader:
    """Reads big-endian data from a stream.
    Used for parsing PSD file format which uses big-endian byte order.
    """

    def __init__(self, stream, leave_open=False):
        # Stores the underlying source stream.
        self._stream = stream
        # Indicates whether disposing the reader should leave the stream open.
        self._leave_open = leave_open

    @property
    def position(self):
        """Gets the current position within the stream."""
        return self._stream.tell()

    @property
    def length(self):
        """Gets the total length of the stream."""
        current = self._stream.tell()
        self._stream.seek(0, 2)  # SEEK_END
        length = self._stream.tell()
        self._stream.seek(current, 0)  # SEEK_SET
        return length

    def seek(self, offset, origin):
        """Seeks to a position in the stream."""
        self._stream.seek(offset, origin)

    def read_byte(self):
        """Reads a single byte from the stream."""
        b = self._stream.read(1)
        if len(b) == 0:
            raise EOFError()
        return b[0]

    def read_sbyte(self):
        """Reads a signed byte (sbyte) from the stream."""
        b = self._stream.read(1)
        if len(b) == 0:
            raise EOFError()
        value = b[0]
        return value - 256 if value >= 128 else value

    def read_bytes(self, count):
        """Reads a specified number of bytes from the stream."""
        buffer = bytearray()
        while len(buffer) < count:
            chunk = self._stream.read(count - len(buffer))
            if not chunk:
                raise EOFError()
            buffer.extend(chunk)
        return bytes(buffer)

    def read_int16(self):
        """Reads a 16-bit signed integer in big-endian format."""
        data = self._read_exactly(2)
        return int.from_bytes(data, "big", signed=True)

    def read_uint16(self):
        """Reads a 16-bit unsigned integer in big-endian format."""
        data = self._read_exactly(2)
        return int.from_bytes(data, "big", signed=False)

    def read_int32(self):
        """Reads a 32-bit signed integer in big-endian format."""
        data = self._read_exactly(4)
        return int.from_bytes(data, "big", signed=True)

    def read_uint32(self):
        """Reads a 32-bit unsigned integer in big-endian format."""
        data = self._read_exactly(4)
        return int.from_bytes(data, "big", signed=False)

    def read_int64(self):
        """Reads a 64-bit signed integer in big-endian format."""
        data = self._read_exactly(8)
        return int.from_bytes(data, "big", signed=True)

    def read_uint64(self):
        """Reads a 64-bit unsigned integer in big-endian format."""
        data = self._read_exactly(8)
        return int.from_bytes(data, "big", signed=False)

    def read_single(self):
        """Reads a 32-bit floating-point number in big-endian format."""
        data = self._read_exactly(4)
        return struct.unpack(">f", data)[0]

    def read_double(self):
        """Reads a 64-bit floating-point number in big-endian format."""
        data = self._read_exactly(8)
        return struct.unpack(">d", data)[0]

    def read_pascal_string(self, max_length=256):
        """Reads a PSD Pascal string whose length byte and payload are
        padded to a 4-byte boundary.
        """
        return self._read_pascal_string_aligned_to(4, max_length)

    def read_pascal_string_aligned_to2(self, max_length=255):
        """Reads a PSD resource Pascal string whose length byte and
        payload are padded to a 2-byte boundary.
        """
        return self._read_pascal_string_aligned_to(2, max_length)

    def read_pascal_string_aligned_to4(self, max_length=255):
        """Reads a PSD layer Pascal string whose length byte and payload
        are padded to a 4-byte boundary.
        """
        return self._read_pascal_string_aligned_to(4, max_length)

    def _read_pascal_string_aligned_to(self, boundary, max_length):
        """Reads a Pascal string and consumes alignment padding according to
        the enclosing PSD structure.
        """
        length = self.read_byte()
        if length > max_length:
            raise PsdLoadException(
                f"PSD Pascal string length {length} exceeds the supported "
                f"maximum {max_length}."
            )

        result = ""
        if length > 0:
            bytes_data = self.read_bytes(length)
            result = bytes_data.decode("ascii")

        padding = self._get_padding_length(length, boundary)
        if padding > 0:
            self.read_bytes(padding)

        return result

    def _read_exactly(self, size):
        """Reads exactly the requested number of bytes into a buffer."""
        buffer = bytearray()
        while len(buffer) < size:
            chunk = self._stream.read(size - len(buffer))
            if not chunk:
                raise EOFError()
            buffer.extend(chunk)
        return bytes(buffer)

    @staticmethod
    def _get_padding_length(payload_length, boundary):
        """Calculates padding after a Pascal string length byte and payload."""
        return (boundary - ((payload_length + 1) % boundary)) % boundary

    def skip(self, count):
        """Skips the specified number of bytes in the stream."""
        self._stream.seek(count, 1)  # SEEK_CUR

    def dispose(self):
        """Releases the stream resources."""
        if not self._leave_open:
            self._stream.close()

