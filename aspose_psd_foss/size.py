from typing import Optional

class Size:
    Empty: Optional["Size"] = None

    @classmethod
    def empty(cls):
        return cls()

    def __init__(self, width: int = 0, height: int = 0):
        self.width = width
        self.height = height

    @property
    def is_empty(self) -> bool:
        return self.width == 0 and self.height == 0

    @property
    def IsEmpty(self) -> bool:
        return self.is_empty

    def equals(self, other) -> bool:
        return isinstance(other, Size) and self.width == other.width and self.height == other.height

    def __eq__(self, obj) -> bool:
        return self.equals(obj)

    def __hash__(self) -> int:
        return hash((self.width, self.height))

    def __str__(self) -> str:
        return f"{{Width={self.width}, Height={self.height}}}"

    def __ne__(self, other) -> bool:
        return not self.__eq__(other)

Size.Empty = Size()
