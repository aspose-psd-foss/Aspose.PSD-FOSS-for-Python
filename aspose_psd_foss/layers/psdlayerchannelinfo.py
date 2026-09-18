"""Provides a read‑only summary of one parsed layer channel record."""

class PsdLayerChannelInfo:
    """Initializes a new instance of the PsdLayerChannelInfo class.

    Args:
        channel_id (int): The PSD channel identifier.
        data_length (int): The declared payload length in bytes.
    """

    def __init__(self, channel_id: int, data_length: int):
        self._channel_id = channel_id
        self._data_length = data_length

    @property
    def channel_id(self) -> int:
        """Gets the PSD channel identifier."""
        return self._channel_id

    @property
    def data_length(self) -> int:
        """Gets the declared payload length in bytes."""
        return self._data_length
