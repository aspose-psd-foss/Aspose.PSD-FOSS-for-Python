from .point import Point
from .size import Size

class Rectangle:
    """Stores a set of four integers that represent the location and size of a rectangle."""

    Empty = None  # type: Rectangle

    def __init__(self, x=None, y=None, width=None, height=None):
        """
        Initializes a new instance of the Rectangle structure.

        Args:
            x: The left coordinate or Point instance for location.
            y: The top coordinate (if x is int) or Size instance for size (if x is int).
            width: The rectangle width (only used if x and y are int).
            height: The rectangle height (only used if x and y are int).
        """
        if isinstance(x, Point) and isinstance(y, Size):
            self._x = x.x
            self._y = y.y
            self._width = y.width
            self._height = y.height
        else:
            self._x = 0 if x is None else x
            self._y = 0 if y is None else y
            self._width = 0 if width is None else width
            self._height = 0 if height is None else height

    @property
    def x(self):
        """Gets or sets the x-coordinate of the upper-left corner of this Rectangle."""
        return self._x

    @x.setter
    def x(self, value):
        self._x = value

    @property
    def y(self):
        """Gets or sets the y-coordinate of the upper-left corner of this Rectangle."""
        return self._y

    @y.setter
    def y(self, value):
        self._y = value

    @property
    def width(self):
        """Gets or sets the width of this Rectangle."""
        return self._width

    @width.setter
    def width(self, value):
        self._width = value

    @property
    def height(self):
        """Gets or sets the height of this Rectangle."""
        return self._height

    @height.setter
    def height(self, value):
        self._height = value

    @property
    def bottom(self):
        """Gets or sets the y-coordinate of the bottom edge of this Rectangle."""
        return self.y + self.height

    @bottom.setter
    def bottom(self, value):
        self.height = value - self.y

    @property
    def is_empty(self):
        """Gets a value indicating whether this Rectangle has no location or size."""
        return self.x == 0 and self.y == 0 and self.width == 0 and self.height == 0

    @property
    def left(self):
        """Gets or sets the x-coordinate of the left edge of this Rectangle."""
        return self.x

    @left.setter
    def left(self, value):
        right = self.right
        self.x = value
        self.width = right - value

    @property
    def location(self):
        """Gets or sets the coordinates of the upper-left corner of this Rectangle."""
        from .point import Point
        return Point(self.x, self.y)

    @location.setter
    def location(self, value):
        self.x = value.x
        self.y = value.y

    @property
    def right(self):
        """Gets or sets the x-coordinate of the right edge of this Rectangle."""
        return self.x + self.width

    @right.setter
    def right(self, value):
        self.width = value - self.x

    @property
    def size(self):
        """Gets or sets the size of this Rectangle."""
        from .size import Size
        return Size(self.width, self.height)

    @size.setter
    def size(self, value):
        self.width = value.width
        self.height = value.height

    @property
    def top(self):
        """Gets or sets the y-coordinate of the top edge of this Rectangle."""
        return self.y

    @top.setter
    def top(self, value):
        bottom = self.bottom
        self.y = value
        self.height = bottom - value

    @classmethod
    def ceiling(cls, value):
        """Converts a RectangleF structure to a Rectangle structure by rounding up the coordinates and size."""
        import math
        return cls(
            int(math.ceil(value.x)),
            int(math.ceil(value.y)),
            int(math.ceil(value.width)),
            int(math.ceil(value.height))
        )

    @classmethod
    def from_left_top_right_bottom(cls, left, top, right, bottom):
        """Creates a rectangle from edge coordinates."""
        return cls(left, top, right - left, bottom - top)

    @classmethod
    def from_ltrb(cls, left, top, right, bottom):
        """Creates a rectangle from edge coordinates for internal PSD record parsing."""
        return cls.from_left_top_right_bottom(left, top, right, bottom)

    @classmethod
    def from_points(cls, point1, point2):
        """Creates a rectangle that spans the specified points."""
        left = min(point1.x, point2.x)
        top = min(point1.y, point2.y)
        right = max(point1.x, point2.x)
        bottom = max(point1.y, point2.y)
        return cls.from_left_top_right_bottom(left, top, right, bottom)

    @classmethod
    def inflate_rect(cls, rectangle, x, y):
        """Inflates the specified rectangle by the given amounts."""
        result = Rectangle(rectangle.x, rectangle.y, rectangle.width, rectangle.height)
        result._inflate_impl(x, y)
        return result

    @classmethod
    def intersect_rect(cls, a, b):
        """Returns a rectangle that represents the intersection of two rectangles."""
        left = max(a.left, b.left)
        top = max(a.top, b.top)
        right = min(a.right, b.right)
        bottom = min(a.bottom, b.bottom)

        if right > left and bottom > top:
            return cls.from_left_top_right_bottom(left, top, right, bottom)
        else:
            return cls.Empty

    @classmethod
    def round(cls, value):
        """Converts a RectangleF structure to a Rectangle structure by rounding the coordinates and size."""
        return cls(
            int(round(value.x)),
            int(round(value.y)),
            int(round(value.width)),
            int(round(value.height))
        )

    @classmethod
    def truncate(cls, value):
        """Converts a RectangleF structure to a Rectangle structure by truncating the coordinates and size."""
        return cls(int(value.x), int(value.y), int(value.width), int(value.height))

    @classmethod
    def union(cls, a, b):
        """Returns a rectangle that contains the union of two rectangles."""
        left = min(a.left, b.left)
        top = min(a.top, b.top)
        right = max(a.right, b.right)
        bottom = max(a.bottom, b.bottom)
        return cls.from_left_top_right_bottom(left, top, right, bottom)

    def contains(self, x, y=None):
        """Determines whether the specified point or rectangle is contained within this Rectangle."""
        if isinstance(x, Point):
            return self.contains(x.x, x.y)
        elif y is None and isinstance(x, Rectangle):
            other = x
            return (self.left <= other.left and
                    other.right <= self.right and
                    self.top <= other.top and
                    other.bottom <= self.bottom)
        else:
            return x >= self.left and x < self.right and y >= self.top and y < self.bottom

    def equals(self, other):
        """Determines whether the specified rectangle is equal to this rectangle."""
        if not isinstance(other, Rectangle):
            return False
        return (self.x == other.x and
                self.y == other.y and
                self.width == other.width and
                self.height == other.height)

    def __eq__(self, other):
        return self.equals(other)

    def __ne__(self, other):
        return not self.equals(other)

    def __hash__(self):
        return hash((self.x, self.y, self.width, self.height))

    def _inflate_impl(self, width, height=None):
        """Internal implementation for inflation."""
        if isinstance(width, Size):
            height = width.height
            width = width.width

        self.x -= width
        self.y -= height
        self.width += width * 2
        self.height += height * 2

    def inflate(self, width, height=None):
        """Inflates this rectangle by the specified horizontal and vertical amounts."""
        self._inflate_impl(width, height)

    def intersect(self, rectangle):
        """Replaces this rectangle with its intersection with the specified rectangle."""
        result = Rectangle.intersect_rect(self, rectangle)
        self.x = result.x
        self.y = result.y
        self.width = result.width
        self.height = result.height

    def intersect_with(self, rectangle):
        """Determines whether this rectangle intersects with the specified rectangle."""
        return (rectangle.left < self.right and
                self.left < rectangle.right and
                rectangle.top < self.bottom and
                self.top < rectangle.bottom)

    def normalize(self):
        """Normalizes this rectangle so that width and height are non-negative."""
        if self.width < 0:
            self.x += self.width
            self.width = -self.width

        if self.height < 0:
            self.y += self.height
            self.height = -self.height

    def offset(self, x, y=None):
        """Moves this rectangle by the specified horizontal and vertical amounts."""
        if isinstance(x, Point):
            y = x.y
            x = x.x

        self.x += x
        self.y += y

    def __str__(self):
        return "{{X={}, Y={}, Width={}, Height={}}}".format(self.x, self.y, self.width, self.height)


# Initialize Empty
Rectangle.Empty = Rectangle()
