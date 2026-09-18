from enum import IntEnum

class CompressionMethod(IntEnum):
    """Defines the compression methods used for image data in PSD files."""
    RAW = 0
    RLE = 1
    ZIP_WITHOUT_PREDICTION = 2
    ZIP_WITH_PREDICTION = 3
