from __future__ import annotations

from ..bigendianreader import BigEndianReader
from ..bigendianwriter import BigEndianWriter
from ..colormodes import ColorModes
from ..psdsectionreader import read_bytes
from .psdcolordatakind import PsdColorDataKind
from .psdcolordatainfo import PsdColorDataInfo
from ..resources.indexedcolorpalette import IndexedColorPalette


class ColorData:
    """Stores the PSD Color Mode Data section as raw bytes plus mode-aware parsed structure when available."""

    EMPTY: "ColorData"

    def __init__(self, raw_data: bytes, kind: PsdColorDataKind, indexed_palette: IndexedColorPalette | None = None):
        self.raw_data = raw_data
        self.kind = kind
        self.indexed_palette = indexed_palette

    @staticmethod
    def load(reader: BigEndianReader, color_mode: ColorModes) -> "ColorData":
        length = reader.read_uint32()
        if length == 0:
            return ColorData.EMPTY

        raw_data = read_bytes(reader, length, "Color Mode Data section")
        if color_mode == ColorModes.INDEXED:
            return ColorData(raw_data, PsdColorDataKind.INDEXED_PALETTE, IndexedColorPalette.parse(raw_data))
        if color_mode == ColorModes.RGB:
            return ColorData(raw_data, PsdColorDataKind.RGB_PAYLOAD)
        if color_mode == ColorModes.CMYK:
            return ColorData(raw_data, PsdColorDataKind.CMYK_PAYLOAD)
        return ColorData(raw_data, PsdColorDataKind.RAW_PRESERVED)

    def save(self, writer: BigEndianWriter) -> None:
        writer.write_uint32(len(self.raw_data))
        if self.raw_data:
            writer.write(self.raw_data)

    def to_public_info(self) -> PsdColorDataInfo:
        return PsdColorDataInfo(
            self.kind,
            len(self.raw_data),
            self.indexed_palette.to_public_info() if self.indexed_palette else None,
        )


# Empty color data section singleton
ColorData.EMPTY = ColorData(b"", PsdColorDataKind.NONE)
