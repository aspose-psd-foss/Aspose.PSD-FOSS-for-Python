from aspose_psd_foss.compressionmethod import CompressionMethod
from aspose_psd_foss.psdversion import PsdVersion


class ChannelInformation:
    """Represents PSD layer channel information."""

    def __init__(self, compression_method, bit_depth=None, psd_version=None, channel_id=None, length=None):
        """Initializes a new instance of the ChannelInformation class.

        Args:
            compression_method: The channel compression method (used in public constructor).
            bit_depth: The channel bit depth (unused in current implementation, preserved for API compatibility).
            psd_version: The PSD version number (used in public constructor).
            channel_id: The channel identifier (used in private constructor).
            length: The declared channel data length (used in private constructor).
        """
        if channel_id is not None and length is not None:
            # Private constructor: from parsed layer record metadata
            self.channel_id = channel_id
            self.compression_method = CompressionMethod.Raw
            self._length = length
        elif compression_method is not None and psd_version is not None:
            # Public constructor
            self.compression_method = compression_method
            self._length = self._get_header_length(psd_version)
        else:
            raise ValueError("Invalid constructor arguments. Provide either (compression_method, bit_depth, psd_version) or (channel_id, length).")

    @property
    def channel_id(self):
        """Gets or sets the channel identifier."""
        return self._channel_id

    @channel_id.setter
    def channel_id(self, value):
        self._channel_id = value

    @property
    def compression_method(self):
        """Gets or sets the channel compression method."""
        return self._compression_method

    @compression_method.setter
    def compression_method(self, value):
        self._compression_method = value

    @property
    def length(self):
        """Gets the channel length in bytes."""
        return self._length

    @classmethod
    def from_layer_channel_info(cls, channel_info):
        """Creates public channel information from the internal layer channel metadata.

        Args:
            channel_info: The internal layer channel metadata.

        Returns:
            The public channel information.
        """
        length = int(channel_info.DataLength) if channel_info.DataLength <= 2**31 - 1 else 2**31 - 1
        return cls(channel_id=channel_info.ChannelId, length=length)

    @staticmethod
    def _get_header_length(psd_version):
        """Gets the minimum channel data header length for the specified PSD version.

        Args:
            psd_version: The PSD version number.

        Returns:
            The channel data header length.
        """
        return 8 if psd_version == PsdVersion.Psb else 2
