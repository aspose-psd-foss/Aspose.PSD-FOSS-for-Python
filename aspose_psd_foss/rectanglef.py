from typing import Optional

class RectangleF:
    """Stores a set of four floating-point numbers that represent the location and size of a rectangle."""

    EMPTY: Optional["RectangleF"] = None

    def __init__(self, x: float = 0.0, y: float = 0.0, width: float = 0.0, height: float = 0.0):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    @property
    def bottom(self) -> float:
        return self.y + self.height

    @property
    def is_empty(self) -> bool:
        return self.x == 0 and self.y == 0 and self.width == 0 and self.height == 0

    @property
    def left(self) -> float:
        return self.x

    @property
    def right(self) -> float:
        return self.x + self.width

    @property
    def top(self) -> float:
        return self.y

    def __eq__(self, other) -> bool:
        if isinstance(other, RectangleF):
            return (
                self.x == other.x
                and self.y == other.y
                and self.width == other.width
                and self.height == other.height
            )
        return False

    def __hash__(self) -> int:
        return hash((self.x, self.y, self.width, self.height))

    def __str__(self) -> str:
        return (
            f"Left={self.left}, Top={self.top}, Right={self.right}, "
            f"Bottom={self.bottom}, Width={self.width}, Height={self.height}"
        )

    def __ne__(self, other) -> bool:
        return not self.__eq__(other)


RectangleF.EMPTY = RectangleF()

