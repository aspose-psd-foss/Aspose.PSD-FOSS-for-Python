import sys
from aspose_psd_foss.bigendianreader import BigEndianReader
from aspose_psd_foss.coreexceptions.psdloadexception import PsdLoadException


class PsdSectionReader:
    """Provides bounded reads for PSD/PSB sections that are stored in memory by this implementation."""

    @classmethod
    def read_bytes(cls, reader, length, section_name):
        """Reads a declared section payload after validating stream boundaries and the in-memory size limit.

        Args:
            reader: The reader positioned at the start of the section payload.
            length: The declared payload length.
            section_name: The PSD/PSB section name used in error messages.

        Returns:
            The section payload bytes.
        """
        bounded_length = cls.get_memory_backed_length(reader, length, section_name)
        return [] if bounded_length == 0 else reader.read_bytes(bounded_length)

    @classmethod
    def get_memory_backed_length(cls, reader, length, section_name):
        """Validates a declared section length and returns the equivalent in-memory array size.

        Args:
            reader: The reader positioned at the start of the section payload.
            length: The declared payload length.
            section_name: The PSD/PSB section name used in error messages.

        Returns:
            The validated length as an int.

        Raises:
            PsdLoadException: Thrown when the declared length cannot be represented or exceeds available bytes.
        """
        if length > sys.maxsize:
            raise PsdLoadException(f"{section_name} length {length} exceeds the current in-memory parser limit of {sys.maxsize} bytes.")

        remaining = cls.get_remaining_bytes(reader, section_name)
        if length > remaining:
            raise PsdLoadException(f"{section_name} length {length} exceeds the remaining stream data ({remaining} bytes).")

        return int(length)

    @classmethod
    def validate_signed_length(cls, length, section_name):
        """Validates a signed length field that belongs to a bounded section.

        Args:
            length: The declared signed length.
            section_name: The PSD/PSB section name used in error messages.

        Returns:
            The non-negative length.

        Raises:
            PsdLoadException: Thrown when the length is negative.
        """
        if length < 0:
            raise PsdLoadException(f"{section_name} length cannot be negative.")

        return length

    @classmethod
    def get_nested_memory_backed_length(cls, reader, length, section_end, section_name):
        """Validates that a nested payload stays inside the already-bounded enclosing section.

        Args:
            reader: The reader positioned at the nested payload start.
            length: The nested payload length.
            section_end: The byte position of the enclosing section end.
            section_name: The PSD/PSB subsection name used in error messages.

        Returns:
            The validated length as an int.

        Raises:
            PsdLoadException: Thrown when the nested payload exceeds its enclosing section.
        """
        if length > sys.maxsize:
            raise PsdLoadException(f"{section_name} length {length} exceeds the current in-memory parser limit of {sys.maxsize} bytes.")

        remaining = section_end - reader.position
        if remaining < 0 or length > remaining:
            raise PsdLoadException(f"{section_name} length {length} exceeds the enclosing section boundary.")

        return int(length)

    @classmethod
    def get_remaining_bytes(cls, reader, section_name):
        """Returns the remaining bytes in a seekable reader stream.

        Args:
            reader: The reader to inspect.
            section_name: The PSD/PSB section name used in error messages.

        Returns:
            The number of remaining bytes.

        Raises:
            PsdLoadException: Thrown when the reader position is outside the stream.
        """
        remaining = reader.length - reader.position
        if remaining < 0:
            raise PsdLoadException(f"{section_name} reader position is beyond the stream length.")

        return remaining
