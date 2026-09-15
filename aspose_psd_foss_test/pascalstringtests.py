import io
import unittest
from aspose_psd_foss_test.psd_test_fixture_base import PsdTestFixtureBase
from aspose_psd_foss.big_endian_reader import BigEndianReader


class PascalStringTests(PsdTestFixtureBase, unittest.TestCase):
    """Contains PascalString tests."""

    def test_read_aligned2_consumes_padding(self):
        """Tests that 2-byte-aligned PSD Pascal strings consume padding even when
        the payload is empty."""
        stream = io.BytesIO(bytes([0x00, 0x00, 0x7F]))
        reader = BigEndianReader(stream, leave_open=True)

        value = reader.read_pascal_string_aligned_to_2()

        self.assertEqual(value, "")
        self.assertEqual(reader.position, 2)
        self.assertEqual(reader.read_byte(), 0x7F)

    def test_read_aligned4_consumes_padding(self):
        """Tests that 4-byte-aligned PSD Pascal strings consume padding even when
        the payload is empty."""
        stream = io.BytesIO(bytes([0x00, 0x00, 0x00, 0x00, 0x7F]))
        reader = BigEndianReader(stream, leave_open=True)

        value = reader.read_pascal_string_aligned_to_4()

        self.assertEqual(value, "")
        self.assertEqual(reader.position, 4)
        self.assertEqual(reader.read_byte(), 0x7F)
