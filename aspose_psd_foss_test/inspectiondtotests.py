import os
import unittest

from aspose_psd_foss.layers.layer import Layer
from aspose_psd_foss.psdimage import PsdImage
from aspose_psd_foss.resources.psdresourcekind import PsdResourceKind
from aspose_psd_foss.sections.imagedatakind import ImageDataKind
from aspose_psd_foss.sections.psdcolordatakind import PsdColorDataKind
from aspose_psd_foss_test.psdtestfixturebase import PsdTestFixtureBase


class InspectionDtoTests(PsdTestFixtureBase, unittest.TestCase):
    """Contains InspectionDTO tests."""

    def test_load_document_dtos_read_values(self):
        """Tests that document-level DTO inspection API exposes unknown-only resource summaries and other structural metadata."""
        test_path = os.path.join(
            os.path.dirname(__file__), "testdata", "test.psd"
        )
        with PsdImage.load(test_path) as image:
            self.assertEqual(len(image.resources), 26)
            self.assertEqual(image.resources[0].kind, PsdResourceKind.UNKNOWN)
            self.assertEqual(image.resources[1].kind, PsdResourceKind.UNKNOWN)
            self.assertEqual(image.resources[2].kind, PsdResourceKind.UNKNOWN)

            self.assertIsNone(image.resources[0].global_angle)
            self.assertIsNone(image.resources[1].global_angle)
            self.assertIsNone(image.resources[2].global_angle)

            self.assertFalse(image.has_icc_profile)
            self.assertIsNone(image.is_icc_profile_untagged)
            self.assertEqual(image.global_angle, 0)

            self.assertEqual(image.color_data_info.kind, PsdColorDataKind.NONE)
            self.assertEqual(image.color_data_info.raw_data_length, 0)
            self.assertIsNone(image.indexed_palette)

            self.assertEqual(image.image_data_info.kind, ImageDataKind.RLE)
            # sizeof(ushort) == 2
            self.assertEqual(
                image.image_data_info.row_length_field_size, 2
            )
            self.assertEqual(len(image.image_data_info.row_byte_counts), 300)
            self.assertGreater(image.image_data_info.compressed_payload_length, 0)
            self.assertFalse(image.image_data_info.uses_prediction)

    def test_load_layer_dtos_read_values(self):
        """Tests that layer-level DTO inspection API exposes channel and subsection summaries."""
        test_path = os.path.join(
            os.path.dirname(__file__), "testdata", "test.psd"
        )
        with PsdImage.load(test_path) as image:
            layer: Layer = image.layers[0]

            self.assertEqual(len(layer.channels), 4)
            self.assertEqual(layer.channels[0].channel_id, -1)
            self.assertEqual(layer.channels[1].channel_id, 0)
            self.assertEqual(layer.channels[2].channel_id, 1)
            self.assertEqual(layer.channels[3].channel_id, 2)
            self.assertGreater(layer.channels[0].data_length, 0)

            self.assertFalse(layer.mask_info.is_present)
            self.assertEqual(layer.mask_info.raw_data_length, 4)
            self.assertTrue(layer.blending_ranges_info.is_present)
            self.assertEqual(layer.blending_ranges_info.raw_data_length, 44)
