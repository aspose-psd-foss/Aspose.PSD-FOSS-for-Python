from enum import Enum

class CompressionMethod(Enum):
    """Defines the compression methods used for image data in PSD files."""

    #: Raw (uncompressed) data.
    Raw = 0

    #: RLE (Run-Length Encoded) compression.
    RLE = 1

    #: ZIP (lossless) compression.
    ZipWithoutPrediction = 2

    #: ZIP compression with prediction.
    ZipWithPrediction = 3
