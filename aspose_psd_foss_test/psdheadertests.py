import io
import pytest
from aspose_psd_foss.sections.psdheader import PsdHeader
from aspose_psd_foss.sections.psdcolordatakind import PsdColorDataKind
from aspose_psd_foss.colormodes import ColorModes
from aspose_psd_foss.bigendianreader import BigEndianReader
from aspose_psd_foss.coreexceptions.psdloadexception import PsdLoadException
from aspose_psd_foss_test.psdtestfixturebase import PsdTestFixtureBase


class PsdHeaderTests(PsdTestFixtureBase):
    """Tests for PsdHeader functionality."""

    def test_load_nonzeroreserved_throws(self):
        """Tests that non-zero reserved header bytes are rejected."""
        bytes_data = self.build_header_bytes(PsdHeader.PSD_VERSION)
        bytes_data[6] = 1
        stream = io.BytesIO(bytes_data)
        reader = BigEndianReader(stream, leave_open=True)

        with pytest.raises(PsdLoadException):
            PsdHeader.load(reader)

    @pytest.mark.parametrize(
        "channels,width,height,bit_depth,color_mode",
        [
            (0, 1, 1, 8, ColorModes.RGB),
            (57, 1, 1, 8, ColorModes.RGB),
            (3, 0, 1, 8, ColorModes.RGB),
            (3, 1, 0, 8, ColorModes.RGB),
            (3, 30001, 1, 8, ColorModes.RGB),
            (3, 1, 1, 12, ColorModes.RGB),
            (3, 1, 1, 8, 99),
        ],
    )
    def test_load_invalid_header_field_throws(self, channels, width, height, bit_depth, color_mode):
        """Tests that invalid PSD header field ranges are rejected at the file boundary."""
        bytes_data = self.build_header_bytes(
            PsdHeader.PSD_VERSION,
            channels,
            width,
            height,
            bit_depth,
            color_mode,
        )
        stream = io.BytesIO(bytes_data)
        reader = BigEndianReader(stream, leave_open=True)

        with pytest.raises(PsdLoadException):
            PsdHeader.load(reader)

    def test_load_psdheader_readsmetadata(self):
        """Tests that a minimal PSD without layers loads correctly."""
        bytes_data = self.build_header_bytes(PsdHeader.PSD_VERSION)
        stream = io.BytesIO(bytes_data)
        reader = BigEndianReader(stream, leave_open=True)

        header = PsdHeader.load(reader)

        assert header.version == PsdHeader.PSD_VERSION
        assert header.width == 1
        assert header.height == 1
        assert header.channels == 3
        assert header.bit_depth == 8
        assert header.color_mode == ColorModes.RGB

    def test_load_psbheader_readsmetadata(self):
        """Tests that a minimal synthetic PSB file loads expected document metadata without layers."""
        bytes_data = self.build_header_bytes(PsdHeader.PSB_VERSION)
        stream = io.BytesIO(bytes_data)
        reader = BigEndianReader(stream, leave_open=True)

        header = PsdHeader.load(reader)

        assert header.version == PsdHeader.PSB_VERSION
        assert header.is_large_document is True
        assert header.width == 1
        assert header.height == 1
        assert header.channels == 3
        assert header.bit_depth == 8
        assert header.color_mode == ColorModes.RGB

