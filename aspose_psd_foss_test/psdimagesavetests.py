import os
import pytest
from aspose_psd_foss.psdimage import PsdImage
from aspose_psd_foss_test.psdtestfixturebase import PsdTestFixtureBase


class TestPsdImageSaveTests(PsdTestFixtureBase):
    """
    Contains PSD ImageSave tests.
    """

    def test_save_round_trip_loads_again(self):
        """
        Tests that saving a PSD file without mutations produces a valid file.
        Verifies that the saved file can be reloaded with equivalent properties.
        """
        test_file = os.path.join(self.get_test_data_path(), "testdata", "test.psd")
        output_file = self.get_persistent_artifact_path("roundtrip_test.psd")

        with PsdImage.load(test_file) as image1:
            original_length = len(image1.layers)
            original_layer_name = image1.layers[0].name if len(image1.layers) > 0 else ""
            image1.save(output_file)
            self.log_artifact_directory(output_file)

        with PsdImage.load(output_file) as image2:
            assert image2.width == image1.width
            assert image2.height == image1.height
            assert image2.channels == image1.channels
            assert image2.bits_per_channel == image1.bits_per_channel
            assert len(image2.layers) == original_length
            if len(image2.layers) > 0:
                assert image2.layers[0].name == original_layer_name

    def test_save_round_trip_is_byte_exact(self):
        """
        Tests strict no-mutation round-trip with byte-for-byte comparison.
        Verifies that saving a PSD file without mutations produces a file
        that is byte-for-byte identical to the original.
        """
        test_file = os.path.join(self.get_test_data_path(), "testdata", "test.psd")
        output_file = self.get_persistent_artifact_path("roundtrip_byteexact_test.psd")

        with open(test_file, "rb") as file_handle:
            original_bytes = file_handle.read()

        with PsdImage.load(test_file) as image:
            image.save(output_file)
            self.log_artifact_directory(output_file)

        with open(output_file, "rb") as file_handle:
            saved_bytes = file_handle.read()

        assert len(saved_bytes) == len(original_bytes), \
            "Round-trip output file length must match original file length."

        for i in range(len(original_bytes)):
            assert saved_bytes[i] == original_bytes[i], \
                f"Byte mismatch at position {i}: expected {original_bytes[i]:X2}, got {saved_bytes[i]:X2}"

    def test_save_changes_layer_name(self):
        """
        Tests that changing a layer name and saving produces a valid file with the new name.
        """
        test_file = os.path.join(self.get_test_data_path(), "testdata", "test.psd")
        output_file = self.get_persistent_artifact_path("layer_name_test.psd")

        with PsdImage.load(test_file) as image:
            assert len(image.layers) > 0

            image.layers[0].name = "Test Layer Name"
            image.save(output_file)
            self.log_artifact_directory(output_file)

        with PsdImage.load(output_file) as reloaded:
            assert reloaded.layers[0].name == "Test Layer Name"

    def test_save_changes_layer_visibility(self):
        """
        Tests that changing a layer's visibility and saving produces a valid file with the new state.
        """
        test_file = os.path.join(self.get_test_data_path(), "testdata", "test.psd")
        output_file = self.get_persistent_artifact_path("layer_visible_test.psd")

        with PsdImage.load(test_file) as image:
            assert len(image.layers) > 0

            original_visible = image.layers[0].is_visible
            image.layers[0].is_visible = not original_visible
            image.save(output_file)
            self.log_artifact_directory(output_file)

        with PsdImage.load(output_file) as reloaded:
            assert reloaded.layers[0].is_visible == (not original_visible)

    def test_save_changes_layer_opacity(self):
        """
        Tests that changing a layer's opacity and saving produces a valid file with the new opacity.
        """
        test_file = os.path.join(self.get_test_data_path(), "testdata", "test.psd")
        output_file = self.get_persistent_artifact_path("layer_opacity_test.psd")

        with PsdImage.load(test_file) as image:
            assert len(image.layers) > 0

            original_opacity = image.layers[0].opacity
            new_opacity = max(0, original_opacity - 50)
            image.layers[0].opacity = new_opacity
            image.save(output_file)
            self.log_artifact_directory(output_file)

        with PsdImage.load(output_file) as reloaded:
            assert reloaded.layers[0].opacity == new_opacity

    def test_save_mutation_preserves_flags(self):
        """
        Tests that saving after a supported mutation preserves raw layer flags and the original blend mode key.
        """
        test_file = os.path.join(self.get_test_data_path(), "testdata", "test.psd")
        output_file = self.get_persistent_artifact_path("preserve_flags_and_blend.psd")

        with PsdImage.load(test_file) as image:
            image.layers[0].name = "Renamed"
            image.save(output_file)
            self.log_artifact_directory(output_file)

        with PsdImage.load(output_file) as reloaded:
            assert reloaded.layers[0].raw_blend_mode_key == "norm"
            assert reloaded.layers[0].is_visible is True
