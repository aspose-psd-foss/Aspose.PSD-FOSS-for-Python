import pytest
from pathlib import Path

from aspose_psd_foss.coreexceptions.psdloadexception import PsdLoadException
from aspose_psd_foss.psdimage import PsdImage
from aspose_psd_foss.colormodes import ColorModes
from aspose_psd_foss.bigendianreader import BigEndianReader
from aspose_psd_foss.sections.colordata import ColorData
from aspose_psd_foss.sections.psdcolordatakind import PsdColorDataKind
from aspose_psd_foss_test.psdtestfixturebase import PsdTestFixtureBase

import struct


class TestColorData(PsdTestFixtureBase):
    def test_load_toolongcolormode_throws(self):
        bytes_data = bytearray(
            Path(self.get_test_data_path("test.psd")).read_bytes()
        )
        self._write_uint32_big_endian(bytes_data, 26, 100000)

        with pytest.raises(PsdLoadException):
            with self._memory_stream(bytes_data) as stream:
                PsdImage.load(stream)

    def test_load_rgbpayload_classifies(self):
        payload = bytes([0x10, 0x20, 0x30, 0x40])
        with self._memory_stream(self._build_color_data_section(payload)) as stream:
            with BigEndianReader(stream, leave_open=True) as reader:
                color_data = ColorData.load(reader, ColorModes.RGB)

                assert color_data.kind == PsdColorDataKind.RGB_PAYLOAD
                assert color_data.raw_data == payload
                assert color_data.indexed_palette is None

    def test_load_indexeddata_parsespalette(self):
        payload = self._build_indexed_palette_payload()
        with self._memory_stream(self._build_color_data_section(payload)) as stream:
            with BigEndianReader(stream, leave_open=True) as reader:
                color_data = ColorData.load(reader, ColorModes.INDEXED)

                assert color_data.kind == PsdColorDataKind.INDEXED_PALETTE
                assert color_data.raw_data == payload
                assert color_data.indexed_palette is not None
                assert len(color_data.indexed_palette.entries) == 256
                assert color_data.indexed_palette.entries[0] == (0x00, 0xFF, 0x80)
                assert color_data.indexed_palette.entries[17] == (0x11, 0xEE, 0x91)

    def test_load_cmykpayload_classifies(self):
        payload = bytes([0xCA, 0xFE, 0xBA, 0xBE])
        with self._memory_stream(self._build_color_data_section(payload)) as stream:
            with BigEndianReader(stream, leave_open=True) as reader:
                color_data = ColorData.load(reader, ColorModes.CMYK)

                assert color_data.kind == PsdColorDataKind.CMYK_PAYLOAD
                assert color_data.raw_data == payload
                assert color_data.indexed_palette is None

    def test_load_indexedfixture_readsdata(self):
        with PsdImage.load(self.get_test_data_path("basic-indexed.psd")) as image:
            assert image.width == 200
            assert image.height == 200
            assert image.channels == 1
            assert image.color_mode == ColorModes.INDEXED
            assert image.has_color_mode_data is True
            assert image.color_data_info.kind == PsdColorDataKind.INDEXED_PALETTE
            assert image.color_data_info.raw_data_length == 768
            assert image.layer_count == 0
            assert image.resource_count == 24

    def test_save_indexedfixture_isbyteexact(self):
        self.assert_byte_exact_round_trip("basic-indexed.psd")

    # --- helpers ---

    @staticmethod
    def _write_uint32_big_endian(data: bytearray, offset: int, value: int) -> None:
        data[offset : offset + 4] = struct.pack(">I", value)

    @staticmethod
    def _memory_stream(data: bytes):
        import io

        return io.BytesIO(data)

    @staticmethod
    def _build_color_data_section(payload: bytes) -> bytes:
        return struct.pack(">I", len(payload)) + payload

    @staticmethod
    def _build_indexed_palette_payload() -> bytes:
        payload = bytearray(768)
        # Entry 0: RGB (0x00, 0xFF, 0x80)
        payload[0] = 0x00
        payload[1] = 0xFF
        payload[2] = 0x80
        # Entry 17: RGB (0x11, 0xEE, 0x91)
        payload[17 * 3] = 0x11
        payload[17 * 3 + 1] = 0xEE
        payload[17 * 3 + 2] = 0x91
        return bytes(payload)