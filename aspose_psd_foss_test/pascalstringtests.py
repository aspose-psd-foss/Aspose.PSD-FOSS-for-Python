import io

from aspose_psd_foss_test.psdtestfixturebase import PsdTestFixtureBase
from aspose_psd_foss.bigendianreader import BigEndianReader


class TestPascalString(PsdTestFixtureBase):
    def test_read_aligned2_consumes_padding(self):
        stream = io.BytesIO(bytes([0x00, 0x00, 0x7F]))
        reader = BigEndianReader(stream, leave_open=True)

        value = reader.read_pascal_string_aligned_to2()

        assert value == ''
        assert reader.position == 2
        assert reader.read_byte() == 0x7F

    def test_read_aligned4_consumes_padding(self):
        stream = io.BytesIO(bytes([0x00, 0x00, 0x00, 0x00, 0x7F]))
        reader = BigEndianReader(stream, leave_open=True)

        value = reader.read_pascal_string_aligned_to4()

        assert value == ''
        assert reader.position == 4
        assert reader.read_byte() == 0x7F
