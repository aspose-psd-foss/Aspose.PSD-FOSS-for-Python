import io

import pytest

from aspose_psd_foss.bigendianreader import BigEndianReader
from aspose_psd_foss_test.psdtestfixturebase import PsdTestFixtureBase


class PascalStringTests(PsdTestFixtureBase):
    """Contains PascalString tests."""

    def test_read_aligned2_consumes_padding(self):
        """Tests that 2-byte-aligned PSD Pascal strings consume padding even when the payload is empty."""
        stream = io.BytesIO(bytes([0x00, 0x00, 0x7F]))
        reader = BigEndianReader(stream, leave_open=True)

        value = reader.read_pascal_string_aligned_to_2()

        assert value == ''
        assert reader.position == 2
        assert reader.read_byte() == 0x7F

    def test_read_aligned4_consumes_padding(self):
        """Tests that 4-byte-aligned PSD Pascal strings consume padding even when the payload is empty."""
        stream = io.BytesIO(bytes([0x00, 0x00, 0x00, 0x00, 0x7F]))
        reader = BigEndianReader(stream, leave_open=True)

        value = reader.read_pascal_string_aligned_to_4()

        assert value == ''
        assert reader.position == 4
        assert reader.read_byte() == 0x7F
