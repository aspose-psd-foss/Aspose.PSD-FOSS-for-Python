import io
import struct
from pathlib import Path

import pytest

from aspose_psd_foss.coreexceptions.argumentnullexception import ArgumentNullException
from aspose_psd_foss.coreexceptions.psdloadexception import PsdLoadException
from aspose_psd_foss.psdimage import PsdImage
from aspose_psd_foss.colormodes import ColorModes
from aspose_psd_foss.layers.blendmode import BlendMode
from aspose_psd_foss.compressionmethod import CompressionMethod
from aspose_psd_foss.bigendianreader import BigEndianReader
from aspose_psd_foss.rectangle import Rectangle
from aspose_psd_foss.sections.imagedatakind import ImageDataKind
from aspose_psd_foss.sections.psdheader import PsdHeader
from aspose_psd_foss_test.psdtestfixturebase import PsdTestFixtureBase


class TestPsdImageLoad(PsdTestFixtureBase):
    def test_load_document_readsproperties(self):
        test_file = self.get_test_data_path("test.psd")

        assert Path(test_file).exists(), "Test file not found"

        with PsdImage.load(test_file) as image:
            assert image.width > 0
            assert image.height > 0
            assert image.channels > 0
            assert image.bits_per_channel == 8
            assert image.color_mode == ColorModes.RGB
            assert 0 < image.version <= 6
            assert len(image.layers) > 0

    def test_load_layer_readsproperties(self):
        test_file = self.get_test_data_path("test.psd")

        with PsdImage.load(test_file) as image:
            assert len(image.layers) > 0

            first_layer = image.layers[0]

            assert first_layer.name == "Background copy"
            assert first_layer.bounds != Rectangle()
            assert first_layer.is_visible is True
            assert 0 <= first_layer.opacity <= 255
            assert first_layer.blend_mode_key == BlendMode.NORMAL

            assert image.layers[1].name == "Pattern Fill 1"

    def test_load_layers_indexable(self):
        test_file = self.get_test_data_path("test.psd")

        with PsdImage.load(test_file) as image:
            assert image.layers[0] is not None
            assert image.layers[1] is not None

    def test_load_seekable_preservesposition(self):
        bytes_data = Path(self.get_test_data_path("test.psd")).read_bytes()
        prefix = bytes([1, 2, 3, 4, 5])
        stream = io.BytesIO()
        stream.write(prefix)
        stream.write(bytes_data)
        stream.seek(len(prefix))

        with PsdImage.load(stream) as image:
            assert stream.tell() == len(prefix)
            assert image.width > 0

    def test_load_nonseekablestream_succeeds(self):
        bytes_data = Path(self.get_test_data_path("test.psd")).read_bytes()
        with self._non_seekable_read_stream(bytes_data) as stream:
            with PsdImage.load(stream) as image:
                assert image.width > 0
                assert len(image.layers) > 0

    def test_load_nullstream_throws(self):
        with pytest.raises(ArgumentNullException):
            PsdImage.load(None)

    def test_load_missingfile_throws(self):
        missing_file = "missing.psd"
        with pytest.raises(FileNotFoundError):
            PsdImage.load(str(missing_file))

    def test_load_invalidsignature_throws(self):
        with io.BytesIO(self._build_header_bytes(PsdHeader.PSD_VERSION)) as stream:
            with BigEndianReader(stream, leave_open=True) as reader:
                stream.seek(0)
                stream.write(b"B")
                stream.seek(0)

                with pytest.raises(PsdLoadException):
                    PsdHeader.load(reader)

    def test_load_docinspection_reads(self):
        with PsdImage.load(self.get_test_data_path("test.psd")) as image:
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

    # --- helpers ---

    @staticmethod
    def _build_header_bytes(
            version,
            channels=3,
            width=1,
            height=1,
            bit_depth=8,
            color_mode=ColorModes.RGB,
    ):
        # Big-endian: '>' prefix
        return (
                b"8BPS"
                + struct.pack(">H", version)  # ushort version
                + b"\x00" * 6  # 6 reserved bytes
                + struct.pack(">H", channels)  # ushort channels
                + struct.pack(">I", height)  # int height
                + struct.pack(">I", width)  # int width
                + struct.pack(">H", bit_depth)  # ushort bitDepth
                + struct.pack(">H", int(color_mode))  # ushort colorMode
        )

    class _non_seekable_read_stream:
        def __init__(self, data: bytes):
            self._buffer = io.BytesIO(data)

        def read(self, size: int = -1) -> bytes:
            return self._buffer.read(size)

        def __enter__(self):
            return self

        def __exit__(self, *args):
            self._buffer.close()