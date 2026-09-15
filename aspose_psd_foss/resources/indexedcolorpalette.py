from __future__ import annotations

from aspose_psd_foss.indexedcolorpaletteinfo import IndexedColorPaletteInfo


class IndexedColorPalette:
    """
    Represents the standard 256-entry palette stored in indexed-color PSD documents.
    """

    EXPECTED_RAW_LENGTH = 768

    def __init__(self, entries):
        """
        Initializes a new instance of the IndexedColorPalette class.

        :param entries: The decoded palette entries in RGB order.
        """
        self._entries = entries

    @property
    def entries(self):
        """
        Gets the decoded 256 palette entries.
        """
        return self._entries

    @staticmethod
    def parse(raw_data):
        """
        Parses a PSD indexed palette from the raw non-interleaved RGB payload.

        :param raw_data: The raw 768-byte palette payload.
        :return: The parsed palette.
        """
        entries = [
            (raw_data[i], raw_data[i + 256], raw_data[i + 512])
            for i in range(256)
        ]
        return IndexedColorPalette(entries)

    def to_public_info(self):
        """
        Creates a read-only public summary of the indexed palette.

        :return: The public indexed palette summary.
        """
        return IndexedColorPaletteInfo(self.entries)
