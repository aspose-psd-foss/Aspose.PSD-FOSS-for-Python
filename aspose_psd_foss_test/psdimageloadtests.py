import os
import io
import pytest

from aspose_psd_foss_test.psdtestfixturebase import PsdTestFixtureBase
from aspose_psd_foss.psdimage import PsdImage
from aspose_psd_foss.colormodes import ColorModes
from aspose_psd_foss.compressionmethod import CompressionMethod
from aspose_psd_foss.sections.imagedatakind import ImageDataKind
from aspose_psd_foss.sections.psdheader import PsdHeader
from aspose_psd_foss.layers.blendmode import BlendMode
from aspose_psd_foss_test.nonseekablereadstream import NonSeekableReadStream
from aspose_psd_foss.bigendianreader import BigEndianReader
from aspose_psd_foss.coreexceptions.psdloadexception import PsdLoadException
from aspose_psd_foss.coreexceptions.argumentnullexception import ArgumentNullException
from aspose_psd_foss.rectangle import Rectangle


class TestPsdImageLoadTests(PsdTestFixtureBase):
    def test_load_document_reads_properties(self):
        test_file = os.path.join(self._test_dir, "testdata", "test.psd")
        assert os.path.isfile(test_file), "Test file not found"

        image = PsdImage.load(test_file)
        try:
            assert image.width > 0
            assert image.height > 0
            assert image.channels > 0
            assert image.bits_per_channel == 8
            assert image.color_mode == ColorModes.RGB
            assert 0 < image.version <= 6
            assert len(image.layers) > 0
        finally:
            image.close()

    def test_load_layer_reads_properties(self):
        test_file = os.path.join(self._test_dir, "testdata", "test.psd")
        image = PsdImage.load(test_file)
        try:
            assert len(image.layers) > 0
            first_layer = image.layers[0]

            assert first_layer.name == "Background copy"
            assert first_layer.bounds != Rectangle()
            assert first_layer.is_visible is True
            assert 0 <= first_layer.opacity <= 255
            assert first_layer.blend_mode_key == BlendMode.NORMAL

            assert image.layers[1].name == "Pattern Fill 1"
        finally:
            image.close()

    def test_load_layers_indexable(self):
        test_file = os.path.join(self._test_dir, "testdata", "test.psd")
        image = PsdImage.load(test_file)
        try:
            assert image.layers[0] is not None
            assert image.layers[1] is not None
        finally:
            image.close()

    def test_load_seekable_preserves_position(self):
        test_path = os.path.join(self._test_dir, "testdata", "test.psd")
        with open(test_path, "rb") as f:
            bytes_data = f.read()
        prefix = bytes([1, 2, 3, 4, 5])
        stream = io.BytesIO()
        stream.write(prefix)
        stream.write(bytes_data)
        stream.seek(len(prefix))

        image = PsdImage.load(stream)
        try:
            assert stream.tell() == len(prefix)
            assert image.width > 0
        finally:
            image.close()

    def test_load_non_seekable_stream_succeeds(self):
        test_path = os.path.join(self._test_dir, "testdata", "test.psd")
        with open(test_path, "rb") as f:
            bytes_data = f.read()
        stream = NonSeekableReadStream(bytes_data)
        image = PsdImage.load(stream)
        try:
            assert image.width > 0
            assert len(image.layers) > 0
        finally:
            image.close()

    def test_load_null_stream_throws(self):
        with pytest.raises(ArgumentNullException):
            PsdImage.load(None)

    def test_load_missing_file_throws(self):
        missing_file = os.path.join(self._test_dir, "missing.psd")
        with pytest.raises(FileNotFoundError):
            PsdImage.load(missing_file)

    def test_load_invalid_signature_throws(self):
        header_bytes = self.build_header_bytes(PsdHeader.PSD_VERSION)
        stream = io.BytesIO(header_bytes)
        # Corrupt the first byte to make the signature invalid
        stream.seek(0)
        stream.write(b'B')
        stream.seek(0)

        reader = BigEndianReader(stream, leave_open=True)
        with pytest.raises(PsdLoadException):
            PsdHeader.load(reader)

    def test_load_doc_inspection_reads(self):
        test_file = os.path.join(self._test_dir, "testdata", "test.psd")
        image = PsdImage.load(test_file)
        try:
            assert image.header is not None
            assert image.is_large_document is False
            assert image.is_psb is False
            assert image.layer_count == 2
            assert image.has_image_resources is True
            assert image.resource_count == 26
            assert image.has_color_mode_data is False
            assert image.has_merged_image_data is True
            assert image.compression == CompressionMethod.RLE
            assert image.image_data_kind == ImageDataKind.RLE
            assert image.uses_prediction is False
            assert image.version == 6
            assert image.header.version == PsdHeader.PSD_VERSION
            assert image.header.color_mode == image.color_mode
        finally:
            image.close()

