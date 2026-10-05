import os
import pytest
from aspose_psd_foss.psdimage import PsdImage
from aspose_psd_foss_test.psdtestfixturebase import PsdTestFixtureBase


class TestPsdImagesaveTests(PsdTestFixtureBase):
    def test_save_roundtrip_loads_again(self):
        test_file = os.path.join(os.path.dirname(__file__), "testdata", "test.psd")
        output_file = self.get_persistent_artifact_path("roundtrip_test.psd")

        # Keep the original image alive for later assertions
        image1 = PsdImage.load(test_file)
        original_length = len(image1.layers)
        original_layer_name = image1.layers[0].name if original_length > 0 else ""

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

        # Dispose the original image if a close/dispose method exists
        if hasattr(image1, "close"):
            image1.close()
        elif hasattr(image1, "Dispose"):
            image1.Dispose()

    def test_save_roundtrip_is_byte_exact(self):
        test_file = os.path.join(os.path.dirname(__file__), "testdata", "test.psd")
        output_file = self.get_persistent_artifact_path("roundtrip_byteexact_test.psd")

        with open(test_file, "rb") as f:
            original_bytes = f.read()

        with PsdImage.load(test_file) as image:
            image.save(output_file)
            self.log_artifact_directory(output_file)

        with open(output_file, "rb") as f:
            saved_bytes = f.read()

        assert len(saved_bytes) == len(original_bytes), (
            "Round-trip output file length must match original file length."
        )

        for i in range(len(original_bytes)):
            assert saved_bytes[i] == original_bytes[i], (
                f"Byte mismatch at position {i}: expected "
                f"{original_bytes[i]:02X}, got {saved_bytes[i]:02X}"
            )

    def test_save_changes_layer_name(self):
        test_file = os.path.join(os.path.dirname(__file__), "testdata", "test.psd")
        output_file = self.get_persistent_artifact_path("layer_name_test.psd")

        with PsdImage.load(test_file) as image:
            assert len(image.layers) > 0

            original_name = image.layers[0].name
            image.layers[0].name = "Test Layer name"

            image.save(output_file)
            self.log_artifact_directory(output_file)

        with PsdImage.load(output_file) as reloaded:
            assert reloaded.layers[0].name == "Test Layer name"

    def test_save_changes_layer_visibility(self):
        test_file = os.path.join(os.path.dirname(__file__), "testdata", "test.psd")
        output_file = self.get_persistent_artifact_path("layer_visible_test.psd")

        with PsdImage.load(test_file) as image:
            assert len(image.layers) > 0

            original_visible = image.layers[0].IsVisible
            image.layers[0].is_visible = not original_visible

            image.save(output_file)
            self.log_artifact_directory(output_file)

        with PsdImage.load(output_file) as reloaded:
            assert reloaded.layers[0].IsVisible == (not original_visible)

    def test_save_changes_layer_opacity(self):
        test_file = os.path.join(os.path.dirname(__file__), "testdata", "test.psd")
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
        test_file = os.path.join(os.path.dirname(__file__), "testdata", "test.psd")
        output_file = self.get_persistent_artifact_path("preserve_flags_and_blend.psd")

        with PsdImage.load(test_file) as image:
            image.layers[0].name = "Renamed"
            image.save(output_file)
            self.log_artifact_directory(output_file)

        with PsdImage.load(output_file) as reloaded:
            assert reloaded.layers[0].raw_blend_mode_key == "norm"
            assert reloaded.layers[0].IsVisible is True
