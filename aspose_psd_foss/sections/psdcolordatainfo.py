# Provides a read-only summary of the PSD Color Mode Data section.
from typing import Optional

from aspose_psd_foss.sections.psdcolordatakind import PsdColorDataKind
from aspose_psd_foss.resources.indexedcolorpaletteinfo import IndexedColorPaletteInfo


class PsdColorDataInfo:
    """Provides a read-only summary of the PSD Color Mode Data section."""

    def __init__(
        self,
        kind: PsdColorDataKind,
        raw_data_length: int,
        indexed_palette: Optional[IndexedColorPaletteInfo] = None,
    ):
        """
        Initializes a new instance of the PsdColorDataInfo class.

        :param kind: The interpreted kind of the payload.
        :param raw_data_length: The raw payload length in bytes.
        :param indexed_palette: The parsed indexed palette, when present.
        """
        self._kind = kind
        self._raw_data_length = raw_data_length
        self._indexed_palette = indexed_palette

    @property
    def kind(self) -> PsdColorDataKind:
        """Gets the interpreted kind of the payload."""
        return self._kind

    @property
    def raw_data_length(self) -> int:
        """Gets the raw payload length in bytes."""
        return self._raw_data_length

    @property
    def indexed_palette(self) -> Optional[IndexedColorPaletteInfo]:
        """Gets the parsed indexed palette, when present."""
        return self._indexed_palette
