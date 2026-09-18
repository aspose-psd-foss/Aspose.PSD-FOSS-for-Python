from enum import Enum


class PsdColorDataKind(Enum):
    NONE = 0
    INDEXED_PALETTE = 1
    RGB_PAYLOAD = 2
    CMYK_PAYLOAD = 3
    RAW_PRESERVED = 4
