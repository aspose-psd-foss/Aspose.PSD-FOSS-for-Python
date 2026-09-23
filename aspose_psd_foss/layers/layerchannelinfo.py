class LayerChannelInfo:
    """Stores one channel metadata entry from a layer record."""

    def __init__(self, channel_id=0, data_length=0):
        """Initialize a layer channel info instance.

        Args:
            channel_id (int): PSD channel identifier.
            data_length (int): Declared byte length of the channel data payload.
        """
        self.channel_id = channel_id
        """PSD channel identifier."""
        self.data_length = data_length
        """Declared byte length of the channel data payload."""
