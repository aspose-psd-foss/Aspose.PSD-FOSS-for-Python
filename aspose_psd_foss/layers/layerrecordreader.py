from .layerchannelinfo import LayerChannelInfo
from .layerblendmodemapper import LayerBlendModeMapper
from .rawlayermasksection import RawLayerMaskSection
from .rawlayerblendingrangessection import RawLayerBlendingRangesSection
from .layerrawdata import LayerRawData
from ..coreexceptions.psdloadexception import PsdLoadException
from ..rectangle import Rectangle
from ..psdsectionreader import PsdSectionReader

from .layer import Layer

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .layer import Layer

AdobeLayerSignature = 0x3842494D
AdobeLayerSignatureText = "8BIM"
LayerInvisibleFlag = 0x02


def load(reader, is_large_document):
    top = reader.ReadInt32()
    left = reader.ReadInt32()
    bottom = reader.ReadInt32()
    right = reader.ReadInt32()

    actual_channel_count = reader.ReadUInt16()
    channel_info_array = [None] * actual_channel_count

    for i in range(actual_channel_count):
        channel_id = reader.ReadInt16()
        data_length = reader.ReadUInt64() if is_large_document else reader.ReadUInt32()

        channel_info_array[i] = LayerChannelInfo(
            ChannelId=channel_id,
            DataLength=data_length
        )

    signature = reader.ReadInt32()
    if signature != AdobeLayerSignature:
        raise PsdLoadException(f"Invalid layer blend mode signature. Expected '{AdobeLayerSignatureText}'.")

    blend_mode_key_bytes = reader.ReadBytes(4)
    original_blend_mode_key = blend_mode_key_bytes.decode('ascii')
    blend_mode = LayerBlendModeMapper.ParseBlendModeKey(blend_mode_key_bytes)

    opacity = reader.ReadByte()
    clipping = reader.ReadByte()
    flags = reader.ReadByte()
    reader.ReadByte()

    extra_length = reader.ReadInt32()
    if extra_length < 0:
        raise PsdLoadException("Layer extra data length cannot be negative.")

    layer_name = ""
    layer_mask_data = RawLayerMaskSection.Empty
    blending_ranges_data = RawLayerBlendingRangesSection.Empty
    additional_layer_data = b''

    if extra_length > 0:
        extra_start = reader.Position
        extra_end = extra_start + extra_length

        layer_mask_data = RawLayerMaskSection.Load(reader, extra_end)
        if reader.Position + 4 > extra_end:
            raise PsdLoadException("Layer extra data is truncated before the blending ranges length field.")

        blending_ranges_data = RawLayerBlendingRangesSection.Load(reader, extra_end)
        layer_name = reader.ReadPascalStringAlignedTo4()

        remaining = extra_end - reader.Position
        if remaining < 0:
            raise PsdLoadException("Layer extra data parser read beyond the declared extra data boundary.")

        if remaining > 0:
            additional_layer_data = reader.ReadBytes(
                PsdSectionReader.GetNestedMemoryBackedLength(reader, remaining, extra_end, "Additional layer data"))

    bounds = Rectangle.FromLTRB(left, top, right, bottom)
    visible = (flags & LayerInvisibleFlag) == 0

    raw_data = LayerRawData(
        Flags=flags,
        OriginalBlendModeKey=original_blend_mode_key,
        ChannelInfoArray=channel_info_array,
        LayerMaskData=layer_mask_data,
        BlendingRangesData=blending_ranges_data,
        AdditionalLayerData=additional_layer_data
    )

    return Layer.CreateParsed(
        LayerName=layer_name,
        Bounds=bounds,
        Visible=visible,
        Opacity=opacity,
        Clipping=clipping,
        BlendMode=blend_mode,
        RawData=raw_data
    )


class LayerRecordReader:
    def __init__(self, stream):
        self._stream = stream

    @classmethod
    def load(cls, reader, is_large_document):
        return load(reader, is_large_document)

    def read(self, is_large_document):
        return load(self._stream, is_large_document)


__all__ = ["LayerRecordReader"]
