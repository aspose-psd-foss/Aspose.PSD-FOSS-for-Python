import struct

from aspose_psd_foss.coreexceptions.psdloadexception import PsdLoadException


class BigEndianReader:
    """
    Reads big-endian data from a stream.
    Used for parsing PSD file format which uses big-endian byte order.
    """

    def __init__(self, stream, leave_open=False):
        """
        Initializes a new instance of the BigEndianReader class.
        
        :param stream: The stream to read from.
        :param leave_open: True to keep the stream open; otherwise, False.
        """
        self._stream = stream
        self._leave_open = leave_open

    @property
    def position(self):
        """Gets the current position within the stream."""
        return self._stream.tell()

    @property
    def length(self):
        """Gets the total length of the stream."""
        current_pos = self._stream.tell()
        self._stream.seek(0, 2)
        length = self._stream.tell()
        self._stream.seek(current_pos, 0)
        return length

    def seek(self, offset, origin):
        """
        Seeks to a position in the stream.
        
        :param offset: The byte offset relative to the origin.
        :param origin: The reference point used to obtain the new position.
        """
        self._stream.seek(offset, origin)

    def read_byte(self):
        """
        Reads a single byte from the stream.
        
        :return: The byte read from the stream.
        :raises EndOfStreamException: Thrown when the end of the stream is reached.
        """
        b = self._stream.read(1)
        if not b:
            raise EndOfStreamException()
        return b[0]

    def read_sbyte(self):
        """
        Reads a signed byte (sbyte) from the stream.
        
        :return: The sbyte read from the stream.
        :raises EndOfStreamException: Thrown when the end of the stream is reached.
        """
        b = self._stream.read(1)
        if not b:
            raise EndOfStreamException()
        return struct.unpack('b', b)[0]

    def read_bytes(self, count):
        """
        Reads a specified number of bytes from the stream.
        
        :param count: The number of bytes to read.
        :return: The byte array containing the data read from the stream.
        :raises EndOfStreamException: Thrown when the end of the stream is reached before reading the requested count.
        """
        buffer = bytearray(count)
        total_read = 0

        while total_read < count:
            chunk = self._stream.read(count - total_read)
            if not chunk:
                raise EndOfStreamException()
            buffer[total_read:total_read + len(chunk)] = chunk
            total_read += len(chunk)

        return bytes(buffer)

    def read_int16(self):
        """
        Reads a 16-bit signed integer in big-endian format.
        
        :return: The 16-bit signed integer read from the stream.
        """
        data = self.read_bytes(2)
        return struct.unpack('>h', data)[0]

    def read_uint16(self):
        """
        Reads a 16-bit unsigned integer in big-endian format.
        
        :return: The 16-bit unsigned integer read from the stream.
        """
        data = self.read_bytes(2)
        return struct.unpack('>H', data)[0]

    def read_int32(self):
        """
        Reads a 32-bit signed integer in big-endian format.
        
        :return: The 32-bit signed integer read from the stream.
        """
        data = self.read_bytes(4)
        return struct.unpack('>i', data)[0]

    def read_uint32(self):
        """
        Reads a 32-bit unsigned integer in big-endian format.
        
        :return: The 32-bit unsigned integer read from the stream.
        """
        data = self.read_bytes(4)
        return struct.unpack('>I', data)[0]

    def read_int64(self):
        """
        Reads a 64-bit signed integer in big-endian format.
        
        :return: The 64-bit signed integer read from the stream.
        """
        data = self.read_bytes(8)
        return struct.unpack('>q', data)[0]

    def read_uint64(self):
        """
        Reads a 64-bit unsigned integer in big-endian format.
        
        :return: The 64-bit unsigned integer read from the stream.
        """
        data = self.read_bytes(8)
        return struct.unpack('>Q', data)[0]

    def read_single(self):
        """
        Reads a 32-bit floating-point number in big-endian format.
        
        :return: The 32-bit floating-point number read from the stream.
        """
        data = self.read_bytes(4)
        return struct.unpack('>f', data)[0]

    def read_double(self):
        """
        Reads a 64-bit floating-point number in big-endian format.
        
        :return: The 64-bit floating-point number read from the stream.
        """
        data = self.read_bytes(8)
        return struct.unpack('>d', data)[0]

    def read_pascal_string(self, max_length=256):
        """
        Reads a PSD Pascal string whose length byte and payload are padded to a 4-byte boundary.
        
        :param max_length: The maximum length of the string to read.
        :return: The string read from the stream.
        """
        return self.read_pascal_string_aligned_to_4(max_length)

    def read_pascal_string_aligned_to_2(self, max_length=255):
        """
        Reads a PSD resource Pascal string whose length byte and payload are padded to a 2-byte boundary.
        
        :param max_length: The maximum payload length to accept.
        :return: The decoded ASCII string.
        :raises PsdLoadException: Thrown when the stored string length exceeds max_length.
        """
        return self.read_pascal_string_aligned_to(2, max_length)

    def read_pascal_string_aligned_to_4(self, max_length=255):
        """
        Reads a PSD layer Pascal string whose length byte and payload are padded to a 4-byte boundary.
        
        :param max_length: The maximum payload length to accept.
        :return: The decoded ASCII string.
        :raises PsdLoadException: Thrown when the stored string length exceeds max_length.
        """
        return self.read_pascal_string_aligned_to(4, max_length)

    def read_pascal_string_aligned_to(self, boundary, max_length):
        """
        Reads a Pascal string and consumes alignment padding according to the enclosing PSD structure.
        
        :param boundary: The byte boundary used by the enclosing structure.
        :param max_length: The maximum payload length to accept.
        :return: The decoded ASCII string.
        :raises PsdLoadException: Thrown when the stored string length exceeds max_length.
        """
        length = self.read_byte()
        if length > max_length:
            raise PsdLoadException(f"PSD Pascal string length {length} exceeds the supported maximum {max_length}.")

        result = ""
        if length > 0:
            data = self.read_bytes(length)
            result = data.decode('ascii')

        padding = self._get_padding_length(length, boundary)
        if padding > 0:
            self.read_bytes(padding)

        return result

    def skip(self, count):
        """
        Skips the specified number of bytes in the stream.
        
        :param count: The number of bytes to skip.
        """
        self._stream.seek(count, 1)

    def dispose(self):
        """
        Releases the stream resources.
        """
        if not self._leave_open:
            self._stream.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.dispose()

    @classmethod
    def _get_padding_length(cls, payload_length, boundary):
        """
        Calculates padding after a Pascal string length byte and payload.
        
        :param payload_length: The stored Pascal string payload length.
        :param boundary: The byte boundary used by the enclosing structure.
        :return: The number of padding bytes to consume.
        """
        return (boundary - ((payload_length + 1) % boundary)) % boundary


class EndOfStreamException(Exception):
    """Exception thrown when the end of the stream is reached."""
    pass
