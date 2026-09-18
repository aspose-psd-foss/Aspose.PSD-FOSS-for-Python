from enum import Enum


class ImageDataKind(Enum):
    """Identifies the structural shape of the PSD Image Data payload."""
    # The payload is raw pixel data.
    RAW = 0
    # The payload starts with an RLE row-length table followed by compressed scan data.
    RLE = 1
    # The payload is ZIP-compressed scan data, optionally with prediction.
    ZIP = 2
    # The payload uses an unrecognized compression code and is preserved as‑is.
    UNKNOWN = 3
