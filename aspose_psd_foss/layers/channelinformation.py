from aspose_psd_foss.compressionmethod import CompressionMethod
from .layerchannelinfo import LayerChannelInfo
from aspose_psd_foss.psdversion import PsdVersion


class ChannelInformation:
    """
    Represents PSD layer channel information.
    """

    def __init__(self, compression_method, bit_depth, psd_version):
        """
        Initializes a new instance of the ChannelInformation class.

        :param compression_method: The channel compression method.
        :param bit_depth: The channel bit depth.
        :param psd_version: The PSD version number.
        """
        self.compression_method = compression_method
        self.length = self._get_header_length(psd_version)
        self._channel_id = 0  # default value matching C# default

    @property
    def ChannelID(self):
        """
        Gets or sets the channel identifier.
        """
        return self._channel_id

    @ChannelID.setter
    def ChannelID(self, value):
        self._channel_id = value

    @classmethod
    def _create_internal(cls, channel_id, length):
        """
        Initializes a new instance of the ChannelInformation class from parsed layer record metadata.

        :param channel_id: The channel identifier.
        :param length: The declared channel data length.
        :return: A ChannelInformation instance.
        """
        obj = cls.__new__(cls)
        obj._channel_id = channel_id
        obj.compression_method = CompressionMethod.Raw
        obj.length = length
        return obj

    @classmethod
    def from_layer_channel_info(cls, channel_info):
        """
        Creates public channel information from the internal layer channel metadata.

        :param channel_info: The internal layer channel metadata.
        :return: The public channel information.
        """
        max_int = 0x7FFFFFFF
        length = (
            channel_info.DataLength
            if channel_info.DataLength <= max_int
            else max_int
        )
        return cls._create_internal(channel_info.ChannelId, length)

    @classmethod
    def _get_header_length(cls, psd_version):
        """
        Gets the minimum channel data header length for the specified PSD version.

        :param psd_version: The PSD version number.
        :return: The channel data header length.
        """
        return 8 if psd_version == PsdVersion.Psb else 2
