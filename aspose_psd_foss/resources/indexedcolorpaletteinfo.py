# Provides a read‑only view over an indexed‑color PSD palette.


class IndexedColorPaletteInfo:
    """Provides a read‑only view over an indexed‑color PSD palette."""

    def __init__(self, entries):
        """Initializes a new instance of the IndexedColorPaletteInfo class.

        Args:
            entries: The decoded palette entries.
        """
        self._entries = tuple(entries)

    @property
    def entries(self):
        """Gets the decoded palette entries."""
        return self._entries
