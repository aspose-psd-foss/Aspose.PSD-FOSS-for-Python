import os
import io
from aspose_psd_foss_test.psdtestfixturebase import PsdTestFixtureBase
from aspose_psd_foss.resources.imageresourceids import ImageResourceIds
from aspose_psd_foss.resources.unknownresource import UnknownResource
from aspose_psd_foss.resources.psdresourcekind import PsdResourceKind
from aspose_psd_foss.psdimage import PsdImage
from aspose_psd_foss.bigendianreader import BigEndianReader


class ImageResourcesSectionTests(PsdTestFixtureBase):

    def build_resources_payload(self, *resources):
        payload = bytearray()
        for resource_id, name, data in resources:
            name_bytes = name.encode('utf-16-be') if name else b''
            payload.append(0)  # 1-byte padding after signature
            payload.extend(name_bytes)
            if len(name_bytes) % 2 == 0:
                payload.append(0)  # 2-byte padding if name length even
            payload.extend(data)
            payload.extend(b'\x00' * ((4 - len(data) % 4) % 4))  # 4-byte alignment
        return bytes(payload)

    def test_load_resources_reads_blocks(self):
        resources_payload = self.build_resources_payload(
            (ImageResourceIds.GLOBAL_ANGLE, "glba", [0x00, 0x00, 0x00, 0x2D]),
            (ImageResourceIds.ICC_PROFILE, "icc", [0x49, 0x43, 0x43, 0x50]),
            (ImageResourceIds.ICC_UNTAGGED_PROFILE, "", [0x01]))
        stream = io.BytesIO(resources_payload)
        reader = BigEndianReader(stream, leave_open=True)

        resources = []
        while reader.position < len(resources_payload):
            resource = UnknownResource.load(reader, len(resources_payload))
            assert resource is not None
            resources.append(resource)

        assert len(resources) == 3
        assert resources[0].resource_id == ImageResourceIds.GLOBAL_ANGLE
        assert resources[0].data == bytes([0x00, 0x00, 0x00, 0x2D])
        assert resources[1].resource_id == ImageResourceIds.ICC_PROFILE
        assert resources[1].data == bytes([0x49, 0x43, 0x43, 0x50])
        assert resources[2].resource_id == ImageResourceIds.ICC_UNTAGGED_PROFILE
        assert resources[2].data == bytes([0x01])

    def test_save_resources_preserves_raw(self):
        test_file = os.path.join(self.test_directory, "testdata", "test.psd")
        original_bytes = open(test_file, 'rb').read()
        output_file = self.get_persistent_artifact_path("resources_roundtrip_test.psd")

        with PsdImage.load(test_file) as image:
            image.save(output_file)
            self.log_artifact_directory(output_file)

        saved_bytes = open(output_file, 'rb').read()
        original_resources_section = self.extract_image_resources_section(original_bytes)
        saved_resources_section = self.extract_image_resources_section(saved_bytes)

        assert saved_resources_section == original_resources_section

        with PsdImage.load(output_file) as reloaded:
            assert reloaded.has_image_resources is True
            assert reloaded.resource_count == 26

    def test_load_resources_fixture_reads(self):
        test_file = self.get_test_data_path("resources.psd")
        with PsdImage.load(test_file) as image:
            assert image.resource_count == 28
            assert image.resources[0].kind == PsdResourceKind.UNKNOWN
            assert image.has_image_resources is True
            assert len(image.layers) == 3

    def test_save_resources_fixture_raw(self):
        test_file = self.get_test_data_path("resources.psd")
        original_bytes = open(test_file, 'rb').read()
        output_file = self.get_persistent_artifact_path("resources_fixture_roundtrip_test.psd")

        with PsdImage.load(test_file) as image:
            image.save(output_file)
            self.log_artifact_directory(output_file)

        saved_bytes = open(output_file, 'rb').read()
        assert self.extract_image_resources_section(saved_bytes) == self.extract_image_resources_section(original_bytes)
