from typing import List
from aspose_psd_foss.bigendianreader import BigEndianReader
from aspose_psd_foss.coreexceptions.psdloadexception import PsdLoadException
from aspose_psd_foss.layers.layerchannelinfo import LayerChannelInfo
from aspose_psd_foss.layers.layerrawdata import LayerRawData
from aspose_psd_foss.layers.layer import Layer
from aspose_psd_foss.layers.layerblendmodemapper import LayerBlendModeMapper
from aspose_psd_foss.layers.rawlayermasksection import RawLayerMaskSection
from aspose_psd_foss.layers.rawlayerblendingrangessection import RawLayerBlendingRangesSection
from aspose_psd_foss.psdsectionreader import PsdSectionReader
from aspose_psd_foss.rectangle import Rectangle


class LayerRecordReader:
    ADOBE_LAYER_SIGNATURE = 0x3842494D
    ADOBE_LAYER_SIGNATURE_TEXT = "8BIM"
    LAYER_INVISIBLE_FLAG = 0x02

    @classmethod
    def load(cls, reader: BigEndianReader, is_large_document: bool):
        top = reader.read_int32()
        left = reader.read_int32()
        bottom = reader.read_int32()
        right = reader.read_int32()

        actual_channel_count = reader.read_uint16()
        channel_info_array: List[LayerChannelInfo] = []

        for i in range(actual_channel_count):
            channel_id = reader.read_int16()
            data_length = (
                reader.read_uint64()
                if is_large_document
                else reader.read_uint32()
            )
            channel_info_array.append(
                LayerChannelInfo(
                    channel_id=channel_id,
                    data_length=data_length,
                )
            )

        signature = reader.read_int32()
        if signature != cls.ADOBE_LAYER_SIGNATURE:
            raise PsdLoadException(
                f"Invalid layer blend mode signature. Expected '{cls.ADOBE_LAYER_SIGNATURE_TEXT}'."
            )

        blend_mode_key = reader.read_bytes(4)
        original_blend_mode_key = blend_mode_key.decode("ascii")
        blend_mode = LayerBlendModeMapper.parse_blend_mode_key(blend_mode_key)

        opacity = reader.read_byte()
        clipping = reader.read_byte()
        flags = reader.read_byte()
        reader.read_byte()  # padding

        extra_length = reader.read_int32()
        if extra_length < 0:
            raise PsdLoadException("Layer extra data length cannot be negative.")

        layer_name = ""
        layer_mask_data = RawLayerMaskSection.empty()
        blending_ranges_data = RawLayerBlendingRangesSection.empty()
        additional_layer_data = b""

        if extra_length > 0:
            extra_start = reader.position
            extra_end = extra_start + extra_length

            layer_mask_data = RawLayerMaskSection.load(reader, extra_end)
            if reader.position + 4 > extra_end:
                raise PsdLoadException(
                    "Layer extra data is truncated before the blending ranges length field."
                )

            blending_ranges_data = RawLayerBlendingRangesSection.load(reader, extra_end)
            layer_name = reader.read_pascal_string_aligned_to4()

            remaining = extra_end - reader.position
            if remaining < 0:
                raise PsdLoadException(
                    "Layer extra data parser read beyond the declared extra data boundary."
                )
            if remaining > 0:
                additional_layer_data = reader.read_bytes(
                    PsdSectionReader.get_nested_memory_backed_length(
                        reader,
                        remaining,
                        extra_end,
                        "Additional layer data",
                    )
                )

        bounds = Rectangle.from_ltrb(left, top, right, bottom)
        visible = (flags & cls.LAYER_INVISIBLE_FLAG) == 0

        raw_data = LayerRawData(
            flags,
            original_blend_mode_key,
            channel_info_array,
            layer_mask_data,
            blending_ranges_data,
            additional_layer_data,
        )

        return Layer.create_parsed(
            layer_name,
            bounds,
            visible,
            opacity,
            clipping,
            blend_mode,
            raw_data,
        )
