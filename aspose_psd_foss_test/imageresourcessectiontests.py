import os
import io
import unittest

from aspose_psd_foss.psd_test_fixture_base import PsdTestFixtureBase
from aspose_psd_foss.resources.imageresourceids import ImageResourceIds
from aspose_psd_foss.big_endian_reader import BigEndianReader
from aspose_psd_foss.resources.unknownresource import UnknownResource
from aspose_psd_foss.psd_image import PsdImage
from aspose_psd_foss.resources.psdresourcekind import PsdResourceKind


class ImageResourcesSectionTests(PsdTestFixtureBase, unittest.TestCase):
    def test_load_resources_reads_blocks(self):
        resources_payload = self.build_resources_payload(
            (ImageResourceIds.GlobalAngle, "glba", [0x00, 0x00, 0x00, 0x2D]),
            (ImageResourceIds.IccProfile, "icc", [0x49, 0x43, 0x43, 0x50]),
            (ImageResourceIds.IccUntaggedProfile, "", [0x01])
        )
        stream = io.BytesIO(resources_payload)
        reader = BigEndianReader(stream, leave_open=True)

        resources = []
        while reader.position < len(resources_payload):
            resource = UnknownResource.load(reader, len(resources_payload))
            self.assertIsNotNone(resource)
            resources.append(resource)

        self.assertEqual(len(resources), 3)
        self.assertEqual(resources[0].resource_id, ImageResourceIds.GlobalAngle)
        self.assertEqual(resources[0].data, bytes([0x00, 0x00, 0x00, 0x2D]))
        self.assertEqual(resources[1].resource_id, ImageResourceIds.IccProfile)
        self.assertEqual(resources[1].data, bytes([0x49, 0x43, 0x43, 0x50]))
        self.assertEqual(resources[2].resource_id, ImageResourceIds.IccUntaggedProfile)
        self.assertEqual(resources[2].data, bytes([0x01]))

    def test_save_resources_preserves_raw(self):
        test_file = os.path.join(self.test_context.current_context.test_directory, "testdata", "test.psd")
        with open(test_file, "rb") as f:
            original_bytes = f.read()
        output_file = self.get_persistent_artifact_path("resources_roundtrip_test.psd")

        image = PsdImage.load(test_file)
        image.save(output_file)
        self.log_artifact_directory(output_file)

        with open(output_file, "rb") as f:
            saved_bytes = f.read()
        original_resources_section = self.extract_image_resources_section(original_bytes)
        saved_resources_section = self.extract_image_resources_section(saved_bytes)

        self.assertEqual(saved_resources_section, original_resources_section)

        reloaded = PsdImage.load(output_file)
        self.assertTrue(reloaded.has_image_resources)
        self.assertEqual(reloaded.resource_count, 26)

    def test_load_resourcesfixture_reads(self):
        image = PsdImage.load(self.get_test_data_path("resources.psd"))

        self.assertEqual(image.resource_count, 28)
        self.assertEqual(image.resources[0].kind, PsdResourceKind.Unknown)
        self.assertTrue(image.has_image_resources)
        self.assertEqual(len(image.layers), 3)

    def test_save_resourcesfixture_raw(self):
        test_file = self.get_test_data_path("resources.psd")
        with open(test_file, "rb") as f:
            original_bytes = f.read()
        output_file = self.get_persistent_artifact_path("resources_fixture_roundtrip_test.psd")

        image = PsdImage.load(test_file)
        image.save(output_file)
        self.log_artifact_directory(output_file)

        with open(output_file, "rb") as f:
            saved_bytes = f.read()
        self.assertEqual(
            self.extract_image_resources_section(saved_bytes),
            self.extract_image_resources_section(original_bytes)
        )
