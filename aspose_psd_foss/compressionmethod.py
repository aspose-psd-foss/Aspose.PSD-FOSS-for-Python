from enum import IntEnum


class CompressionMethod(IntEnum):
    """Defines the compression methods used for image data in PSD files."""

    #: Raw (uncompressed) data.
    RAW = 0

    #: RLE (Run-Length Encoded) compression.
    RLE = 1

    #: ZIP (lossless) compression.
    ZIP_WITHOUT_PREDICTION = 2

    #: ZIP compression with prediction.
    ZIP_WITH_PREDICTION = 3
