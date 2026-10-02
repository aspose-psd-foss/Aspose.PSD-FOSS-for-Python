import pytest
from pathlib import Path

from aspose_psd_foss.psdimage import PsdImage
from aspose_psd_foss.colormodes import ColorModes
from aspose_psd_foss.layers.blendmode import BlendMode
from aspose_psd_foss.compressionmethod import CompressionMethod
from aspose_psd_foss.sections.psdheader import PsdHeader
from aspose_psd_foss_test.psdtestfixturebase import PsdTestFixtureBase


class TestFixtureDocument(PsdTestFixtureBase):
    def test_load_basicrgb_readsmetadata(self):
        with PsdImage.load(self.get_test_data_path("basic-rgb.psd")) as image:
            assert image.width == 200
            assert image.height == 200
            assert image.channels == 3
            assert image.bits_per_channel == 8
            assert image.color_mode == ColorModes.RGB
            assert image.version == 6
            assert image.header.version == PsdHeader.PSD_VERSION
            assert image.layer_count == 3
            assert image.resource_count == 26
            assert image.compression == CompressionMethod.RLE

    def test_save_basicrgb_isbyteexact(self):
        self.assert_byte_exact_round_trip("basic-rgb.psd")

    def test_save_basicrgb_renameslayer(self):
        self.assert_rename_save("basic-rgb.psd", layer_index=1, new_name="Renamed Rectangle")

    def test_load_basiccmyk_readsmetadata(self):
        with PsdImage.load(self.get_test_data_path("basic-cmyk.psd")) as image:
            assert image.width == 200
            assert image.height == 200
            assert image.channels == 4
            assert image.color_mode == ColorModes.CMYK
            assert image.layer_count == 3
            assert image.resource_count == 28
            assert image.compression == CompressionMethod.RLE
            assert len(image.image_data_info.row_byte_counts) == 800

    def test_save_basiccmyk_isbyteexact(self):
        self.assert_byte_exact_round_trip("basic-cmyk.psd")

    def test_load_basicpsb_readsmetadata(self):
        with PsdImage.load(self.get_test_data_path("basic.psb")) as image:
            assert image.version == 6
            assert image.header.version == PsdHeader.PSB_VERSION
            assert image.is_large_document is True
            assert image.is_psb is True
            assert image.width == 200
            assert image.height == 200
            assert image.layer_count == 0
            assert image.resource_count == 24
            assert image.compression == CompressionMethod.RLE
            assert image.image_data_info.row_length_field_size == 4  # sizeof(uint)

    def test_save_basicpsb_isbyteexact(self):
        self.assert_byte_exact_round_trip("basic.psb")

    def test_load_layeredpsb_readslayers(self):
        with PsdImage.load(self.get_test_data_path("layered.psb")) as image:
            assert image.version == 6
            assert image.header.version == PsdHeader.PSB_VERSION
            assert image.layer_count == 3
            assert image.layers[0].name == "Background"
            assert image.layers[1].name == "Rectangle 1"
            assert image.layers[2].name == "Ellipse 1"
            assert image.layers[2].opacity == 191

    def test_save_layeredpsb_renameslayer(self):
        self.assert_rename_save("layered.psb", layer_index=1, new_name="Renamed Rectangle")

    def test_save_layeredpsb_changesblendmode(self):
        test_file = self.get_test_data_path("layered.psb")
        output_file = self.get_persistent_artifact_path(
            "layered_psb_blend_mode_test.psb"
        )

        with PsdImage.load(test_file) as image:
            image.layers[1].blend_mode_key = BlendMode.MULTIPLY
            image.save(output_file)
        self.log_artifact_directory(output_file)

        with PsdImage.load(output_file) as reloaded:
            assert reloaded.layers[1].blend_mode_key == BlendMode.MULTIPLY

    def test_load_layervariants_readsflags(self):
        with PsdImage.load(self.get_test_data_path("layer-variants.psd")) as image:
            assert image.layer_count == 4
            assert image.layers[1].is_visible is False
            assert image.layers[2].blend_mode_key == BlendMode.LINEAR_BURN
            assert image.layers[2].raw_blend_mode_key == "lbrn"
            assert image.layers[3].clipping == 1
            assert image.layers[3].additional_layer_data

    def test_save_layervariants_clipping(self):
        test_file = self.get_test_data_path("layer-variants.psd")
        output_file = self.get_persistent_artifact_path(
            "layer_variants_clipping_test.psd"
        )

        with PsdImage.load(test_file) as image:
            image.layers[3].clipping = 0
            image.save(output_file)
        self.log_artifact_directory(output_file)

        with PsdImage.load(output_file) as reloaded:
            assert reloaded.layers[3].clipping == 0

    def test_save_layervariants_preservestail(self):
        test_file = self.get_test_data_path("layer-variants.psd")
        original_bytes = Path(test_file).read_bytes()
        output_file = self.get_persistent_artifact_path(
            "layer_variants_tail_test.psd"
        )

        with PsdImage.load(test_file) as image:
            image.layers[2].name = "Ellipse 1 Updated"
            image.save(output_file)
        self.log_artifact_directory(output_file)

        saved_bytes = Path(output_file).read_bytes()
        assert self.read_layer_and_mask_tail(saved_bytes) == self.read_layer_and_mask_tail(
            original_bytes
        )