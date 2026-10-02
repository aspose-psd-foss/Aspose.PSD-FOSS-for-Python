import enum


class PsdColorDataKind(enum.Enum):
    """Describes how the Color Mode Data payload was interpreted for the loaded document."""
    NONE = 0
    INDEXED_PALETTE = 1
    RGB_PAYLOAD = 2
    CMYK_PAYLOAD = 3
    RAW_PRESERVED = 4
