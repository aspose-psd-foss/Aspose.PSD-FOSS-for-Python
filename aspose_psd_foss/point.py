from typing import Optional

# Represents an ordered pair of integer x- and y-coordinates that defines a point in a two-dimensional plane.
class Point:
    """Represents an ordered pair of integer x- and y-coordinates that defines a point in a two-dimensional plane."""

    EMPTY: Optional['Point'] = None  # will be set after class definition

    def __init__(self, x: int = 0, y: int = 0):
        """Initializes a new instance of the Point structure with the specified coordinates."""
        self.x = x
        self.y = y

    @property
    def x(self) -> int:
        """Gets or sets the x-coordinate of this Point."""
        return self._x

    @x.setter
    def x(self, value: int):
        self._x = value

    @property
    def y(self) -> int:
        """Gets or sets the y-coordinate of this Point."""
        return self._y

    @y.setter
    def y(self, value: int):
        self._y = value

    @property
    def is_empty(self) -> bool:
        """Gets a value indicating whether this Point has coordinates left uninitialized."""
        return self.x == 0 and self.y == 0

    def __eq__(self, other):
        """Determines whether the specified point is equal to this point."""
        if isinstance(other, Point):
            return self.x == other.x and self.y == other.y
        return False

    def __hash__(self):
        """Returns a hash code for this point."""
        return hash((self.x, self.y))

    def __str__(self):
        """Returns a compact coordinate representation."""
        return f"X={self.x}, Y={self.y}"

    def __repr__(self):
        return f"Point({self.x}, {self.y})"

    def __ne__(self, other):
        """Determines whether two points are not equal."""
        return not self.__eq__(other)


# Initialize the static EMPTY field
Point.EMPTY = Point()

