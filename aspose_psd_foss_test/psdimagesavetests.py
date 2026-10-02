import os
import pytest
from aspose_psd_foss.psdimage import PsdImage
from aspose_psd_foss_test.psdtestfixturebase import PsdTestFixtureBase


class TestPsdImageSaveTests(PsdTestFixtureBase):
    def test_save_roundtrip_loads_again(self):
        test_file = os.path.join(os.path.dirname(__file__), "testdata", "test.psd")
        output_file = self.GetPersistentArtifactPath("roundtrip_test.psd")

        # Keep the original image alive for later assertions
        image1 = PsdImage.Load(test_file)
        original_length = len(image1.Layers)
        original_layer_name = image1.Layers[0].Name if original_length > 0 else ""

        image1.Save(output_file)
        self.LogArtifactDirectory(output_file)

        with PsdImage.Load(output_file) as image2:
            assert image2.Width == image1.Width
            assert image2.Height == image1.Height
            assert image2.Channels == image1.Channels
            assert image2.BitsPerChannel == image1.BitsPerChannel
            assert len(image2.Layers) == original_length
            if len(image2.Layers) > 0:
                assert image2.Layers[0].Name == original_layer_name

        # Dispose the original image if a close/dispose method exists
        if hasattr(image1, "close"):
            image1.close()
        elif hasattr(image1, "Dispose"):
            image1.Dispose()

    def test_save_roundtrip_is_byte_exact(self):
        test_file = os.path.join(os.path.dirname(__file__), "testdata", "test.psd")
        output_file = self.GetPersistentArtifactPath("roundtrip_byteexact_test.psd")

        with open(test_file, "rb") as f:
            original_bytes = f.read()

        with PsdImage.Load(test_file) as image:
            image.Save(output_file)
            self.LogArtifactDirectory(output_file)

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
        output_file = self.GetPersistentArtifactPath("layer_name_test.psd")

        with PsdImage.Load(test_file) as image:
            assert len(image.Layers) > 0

            original_name = image.Layers[0].Name
            image.Layers[0].Name = "Test Layer Name"

            image.Save(output_file)
            self.LogArtifactDirectory(output_file)

        with PsdImage.Load(output_file) as reloaded:
            assert reloaded.Layers[0].Name == "Test Layer Name"

    def test_save_changes_layer_visibility(self):
        test_file = os.path.join(os.path.dirname(__file__), "testdata", "test.psd")
        output_file = self.GetPersistentArtifactPath("layer_visible_test.psd")

        with PsdImage.Load(test_file) as image:
            assert len(image.Layers) > 0

            original_visible = image.Layers[0].IsVisible
            image.Layers[0].IsVisible = not original_visible

            image.Save(output_file)
            self.LogArtifactDirectory(output_file)

        with PsdImage.Load(output_file) as reloaded:
            assert reloaded.Layers[0].IsVisible == (not original_visible)

    def test_save_changes_layer_opacity(self):
        test_file = os.path.join(os.path.dirname(__file__), "testdata", "test.psd")
        output_file = self.GetPersistentArtifactPath("layer_opacity_test.psd")

        with PsdImage.Load(test_file) as image:
            assert len(image.Layers) > 0

            original_opacity = image.Layers[0].Opacity
            new_opacity = max(0, original_opacity - 50)
            image.Layers[0].Opacity = new_opacity

            image.Save(output_file)
            self.LogArtifactDirectory(output_file)

        with PsdImage.Load(output_file) as reloaded:
            assert reloaded.Layers[0].Opacity == new_opacity

    def test_save_mutation_preserves_flags(self):
        test_file = os.path.join(os.path.dirname(__file__), "testdata", "test.psd")
        output_file = self.GetPersistentArtifactPath("preserve_flags_and_blend.psd")

        with PsdImage.Load(test_file) as image:
            image.Layers[0].Name = "Renamed"
            image.Save(output_file)
            self.LogArtifactDirectory(output_file)

        with PsdImage.Load(output_file) as reloaded:
            assert reloaded.Layers[0].RawBlendModeKey == "norm"
            assert reloaded.Layers[0].IsVisible is True
