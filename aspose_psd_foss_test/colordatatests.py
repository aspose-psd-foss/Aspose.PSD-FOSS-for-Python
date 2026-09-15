import io
import os

from src.test.psd_test_fixture_base import PsdTestFixtureBase
from src.psd_image import PsdImage
from src.big_endian_reader import BigEndianReader
from src.sections.color_data import ColorData
from src.color_modes import ColorModes
from src.sections.psd_color_data_kind import PsdColorDataKind
from src.core_exceptions.psd_load_exception import PsdLoadException


class ColorDataTests(PsdTestFixtureBase):
    """Contains ColorData tests."""

    def test_load_too_long_color_mode_throws(self):
        """Tests that a malformed color mode length field is rejected with PsdLoadException."""
        file_path = os.path.join(
            self.test_context.test_directory, "testdata", "test.psd"
        )
        bytes_ = open(file_path, "rb").read()
        self.write_uint32_big_endian(bytes_, 26, 100000)
        stream = io.BytesIO(bytes_)
        with self.assertRaises(PsdLoadException):
            PsdImage.load(stream)

    def test_load_rgb_payload_classifies(self):
        """Tests that unexpected RGB color mode data is classified explicitly and preserved."""
        payload = bytes([0x10, 0x20, 0x30, 0x40])
        stream = io.BytesIO(self.build_color_data_section(payload))
        reader = BigEndianReader(stream, leave_open=True)

        color_data = ColorData.load(reader, ColorModes.RGB)

        self.assertEqual(color_data.kind, PsdColorDataKind.RGB_PAYLOAD)
        self.assertEqual(color_data.raw_data, payload)
        self.assertIsNone(color_data.indexed_palette)

    def test_load_indexed_data_parses_palette(self):
        """Tests that indexed color mode data is parsed into a structured 256-color palette."""
        payload = self.build_indexed_palette_payload()
        stream = io.BytesIO(self.build_color_data_section(payload))
        reader = BigEndianReader(stream, leave_open=True)

        color_data = ColorData.load(reader, ColorModes.INDEXED)

        self.assertEqual(color_data.kind, PsdColorDataKind.INDEXED_PALETTE)
        self.assertEqual(color_data.raw_data, payload)
        self.assertIsNotNone(color_data.indexed_palette)
        self.assertEqual(len(color_data.indexed_palette.entries), 256)
        self.assertEqual(
            color_data.indexed_palette.entries[0],
            self.system_drawing_color_from_argb(0x00, 0xFF, 0x80),
        )
        self.assertEqual(
            color_data.indexed_palette.entries[17],
            self.system_drawing_color_from_argb(0x11, 0xEE, 0x91),
        )

    def test_load_cmyk_payload_classifies(self):
        """Tests that CMYK color mode data is classified explicitly and preserved."""
        payload = bytes([0xCA, 0xFE, 0xBA, 0xBE])
        stream = io.BytesIO(self.build_color_data_section(payload))
        reader = BigEndianReader(stream, leave_open=True)

        color_data = ColorData.load(reader, ColorModes.CMYK)

        self.assertEqual(color_data.kind, PsdColorDataKind.CMYK_PAYLOAD)
        self.assertEqual(color_data.raw_data, payload)
        self.assertIsNone(color_data.indexed_palette)

    def test_load_indexed_fixture_reads_data(self):
        """Tests that the basic indexed fixture exposes indexed color mode data and palette metadata."""
        image = PsdImage.load(self.get_test_data_path("basic-indexed.psd"))

        self.assertEqual(image.width, 200)
        self.assertEqual(image.height, 200)
        self.assertEqual(image.channels, 1)
        self.assertEqual(image.color_mode, ColorModes.INDEXED)
        self.assertTrue(image.has_color_mode_data)
        self.assertEqual(image.color_data_info.kind, PsdColorDataKind.INDEXED_PALETTE)
        self.assertEqual(image.color_data_info.raw_data_length, 768)
        self.assertEqual(image.layer_count, 0)
        self.assertEqual(image.resource_count, 24)

    def test_save_indexed_fixture_is_byte_exact(self):
        """Tests that saving the basic indexed fixture without mutations preserves the file byte-for-byte."""
        self.assert_byte_exact_round_trip("basic-indexed.psd")
