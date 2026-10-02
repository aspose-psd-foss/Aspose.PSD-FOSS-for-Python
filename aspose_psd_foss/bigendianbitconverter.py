# Provides helper methods for reading big-endian primitive values from byte arrays.
class BigEndianBitConverter:
    """Provides helper methods for reading big-endian primitive values from byte arrays."""

    @classmethod
    def to_int32(cls, byte_array, offset):
        """Reads a 32-bit signed integer in big-endian format from the specified byte array."""
        return (
            (byte_array[offset] << 24)
            | (byte_array[offset + 1] << 16)
            | (byte_array[offset + 2] << 8)
            | byte_array[offset + 3]
        )
