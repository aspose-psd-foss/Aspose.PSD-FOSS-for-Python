from aspose_psd_foss.bigendianreader import BigEndianReader
from aspose_psd_foss.coreexceptions.psdloadexception import PsdLoadException


def read_bytes(reader, length, section_name):
    """
    Reads a declared section payload after validating stream boundaries and the
    in-memory size limit.

    :param reader: The reader positioned at the start of the section payload.
    :param length: The declared payload length.
    :param section_name: The PSD/PSB section name used in error messages.
    :return: The section payload bytes.
    :raises PsdLoadException: When the declared length cannot be read safely.
    """
    bounded_length = get_memory_backed_length(reader, length, section_name)
    return b"" if bounded_length == 0 else reader.read_bytes(bounded_length)


def get_memory_backed_length(reader, length, section_name):
    """
    Validates a declared section length and returns the equivalent in-memory
    array size.

    :param reader: The reader positioned at the start of the section payload.
    :param length: The declared payload length.
    :param section_name: The PSD/PSB section name used in error messages.
    :return: The validated length as an int.
    :raises PsdLoadException: When the declared length cannot be represented
        or exceeds available bytes.
    """
    int_max = (1 << 31) - 1
    if length > int_max:
        raise PsdLoadException(
            f"{section_name} length {length} exceeds the current in-memory parser "
            f"limit of {int_max} bytes."
        )

    remaining = _get_remaining_bytes(reader, section_name)
    if length > remaining:
        raise PsdLoadException(
            f"{section_name} length {length} exceeds the remaining stream data "
            f"({remaining} bytes)."
        )

    return int(length)


def validate_signed_length(length, section_name):
    """
    Validates a signed length field that belongs to a bounded section.

    :param length: The declared signed length.
    :param section_name: The PSD/PSB section name used in error messages.
    :return: The non-negative length.
    :raises PsdLoadException: When the length is negative.
    """
    if length < 0:
        raise PsdLoadException(f"{section_name} length cannot be negative.")
    return length


def get_nested_memory_backed_length(reader, length, section_end, section_name):
    """
    Validates that a nested payload stays inside the already-bounded enclosing
    section.

    :param reader: The reader positioned at the nested payload start.
    :param length: The nested payload length.
    :param section_end: The byte position of the enclosing section end.
    :param section_name: The PSD/PSB subsection name used in error messages.
    :return: The validated length as an int.
    :raises PsdLoadException: When the nested payload exceeds its enclosing
        section.
    """
    int_max = (1 << 31) - 1
    if length > int_max:
        raise PsdLoadException(
            f"{section_name} length {length} exceeds the current in-memory parser "
            f"limit of {int_max} bytes."
        )

    remaining = section_end - reader.position
    if remaining < 0 or length > remaining:
        raise PsdLoadException(
            f"{section_name} length {length} exceeds the enclosing section boundary."
        )

    return int(length)


def _get_remaining_bytes(reader, section_name):
    """
    Returns the remaining bytes in a seekable reader stream.

    :param reader: The reader to inspect.
    :param section_name: The PSD/PSB section name used in error messages.
    :return: The number of remaining bytes.
    :raises PsdLoadException: When the reader position is outside the stream.
    """
    remaining = reader.length - reader.position
    if remaining < 0:
        raise PsdLoadException(
            f"{section_name} reader position is beyond the stream length."
        )
    return remaining
