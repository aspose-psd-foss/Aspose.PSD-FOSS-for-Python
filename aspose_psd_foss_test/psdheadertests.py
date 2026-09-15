import aspose_psd_foss.file_formats.psd
import sys
import unittest
import io

from aspose_psd_foss_test.psd_test_fixture_base import PsdTestFixtureBase
from aspose_psd_foss.sections.psd_header import PsdHeader
from aspose_psd_foss.big_endian_reader import BigEndianReader
from aspose_psd_foss.core_exceptions.psd_load_exception import PsdLoadException
from aspose_psd_foss.color_modes import ColorModes


class PsdHeaderTests(PsdTestFixtureBase):
    """Contains PSD Header tests."""

    def test_load_nonzero_reserved_throws(self):
        """Tests that non-zero reserved header bytes are rejected."""
        bytes_ = self.build_header_bytes(PsdHeader.PSD_VERSION)
        bytes_[6] = 1
        stream = io.BytesIO(bytes_)
        reader = BigEndianReader(stream, leave_open=True)

        with self.assertRaises(PsdLoadException):
            PsdHeader.load(reader)

    def test_load_invalid_header_field_throws(self):
        """Tests that invalid PSD header field ranges are rejected at the file boundary."""
        test_cases = [
            (0, 1, 1, 8, int(ColorModes.RGB)),
            (57, 1, 1, 8, int(ColorModes.RGB)),
            (3, 0, 1, 8, int(ColorModes.RGB)),
            (3, 1, 0, 8, int(ColorModes.RGB)),
            (3, 30001, 1, 8, int(ColorModes.RGB)),
            (3, 1, 1, 12, int(ColorModes.RGB)),
            (3, 1, 1, 8, 99)
        ]

        for channels, width, height, bit_depth, color_mode in test_cases:
            with self.subTest(
                channels=channels,
                width=width,
                height=height,
                bit_depth=bit_depth,
                color_mode=color_mode,
            ):
                bytes_ = self.build_header_bytes(
                    PsdHeader.PSD_VERSION,
                    channels=channels,
                    width=width,
                    height=height,
                    bit_depth=bit_depth,
                    color_mode=ColorModes(color_mode),
                )
                stream = io.BytesIO(bytes_)
                reader = BigEndianReader(stream, leave_open=True)

                with self.assertRaises(PsdLoadException):
                    PsdHeader.load(reader)

    def test_load_psd_header_reads_metadata(self):
        """Tests that a minimal PSD without layers loads correctly."""
        stream = io.BytesIO(self.build_header_bytes(PsdHeader.PSD_VERSION))
        reader = BigEndianReader(stream, leave_open=True)

        header = PsdHeader.load(reader)

        self.assertEqual(header.version, PsdHeader.PSD_VERSION)
        self.assertEqual(header.width, 1)
        self.assertEqual(header.height, 1)
        self.assertEqual(header.channels, 3)
        self.assertEqual(header.bit_depth, 8)
        self.assertEqual(header.color_mode, ColorModes.RGB)

    def test_load_psb_header_reads_metadata(self):
        """Tests that a minimal synthetic PSB file loads expected document metadata without layers."""
        stream = io.BytesIO(self.build_header_bytes(PsdHeader.PSB_VERSION))
        reader = BigEndianReader(stream, leave_open=True)

        header = PsdHeader.load(reader)

        self.assertEqual(header.version, PsdHeader.PSB_VERSION)
        self.assertTrue(header.is_large_document)
        self.assertEqual(header.width, 1)
        self.assertEqual(header.height, 1)
        self.assertEqual(header.channels, 3)
