from aspose_psd_foss.sections.psdcolordatakind import PsdColorDataKind
from aspose_psd_foss.colormodes import ColorModes
from aspose_psd_foss.sections.psdcolordatainfo import PsdColorDataInfo
from aspose_psd_foss.resources.indexedcolorpalette import IndexedColorPalette
from aspose_psd_foss.psdsectionreader import PsdSectionReader
from aspose_psd_foss.bigendianreader import BigEndianReader
from aspose_psd_foss.bigendianwriter import BigEndianWriter


class ColorData:
    """
    Stores the PSD Color Mode Data section as raw bytes plus mode-aware parsed structure when available.
    """

    _empty = None

    def __init__(self, raw_data, kind, indexed_palette=None):
        """
        Initializes a new instance of the ColorData class.

        :param raw_data: The raw color mode data payload.
        :param kind: The public semantic interpretation of the payload.
        :param indexed_palette: The parsed indexed palette, when present.
        """
        self._raw_data = raw_data
        self._kind = kind
        self._indexed_palette = indexed_palette

    @property
    def kind(self):
        """
        Gets the semantic interpretation applied to the raw color mode payload.
        """
        return self._kind

    @property
    def raw_data(self):
        """
        Gets the raw color mode data payload.
        """
        return self._raw_data

    @property
    def indexed_palette(self):
        """
        Gets the parsed indexed color palette when the payload represents a standard PSD indexed palette.
        """
        return self._indexed_palette

    @classmethod
    def empty(cls):
        """
        Gets an empty color data section.
        """
        if cls._empty is None:
            cls._empty = cls([], PsdColorDataKind.EMPTY)
        return cls._empty

    @classmethod
    def load(cls, reader, color_mode):
        """
        Loads the Color Mode Data section from the reader.

        :param reader: The reader positioned at the section length field.
        :param color_mode: The color mode declared in the PSD header.
        :return: The loaded ColorData instance.
        """
        length = reader.read_uint32()
        if length == 0:
            return cls.empty()

        raw_data = PsdSectionReader.read_bytes(reader, length, "Color Mode Data section")
        if color_mode == ColorModes.INDEXED and len(raw_data) == IndexedColorPalette.expected_raw_length:
            return cls(raw_data, PsdColorDataKind.INDEXED_PALETTE, IndexedColorPalette.parse(raw_data))
        elif color_mode == ColorModes.RGB:
            return cls(raw_data, PsdColorDataKind.RGB_PAYLOAD)
        elif color_mode == ColorModes.CMYK:
            return cls(raw_data, PsdColorDataKind.CMYK_PAYLOAD)
        else:
            return cls(raw_data, PsdColorDataKind.RAW_PRESERVED)

    def save(self, writer):
        """
        Writes the Color Mode Data section to the writer.

        :param writer: The destination writer.
        """
        writer.write_uint32(len(self._raw_data))
        if len(self._raw_data) > 0:
            writer.write_bytes(self._raw_data)

    def to_public_info(self):
        """
        Creates a read-only public summary for the current Color Mode Data section.

        :return: The public color data summary.
        """
        palette_info = self._indexed_palette.to_public_info() if self._indexed_palette is not None else None
        return PsdColorDataInfo(self._kind, len(self._raw_data), palette_info)

Empty = ColorData.empty()

