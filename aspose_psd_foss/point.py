from typing import Optional

# Represents an ordered pair of integer x- and y-coordinates that defines a point in a two-dimensional plane.
class Point:
    # Static readonly equivalent to C#'s Point.Empty
    Empty: Optional["Point"] = None  # will be initialized after class definition

    # Represents a Point with coordinates left uninitialized.
    @classmethod
    def empty(cls):
        return cls(0, 0)

    # Initializes a new instance of the Point structure with the specified coordinates.
    def __init__(self, x, y):
        self.x = x
        self.y = y

    # Gets a value indicating whether this Point has coordinates left uninitialized.
    @property
    def is_empty(self):
        return self.x == 0 and self.y == 0

    # Determines whether the specified point is equal to this point.
    def equals(self, other):
        return self.x == other.x and self.y == other.y

    # Determines whether the specified object is equal to this point.
    def __eq__(self, obj):
        return isinstance(obj, Point) and self.equals(obj)

    # Determines whether two points are not equal.
    def __ne__(self, obj):
        return not self.__eq__(obj)

    # Returns a hash code for this point.
    def __hash__(self):
        return hash((self.x, self.y))

    # Returns a compact coordinate representation.
    def __str__(self):
        return f"X={self.x}, Y={self.y}"

# Initialize the Empty class attribute
Point.Empty = Point(0, 0)
