import io
import os

import pytest

from aspose_psd_foss_test.psdtestfixturebase import PsdTestFixtureBase
from aspose_psd_foss.psdimage import PsdImage
from aspose_psd_foss.colormodes import ColorModes
from aspose_psd_foss.sections.colordata import ColorData
from aspose_psd_foss.sections.psdcolordatakind import PsdColorDataKind
from aspose_psd_foss.bigendianreader import BigEndianReader
from aspose_psd_foss.coreexceptions.psdloadexception import PsdLoadException


class TestColorDataTests(PsdTestFixtureBase):
    def test_load_too_long_color_mode_throws(self):
        test_path = os.path.join(
            self.test_context.current_directory,
            "testdata",
            "test.psd",
        )
        with open(test_path, "rb") as f:
            bytes_data = bytearray(f.read())
        self.write_uint32_big_endian(bytes_data, 26, 100000)
        stream = io.BytesIO(bytes_data)
        with pytest.raises(PsdLoadException):
            PsdImage.load(stream)

    def test_load_rgb_payload_classifies(self):
        payload = bytearray([0x10, 0x20, 0x30, 0x40])
        stream = io.BytesIO(self.build_color_data_section(payload))
        reader = BigEndianReader(stream, leave_open=True)
        color_data = ColorData.load(reader, ColorModes.Rgb)
        assert color_data.kind == PsdColorDataKind.RgbPayload
        assert color_data.raw_data == payload
        assert color_data.indexed_palette is None

    def test_load_indexed_data_parses_palette(self):
        payload = self.build_indexed_palette_payload()
        stream = io.BytesIO(self.build_color_data_section(payload))
        reader = BigEndianReader(stream, leave_open=True)
        color_data = ColorData.load(reader, ColorModes.Indexed)
        assert color_data.kind == PsdColorDataKind.IndexedPalette
        assert color_data.raw_data == payload
        assert color_data.indexed_palette is not None
        assert len(color_data.indexed_palette.entries) == 256
        assert color_data.indexed_palette.entries[0] == (0x00, 0xFF, 0x80)
        assert color_data.indexed_palette.entries[17] == (0x11, 0xEE, 0x91)

    def test_load_cmyk_payload_classifies(self):
        payload = bytearray([0xCA, 0xFE, 0xBA, 0xBE])
        stream = io.BytesIO(self.build_color_data_section(payload))
        reader = BigEndianReader(stream, leave_open=True)
        color_data = ColorData.load(reader, ColorModes.Cmyk)
        assert color_data.kind == PsdColorDataKind.CmykPayload
        assert color_data.raw_data == payload
        assert color_data.indexed_palette is None

    def test_load_indexed_fixture_reads_data(self):
        image = PsdImage.load(self.get_test_data_path("basic-indexed.psd"))
        assert image.width == 200
        assert image.height == 200
        assert image.channels == 1
        assert image.color_mode == ColorModes.Indexed
        assert image.has_color_mode_data is True
        assert image.color_data_info.kind == PsdColorDataKind.IndexedPalette
        assert image.color_data_info.raw_data_length == 768
        assert image.layer_count == 0
        assert image.resource_count == 24

    def test_save_indexed_fixture_is_byte_exact(self):
        self.assert_byte_exact_round_trip("basic-indexed.psd")
