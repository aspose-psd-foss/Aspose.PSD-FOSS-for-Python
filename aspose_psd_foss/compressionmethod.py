import enum


class CompressionMethod(enum.IntEnum):
    """Defines the compression methods used for image data in PSD files."""
    RAW = 0  # Raw (uncompressed) data.
    RLE = 1  # RLE (Run-Length Encoded) compression.
    ZIP_WITHOUT_PREDICTION = 2  # ZIP (lossless) compression.
    ZIP_WITH_PREDICTION = 3  # ZIP compression with prediction.
