"""Stores the PSD Color Mode Data section as raw bytes plus mode-aware parsed
structure when available."""
from aspose_psd_foss.bigendianreader import BigEndianReader
from aspose_psd_foss.bigendianwriter import BigEndianWriter
from aspose_psd_foss.colormodes import ColorModes
from aspose_psd_foss.psdsectionreader import PsdSectionReader
from aspose_psd_foss.resources.indexedcolorpalette import IndexedColorPalette
from aspose_psd_foss.sections.psdcolordatainfo import PsdColorDataInfo
from aspose_psd_foss.sections.psdcolordatakind import PsdColorDataKind


class ColorData:
    """Stores the PSD Color Mode Data section as raw bytes plus mode-aware
    parsed structure when available."""

    #: An empty color data section.
    Empty = None  # will be initialized after the class definition

    def __init__(
        self,
        raw_data: bytes,
        kind: PsdColorDataKind,
        indexed_palette: IndexedColorPalette = None,
    ):
        """
        Initializes a new instance of the ColorData class.

        :param raw_data: The raw color mode data payload.
        :param kind: The public semantic interpretation of the payload.
        :param indexed_palette: The parsed indexed palette, when present.
        """
        self.raw_data = raw_data
        self.kind = kind
        self.indexed_palette = indexed_palette

    @staticmethod
    def load(reader: BigEndianReader, color_mode: ColorModes) -> "ColorData":
        """
        Loads the Color Mode Data section from the reader.

        :param reader: The reader positioned at the section length field.
        :param color_mode: The color mode declared in the PSD header.
        :return: The loaded ColorData instance.
        """
        length = reader.read_uint32()
        if length == 0:
            return ColorData.Empty

        raw_data = PsdSectionReader.read_bytes(
            reader, length, "Color Mode Data section"
        )

        if (
            color_mode == ColorModes.INDEXED
            and len(raw_data) == IndexedColorPalette.EXPECTED_RAW_LENGTH
        ):
            return ColorData(
                raw_data,
                PsdColorDataKind.INDEXED_PALETTE,
                IndexedColorPalette.parse(raw_data),
            )
        if color_mode == ColorModes.RGB:
            return ColorData(raw_data, PsdColorDataKind.RGB_PAYLOAD)
        if color_mode == ColorModes.CMYK:
            return ColorData(raw_data, PsdColorDataKind.CMYK_PAYLOAD)

        return ColorData(raw_data, PsdColorDataKind.RAW_PRESERVED)

    def save(self, writer: BigEndianWriter):
        """
        Writes the Color Mode Data section to the writer.

        :param writer: The destination writer.
        """
        writer.write_uint32(len(self.raw_data))
        if len(self.raw_data) > 0:
            writer.write(self.raw_data)

    def to_public_info(self) -> PsdColorDataInfo:
        """
        Creates a read‑only public summary for the current Color Mode Data
        section.

        :return: The public color data summary.
        """
        palette_info = (
            self.indexed_palette.to_public_info()
            if self.indexed_palette
            else None
        )
        return PsdColorDataInfo(self.kind, len(self.raw_data), palette_info)


# Initialize the static Empty instance
ColorData.Empty = ColorData(b"", PsdColorDataKind.NONE)
