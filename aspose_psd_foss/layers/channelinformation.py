from aspose_psd_foss.compressionmethod import CompressionMethod
from aspose_psd_foss.psdversion import PsdVersion

class ChannelInformation:
    def __init__(self, compression_method, _bit_depth, psd_version):
        self.compression_method = compression_method
        self.length = self._get_header_length(psd_version)

    @classmethod
    def _from_internal(cls, channel_id, length):
        obj = cls.__new__(cls)
        obj.channel_id = channel_id
        obj.compression_method = CompressionMethod.Raw
        obj.length = length
        return obj

    @staticmethod
    def from_layer_channel_info(channel_info):
        max_int = 2**31 - 1
        length = max_int if channel_info.data_length > max_int else int(channel_info.data_length)
        return ChannelInformation._from_internal(channel_info.channel_id, length)

    @staticmethod
    def _get_header_length(psd_version):
        return 8 if psd_version == PsdVersion.Psb else 2
