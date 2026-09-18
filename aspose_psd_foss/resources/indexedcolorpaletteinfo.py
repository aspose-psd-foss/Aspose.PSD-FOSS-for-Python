from typing import Tuple, Any


class IndexedColorPaletteInfo:
    def __init__(self, entries: Tuple[Any, ...]):
        self._entries: Tuple[Any, ...] = tuple(entries)

    @property
    def entries(self) -> Tuple[Any, ...]:
        return self._entries
