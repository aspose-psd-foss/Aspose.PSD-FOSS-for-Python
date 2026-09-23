from enum import Enum, auto


class PsdColorDataKind(Enum):
    NONE = auto()
    INDEXED_PALETTE = auto()
    RGB_PAYLOAD = auto()
    CMYK_PAYLOAD = auto()
    RAW_PRESERVED = auto()
