import os
from io import BytesIO

import pytest

from aspose_psd_foss.coreexceptions.psdloadexception import PsdLoadException
from aspose_psd_foss.layers.blendmode import BlendMode
from aspose_psd_foss_test.psdtestfixturebase import PsdTestFixtureBase
from aspose_psd_foss.psdimage import PsdImage
from aspose_psd_foss.layers.layer import Layer
from aspose_psd_foss.rectangle import Rectangle
from aspose_psd_foss.bigendianreader import BigEndianReader
from aspose_psd_foss.bigendianbitconverter import BigEndianBitConverter


class TestLayerSection(PsdTestFixtureBase):

    def test_load_toolonglayermask_throws(self):
        path = self.get_test_data_path("test.psd")

        with open(path, "rb") as f:
            bytes_data = bytearray(f.read())

        color_mode_length = BigEndianBitConverter.to_int32(bytes_data, 26)
        resources_length_offset = 26 + 4 + color_mode_length
        resources_payload_length = BigEndianBitConverter.to_int32(
            bytes_data, resources_length_offset
        )
        layer_and_mask_length_offset = (
            resources_length_offset + 4 + resources_payload_length
        )
        self.write_uint32_big_endian(
            bytes_data, layer_and_mask_length_offset, 100000
        )
        stream = BytesIO(bytes(bytes_data))

        with pytest.raises(PsdLoadException):
            PsdImage.load(stream)

    def test_load_toolonglayerextra_throws(self):
        layer_bytes = self.build_layer_record_bytes_with_extra_data(
            bytes([0x00, 0x00, 0x00, 0x10, 0x00, 0x00, 0x00, 0x00])
        )
        stream = BytesIO(layer_bytes)
        reader = BigEndianReader(stream, leave_open=True)

        with pytest.raises(PsdLoadException):
            Layer.load(reader, is_large_document=False)

    def test_load_negativelayerextra_throws(self):
        layer_bytes = bytearray(self.build_layer_record_bytes_with_extra_data(bytes([])))
        self.write_uint32_big_endian(
            layer_bytes, 30, 0xFFFFFFFF
        )

        stream = BytesIO(bytes(layer_bytes))
        reader = BigEndianReader(stream, leave_open=True)

        with pytest.raises(PsdLoadException):
            Layer.load(reader, is_large_document=False)

    def test_load_layerinspection_readsvalues(self):
        path = self.get_test_data_path("test.psd")
        with PsdImage.load(path) as image:
            first_layer = image.layers[0]

            assert first_layer.bounds == Rectangle(0, 0, 100, 100)
            assert first_layer.width == first_layer.bounds.width
            assert first_layer.height == first_layer.bounds.height
            assert first_layer.top == 0
            assert first_layer.left == 0
            assert first_layer.bottom == 100
            assert first_layer.right == 100
            assert first_layer.channels_count > 0
            assert len(first_layer.raw_blend_mode_key) == 4
            assert first_layer.layer_mask_data is None
            assert first_layer.layer_blending_ranges_data.length == (
                first_layer.blending_ranges_info.raw_data_length - 4
            )
            assert first_layer.additional_layer_data

    def test_save_changesblendmode(self):
        test_file = self.get_test_data_path("test.psd")
        output_file = self.get_persistent_artifact_path("layer_blend_mode_test.psd")

        with PsdImage.load(test_file) as image:
            image.layers[0].blend_mode_key = BlendMode.MULTIPLY
            image.save(output_file)
        self.log_artifact_directory(output_file)

        with PsdImage.load(output_file) as reloaded:
            assert reloaded.layers[0].blend_mode_key == BlendMode.MULTIPLY

        with open(test_file, "rb") as f:
            original_bytes = f.read()
        with open(output_file, "rb") as f:
            saved_bytes = f.read()
        assert self.read_layer_info_length(original_bytes) == self.read_layer_info_length(
            saved_bytes
        )

    def test_save_changesclipping(self):
        test_file = self.get_test_data_path("test.psd")

        output_file = self.get_persistent_artifact_path("layer_clipping_test.psd")
        with open(test_file, "rb") as f:
            original_bytes = f.read()

        with PsdImage.load(test_file) as image:
            image.layers[0].clipping = 1
            image.save(output_file)
        self.log_artifact_directory(output_file)

        with PsdImage.load(output_file) as reloaded:
            assert reloaded.layers[0].clipping == 1

        with open(output_file, "rb") as f:
            saved_bytes = f.read()
        assert self.read_layer_and_mask_tail(original_bytes) == self.read_layer_and_mask_tail(
            saved_bytes
        )

    def test_save_changesbounds(self):
        test_file = self.get_test_data_path("test.psd")

        output_file = self.get_persistent_artifact_path("layer_bounds_test.psd")

        with PsdImage.load(test_file) as image:
            new_bounds = Rectangle.from_left_top_right_bottom(10, 20, 40, 60)
            image.layers[0].left = new_bounds.left
            image.layers[0].top = new_bounds.top
            image.layers[0].right = new_bounds.right
            image.layers[0].bottom = new_bounds.bottom
            image.save(output_file)
        self.log_artifact_directory(output_file)

        with PsdImage.load(output_file) as reloaded:
            assert reloaded.layers[0].bounds == Rectangle(
                0, 0, new_bounds.width, new_bounds.height
            )
            assert reloaded.layers[0].left == new_bounds.left
            assert reloaded.layers[0].top == new_bounds.top
            assert reloaded.layers[0].right == new_bounds.right
            assert reloaded.layers[0].bottom == new_bounds.bottom

    def test_save_changescoordinates(self):
        test_file = self.get_test_data_path("test.psd")

        output_file = self.get_persistent_artifact_path("layer_coordinates_test.psd")

        with PsdImage.load(test_file) as image:
            layer = image.layers[0]
            layer.top = 10
            layer.left = 20
            layer.bottom = 30
            layer.right = 50
            image.save(output_file)
        self.log_artifact_directory(output_file)

        with PsdImage.load(output_file) as reloaded:
            assert reloaded.layers[0].bounds == Rectangle(0, 0, 30, 20)
            assert reloaded.layers[0].left == 20
            assert reloaded.layers[0].top == 10
            assert reloaded.layers[0].right == 50
            assert reloaded.layers[0].bottom == 30

    def test_load_psblayerrecord_reads(self):
        stream = BytesIO(self.build_psb_layer_record_bytes())
        reader = BigEndianReader(stream, leave_open=True)

        layer = Layer.load(reader, is_large_document=True)

        assert layer.name == "Layer 1"
        assert layer.bounds == Rectangle(0, 0, 1, 1)
        assert layer.opacity == 200
        assert layer.is_visible is True