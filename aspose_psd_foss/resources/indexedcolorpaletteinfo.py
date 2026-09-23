from copy import deepcopy
from typing import List, Tuple

class IndexedColorPaletteInfo:
    """
    Provides a read-only view over an indexed-color PSD palette.
    """

    def __init__(self, entries: List[Tuple[int, int, int, int]]):
        """
        Initializes a new instance of the IndexedColorPaletteInfo class.
        """
        self._entries = deepcopy(entries)

    @property
    def entries(self) -> List[Tuple[int, int, int, int]]:
        """
        Gets the decoded palette entries.
        """
        return self._entries
