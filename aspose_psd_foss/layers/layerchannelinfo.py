# Stores one channel metadata entry from a layer record.

class LayerChannelInfo:
    """Stores one channel metadata entry from a layer record."""

    def __init__(self, channel_id, data_length):
        # Gets or sets the PSD channel identifier.
        self.channel_id = channel_id
        # Gets or sets the declared byte length of the channel data payload.
        self.data_length = data_length
