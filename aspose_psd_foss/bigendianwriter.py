import io

from aspose_psd_foss.core_exceptions.psd_save_exception import PsdSaveException


class BigEndianWriter:
    """Writes big-endian data to a stream.
    Used for writing PSD file format which uses big-endian byte order.
    """

    def __init__(self, stream: io.BufferedIOBase, leave_open: bool = False):
        """Initializes a new instance of the BigEndianWriter class.

        :param stream: The stream to write to.
        :param leave_open: true to keep the stream open; otherwise, false.
        """
        self._stream = stream
        self._leave_open = leave_open
        self._disposed = False

    @property
    def position(self) -> int:
        """Gets the current position within the stream."""
        return self._stream.tell()

    def seek(self, offset: int, origin: int):
        """Seeks to a position in the stream.

        :param offset: The byte offset relative to the origin.
        :param origin: The reference point used to obtain the new position.
        """
        self._stream.seek(offset, origin)

    def write_byte(self, value: int):
        """Writes a single byte to the stream.

        :param value: The byte value to write.
        """
        self._stream.write(bytes([value & 0xFF]))

    def write(self, buffer: bytes, offset: int = None, count: int = None):
        """Writes bytes to the stream.

        Overloads:
        - write(buffer: bytes)
        - write(buffer: bytes, offset: int, count: int)

        :param buffer: The byte array to write.
        :param offset: The zero-based byte offset in buffer at which to begin writing bytes.
        :param count: The number of bytes to write.
        """
        if offset is None and count is None:
            self._stream.write(buffer)
        else:
            self._stream.write(buffer[offset:offset + count])

    def write_sbyte(self, value: int):
        """Writes a signed byte (sbyte) to the stream.

        :param value: The sbyte value to write.
        """
        self._stream.write(bytes([value & 0xFF]))

    def write_int16(self, value: int):
        """Writes a 16-bit signed integer in big-endian format.

        :param value: The 16-bit signed integer to write.
        """
        self._stream.write(value.to_bytes(2, byteorder='big', signed=True))

    def write_uint16(self, value: int):
        """Writes a 16-bit unsigned integer in big-endian format.

        :param value: The 16-bit unsigned integer to write.
        """
        self._stream.write(value.to_bytes(2, byteorder='big', signed=False))

    def write_int32(self, value: int):
        """Writes a 32-bit signed integer in big-endian format.

        :param value: The 32-bit signed integer to write.
        """
        self._stream.write(value.to_bytes(4, byteorder='big', signed=True))

    def write_uint32(self, value: int):
        """Writes a 32-bit unsigned integer in big-endian format.

        :param value: The 32-bit unsigned integer to write.
        """
        self._stream.write(value.to_bytes(4, byteorder='big', signed=False))

    def write_int64(self, value: int):
        """Writes a 64-bit signed integer in big-endian format.

        :param value: The 64-bit signed integer to write.
        """
        self._stream.write(value.to_bytes(8, byteorder='big', signed=True))

    def write_uint64(self, value: int):
        """Writes a 64-bit unsigned integer in big-endian format.

        :param value: The 64-bit unsigned integer to write.
        """
        self._stream.write(value.to_bytes(8, byteorder='big', signed=False))

    def write_pascal_string(self, value: str):
        """Writes a PSD Pascal string whose length byte and payload are padded to a 4‑byte
        boundary.

        :param value: The string to write.
        """
        self.write_pascal_string_aligned_to4(value)

    def write_pascal_string_aligned_to2(self, value: str):
        """Writes a PSD resource Pascal string whose length byte and payload are padded to a
        2‑byte boundary.

        :param value: The ASCII string to write.
        :raises PsdSaveException: When the encoded string is too long for a PSD Pascal string.
        """
        self._write_pascal_string_aligned_to(value, boundary=2)

    def write_pascal_string_aligned_to4(self, value: str):
        """Writes a PSD layer Pascal string whose length byte and payload are padded to a
        4‑byte boundary.

        :param value: The ASCII string to write.
        :raises PsdSaveException: When the encoded string is too long for a PSD Pascal string.
        """
        self._write_pascal_string_aligned_to(value, boundary=4)

    @staticmethod
    def get_pascal_string_storage_length_aligned_to4(value: str) -> int:
        """Returns the stored byte count for a PSD Pascal string aligned to a 4‑byte boundary.

        :param value: The ASCII string to measure.
        :return: The length byte, payload, and padding byte count.
        """
        length = 0 if not value else len(value.encode('ascii'))
        return 1 + length + BigEndianWriter._get_padding_length(length, boundary=4)

    def _write_pascal_string_aligned_to(self, value: str, boundary: int):
        """Writes a Pascal string and pads it according to the enclosing PSD structure.

        :param value: The ASCII string to write.
        :param boundary: The byte boundary used by the enclosing structure.
        """
        bytes_val = value.encode('ascii')
        if len(bytes_val) > 0xFF:
            raise PsdSaveException(
                f"PSD Pascal string length {len(bytes_val)} exceeds the supported maximum {0xFF}."
            )
        self.write_byte(len(bytes_val))
        if bytes_val:
            self.write(bytes_val)
        padding = self._get_padding_length(len(bytes_val), boundary)
        for _ in range(padding):
            self.write_byte(0)

    @staticmethod
    def _get_padding_length(payload_length: int, boundary: int) -> int:
        """Calculates padding after a Pascal string length byte and payload.

        :param payload_length: The stored Pascal string payload length.
        :param boundary: The byte boundary used by the enclosing structure.
        :return: The number of padding bytes to write.
        """
        return (boundary - ((payload_length + 1) % boundary)) % boundary

    def write_all_bytes(self, data: bytes):
        """Writes all bytes from the specified array to the stream.

        :param data: The byte array to write.
        """
        self.write(data)

    def dispose(self):
        """Releases the stream resources."""
        if self._disposed:
            return
        self._disposed = True
        if not self._leave_open:
            self._stream.close()

