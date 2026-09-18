import io
import os

import pytest

from aspose_psd_foss.bigendianreader import BigEndianReader
from aspose_psd_foss.colormodes import ColorModes
from aspose_psd_foss.coreexceptions.psdloadexception import PsdLoadException
from aspose_psd_foss.psdimage import PsdImage
from aspose_psd_foss.sections.colordata import ColorData
from aspose_psd_foss.sections.psdcolordatakind import PsdColorDataKind
from aspose_psd_foss_test.psdtestfixturebase import PsdTestFixtureBase


class TestColorData(PsdTestFixtureBase):
    """Contains ColorData tests."""

    def test_load_too_long_color_mode_throws(self):
        """Tests that a malformed color mode length field is rejected with PsdLoadException."""
        file_path = os.path.join(
            os.getcwd(), "testdata", "test.psd"
        )
        with open(file_path, "rb") as f:
            bytes_ = bytearray(f.read())
        self.write_uint32_big_endian(bytes_, 26, 100000)
        stream = io.BytesIO(bytes_)
        stream.seek(0)
        with pytest.raises(PsdLoadException):
            PsdImage.load_from_stream(stream)

    def test_load_rgb_payload_classifies(self):
        """Tests that unexpected RGB color mode data is classified explicitly and preserved."""
        payload = bytes([0x10, 0x20, 0x30, 0x40])
        stream = io.BytesIO(self.build_color_data_section(payload))
        reader = BigEndianReader(stream, leave_open=True)

        color_data = ColorData.load(reader, ColorModes.RGB)

        assert color_data.kind == PsdColorDataKind.RGB_PAYLOAD
        assert color_data.raw_data == payload
        assert color_data.indexed_palette is None

    def test_load_indexed_data_parses_palette(self):
        """Tests that indexed color mode data is parsed into a structured 256-color palette."""
        payload = self.build_indexed_palette_payload()
        stream = io.BytesIO(self.build_color_data_section(payload))
        reader = BigEndianReader(stream, leave_open=True)

        color_data = ColorData.load(reader, ColorModes.INDEXED)

        assert color_data.kind == PsdColorDataKind.INDEXED_PALETTE
        assert color_data.raw_data == payload
        assert color_data.indexed_palette is not None
        assert len(color_data.indexed_palette.entries) == 256
        assert (
            color_data.indexed_palette.entries[0]
            == self.system_drawing_color_from_argb(0x00, 0xFF, 0x80)
        )
        assert (
            color_data.indexed_palette.entries[17]
            == self.system_drawing_color_from_argb(0x11, 0xEE, 0x91)
        )

    def test_load_cmyk_payload_classifies(self):
        """Tests that CMYK color mode data is classified explicitly and preserved."""
        payload = bytes([0xCA, 0xFE, 0xBA, 0xBE])
        stream = io.BytesIO(self.build_color_data_section(payload))
        reader = BigEndianReader(stream, leave_open=True)

        color_data = ColorData.load(reader, ColorModes.CMYK)

        assert color_data.kind == PsdColorDataKind.CMYK_PAYLOAD
        assert color_data.raw_data == payload
        assert color_data.indexed_palette is None

    def test_load_indexed_fixture_reads_data(self):
        """Tests that the basic indexed fixture exposes indexed color mode data and palette metadata."""
        image = PsdImage.load(self.get_test_data_path("basic-indexed.psd"))

        assert image.width == 200
        assert image.height == 200
        assert image.channels == 1
        assert image.color_mode == ColorModes.INDEXED
        assert image.has_color_mode_data
        assert image.color_data_info.kind == PsdColorDataKind.INDEXED_PALETTE
        assert image.color_data_info.raw_data_length == 768
        assert image.layer_count == 0
        assert image.resource_count == 24

    def test_save_indexed_fixture_is_byte_exact(self):
        """Tests that saving the basic indexed fixture without mutations preserves the file byte-for-byte."""
        self.assert_byte_exact_round_trip("basic-indexed.psd")