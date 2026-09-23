from enum import Enum


class ImageDataKind(Enum):
    """
    Identifies the structural shape of the PSD Image Data payload.
    """
    RAW = 0
    """
    The payload is raw pixel data.
    """
    RLE = 1
    """
    The payload starts with an RLE row-length table followed by compressed scan data.
    """
    ZIP = 2
    """
    The payload is ZIP-compressed scan data, optionally with prediction.
    """
    UNKNOWN = 3
    """
    The payload uses an unrecognized compression code and is preserved as-is.
    """
