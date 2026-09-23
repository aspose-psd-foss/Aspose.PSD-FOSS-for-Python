# Provides a read‑only summary of the parsed layer blending ranges subsection.
class LayerBlendingRangesInfo:
    """Provides a read‑only summary of the parsed layer blending ranges subsection."""

    def __init__(self, is_present, raw_data_length):
        """Initializes a new instance of the LayerBlendingRangesInfo class.

        Args:
            is_present (bool): Whether the subsection contains payload bytes.
            raw_data_length (int): The raw subsection length including the leading length field.
        """
        self._is_present = is_present
        self._raw_data_length = raw_data_length

    @property
    def is_present(self):
        """Gets a value indicating whether the subsection contains payload bytes."""
        return self._is_present

    @property
    def raw_data_length(self):
        """Gets the raw subsection length including the leading length field."""
        return self._raw_data_length
