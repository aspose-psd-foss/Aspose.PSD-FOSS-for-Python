from aspose_psd_foss.sections.psdcolordatakind import PsdColorDataKind
from aspose_psd_foss.resources.indexedcolorpaletteinfo import IndexedColorPaletteInfo


class PsdColorDataInfo:
    """Provides a read-only summary of the PSD Color Mode Data section."""
    def __init__(self, kind, raw_data_length, indexed_palette):
        self._kind = kind
        self._raw_data_length = raw_data_length
        self._indexed_palette = indexed_palette

    @property
    def kind(self):
        """Gets the interpreted kind of the payload."""
        return self._kind

    @property
    def raw_data_length(self):
        """Gets the raw payload length in bytes."""
        return self._raw_data_length

    @property
    def indexed_palette(self):
        """Gets the parsed indexed palette, when present."""
        return self._indexed_palette
