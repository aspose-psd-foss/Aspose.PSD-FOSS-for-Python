from __future__ import annotations

from typing import Sequence

from aspose_psd_foss.sections.imagedatakind import ImageDataKind


class PsdImageDataInfo:
    """
    Provides a read-only summary of the PSD merged image data structure.
    """

    def __init__(
        self,
        kind: ImageDataKind,
        row_length_field_size: int,
        row_byte_counts: Sequence[int],
        compressed_payload_length: int,
        uses_prediction: bool,
    ) -> None:
        """
        Initializes a new instance of the PsdImageDataInfo class.

        :param kind: The structural kind of the payload.
        :param row_length_field_size: The size of one row-length entry in bytes.
        :param row_byte_counts: The parsed row byte counts for RLE payloads.
        :param compressed_payload_length: The payload length after any structural headers.
        :param uses_prediction: Whether ZIP prediction is in effect.
        """
        self._kind: ImageDataKind = kind
        self._row_length_field_size: int = row_length_field_size
        # Store as a tuple to provide read‑only semantics.
        self._row_byte_counts: tuple[int, ...] = tuple(row_byte_counts)
        self._compressed_payload_length: int = compressed_payload_length
        self._uses_prediction: bool = uses_prediction

    @property
    def kind(self) -> ImageDataKind:
        """Gets the structural kind of the payload."""
        return self._kind

    @property
    def row_length_field_size(self) -> int:
        """Gets the size of one RLE row-length entry in bytes."""
        return self._row_length_field_size

    @property
    def row_byte_counts(self) -> tuple[int, ...]:
        """Gets the parsed row byte counts for RLE payloads."""
        return self._row_byte_counts

    @property
    def compressed_payload_length(self) -> int:
        """Gets the payload length after structural headers such as the RLE row-length table."""
        return self._compressed_payload_length

    @property
    def uses_prediction(self) -> bool:
        """Gets a value indicating whether ZIP prediction is in effect."""
        return self._uses_prediction
