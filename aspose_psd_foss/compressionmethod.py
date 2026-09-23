# Defines the compression methods used for image data in PSD files.

from enum import Enum


class CompressionMethod(Enum):
    """Compression methods used for image data in PSD files."""
    RAW = 0
    RLE = 1
    ZIP_WITHOUT_PREDICTION = 2
    ZIP_WITH_PREDICTION = 3
