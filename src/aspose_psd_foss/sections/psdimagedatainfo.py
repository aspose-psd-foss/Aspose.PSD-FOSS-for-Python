from typing import Tuple
from aspose_psd_foss.sections.imagedatakind import ImageDataKind


class PsdImageDataInfo:
    def __init__(
        self,
        kind: ImageDataKind,
        row_length_field_size: int,
        row_byte_counts,
        compressed_payload_length: int,
        uses_prediction: bool,
    ):
        self._kind = kind
        self._row_length_field_size = row_length_field_size
        self._row_byte_counts = tuple(row_byte_counts)
        self._compressed_payload_length = compressed_payload_length
        self._uses_prediction = uses_prediction

    @property
    def kind(self) -> ImageDataKind:
        return self._kind

    @property
    def row_length_field_size(self) -> int:
        return self._row_length_field_size

    @property
    def row_byte_counts(self) -> Tuple[int, ...]:
        return self._row_byte_counts

    @property
    def compressed_payload_length(self) -> int:
        return self._compressed_payload_length

    @property
    def uses_prediction(self) -> bool:
        return self._uses_prediction
