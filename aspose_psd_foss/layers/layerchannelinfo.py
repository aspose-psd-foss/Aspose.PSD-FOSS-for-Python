from __future__ import annotations


class LayerChannelInfo:
    """Stores one channel metadata entry from a layer record."""

    def __init__(self, channel_id: int = 0, data_length: int = 0):
        self.channel_id = channel_id
        self.data_length = data_length
