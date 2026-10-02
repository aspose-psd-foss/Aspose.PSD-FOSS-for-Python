from aspose_psd_foss.sections.imagedatakind import ImageDataKind


class ImageDataStructure:
    """Describes the validated structural layout of the PSD Image Data payload."""

    def __init__(
        self,
        kind,
        row_length_field_size,
        row_byte_counts,
        compressed_payload_length,
        uses_prediction,
    ):
        self._kind = kind
        self._row_length_field_size = row_length_field_size
        self._row_byte_counts = row_byte_counts
        self._compressed_payload_length = compressed_payload_length
        self._uses_prediction = uses_prediction

    @property
    def Kind(self):
        return self._kind

    @property
    def RowLengthFieldSize(self):
        return self._row_length_field_size

    @property
    def RowByteCounts(self):
        return self._row_byte_counts

    @property
    def CompressedPayloadLength(self):
        return self._compressed_payload_length

    @property
    def UsesPrediction(self):
        return self._uses_prediction

    @classmethod
    def create_raw(cls, payload_length):
        """Creates a structure descriptor for raw image data."""
        return cls(ImageDataKind.RAW, 0, [], payload_length, False)

    @classmethod
    def create_rle(cls, row_byte_counts, row_length_field_size, compressed_payload_length):
        """Creates a structure descriptor for RLE image data."""
        return cls(
            ImageDataKind.RLE,
            row_length_field_size,
            row_byte_counts,
            compressed_payload_length,
            False,
        )

    @classmethod
    def create_zip(cls, payload_length, uses_prediction):
        """Creates a structure descriptor for ZIP‑based image data."""
        return cls(ImageDataKind.ZIP, 0, [], payload_length, uses_prediction)

    @classmethod
    def create_unknown(cls, payload_length):
        """Creates a structure descriptor for unsupported compression values."""
        return cls(ImageDataKind.UNKNOWN, 0, [], payload_length, False)
