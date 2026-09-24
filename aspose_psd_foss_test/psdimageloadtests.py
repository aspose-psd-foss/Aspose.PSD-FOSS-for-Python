import os
import pytest
from io import BytesIO

from aspose_psd_foss.psdimage import PsdImage
from aspose_psd_foss.colormodes import ColorModes
from aspose_psd_foss.compressionmethod import CompressionMethod
from aspose_psd_foss.coreexceptions.psdloadexception import PsdLoadException
from aspose_psd_foss.sections.psdheader import PsdHeader
from aspose_psd_foss.bigendianreader import BigEndianReader
from aspose_psd_foss_test.nonseekablereadstream import NonSeekableReadStream
from aspose_psd_foss_test.psdtestfixturebase import PsdTestFixtureBase


class TestPsdImageLoadTests(PsdTestFixtureBase):
    """Tests for PSD image loading functionality."""

    def test_load_document_reads_properties(self):
        """Tests that loading a PSD file returns correct document properties."""
        test_file = os.path.join(self.test_dir, "testdata", "test.psd")

        assert os.path.isfile(test_file), "Test file not found"

        with PsdImage.load(test_file) as image:
            assert image.width > 0
            assert image.height > 0
            assert image.channels > 0
            assert image.bits_per_channel == 8
            assert image.color_mode == ColorModes.RGB
            assert 0 < image.version <= 6
            assert len(image.layers) > 0

    def test_load_layer_reads_properties(self):
        """Tests that loading a PSD file returns correct layer properties."""
        test_file = os.path.join(self.test_dir, "testdata", "test.psd")

        with PsdImage.load(test_file) as image:
            assert len(image.layers) > 0

            first_layer = image.layers[0]

            assert first_layer.name == "Background copy"
            assert first_layer.bounds is not None
            assert first_layer.is_visible is True
            assert 0 <= first_layer.opacity <= 255
            assert first_layer.blend_mode_key == "Normal"

            assert image.layers[1].name == "Pattern Fill 1"

    def test_load_layers_indexable(self):
        """Tests that layers can be accessed by index."""
        test_file = os.path.join(self.test_dir, "testdata", "test.psd")

        with PsdImage.load(test_file) as image:
            assert image.layers[0] is not None
            assert image.layers[1] is not None

    def test_load_seekable_preserves_position(self):
        """Tests that loading from a seekable stream preserves the original stream position."""
        with open(os.path.join(self.test_dir, "testdata", "test.psd"), "rb") as file_handle:
            bytes_content = file_handle.read()
        prefix = bytes([1, 2, 3, 4, 5])
        stream = BytesIO()
        stream.write(prefix)
        stream.write(bytes_content)
        stream.seek(len(prefix))

        with PsdImage.load(stream) as image:
            assert stream.tell() == len(prefix)
            assert image.width > 0

    def test_load_nonseekable_stream_succeeds(self):
        """Tests that loading from a non-seekable stream still succeeds."""
        with open(os.path.join(self.test_dir, "testdata", "test.psd"), "rb") as file_handle:
            bytes_content = file_handle.read()
        stream = NonSeekableReadStream(bytes_content)

        with PsdImage.load(stream) as image:
            assert image.width > 0
            assert len(image.layers) > 0

    def test_load_null_stream_throws(self):
        """Tests that loading from a null stream throws."""
        with pytest.raises(TypeError):
            PsdImage.load(None)

    def test_load_missing_file_throws(self):
        """Tests that loading a missing file path throws."""
        missing_file = os.path.join(self.test_dir, "missing.psd")
        with pytest.raises(FileNotFoundError):
            PsdImage.load(missing_file)

    def test_load_invalid_signature_throws(self):
        """Tests that loading a file with an invalid signature throws."""
        header_bytes = self._build_header_bytes(PsdHeader.PSD_VERSION)
        stream = BytesIO(header_bytes)
        stream.write(b"B")  # overwrite first byte to make signature invalid
        stream.seek(0)

        reader = BigEndianReader(stream, leave_open=True)
        with pytest.raises(PsdLoadException):
            PsdHeader.load(reader)

    def test_load_doc_inspection_reads(self):
        """Tests that simple document-level inspection properties expose the parsed structural state."""
        test_file = os.path.join(self.test_dir, "testdata", "test.psd")

        with PsdImage.load(test_file) as image:
            assert image.header is not None
            assert image.is_large_document is False
            assert image.is_psb is False
            assert image.layer_count == 2
            assert image.has_image_resources is True
            assert image.resource_count == 26
            assert image.has_color_mode_data is False
            assert image.has_merged_image_data is True
            assert image.compression == CompressionMethod.RLE
            assert image.image_data_kind == "RLE"
            assert image.uses_prediction is False
            assert image.version == 6
            assert image.header.version == PsdHeader.PSD_VERSION
            assert image.header.color_mode == image.color_mode

    @staticmethod
    def _build_header_bytes(version):
        """Helper to build a minimal valid PSD header structure as bytes."""
        signature = b"8BPS"
        version_bytes = version.to_bytes(2, byteorder="big")
        reserved = b"\x00" * 6
        channels = 1
        height = 10
        width = 10
        depth = 8
        mode = 1  # RGB

        header = (
            signature +
            version_bytes +
            reserved +
            channels.to_bytes(2, byteorder="big") +
            height.to_bytes(4, byteorder="big") +
            width.to_bytes(4, byteorder="big") +
            depth.to_bytes(2, byteorder="big") +
            mode.to_bytes(2, byteorder="big")
        )

        return header
