"""
Provides helper methods for reading big-endian primitive values from byte arrays.
"""


class BigEndianBitConverter:
    """Helper methods for reading big-endian primitive values from byte arrays."""

    @staticmethod
    def to_int32(bytes_, offset):
        """Reads a 32-bit signed integer in big-endian format from the specified byte array.

        Args:
            bytes_: The source byte array.
            offset: The zero-based offset of the integer.

        Returns:
            The parsed 32-bit signed integer.
        """
        return (bytes_[offset] << 24) | (bytes_[offset + 1] << 16) | (bytes_[offset + 2] << 8) | bytes_[offset + 3]
