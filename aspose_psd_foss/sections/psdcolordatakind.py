from enum import Enum


class PsdColorDataKind(Enum):
    # No color mode payload was present.
    NONE = 0
    # The payload was parsed as a standard indexed palette.
    INDEXED_PALETTE = 1
    # The payload belongs to an RGB document.
    RGB_PAYLOAD = 2
    # The payload belongs to a CMYK document.
    CMYK_PAYLOAD = 3
    # The payload is preserved as opaque raw data.
    RAW_PRESERVED = 4
