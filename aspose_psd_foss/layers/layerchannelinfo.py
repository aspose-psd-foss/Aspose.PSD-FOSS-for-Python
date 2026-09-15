"""Stores one channel metadata entry from a layer record."""
from dataclasses import dataclass

@dataclass
class LayerChannelInfo:
    """Gets or sets the PSD channel identifier and the declared byte length of the channel data payload."""
    channel_id: int  # Gets or sets the PSD channel identifier.
    data_length: int  # Gets or sets the declared byte length of the channel data payload.
