from typing import Optional

from aspose_psd_foss.bigendianreader import BigEndianReader
from aspose_psd_foss.bigendianwriter import BigEndianWriter
from aspose_psd_foss.psdsectionreader import PsdSectionReader
from aspose_psd_foss.colormodes import ColorModes
from aspose_psd_foss.sections.psdcolordatakind import PsdColorDataKind
from aspose_psd_foss.sections.psdcolordatainfo import PsdColorDataInfo
from aspose_psd_foss.resources.indexedcolorpalette import IndexedColorPalette


class ColorData:
    """Stores the PSD Color Mode Data section as raw bytes plus mode‑aware parsed
    structure when available.
    """

    def __init__(
        self,
        raw_data: bytes,
        kind: PsdColorDataKind,
        indexed_palette: Optional[IndexedColorPalette] = None,
    ) -> None:
        self._raw_data = raw_data
        self._kind = kind
        self._indexed_palette = indexed_palette

    @property
    def kind(self) -> PsdColorDataKind:
        return self._kind

    @property
    def raw_data(self) -> bytes:
        return self._raw_data

    @property
    def indexed_palette(self) -> Optional[IndexedColorPalette]:
        return self._indexed_palette

    @classmethod
    def empty(cls) -> "ColorData":
        return cls(b"", PsdColorDataKind.NONE)

    @classmethod
    def load(cls, reader: BigEndianReader, color_mode: ColorModes) -> "ColorData":
        length = reader.read_uint32()
        if length == 0:
            return cls.empty()
        raw_data = PsdSectionReader.read_bytes(
            reader, length, "Color Mode Data section"
        )
        if (
            color_mode == ColorModes.INDEXED
            and len(raw_data) == IndexedColorPalette.EXPECTED_RAW_LENGTH
        ):
            indexed_pal = IndexedColorPalette.parse(raw_data)
            return cls(raw_data, PsdColorDataKind.INDEXED_PALETTE, indexed_pal)
        if color_mode == ColorModes.RGB:
            return cls(raw_data, PsdColorDataKind.RGB_PAYLOAD)
        if color_mode == ColorModes.CMYK:
            return cls(raw_data, PsdColorDataKind.CMYK_PAYLOAD)
        return cls(raw_data, PsdColorDataKind.RAW_PRESERVED)

    def save(self, writer: BigEndianWriter) -> None:
        writer.write_uint(len(self._raw_data))
        if len(self._raw_data) > 0:
            writer.write(self._raw_data)

    def to_public_info(self) -> PsdColorDataInfo:
        indexed_info = (
            self._indexed_palette.to_public_info()
            if self._indexed_palette is not None
            else None
        )
        return PsdColorDataInfo(self._kind, len(self._raw_data), indexed_info)
