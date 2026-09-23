class IndexedColorPalette:
    """Represents the standard 256-entry palette stored in indexed-color PSD documents."""

    # The PSD raw payload size for a 256-color indexed palette.
    EXPECTED_RAW_LENGTH = 768

    def __init__(self, entries):
        """
        Initializes a new instance of the IndexedColorPalette class.

        :param entries: The decoded palette entries in RGB order.
        """
        self.entries = entries

    @classmethod
    def parse(cls, raw_data):
        """
        Parses a PSD indexed palette from the raw non-interleaved RGB payload.

        :param raw_data: The raw 768-byte palette payload.
        :return: The parsed palette.
        """
        entries = [None] * 256
        for i in range(len(entries)):
            from aspose_psd_foss.colormodes import Color
            entries[i] = Color.from_argb(raw_data[i], raw_data[i + 256], raw_data[i + 512])
        return cls(entries)

    def to_public_info(self):
        """
        Creates a read-only public summary of the indexed palette.

        :return: The public indexed palette summary.
        """
        from aspose_psd_foss.resources.indexedcolorpaletteinfo import IndexedColorPaletteInfo
        return IndexedColorPaletteInfo(self.entries)
