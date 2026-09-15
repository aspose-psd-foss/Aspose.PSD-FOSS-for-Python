import os
from pathlib import Path

import pytest

from aspose_psd_foss_test.psd_test_fixture_base import PsdTestFixtureBase
from aspose_psd_foss.big_endian_bit_converter import BigEndianBitConverter
from aspose_psd_foss.psd_image import PsdImage
from aspose_psd_foss.core_exceptions.psd_load_exception import PsdLoadException
from aspose_psd_foss.big_endian_reader import BigEndianReader
from aspose_psd_foss.layers.layer import Layer
from aspose_psd_foss.rectangle import Rectangle
from aspose_psd_foss.layers.blend_mode import BlendMode


class LayerSectionTests(PsdTestFixtureBase):
    """Contains LayerSection tests."""

    def test_load_too_long_layer_mask_throws(self):
        psd_path = Path(
            os.path.join(
                self.test_context.current_context.test_directory,
                "testdata",
                "test.psd",
            )
        )
        bytes_data = psd_path.read_bytes()
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
        stream = memoryview(bytes_data)

        with pytest.raises(PsdLoadException):
            PsdImage.load(stream)

    def test_load_too_long_layer_extra_throws(self):
        layer_bytes = self.build_layer_record_bytes_with_extra_data(
            [
                0x00,
                0x00,
                0x00,
                0x10,
                0x00,
                0x00,
                0x00,
                0x00,
            ]
        )
        stream = memoryview(layer_bytes)
        reader = BigEndianReader(stream, leave_open=True)

        with pytest.raises(PsdLoadException):
            Layer.load(reader, is_large_document=False)

    def test_load_negative_layer_extra_throws(self):
        layer_bytes = self.build_layer_record_bytes_with_extra_data([])
        self.write_uint32_big_endian(layer_bytes, 30, 0xFFFFFFFF)
        stream = memoryview(layer_bytes)
        reader = BigEndianReader(stream, leave_open=True)

        with pytest.raises(PsdLoadException):
            Layer.load(reader, is_large_document=False)

    def test_load_layer_inspection_reads_values(self):
        image_path = Path(
            os.path.join(
                self.test_context.current_context.test_directory,
                "testdata",
                "test.psd",
            )
        )
        image = PsdImage.load(image_path)
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
        assert (
            len(first_layer.layer_blending_ranges_data)
            == first_layer.blending_ranges_info.raw_data_length - 4
        )
        assert first_layer.additional_layer_data

    def test_save_changes_blend_mode(self):
        test_file = Path(
            os.path.join(
                self.test_context.current_context.test_directory,
                "testdata",
                "test.psd",
            )
        )
        output_file = self.get_persistent_artifact_path(
            "layer_blend_mode_test.psd"
        )

        image = PsdImage.load(test_file)
        image.layers[0].blend_mode_key = BlendMode.MULTIPLY
        image.save(output_file)
        self.log_artifact_directory(output_file)

        reloaded = PsdImage.load(output_file)
        assert reloaded.layers[0].blend_mode_key == BlendMode.MULTIPLY

        original_bytes = test_file.read_bytes()
        saved_bytes = output_file.read_bytes()
        assert self.read_layer_info_length(original_bytes) == self.read_layer_info_length(
            saved_bytes
        )

    def test_save_changes_clipping(self):
        test_file = Path(
            os.path.join(
                self.test_context.current_context.test_directory,
                "testdata",
                "test.psd",
            )
        )
        output_file = self.get_persistent_artifact_path(
            "layer_clipping_test.psd"
        )
        original_bytes = test_file.read_bytes()

        image = PsdImage.load(test_file)
        image.layers[0].clipping = 1
        image.save(output_file)
        self.log_artifact_directory(output_file)

        reloaded = PsdImage.load(output_file)
        assert reloaded.layers[0].clipping == 1

        saved_bytes = output_file.read_bytes()
        assert self.read_layer_and_mask_tail(original_bytes) == self.read_layer_and_mask_tail(
            saved_bytes
        )

    def test_save_changes_bounds(self):
        test_file = Path(
            os.path.join(
                self.test_context.current_context.test_directory,
                "testdata",
                "test.psd",
            )
        )
        output_file = self.get_persistent_artifact_path(
            "layer_bounds_test.psd"
        )

        image = PsdImage.load(test_file)
        new_bounds = Rectangle.from_left_top_right_bottom(10, 20, 40, 60)
        image.layers[0].left = new_bounds.left
        image.layers[0].top = new_bounds.top
        image.layers[0].right = new_bounds.right
        image.layers[0].bottom = new_bounds.bottom
        image.save(output_file)
        self.log_artifact_directory(output_file)

        reloaded = PsdImage.load(output_file)
        assert reloaded.layers[0].bounds == Rectangle(
            0, 0, new_bounds.width, new_bounds.height
        )
        assert reloaded.layers[0].left == new_bounds.left
        assert reloaded.layers[0].top == new_bounds.top
        assert reloaded.layers[0].right == new_bounds.right
        assert reloaded.layers[0].bottom == new_bounds.bottom

    def test_save_changes_coordinates(self):
        test_file = Path(
            os.path.join(
                self.test_context.current_context.test_directory,
                "testdata",
                "test.psd",
            )
        )
        output_file = self.get_persistent_artifact_path(
            "layer_coordinates_test.psd"
        )

        image = PsdImage.load(test_file)
        layer = image.layers[0]
        layer.top = 10
        layer.left = 20
        layer.bottom = 30
        layer.right = 50
        image.save(output_file)
        self.log_artifact_directory(output_file)

        reloaded = PsdImage.load(output_file)
        assert reloaded.layers[0].bounds == Rectangle(0, 0, 30, 20)
        assert reloaded.layers[0].left == 20
        assert reloaded.layers[0].top == 10
        assert reloaded.layers[0].right == 50
        assert reloaded.layers[0].bottom == 30

    def test_load_psb_layer_record_reads(self):
        stream = memoryview(self.build_psb_layer_record_bytes())
        reader = BigEndianReader(stream, leave_open=True)

        layer = Layer.load(reader, is_large_document=True)

        assert layer.name == "Layer 1"
        assert layer.bounds == Rectangle(0, 0, 1, 1)
        assert layer.opacity == 200
        assert layer.is_visible is True

    # Helper methods assumed to exist in the base class or module
    # write_uint32_big_endian, build_layer_record_bytes_with_extra_data,
    # read_layer_info_length, read_layer_and_mask_tail,
    # get_persistent_artifact_path, log_artifact_directory,
    # build_psb_layer_record_bytes
