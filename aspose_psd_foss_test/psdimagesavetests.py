import os
import unittest
from pathlib import Path

from aspose_psd_foss.psdimage import PsdImage
from aspose_psd_foss_test.psdtestfixturebase import PsdTestFixtureBase


class PsdImageSaveTests(PsdTestFixtureBase, unittest.TestCase):
    """
    Contains PSD ImageSave tests.
    """

    def test_save_round_trip_loads_again(self):
        """
        Tests that saving a PSD file without mutations produces a valid file.
        Verifies that the saved file can be reloaded with equivalent properties.
        """
        test_file = (
            Path(__file__).resolve().parents[1] / "testdata" / "test.psd"
        )
        output_file = self.get_persistent_artifact_path(
            "roundtrip_test.psd"
        )

        with PsdImage.load(str(test_file)) as image1:
            original_length = len(image1.layers)
            original_layer_name = (
                image1.layers[0].name if original_length > 0 else ""
            )
            image1.save(str(output_file))
            self.log_artifact_directory(str(output_file))

            with PsdImage.load(str(output_file)) as image2:
                self.assertEqual(image2.width, image1.width)
                self.assertEqual(image2.height, image1.height)
                self.assertEqual(image2.channels, image1.channels)
                self.assertEqual(
                    image2.bits_per_channel, image1.bits_per_channel
                )
                self.assertEqual(len(image2.layers), original_length)
                if len(image2.layers) > 0:
                    self.assertEqual(
                        image2.layers[0].name, original_layer_name
                    )

    def test_save_round_trip_is_byte_exact(self):
        """
        Tests strict no-mutation round-trip with byte-for-byte comparison.
        Verifies that saving a PSD file without mutations produces a file
        that is byte-for-byte identical to the original.
        """
        test_file = (
            Path(__file__).resolve().parents[1] / "testdata" / "test.psd"
        )
        output_file = self.get_persistent_artifact_path(
            "roundtrip_byteexact_test.psd"
        )

        original_bytes = Path(test_file).read_bytes()

        with PsdImage.load(str(test_file)) as image:
            image.save(str(output_file))
            self.log_artifact_directory(str(output_file))

        saved_bytes = Path(output_file).read_bytes()

        self.assertEqual(
            len(saved_bytes),
            len(original_bytes),
            "Round-trip output file length must match original file length.",
        )

        for i in range(len(original_bytes)):
            self.assertEqual(
                saved_bytes[i],
                original_bytes[i],
                f"Byte mismatch at position {i}: "
                f"expected {original_bytes[i]:02X}, got {saved_bytes[i]:02X}",
            )

    def test_save_changes_layer_name(self):
        """
        Tests that changing a layer name and saving produces a valid file with the new name.
        """
        test_file = (
            Path(__file__).resolve().parents[1] / "testdata" / "test.psd"
        )
        output_file = self.get_persistent_artifact_path(
            "layer_name_test.psd"
        )

        with PsdImage.load(str(test_file)) as image:
            self.assertGreater(len(image.layers), 0)

            original_name = image.layers[0].name
            image.layers[0].name = "Test Layer Name"

            image.save(str(output_file))
            self.log_artifact_directory(str(output_file))

            with PsdImage.load(str(output_file)) as reloaded:
                self.assertEqual(
                    reloaded.layers[0].name, "Test Layer Name"
                )

    def test_save_changes_layer_visibility(self):
        """
        Tests that changing a layer's visibility and saving produces a valid file with the new state.
        """
        test_file = (
            Path(__file__).resolve().parents[1] / "testdata" / "test.psd"
        )
        output_file = self.get_persistent_artifact_path(
            "layer_visible_test.psd"
        )

        with PsdImage.load(str(test_file)) as image:
            self.assertGreater(len(image.layers), 0)

            original_visible = image.layers[0].is_visible
            image.layers[0].is_visible = not original_visible

            image.save(str(output_file))
            self.log_artifact_directory(str(output_file))

            with PsdImage.load(str(output_file)) as reloaded:
                self.assertEqual(
                    reloaded.layers[0].is_visible, not original_visible
                )

    def test_save_changes_layer_opacity(self):
        """
        Tests that changing a layer's opacity and saving produces a valid file with the new opacity.
        """
        test_file = (
            Path(__file__).resolve().parents[1] / "testdata" / "test.psd"
        )
        output_file = self.get_persistent_artifact_path(
            "layer_opacity_test.psd"
        )

        with PsdImage.load(str(test_file)) as image:
            self.assertGreater(len(image.layers), 0)

            original_opacity = image.layers[0].opacity
            new_opacity = max(0, original_opacity - 50)
            image.layers[0].opacity = new_opacity

            image.save(str(output_file))
            self.log_artifact_directory(str(output_file))

            with PsdImage.load(str(output_file)) as reloaded:
                self.assertEqual(
                    reloaded.layers[0].opacity, new_opacity
                )

    def test_save_mutation_preserves_flags(self):
        """
        Tests that saving after a supported mutation preserves raw layer flags
        and the original blend mode key.
        """
        test_file = (
            Path(__file__).resolve().parents[1] / "testdata" / "test.psd"
        )
        output_file = self.get_persistent_artifact_path(
            "preserve_flags_and_blend.psd"
        )

        with PsdImage.load(str(test_file)) as image:
            image.layers[0].name = "Renamed"
            image.save(str(output_file))
            self.log_artifact_directory(str(output_file))

            with PsdImage.load(str(output_file)) as reloaded:
                self.assertEqual(
                    reloaded.layers[0].raw_blend_mode_key, "norm"
                )
                self.assertTrue(reloaded.layers[0].is_visible)
