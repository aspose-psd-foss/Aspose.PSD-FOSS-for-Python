from aspose_psd_foss.sections.imagedatakind import ImageDataKind


class ImageDataStructure:
    """Describes the validated structural layout of the PSD Image Data payload."""

    def __init__(self, kind: ImageDataKind, row_length_field_size: int, row_byte_counts, compressed_payload_length: int, uses_prediction: bool):
        self._kind = kind
        self._row_length_field_size = row_length_field_size
        self._row_byte_counts = row_byte_counts
        self._compressed_payload_length = compressed_payload_length
        self._uses_prediction = uses_prediction

    @property
    def kind(self) -> ImageDataKind:
        """Gets the structural kind implied by the compression mode."""
        return self._kind

    @property
    def row_length_field_size(self) -> int:
        """Gets the size of one RLE row-length entry in bytes."""
        return self._row_length_field_size

    @property
    def row_byte_counts(self):
        """Gets the parsed row byte counts for RLE payloads."""
        return self._row_byte_counts

    @property
    def compressed_payload_length(self) -> int:
        """Gets the number of payload bytes after structural headers such as the RLE row-length table."""
        return self._compressed_payload_length

    @property
    def uses_prediction(self) -> bool:
        """Gets a value indicating whether ZIP prediction is in effect."""
        return self._uses_prediction

    @staticmethod
    def create_raw(payload_length: int):
        """Creates a structure descriptor for raw image data.

        Args:
            payload_length: The stored payload length.

        Returns:
            ImageDataStructure: The structure descriptor.
        """
        return ImageDataStructure(ImageDataKind.Raw, 0, [], payload_length, uses_prediction=False)

    @staticmethod
    def create_rle(row_byte_counts, row_length_field_size: int, compressed_payload_length: int):
        """Creates a structure descriptor for RLE image data.

        Args:
            row_byte_counts: The parsed per-row byte counts.
            row_length_field_size: The size of one row-length entry in bytes.
            compressed_payload_length: The payload length after the row-length table.

        Returns:
            ImageDataStructure: The structure descriptor.
        """
        return ImageDataStructure(ImageDataKind.Rle, row_length_field_size, row_byte_counts, compressed_payload_length, uses_prediction=False)

    @staticmethod
    def create_zip(payload_length: int, uses_prediction: bool):
        """Creates a structure descriptor for ZIP-based image data.

        Args:
            payload_length: The stored payload length.
            uses_prediction: Whether ZIP prediction is used.

        Returns:
            ImageDataStructure: The structure descriptor.
        """
        return ImageDataStructure(ImageDataKind.Zip, 0, [], payload_length, uses_prediction)

    @staticmethod
    def create_unknown(payload_length: int):
        """Creates a structure descriptor for unsupported compression values while preserving the payload.

        Args:
            payload_length: The stored payload length.

        Returns:
            ImageDataStructure: The structure descriptor.
        """
        return ImageDataStructure(ImageDataKind.Unknown, 0, [], payload_length, uses_prediction=False)
