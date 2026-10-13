class PsdLayerChannelInfo:
    """Provides a read-only summary of one parsed layer channel record."""

    def __init__(self, channel_id, data_length):
        """Initializes a new instance of the PsdLayerChannelInfo class.

        Args:
            channel_id: The PSD channel identifier.
            data_length: The declared payload length in bytes.
        """
        self._channel_id = channel_id
        self._data_length = data_length

    @property
    def channel_id(self):
        """Gets the PSD channel identifier."""
        return self._channel_id

    @property
    def data_length(self):
        """Gets the declared payload length in bytes."""
        return self._data_length
