import io
import pathlib

import pytest

from aspose_psd_foss.bigendianreader import BigEndianReader
from aspose_psd_foss.psdimage import PsdImage
from aspose_psd_foss.resources.imageresourceids import ImageResourceIds
from aspose_psd_foss.resources.psdresourcekind import PsdResourceKind
from aspose_psd_foss.resources.unknownresource import UnknownResource
from aspose_psd_foss_test.psdtestfixturebase import PsdTestFixtureBase


class TestImageResourcesSection(PsdTestFixtureBase):
    def test_load_resources_reads_blocks(self):
        resources_payload = self.build_resources_payload(
            (ImageResourceIds.GLOBAL_ANGLE, "glba", bytes([0x00, 0x00, 0x00, 0x2D])),
            (ImageResourceIds.ICC_PROFILE, "icc", bytes([0x49, 0x43, 0x43, 0x50])),
            (ImageResourceIds.ICC_UNTAGGED_PROFILE, "", bytes([0x01])),
        )
        stream = io.BytesIO(resources_payload)
        reader = BigEndianReader(stream, leave_open=True)

        resources = []
        stream_length = len(stream.getvalue())
        while reader.position < stream_length:
            resource = UnknownResource.load(reader, stream_length)
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
        test_file = pathlib.Path(self.test_context.current_dir) / "testdata" / "test.psd"
        original_bytes = test_file.read_bytes()
        output_file = pathlib.Path(
            self.get_persistent_artifact_path("resources_roundtrip_test.psd")
        )

        image = PsdImage.load(str(test_file))
        image.save(str(output_file))
        self.log_artifact_directory(str(output_file))

        saved_bytes = output_file.read_bytes()
        original_section = self.extract_image_resources_section(original_bytes)
        saved_section = self.extract_image_resources_section(saved_bytes)

        assert saved_section == original_section

        reloaded = PsdImage.load(str(output_file))
        assert reloaded.has_image_resources is True
        assert reloaded.resource_count == 26

    def test_load_resourcesfixture_reads(self):
        image = PsdImage.load(self.get_test_data_path("resources.psd"))

        assert image.resource_count == 28
        assert image.resources[0].kind == PsdResourceKind.UNKNOWN
        assert image.has_image_resources is True
        assert len(image.layers) == 3

    def test_save_resourcesfixture_raw(self):
        test_file = pathlib.Path(self.get_test_data_path("resources.psd"))
        original_bytes = test_file.read_bytes()
        output_file = pathlib.Path(
            self.get_persistent_artifact_path(
                "resources_fixture_roundtrip_test.psd"
            )
        )

        image = PsdImage.load(str(test_file))
        image.save(str(output_file))
        self.log_artifact_directory(str(output_file))

        saved_bytes = output_file.read_bytes()
        assert (
            self.extract_image_resources_section(saved_bytes)
            == self.extract_image_resources_section(original_bytes)
        )
