import unittest
import os

from aspose_psd_foss.colormodes import ColorModes
from aspose_psd_foss.compressionmethod import CompressionMethod
from aspose_psd_foss.layers.blendmode import BlendMode
from aspose_psd_foss.psdimage import PsdImage
from aspose_psd_foss.sections.psdheader import PsdHeader


class FixtureDocumentTests(PsdTestFixtureBase):
    """Contains FixtureDocument tests."""

    def test_load_basic_rgb_reads_metadata(self):
        """Tests that the basic RGB fixture exposes expected PSD document metadata, layers, resources, and compression."""
        image = PsdImage.load(self.get_test_data_path("basic-rgb.psd"))
        try:
            self.assertEqual(image.width, 200)
            self.assertEqual(image.height, 200)
            self.assertEqual(image.channels, 3)
            self.assertEqual(image.bits_per_channel, 8)
            self.assertEqual(image.color_mode, ColorModes.Rgb)
            self.assertEqual(image.version, 6)
            self.assertEqual(image.header.version, PsdHeader.PsdVersion)
            self.assertEqual(image.layer_count, 3)
            self.assertEqual(image.resource_count, 26)
            self.assertEqual(image.compression, CompressionMethod.RLE)
        finally:
            image.close()

    def test_save_basic_rgb_is_byte_exact(self):
        """Tests that saving the basic RGB fixture without mutations preserves the file byte‑for‑byte."""
        self.assert_byte_exact_round_trip("basic-rgb.psd")

    def test_save_basic_rgb_renames_layer(self):
        """Tests that renaming a layer in the basic RGB fixture persists after save and reload."""
        self.assert_rename_save("basic-rgb.psd", layer_index=1, new_name="Renamed Rectangle")

    def test_load_basic_cmyk_reads_metadata(self):
        """Tests that the basic CMYK fixture exposes expected channels, resources, layers, compression, and row metadata."""
        image = PsdImage.load(self.get_test_data_path("basic-cmyk.psd"))
        try:
            self.assertEqual(image.width, 200)
            self.assertEqual(image.height, 200)
            self.assertEqual(image.channels, 4)
            self.assertEqual(image.color_mode, ColorModes.Cmyk)
            self.assertEqual(image.layer_count, 3)
            self.assertEqual(image.resource_count, 28)
            self.assertEqual(image.compression, CompressionMethod.RLE)
            self.assertEqual(len(image.image_data_info.row_byte_counts), 800)
        finally:
            image.close()

    def test_save_basic_cmyk_is_byte_exact(self):
        """Tests that saving the basic CMYK fixture without mutations preserves the file byte‑for‑byte."""
        self.assert_byte_exact_round_trip("basic-cmyk.psd")

    def test_load_basic_psb_reads_metadata(self):
        """Tests that the basic PSB fixture exposes PSB version, large‑document state, resources, and RLE row‑length sizing."""
        image = PsdImage.load(self.get_test_data_path("basic.psb"))
        try:
            self.assertEqual(image.version, 6)
            self.assertEqual(image.header.version, PsdHeader.PsbVersion)
            self.assertTrue(image.is_large_document)
            self.assertTrue(image.is_psb)
            self.assertEqual(image.width, 200)
            self.assertEqual(image.height, 200)
            self.assertEqual(image.layer_count, 0)
            self.assertEqual(image.resource_count, 24)
            self.assertEqual(image.compression, CompressionMethod.RLE)
            self.assertEqual(
                image.image_data_info.row_length_field_size, 4
            )  # sizeof(uint) == 4
        finally:
            image.close()

    def test_save_basic_psb_is_byte_exact(self):
        """Tests that saving the basic PSB fixture without mutations preserves the file byte‑for‑byte."""
        self.assert_byte_exact_round_trip("basic.psb")

    def test_load_layered_psb_reads_layers(self):
        """Tests that the layered PSB fixture exposes expected layer names, layer count, and opacity metadata."""
        image = PsdImage.load(self.get_test_data_path("layered.psb"))
        try:
            self.assertEqual(image.version, 6)
            self.assertEqual(image.header.version, PsdHeader.PsbVersion)
            self.assertEqual(image.layer_count, 3)
            self.assertEqual(image.layers[0].name, "Background")
            self.assertEqual(image.layers[1].name, "Rectangle 1")
            self.assertEqual(image.layers[2].name, "Ellipse 1")
            self.assertEqual(image.layers[2].opacity, 191)
        finally:
            image.close()

    def test_save_layered_psb_renames_layer(self):
        """Tests that renaming a layer in the layered PSB fixture persists after save and reload."""
        self.assert_rename_save("layered.psb", layer_index=1, new_name="Renamed Rectangle")

    def test_save_layered_psb_changes_blend_mode(self):
        """Tests that changing blend mode in the layered PSB fixture persists with the expected PSD blend key."""
        test_file = self.get_test_data_path("layered.psb")
        output_file = self.get_persistent_artifact_path(
            "layered_psb_blend_mode_test.psb"
        )

        image = PsdImage.load(test_file)
        try:
            image.layers[1].blend_mode_key = BlendMode.Multiply
            image.save(output_file)
        finally:
            image.close()

        self.log_artifact_directory(output_file)

        reloaded = PsdImage.load(output_file)
        try:
            self.assertEqual(reloaded.layers[1].blend_mode_key, BlendMode.Multiply)
        finally:
            reloaded.close()

    def test_load_layer_variants_reads_flags(self):
        """Tests that the layer variants fixture exposes visibility, unknown blend key, clipping, and additional data flags."""
        image = PsdImage.load(self.get_test_data_path("layer-variants.psd"))
        try:
            self.assertEqual(image.layer_count, 4)
            self.assertFalse(image.layers[1].is_visible)
            self.assertEqual(image.layers[2].blend_mode_key, BlendMode.LinearBurn)
            self.assertEqual(image.layers[2].raw_blend_mode_key, "lbrn")
            self.assertEqual(image.layers[3].clipping, 1)
            self.assertTrue(bool(image.layers[3].additional_layer_data))
        finally:
            image.close()

    def test_save_layer_variants_clipping(self):
        """Tests that changing clipping in the layer variants fixture persists after save and reload."""
        test_file = self.get_test_data_path("layer-variants.psd")
        output_file = self.get_persistent_artifact_path(
            "layer_variants_clipping_test.psd"
        )

        image = PsdImage.load(test_file)
        try:
            image.layers[3].clipping = 0
            image.save(output_file)
        finally:
            image.close()

        self.log_artifact_directory(output_file)

        reloaded = PsdImage.load(output_file)
        try:
            self.assertEqual(reloaded.layers[3].clipping, 0)
        finally:
            reloaded.close()

    def test_save_layer_variants_preserves_tail(self):
        """Tests that mutating a layer in the variants fixture preserves the layer‑and‑mask tail bytes."""
        test_file = self.get_test_data_path("layer-variants.psd")
        original_bytes = self._read_all_bytes(test_file)
        output_file = self.get_persistent_artifact_path(
            "layer_variants_tail_test.psd"
        )

        image = PsdImage.load(test_file)
        try:
            image.layers[2].name = "Ellipse 1 Updated"
            image.save(output_file)
        finally:
            image.close()

        self.log_artifact_directory(output_file)

        saved_bytes = self._read_all_bytes(output_file)
        self.assertEqual(
            self.read_layer_and_mask_tail(saved_bytes),
            self.read_layer_and_mask_tail(original_bytes),
        )

    @staticmethod
    def _read_all_bytes(path):
        with open(path, "rb") as f:
            return f.read()
