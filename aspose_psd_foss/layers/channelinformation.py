from aspose_psd_foss.compressionmethod import CompressionMethod
from aspose_psd_foss.psdversion import PsdVersion
from aspose_psd_foss.layers.layerchannelinfo import LayerChannelInfo


class ChannelInformation:
    """
    Represents PSD layer channel information.
    """

    def __init__(self, compression_method, bit_depth, psd_version):
        """
        Initializes a new instance of ChannelInformation.

        :param compression_method: The channel compression method.
        :param bit_depth: The channel bit depth.
        :param psd_version: The PSD version number.
        """
        self.channel_id = None
        self.compression_method = compression_method
        self.length = self._get_header_length(psd_version)

    @classmethod
    def _create_internal(cls, channel_id, length):
        """
        Creates an instance from internal layer channel metadata.

        :param channel_id: The channel identifier.
        :param length: The declared channel data length.
        :return: ChannelInformation instance.
        """
        obj = cls.__new__(cls)
        obj.channel_id = channel_id
        obj.compression_method = CompressionMethod.Raw
        obj.length = length
        return obj

    @staticmethod
    def from_layer_channel_info(channel_info):
        """
        Creates public channel information from the internal layer channel metadata.

        :param channel_info: The internal layer channel metadata.
        :return: The public channel information.
        """
        max_int = 2**31 - 1
        length = max_int if channel_info.data_length > max_int else int(channel_info.data_length)
        return ChannelInformation._create_internal(channel_info.channel_id, length)

    @staticmethod
    def _get_header_length(psd_version):
        """
        Gets the minimum channel data header length for the specified PSD version.

        :param psd_version: The PSD version number.
        :return: The channel data header length.
        """
        return 8 if psd_version == int(PsdVersion.Psb) else 2
