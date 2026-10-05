import os
import pytest
from aspose_psd_foss.psdimage import PsdImage
from aspose_psd_foss.resources.psdresourcekind import PsdResourceKind
from aspose_psd_foss.sections.psdcolordatakind import PsdColorDataKind
from aspose_psd_foss.sections.imagedatakind import ImageDataKind
from aspose_psd_foss.layers.layer import Layer
from aspose_psd_foss_test.psdtestfixturebase import PsdTestFixtureBase


class InspectionDtoTests(PsdTestFixtureBase):
    def test_load_document_dtos_read_values(self):
        test_dir = os.path.join(pytest.config.rootdir, "testdata")
        image_path = os.path.join(test_dir, "test.psd")
        image = PsdImage.load(image_path)

        assert len(image.resources) == 26
        assert image.resources[0].kind == PsdResourceKind.Unknown
        assert image.resources[1].kind == PsdResourceKind.Unknown
        assert image.resources[2].kind == PsdResourceKind.Unknown
        assert image.resources[0].global_angle is None
        assert image.resources[1].global_angle is None
        assert image.resources[2].global_angle is None
        assert image.has_icc_profile is False
        assert image.is_icc_profile_untagged is None
        assert image.global_angle == 0

        assert image.color_data_info.kind == PsdColorDataKind.None_
        assert image.color_data_info.raw_data_length == 0
        assert image.indexed_palette is None

        assert image.image_data_info.kind == ImageDataKind.Rle
        assert image.image_data_info.row_length_field_size == 2  # sizeof(ushort)
        assert len(image.image_data_info.row_byte_counts) == 300
        assert image.image_data_info.compressed_payload_length > 0
        assert image.image_data_info.uses_prediction is False

    def test_load_layer_dtos_read_values(self):
        test_dir = os.path.join(pytest.config.rootdir, "testdata")
        image_path = os.path.join(test_dir, "test.psd")
        image = PsdImage.load(image_path)
        layer: Layer = image.layers[0]

        assert len(layer.channels) == 4
        assert layer.channels[0].channel_id == -1
        assert layer.channels[1].channel_id == 0
        assert layer.channels[2].channel_id == 1
        assert layer.channels[3].channel_id == 2
        assert layer.channels[0].data_length > 0

        assert layer.mask_info.is_present is False
        assert layer.mask_info.raw_data_length == 4
        assert layer.blending_ranges_info.is_present is True
        assert layer.blending_ranges_info.raw_data_length == 44
