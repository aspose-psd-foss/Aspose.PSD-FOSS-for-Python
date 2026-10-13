# Represents the standard 256-entry palette stored in indexed-color PSD documents.
class IndexedColorPalette:
    # The PSD raw payload size for a 256-color indexed palette.
    EXPECTED_RAW_LENGTH = 768

    # Initializes a new instance of the IndexedColorPalette class.
    # entries: The decoded palette entries in RGB order.
    def __init__(self, entries):
        self._entries = entries

    # Gets the decoded 256 palette entries.
    @property
    def entries(self):
        return self._entries

    # Parses a PSD indexed palette from the raw non-interleaved RGB payload.
    # raw_data: The raw 768-byte palette payload.
    # Returns: The parsed palette.
    @classmethod
    def parse(cls, raw_data):
        entries = [(raw_data[i], raw_data[i + 256], raw_data[i + 512]) for i in range(256)]
        return cls(entries)

    # Creates a read-only public summary of the indexed palette.
    # Returns: The public indexed palette summary.
    def to_public_info(self):
        from aspose_psd_foss.resources.indexedcolorpaletteinfo import IndexedColorPaletteInfo
        return IndexedColorPaletteInfo(self.entries)
