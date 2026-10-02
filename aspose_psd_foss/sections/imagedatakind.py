from enum import Enum


class ImageDataKind(Enum):
    """Identifies the structural shape of the PSD Image Data payload."""
    RAW = 0
    RLE = 1
    ZIP = 2
    UNKNOWN = 3
