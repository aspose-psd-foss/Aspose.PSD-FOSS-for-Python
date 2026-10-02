import io
import pytest
from pathlib import Path

from aspose_psd_foss.compressionmethod import CompressionMethod
from aspose_psd_foss.coreexceptions.psdloadexception import PsdLoadException
from aspose_psd_foss.psdimage import PsdImage
from aspose_psd_foss.bigendianreader import BigEndianReader
from aspose_psd_foss.sections.imagedata import ImageData
from aspose_psd_foss.sections.imagedatakind import ImageDataKind
from aspose_psd_foss_test.psdtestfixturebase import PsdTestFixtureBase

import struct


class TestImageData(PsdTestFixtureBase):
    def test_load_rlefixture_readsimagedata(self):
        with PsdImage.load(self.get_test_data_path("rle.psd")) as image:
            assert image.compression == CompressionMethod.RLE
            assert image.image_data_kind == ImageDataKind.RLE
            assert image.image_data_info.row_length_field_size == 2  # sizeof(ushort)
            assert len(image.image_data_info.row_byte_counts) == 600
            assert image.image_data_info.compressed_payload_length == 5219

    def test_save_rlefixture_isbyteexact(self):
        self.assert_byte_exact_round_trip("rle.psd")

    def test_load_zipfixture_readsimagedata(self):
        with PsdImage.load(self.get_test_data_path("zip.psd")) as image:
            assert image.compression == CompressionMethod.RLE
            assert image.image_data_kind == ImageDataKind.RLE
            assert image.image_data_info.row_length_field_size == 2  # sizeof(ushort)
            assert len(image.image_data_info.row_byte_counts) == 600
            assert image.image_data_info.compressed_payload_length == 5219

    def test_save_zipfixture_isbyteexact(self):
        self.assert_byte_exact_round_trip("zip.psd")

    def test_load_psdrle_readsstructure(self):
        with io.BytesIO(
            self._build_image_data_section(
                CompressionMethod.RLE,
                bytes([0x00, 0x02, 0xAB, 0xCD, 0x00, 0x01, 0xEF]),
            )
        ) as stream:
            with BigEndianReader(stream, leave_open=True) as reader:
                image_data = ImageData.load(
                    reader, is_large_document=False, height=1, channel_count=3
                )

                assert image_data.compression == CompressionMethod.RLE
                assert image_data.structure.kind == ImageDataKind.RLE
                assert image_data.structure.row_length_field_size == 2  # sizeof(ushort)
                assert len(image_data.structure.row_byte_counts) == 3
                assert image_data.structure.row_byte_counts[0] == 2
                assert image_data.structure.row_byte_counts[1] == 0xABCD
                assert image_data.structure.row_byte_counts[2] == 1
                assert image_data.structure.compressed_payload_length == 1

    def test_load_psbrle_readsstructure(self):
        with io.BytesIO(
            self._build_image_data_section(
                CompressionMethod.RLE,
                bytes(
                    [
                        0x00, 0x00, 0x00, 0x02,
                        0x00, 0x00, 0x00, 0x01,
                        0x00, 0x00, 0x00, 0x03,
                        0xAB, 0xCD, 0xEF, 0x10, 0x11, 0x12,
                    ]
                ),
            )
        ) as stream:
            with BigEndianReader(stream, leave_open=True) as reader:
                image_data = ImageData.load(
                    reader, is_large_document=True, height=1, channel_count=3
                )

                assert image_data.compression == CompressionMethod.RLE
                assert image_data.structure.kind == ImageDataKind.RLE
                assert image_data.structure.row_length_field_size == 4  # sizeof(uint)
                assert len(image_data.structure.row_byte_counts) == 3
                assert image_data.structure.row_byte_counts[0] == 2
                assert image_data.structure.row_byte_counts[1] == 1
                assert image_data.structure.row_byte_counts[2] == 3
                assert image_data.structure.compressed_payload_length == 6

    def test_load_psdzip_readsstructure(self):
        with io.BytesIO(
            self._build_image_data_section(
                CompressionMethod.ZIP_WITHOUT_PREDICTION,
                bytes([0x78, 0x9C, 0x63, 0x60, 0x04, 0x00, 0x00, 0xFF, 0x00]),
            )
        ) as stream:
            with BigEndianReader(stream, leave_open=True) as reader:
                image_data = ImageData.load(
                    reader, is_large_document=False, height=1, channel_count=3
                )

                assert image_data.compression == CompressionMethod.ZIP_WITHOUT_PREDICTION
                assert image_data.structure.kind == ImageDataKind.ZIP
                assert image_data.structure.uses_prediction is False
                assert image_data.structure.compressed_payload_length == 9

    def test_load_truncatedrlerows_throws(self):
        with io.BytesIO(
            self._build_image_data_section(
                CompressionMethod.RLE,
                bytes([0x00, 0x02, 0xAB, 0xCD, 0x00]),
            )
        ) as stream:
            with BigEndianReader(stream, leave_open=True) as reader:
                with pytest.raises(PsdLoadException):
                    ImageData.load(
                        reader, is_large_document=False, height=1, channel_count=3
                    )

    # --- helpers ---

    @staticmethod
    def _build_image_data_section(compression: int, payload: bytes) -> bytes:
        return struct.pack(">H", compression) + payload