class Point:
    """Represents an ordered pair of integer x- and y-coordinates that defines a point in a two-dimensional plane."""

    empty = None  # type: Point

    def __init__(self, x=0, y=0):
        """Initializes a new instance of the Point structure with the specified coordinates.

        :param x: The x-coordinate of the point.
        :param y: The y-coordinate of the point.
        """
        self.x = x
        self.y = y

    @property
    def x(self):
        """Gets or sets the x-coordinate of this Point."""
        return self._x

    @x.setter
    def x(self, value):
        self._x = value

    @property
    def y(self):
        """Gets or sets the y-coordinate of this Point."""
        return self._y

    @y.setter
    def y(self, value):
        self._y = value

    @property
    def is_empty(self):
        """Gets a value indicating whether this Point has coordinates left uninitialized."""
        return self.x == 0 and self.y == 0

    def equals(self, other):
        """Determines whether the specified point is equal to this point.

        :param other: The point to compare.
        :return: True if the points are equal; otherwise, False.
        """
        if isinstance(other, Point):
            return self.x == other.x and self.y == other.y
        return False

    def __eq__(self, other):
        if isinstance(other, Point):
            return self.equals(other)
        return False

    def __ne__(self, other):
        return not (self == other)

    def __hash__(self):
        return hash((self.x, self.y))

    def __str__(self):
        return f"X={self.x}, Y={self.y}"


Point.empty = Point()
