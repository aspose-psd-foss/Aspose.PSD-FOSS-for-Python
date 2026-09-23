class PsdImageDataInfo:
    def __init__(self, kind, row_length_field_size, row_byte_counts, compressed_payload_length, uses_prediction):
        self._kind = kind
        self._row_length_field_size = row_length_field_size
        self._row_byte_counts = list(row_byte_counts).copy()
        self._compressed_payload_length = compressed_payload_length
        self._uses_prediction = uses_prediction

    @property
    def kind(self):
        return self._kind

    @property
    def row_length_field_size(self):
        return self._row_length_field_size

    @property
    def row_byte_counts(self):
        return self._row_byte_counts

    @property
    def compressed_payload_length(self):
        return self._compressed_payload_length

    @property
    def uses_prediction(self):
        return self._uses_prediction
