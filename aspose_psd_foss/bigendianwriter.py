import math
from typing import Optional

from aspose_psd_foss.coreexceptions.psdsaveexception import PsdSaveException
from aspose_psd_foss.streamcontainer import StreamContainer


class BigEndianWriter:
    """
    Writes big-endian data to a stream.
    Used for writing PSD file format which uses big-endian byte order.
    """

    def __init__(self, stream, leave_open=False):
        """
        Initializes a new instance of the BigEndianWriter class.

        :param stream: The stream to write to.
        :param leave_open: True to keep the stream open; otherwise, False.
        """
        self._stream = stream
        self._leave_open = leave_open
        self._disposed = False

    @property
    def position(self):
        """Gets the current position within the stream."""
        return self._stream.position

    def seek(self, offset, origin):
        """
        Seeks to a position in the stream.

        :param offset: The byte offset relative to the origin.
        :param origin: The reference point used to obtain the new position.
        """
        self._stream.seek(offset, origin)

    def write(self, value, *args):
        """
        Writes data to the stream.

        Overloads:
        - write(value: byte)
        - write(buffer: list[byte])
        - write(buffer: list[byte], offset: int, count: int)
        - write(value: sbyte)
        - write(value: short)
        - write(value: int)
        - write(value: long)
        - write(value: uint)
        - write(value: ulong)
        """
        if len(args) == 0:
            if isinstance(value, int):
                if 0 <= value <= 0xFF:
                    self._stream.write_byte(value)
                elif -0x80 <= value < 0:
                    self._stream.write_byte(value & 0xFF)
                elif -0x8000 <= value < 0x8000:
                    self._stream.write(self._int16_to_bytes(value, big_endian=True))
                elif -0x80000000 <= value < 0x80000000:
                    self._stream.write(self._int32_to_bytes(value, big_endian=True))
                elif value < 0:
                    self._stream.write(self._int64_to_bytes(value, big_endian=True))
                else:
                    # unsigned
                    if value < 0x10000:
                        self._stream.write(self._uint16_to_bytes(value, big_endian=True))
                    elif value < 0x100000000:
                        self._stream.write(self._uint32_to_bytes(value, big_endian=True))
                    else:
                        self._stream.write(self._uint64_to_bytes(value, big_endian=True))
            else:
                raise TypeError("Unsupported type for single argument write")
        elif len(args) == 1 and isinstance(args[0], int):
            count = args[0]
            self._stream.write(value[:count])
        elif len(args) == 2:
            offset, count = args
            self._stream.write(value[offset:offset + count])
        else:
            raise TypeError("Unsupported write overload")

    def write_sbyte(self, value):
        """Writes a signed byte (sbyte) to the stream."""
        self._stream.write_byte(value & 0xFF)

    def write_short(self, value):
        """Writes a 16-bit signed integer in big-endian format."""
        self._stream.write(self._int16_to_bytes(value, big_endian=True))

    def write_ushort(self, value):
        """Writes a 16-bit unsigned integer in big-endian format."""
        self._stream.write(self._uint16_to_bytes(value, big_endian=True))

    def write_int(self, value):
        """Writes a 32-bit signed integer in big-endian format."""
        self._stream.write(self._int32_to_bytes(value, big_endian=True))

    def write_uint(self, value):
        """Writes a 32-bit unsigned integer in big-endian format."""
        self._stream.write(self._uint32_to_bytes(value, big_endian=True))

    def write_long(self, value):
        """Writes a 64-bit signed integer in big-endian format."""
        self._stream.write(self._int64_to_bytes(value, big_endian=True))

    def write_ulong(self, value):
        """Writes a 64-bit unsigned integer in big-endian format."""
        self._stream.write(self._uint64_to_bytes(value, big_endian=True))

    def write_pascal_string(self, value):
        """Writes a PSD Pascal string whose length byte and payload are padded to a 4-byte boundary."""
        self.write_pascal_string_aligned_to_4(value)

    def write_pascal_string_aligned_to_2(self, value):
        """
        Writes a PSD resource Pascal string whose length byte and payload are padded to a 2-byte boundary.

        :param value: The ASCII string to write.
        :raises PsdSaveException: If the encoded string is too long.
        """
        self._write_pascal_string_aligned(value, boundary=2)

    def write_pascal_string_aligned_to_4(self, value):
        """
        Writes a PSD layer Pascal string whose length byte and payload are padded to a 4-byte boundary.

        :param value: The ASCII string to write.
        :raises PsdSaveException: If the encoded string is too long.
        """
        self._write_pascal_string_aligned(value, boundary=4)

    @classmethod
    def get_pascal_string_storage_length_aligned_to_4(cls, value):
        """
        Returns the stored byte count for a PSD Pascal string aligned to a 4-byte boundary.

        :param value: The ASCII string to measure.
        :return: The length byte, payload, and padding byte count.
        """
        length = 0 if not value or value is None else len(value.encode('ascii'))
        return 1 + length + cls._get_padding_length(length, boundary=4)

    def _write_pascal_string_aligned(self, value, boundary):
        bytes_ = value.encode('ascii')
        if len(bytes_) > 0xFF:
            raise PsdSaveException(f"PSD Pascal string length {len(bytes_)} exceeds the supported maximum 255.")

        self._stream.write_byte(len(bytes_))
        if len(bytes_) > 0:
            self._stream.write(bytes_)

        padding = self._get_padding_length(len(bytes_), boundary)
        for _ in range(padding):
            self._stream.write_byte(0)

    @staticmethod
    def _get_padding_length(payload_length, boundary):
        return (boundary - ((payload_length + 1) % boundary)) % boundary

    def write_all_bytes(self, data):
        """Writes all bytes from the specified array to the stream."""
        self.write(data)

    def dispose(self):
        """Releases the stream resources."""
        if self._disposed:
            return

        self._disposed = True

        if not self._leave_open:
            self._stream.dispose()

    @staticmethod
    def _int16_to_bytes(value, big_endian=True):
        """Convert 16-bit signed integer to bytes."""
        if big_endian:
            return bytes([(value >> 8) & 0xFF, value & 0xFF])
        else:
            return bytes([value & 0xFF, (value >> 8) & 0xFF])

    @staticmethod
    def _uint16_to_bytes(value, big_endian=True):
        """Convert 16-bit unsigned integer to bytes."""
        if big_endian:
            return bytes([(value >> 8) & 0xFF, value & 0xFF])
        else:
            return bytes([value & 0xFF, (value >> 8) & 0xFF])

    @staticmethod
    def _int32_to_bytes(value, big_endian=True):
        """Convert 32-bit signed integer to bytes."""
        if big_endian:
            return bytes([
                (value >> 24) & 0xFF,
                (value >> 16) & 0xFF,
                (value >> 8) & 0xFF,
                value & 0xFF
            ])
        else:
            return bytes([
                value & 0xFF,
                (value >> 8) & 0xFF,
                (value >> 16) & 0xFF,
                (value >> 24) & 0xFF
            ])

    @staticmethod
    def _uint32_to_bytes(value, big_endian=True):
        """Convert 32-bit unsigned integer to bytes."""
        if big_endian:
            return bytes([
                (value >> 24) & 0xFF,
                (value >> 16) & 0xFF,
                (value >> 8) & 0xFF,
                value & 0xFF
            ])
        else:
            return bytes([
                value & 0xFF,
                (value >> 8) & 0xFF,
                (value >> 16) & 0xFF,
                (value >> 24) & 0xFF
            ])

    @staticmethod
    def _int64_to_bytes(value, big_endian=True):
        """Convert 64-bit signed integer to bytes."""
        if big_endian:
            return bytes([
                (value >> 56) & 0xFF,
                (value >> 48) & 0xFF,
                (value >> 40) & 0xFF,
                (value >> 32) & 0xFF,
                (value >> 24) & 0xFF,
                (value >> 16) & 0xFF,
                (value >> 8) & 0xFF,
                value & 0xFF
            ])
        else:
            return bytes([
                value & 0xFF,
                (value >> 8) & 0xFF,
                (value >> 16) & 0xFF,
                (value >> 24) & 0xFF,
                (value >> 32) & 0xFF,
                (value >> 40) & 0xFF,
                (value >> 48) & 0xFF,
                (value >> 56) & 0xFF
            ])

    @staticmethod
    def _uint64_to_bytes(value, big_endian=True):
        """Convert 64-bit unsigned integer to bytes."""
        if big_endian:
            return bytes([
                (value >> 56) & 0xFF,
                (value >> 48) & 0xFF,
                (value >> 40) & 0xFF,
                (value >> 32) & 0xFF,
                (value >> 24) & 0xFF,
                (value >> 16) & 0xFF,
                (value >> 8) & 0xFF,
                value & 0xFF
            ])
        else:
            return bytes([
                value & 0xFF,
                (value >> 8) & 0xFF,
                (value >> 16) & 0xFF,
                (value >> 24) & 0xFF,
                (value >> 32) & 0xFF,
                (value >> 40) & 0xFF,
                (value >> 48) & 0xFF,
                (value >> 56) & 0xFF
            ])
