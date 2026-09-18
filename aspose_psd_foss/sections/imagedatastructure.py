from aspose_psd_foss.sections.imagedatakind import ImageDataKind


class ImageDataStructure:
    """Describes the validated structural layout of the PSD Image Data payload."""

    def __init__(self, kind: ImageDataKind, row_length_field_size: int, row_byte_counts: list[int],
                 compressed_payload_length: int, uses_prediction: bool):
        self.kind = kind
        self.row_length_field_size = row_length_field_size
        self.row_byte_counts = row_byte_counts
        self.compressed_payload_length = compressed_payload_length
        self.uses_prediction = uses_prediction

    @property
    def kind(self) -> ImageDataKind:
        """Gets the structural kind implied by the compression mode."""
        return self._kind

    @kind.setter
    def kind(self, value: ImageDataKind):
        self._kind = value

    @property
    def row_length_field_size(self) -> int:
        """Gets the size of one RLE row-length entry in bytes."""
        return self._row_length_field_size

    @row_length_field_size.setter
    def row_length_field_size(self, value: int):
        self._row_length_field_size = value

    @property
    def row_byte_counts(self) -> list[int]:
        """Gets the parsed row byte counts for RLE payloads."""
        return self._row_byte_counts

    @row_byte_counts.setter
    def row_byte_counts(self, value: list[int]):
        self._row_byte_counts = value

    @property
    def compressed_payload_length(self) -> int:
        """Gets the number of payload bytes after structural headers such as the RLE row-length table."""
        return self._compressed_payload_length

    @compressed_payload_length.setter
    def compressed_payload_length(self, value: int):
        self._compressed_payload_length = value

    @property
    def uses_prediction(self) -> bool:
        """Gets a value indicating whether ZIP prediction is in effect."""
        return self._uses_prediction

    @uses_prediction.setter
    def uses_prediction(self, value: bool):
        self._uses_prediction = value

    @staticmethod
    def create_raw(payload_length: int) -> 'ImageDataStructure':
        """Creates a structure descriptor for raw image data."""
        return ImageDataStructure(ImageDataKind.RAW, 0, [], payload_length, False)

    @staticmethod
    def create_rle(row_byte_counts: list[int], row_length_field_size: int,
                   compressed_payload_length: int) -> 'ImageDataStructure':
        """Creates a structure descriptor for RLE image data."""
        return ImageDataStructure(ImageDataKind.RLE, row_length_field_size,
                                  row_byte_counts, compressed_payload_length, False)

    @staticmethod
    def create_zip(payload_length: int, uses_prediction: bool) -> 'ImageDataStructure':
        """Creates a structure descriptor for ZIP-based image data."""
        return ImageDataStructure(ImageDataKind.ZIP, 0, [], payload_length, uses_prediction)

    @staticmethod
    def create_unknown(payload_length: int) -> 'ImageDataStructure':
        """Creates a structure descriptor for unsupported compression values while preserving the payload."""
        return ImageDataStructure(ImageDataKind.UNKNOWN, 0, [], payload_length, False)
