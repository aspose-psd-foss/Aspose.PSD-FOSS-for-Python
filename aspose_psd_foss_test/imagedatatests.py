import io
import pytest

from aspose_psd_foss.psdimage import PsdImage
from aspose_psd_foss.compressionmethod import CompressionMethod
from aspose_psd_foss.sections.imagedatakind import ImageDataKind
from aspose_psd_foss.sections.imagedata import ImageData
from aspose_psd_foss.bigendianreader import BigEndianReader
from aspose_psd_foss.coreexceptions.psdloadexception import PsdLoadException
from aspose_psd_foss_test.psdtestfixturebase import PsdTestFixtureBase


class ImageDataTests(PsdTestFixtureBase):

    def test_load_rle_fixture_reads_image_data(self):
        with PsdImage.load(self.get_test_data_path("rle.psd")) as image:
            assert image.compression == CompressionMethod.RLE
            assert image.image_data_kind == ImageDataKind.RLE
            assert image.image_data_info.row_length_field_size == 2
            assert len(image.image_data_info.row_byte_counts) == 600
            assert image.image_data_info.compressed_payload_length == 5219

    def test_save_rle_fixture_is_byte_exact(self):
        self.assert_byte_exact_round_trip("rle.psd")

    def test_load_zip_fixture_reads_image_data(self):
        with PsdImage.load(self.get_test_data_path("zip.psd")) as image:
            assert image.compression == CompressionMethod.RLE
            assert image.image_data_kind == ImageDataKind.RLE
            assert image.image_data_info.row_length_field_size == 2
            assert len(image.image_data_info.row_byte_counts) == 600
            assert image.image_data_info.compressed_payload_length == 5219

    def test_save_zip_fixture_is_byte_exact(self):
        self.assert_byte_exact_round_trip("zip.psd")

    def test_load_psd_rle_reads_structure(self):
        stream = io.BytesIO(self.build_image_data_section(CompressionMethod.RLE, [0x00, 0x02, 0xAB, 0xCD, 0x00, 0x01, 0xEF]))
        reader = BigEndianReader(stream, leave_open=True)

        image_data = ImageData.load(reader, is_large_document=False, height=1, channel_count=3)

        assert image_data.compression == CompressionMethod.RLE
        assert image_data.structure.kind == ImageDataKind.RLE
        assert image_data.structure.row_length_field_size == 2
        assert len(image_data.structure.row_byte_counts) == 3
        assert image_data.structure.row_byte_counts[0] == 2
        assert image_data.structure.row_byte_counts[1] == 0xABCD
        assert image_data.structure.row_byte_counts[2] == 1
        assert image_data.structure.compressed_payload_length == 1

    def test_load_psb_rle_reads_structure(self):
        stream = io.BytesIO(self.build_image_data_section(
            CompressionMethod.RLE,
            [
                0x00, 0x00, 0x00, 0x02,
                0x00, 0x00, 0x00, 0x01,
                0x00, 0x00, 0x00, 0x03,
                0xAB, 0xCD, 0xEF, 0x10, 0x11, 0x12
            ]))
        reader = BigEndianReader(stream, leave_open=True)

        image_data = ImageData.load(reader, is_large_document=True, height=1, channel_count=3)

        assert image_data.compression == CompressionMethod.RLE
        assert image_data.structure.kind == ImageDataKind.RLE
        assert image_data.structure.row_length_field_size == 4
        assert len(image_data.structure.row_byte_counts) == 3
        assert image_data.structure.row_byte_counts[0] == 2
        assert image_data.structure.row_byte_counts[1] == 1
        assert image_data.structure.row_byte_counts[2] == 3
        assert image_data.structure.compressed_payload_length == 6

    def test_load_psd_zip_reads_structure(self):
        stream = io.BytesIO(self.build_image_data_section(CompressionMethod.ZipWithoutPrediction, [0x78, 0x9C, 0x63, 0x60, 0x04, 0x00, 0x00, 0xFF, 0x00]))
        reader = BigEndianReader(stream, leave_open=True)

        image_data = ImageData.load(reader, is_large_document=False, height=1, channel_count=3)

        assert image_data.compression == CompressionMethod.ZipWithoutPrediction
        assert image_data.structure.kind == ImageDataKind.Zip
        assert image_data.structure.uses_prediction is False
        assert image_data.structure.compressed_payload_length == 9

    def test_load_truncated_rle_rows_throws(self):
        stream = io.BytesIO(self.build_image_data_section(CompressionMethod.RLE, [0x00, 0x02, 0xAB, 0xCD, 0x00]))
        reader = BigEndianReader(stream, leave_open=True)

        with pytest.raises(PsdLoadException):
            ImageData.load(reader, is_large_document=False, height=1, channel_count=3)
