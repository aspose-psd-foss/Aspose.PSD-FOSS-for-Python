from aspose_psd_foss.resources.indexedcolorpaletteinfo import IndexedColorPaletteInfo


class IndexedColorPalette:
    EXPECTED_RAW_LENGTH = 768

    def __init__(self, entries):
        self._entries = entries

    @property
    def entries(self):
        return self._entries

    @staticmethod
    def parse(raw_data):
        entries = [(raw_data[i], raw_data[i + 256], raw_data[i + 512]) for i in range(256)]
        return IndexedColorPalette(entries)

    def to_public_info(self):
        return IndexedColorPaletteInfo(self.entries)
