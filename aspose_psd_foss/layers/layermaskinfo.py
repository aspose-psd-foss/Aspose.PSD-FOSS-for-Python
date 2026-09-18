# Provides a read‑only summary of the parsed layer mask subsection.
class LayerMaskInfo:
    # Initializes a new instance of the LayerMaskInfo class.
    # is_present: Whether the subsection contains payload bytes.
    # raw_data_length: The raw subsection length including the leading length field.
    def __init__(self, is_present, raw_data_length):
        self._is_present = is_present
        self._raw_data_length = raw_data_length

    # Gets a value indicating whether the subsection contains payload bytes.
    @property
    def is_present(self):
        return self._is_present

    # Gets the raw subsection length including the leading length field.
    @property
    def raw_data_length(self):
        return self._raw_data_length
