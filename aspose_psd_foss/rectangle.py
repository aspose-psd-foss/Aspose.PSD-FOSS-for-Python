import math
from typing import ClassVar
from aspose_psd_foss.point import Point
from aspose_psd_foss.size import Size
from aspose_psd_foss.rectanglef import RectangleF
import copy


class Rectangle:
    """Stores a set of four integers that represent the location and size of a rectangle."""

    __slots__ = ("x", "y", "width", "height")
    Empty: ClassVar["Rectangle"]

    def __init__(self, x=0, y=0, width=0, height=0):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    # --- static members -------------------------------------------------
    @classmethod
    def empty(cls):
        """Represents a Rectangle structure with its properties left uninitialized."""
        return cls()

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
    def from_point_and_size(cls, location: Point, size: Size):
        """Initializes a new instance from a Point and a Size."""
        return cls(location.x, location.y, size.width, size.height)

    @classmethod
    def ceiling(cls, value):
        """Converts a RectangleF structure to a Rectangle structure by rounding up the coordinates and size."""
        return cls(
            int(math.ceil(value.x)),
            int(math.ceil(value.y)),
            int(math.ceil(value.width)),
            int(math.ceil(value.height)),
        )

    @classmethod
    def round(cls, value):
        """Converts a RectangleF structure to a Rectangle structure by rounding the coordinates and size."""
        return cls(
            int(round(value.x)),
            int(round(value.y)),
            int(round(value.width)),
            int(round(value.height)),
        )

    @classmethod
    def truncate(cls, value):
        """Converts a RectangleF structure to a Rectangle structure by truncating the coordinates and size."""
        return cls(int(value.x), int(value.y), int(value.width), int(value.height))

    @classmethod
    def inflate_rect(cls, rectangle, x, y):
        """Creates and returns an inflated copy of the specified rectangle."""
        result = rectangle.__copy__()
        result.inflate(x, y)
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
        return cls.empty()

    @classmethod
    def union_rect(cls, a, b):
        """Returns a rectangle that contains the union of two rectangles."""
        left = min(a.left, b.left)
        top = min(a.top, b.top)
        right = max(a.right, b.right)
        bottom = max(a.bottom, b.bottom)
        return cls.from_left_top_right_bottom(left, top, right, bottom)

    # --- properties -----------------------------------------------------
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
    def right(self):
        """Gets or sets the x-coordinate of the right edge of this Rectangle."""
        return self.x + self.width

    @right.setter
    def right(self, value):
        self.width = value - self.x

    @property
    def top(self):
        """Gets or sets the y-coordinate of the top edge of this Rectangle."""
        return self.y

    @top.setter
    def top(self, value):
        bottom = self.bottom
        self.y = value
        self.height = bottom - value

    @property
    def location(self):
        """Gets or sets the coordinates of the upper-left corner of this Rectangle."""
        return Point(self.x, self.y)

    @location.setter
    def location(self, value):
        self.x = value.x
        self.y = value.y

    @property
    def size(self):
        """Gets or sets the size of this Rectangle."""
        return Size(self.width, self.height)

    @size.setter
    def size(self, value):
        self.width = value.width
        self.height = value.height

    # PascalCase aliases to match .NET naming
    X = property(lambda self: self.x, lambda self, v: setattr(self, "x", v))
    Y = property(lambda self: self.y, lambda self, v: setattr(self, "y", v))
    Width = property(lambda self: self.width, lambda self, v: setattr(self, "width", v))
    Height = property(lambda self: self.height, lambda self, v: setattr(self, "height", v))
    Bottom = bottom
    IsEmpty = is_empty
    Left = left
    Right = right
    Top = top
    Location = location
    Size = size

    # --- instance methods -----------------------------------------------
    def contains(self, *args):
        """Determines whether the specified point or rectangle is contained within this Rectangle."""
        if len(args) == 1:
            arg = args[0]
            if isinstance(arg, Point):
                return self.contains(arg.x, arg.y)
            if isinstance(arg, Rectangle):
                return (
                    self.left <= arg.left
                    and arg.right <= self.right
                    and self.top <= arg.top
                    and arg.bottom <= self.bottom
                )
        elif len(args) == 2:
            x, y = args
            return self.left <= x < self.right and self.top <= y < self.bottom
        raise TypeError("Invalid arguments for contains")

    def __eq__(self, other):
        if not isinstance(other, Rectangle):
            return NotImplemented
        return (
            self.x == other.x
            and self.y == other.y
            and self.width == other.width
            and self.height == other.height
        )

    def __ne__(self, other):
        eq = self.__eq__(other)
        if eq is NotImplemented:
            return NotImplemented
        return not eq

    def __hash__(self):
        return hash((self.x, self.y, self.width, self.height))

    def __str__(self):
        return f"{{X={self.x}, Y={self.y}, Width={self.width}, Height={self.height}}}"

    def __repr__(self):
        return f"Rectangle({self.x}, {self.y}, {self.width}, {self.height})"

    def __copy__(self):
        return Rectangle(self.x, self.y, self.width, self.height)

    def inflate(self, *args):
        """Inflates this rectangle by the specified size or dimensions."""
        if len(args) == 1 and isinstance(args[0], Size):
            size = args[0]
            self.inflate(size.width, size.height)
        elif len(args) == 2:
            width, height = args
            self.x -= width
            self.y -= height
            self.width += width * 2
            self.height += height * 2
        else:
            raise TypeError("inflate expects a Size or width and height")

    def intersect(self, rectangle):
        """Replaces this rectangle with its intersection with the specified rectangle."""
        intersected = self.__class__.intersect_rect(self, rectangle)
        self.x = intersected.x
        self.y = intersected.y
        self.width = intersected.width
        self.height = intersected.height

    def intersects_with(self, rectangle):
        """Determines whether this rectangle intersects with the specified rectangle."""
        return (
            rectangle.left < self.right
            and self.left < rectangle.right
            and rectangle.top < self.bottom
            and self.top < rectangle.bottom
        )

    def normalize(self):
        """Normalizes this rectangle so that width and height are non-negative."""
        if self.width < 0:
            self.x += self.width
            self.width = -self.width
        if self.height < 0:
            self.y += self.height
            self.height = -self.height

    def offset(self, *args):
        """Moves this rectangle by the specified point or offsets."""
        if len(args) == 1 and isinstance(args[0], Point):
            point = args[0]
            self.offset(point.x, point.y)
        elif len(args) == 2:
            x, y = args
            self.x += x
            self.y += y
        else:
            raise TypeError("offset expects a Point or x and y values")


# static readonly Empty equivalent
Rectangle.Empty = Rectangle()  # type: ignore[assignment]
