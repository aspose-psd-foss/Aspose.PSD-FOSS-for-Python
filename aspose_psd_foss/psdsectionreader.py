from aspose_psd_foss.bigendianreader import BigEndianReader
from aspose_psd_foss.coreexceptions.psdloadexception import PsdLoadException

MAX_INT = 2**31 - 1


class PsdSectionReader:
    """Provides bounded reads for PSD/PSB sections that are stored in memory by this implementation."""

    @staticmethod
    def read_bytes(reader: BigEndianReader, length: int, section_name: str):
        """Reads a declared section payload after validating stream boundaries and the in-memory size limit.

        Args:
            reader: The reader positioned at the start of the section payload.
            length: The declared payload length.
            section_name: The PSD/PSB section name used in error messages.

        Returns:
            The section payload bytes.

        Raises:
            PsdLoadException: When the declared length cannot be read safely.
        """
        bounded_length = PsdSectionReader.get_memory_backed_length(
            reader, length, section_name
        )
        return b"" if bounded_length == 0 else reader.read_bytes(bounded_length)

    @staticmethod
    def get_memory_backed_length(reader: BigEndianReader, length: int, section_name: str) -> int:
        """Validates a declared section length and returns the equivalent in-memory array size.

        Args:
            reader: The reader positioned at the start of the section payload.
            length: The declared payload length.
            section_name: The PSD/PSB section name used in error messages.

        Returns:
            The validated length as an int.

        Raises:
            PsdLoadException: When the declared length cannot be represented or exceeds available bytes.
        """
        if length > MAX_INT:
            raise PsdLoadException(
                f"{section_name} length {length} exceeds the current in-memory "
                f"parser limit of {MAX_INT} bytes."
            )

        remaining = PsdSectionReader._get_remaining_bytes(reader, section_name)
        if length > remaining:
            raise PsdLoadException(
                f"{section_name} length {length} exceeds the remaining stream data "
                f"({remaining} bytes)."
            )

        return int(length)

    @staticmethod
    def validate_signed_length(length: int, section_name: str) -> int:
        """Validates a signed length field that belongs to a bounded section.

        Args:
            length: The declared signed length.
            section_name: The PSD/PSB section name used in error messages.

        Returns:
            The non-negative length.

        Raises:
            PsdLoadException: When the length is negative.
        """
        if length < 0:
            raise PsdLoadException(f"{section_name} length cannot be negative.")
        return length

    @staticmethod
    def get_nested_memory_backed_length(
        reader: BigEndianReader,
        length: int,
        section_end: int,
        section_name: str,
    ) -> int:
        """Validates that a nested payload stays inside the already-bounded enclosing section.

        Args:
            reader: The reader positioned at the nested payload start.
            length: The nested payload length.
            section_end: The byte position of the enclosing section end.
            section_name: The PSD/PSB subsection name used in error messages.

        Returns:
            The validated length as an int.

        Raises:
            PsdLoadException: When the nested payload exceeds its enclosing section.
        """
        if length > MAX_INT:
            raise PsdLoadException(
                f"{section_name} length {length} exceeds the current in-memory "
                f"parser limit of {MAX_INT} bytes."
            )

        remaining = section_end - reader.position
        if remaining < 0 or length > remaining:
            raise PsdLoadException(
                f"{section_name} length {length} exceeds the enclosing section boundary."
            )

        return int(length)

    @staticmethod
    def _get_remaining_bytes(reader: BigEndianReader, section_name: str) -> int:
        """Returns the remaining bytes in a seekable reader stream.

        Args:
            reader: The reader to inspect.
            section_name: The PSD/PSB section name used in error messages.

        Returns:
            The number of remaining bytes.

        Raises:
            PsdLoadException: When the reader position is outside the stream.
        """
        remaining = reader.length - reader.position
        if remaining < 0:
            raise PsdLoadException(
                f"{section_name} reader position is beyond the stream length."
            )
        return int(remaining)
