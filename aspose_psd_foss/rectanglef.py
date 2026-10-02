import hashlib
from typing import Any, Optional, ClassVar


class RectangleF:
    """Stores a set of four floating-point numbers that represent the location and size of a rectangle."""

    Empty: ClassVar["RectangleF"] = RectangleF()

    def __init__(self, x: float = 0.0, y: float = 0.0, width: float = 0.0, height: float = 0.0):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    @property
    def X(self) -> float:
        """Gets or sets the x-coordinate of the upper‑left corner."""
        return self.x

    @X.setter
    def X(self, value: float) -> None:
        self.x = value

    @property
    def Y(self) -> float:
        """Gets or sets the y-coordinate of the upper‑left corner."""
        return self.y

    @Y.setter
    def Y(self, value: float) -> None:
        self.y = value

    @property
    def Width(self) -> float:
        """Gets or sets the width of the rectangle."""
        return self.width

    @Width.setter
    def Width(self, value: float) -> None:
        self.width = value

    @property
    def Height(self) -> float:
        """Gets or sets the height of the rectangle."""
        return self.height

    @Height.setter
    def Height(self, value: float) -> None:
        self.height = value

    @property
    def bottom(self) -> float:
        """Gets the y-coordinate of the bottom edge of this RectangleF."""
        return self.y + self.height

    @property
    def is_empty(self) -> bool:
        """Gets a value indicating whether this RectangleF has no location or size."""
        return self.x == 0 and self.y == 0 and self.width == 0 and self.height == 0

    @property
    def left(self) -> float:
        """Gets the x-coordinate of the left edge of this RectangleF."""
        return self.x

    @property
    def right(self) -> float:
        """Gets the x-coordinate of the right edge of this RectangleF."""
        return self.x + self.width

    @property
    def top(self) -> float:
        """Gets the y-coordinate of the top edge of this RectangleF."""
        return self.y

    def __eq__(self, other: Any) -> bool:
        """Determines whether the specified rectangle is equal to this rectangle."""
        if isinstance(other, RectangleF):
            return (
                self.x == other.x
                and self.y == other.y
                and self.width == other.width
                and self.height == other.height
            )
        return False

    def __ne__(self, other: Any) -> bool:
        """Determines whether two rectangles are not equal."""
        return not self.__eq__(other)

    def __hash__(self) -> int:
        """Returns a hash code for this rectangle."""
        return hash((self.x, self.y, self.width, self.height))

    def __str__(self) -> str:
        """Returns a compact coordinate representation."""
        return (
            f"Left={self.left}, Top={self.top}, Right={self.right}, "
            f"Bottom={self.bottom}, Width={self.width}, Height={self.height}"
        )

    @classmethod
    def empty(cls) -> "RectangleF":
        """Represents a RectangleF structure with its properties left uninitialized."""
        return cls()


# Initialize the static readonly Empty field
RectangleF.Empty = RectangleF()

