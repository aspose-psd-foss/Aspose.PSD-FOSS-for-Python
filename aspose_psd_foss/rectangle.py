from __future__ import annotations
import math

from aspose_psd_foss.point import Point
from aspose_psd_foss.size import Size
from aspose_psd_foss.rectanglef import RectangleF


class Rectangle:
    """Stores a set of four integers that represent the location and size of a rectangle."""

    EMPTY: Rectangle

    def __init__(self, x: int = 0, y: int = 0, width: int = 0, height: int = 0):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    @property
    def bottom(self) -> int:
        return self.y + self.height

    @bottom.setter
    def bottom(self, value: int):
        self.height = value - self.y

    @property
    def is_empty(self) -> bool:
        return self.x == 0 and self.y == 0 and self.width == 0 and self.height == 0

    @property
    def left(self) -> int:
        return self.x

    @left.setter
    def left(self, value: int):
        right = self.right
        self.x = value
        self.width = right - value

    @property
    def location(self) -> Point:
        return Point(self.x, self.y)

    @location.setter
    def location(self, value: Point):
        self.x = value.x
        self.y = value.y

    @property
    def right(self) -> int:
        return self.x + self.width

    @right.setter
    def right(self, value: int):
        self.width = value - self.x

    @property
    def size(self) -> Size:
        return Size(self.width, self.height)

    @size.setter
    def size(self, value: Size):
        self.width = value.width
        self.height = value.height

    @property
    def top(self) -> int:
        return self.y

    @top.setter
    def top(self, value: int):
        bottom = self.bottom
        self.y = value
        self.height = bottom - value

    @staticmethod
    def ceiling(value: RectangleF) -> Rectangle:
        return Rectangle(
            int(math.ceil(value.x)),
            int(math.ceil(value.y)),
            int(math.ceil(value.width)),
            int(math.ceil(value.height))
        )

    @staticmethod
    def from_left_top_right_bottom(left: int, top: int, right: int, bottom: int) -> Rectangle:
        return Rectangle(left, top, right - left, bottom - top)

    @staticmethod
    def _from_ltrb(left: int, top: int, right: int, bottom: int) -> Rectangle:
        return Rectangle.from_left_top_right_bottom(left, top, right, bottom)

    @staticmethod
    def from_points(point1: Point, point2: Point) -> Rectangle:
        left = min(point1.x, point2.x)
        top = min(point1.y, point2.y)
        right = max(point1.x, point2.x)
        bottom = max(point1.y, point2.y)
        return Rectangle.from_left_top_right_bottom(left, top, right, bottom)

    @staticmethod
    def inflate_rect(rectangle: Rectangle, x: int, y: int) -> Rectangle:
        result = Rectangle(rectangle.x, rectangle.y, rectangle.width, rectangle.height)
        result.inflate(x, y)
        return result

    @staticmethod
    def intersect_rect(a: Rectangle, b: Rectangle) -> Rectangle:
        left = max(a.left, b.left)
        top = max(a.top, b.top)
        right = min(a.right, b.right)
        bottom = min(a.bottom, b.bottom)
        return (
            Rectangle.from_left_top_right_bottom(left, top, right, bottom)
            if right > left and bottom > top
            else Rectangle.EMPTY
        )

    @staticmethod
    def round(value: RectangleF) -> Rectangle:
        return Rectangle(
            int(round(value.x)),
            int(round(value.y)),
            int(round(value.width)),
            int(round(value.height))
        )

    @staticmethod
    def truncate(value: RectangleF) -> Rectangle:
        return Rectangle(int(value.x), int(value.y), int(value.width), int(value.height))

    @staticmethod
    def union(a: Rectangle, b: Rectangle) -> Rectangle:
        left = min(a.left, b.left)
        top = min(a.top, b.top)
        right = max(a.right, b.right)
        bottom = max(a.bottom, b.bottom)
        return Rectangle.from_left_top_right_bottom(left, top, right, bottom)

    def contains(self, *args) -> bool:
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
        if len(args) == 2:
            x, y = args
            return self.left <= x < self.right and self.top <= y < self.bottom
        raise TypeError("Invalid arguments for contains")

    def equals(self, other: Rectangle) -> bool:
        return (
            self.x == other.x
            and self.y == other.y
            and self.width == other.width
            and self.height == other.height
        )

    def __eq__(self, other) -> bool:
        if isinstance(other, Rectangle):
            return self.equals(other)
        return False

    def __ne__(self, other) -> bool:
        return not self == other

    def __hash__(self) -> int:
        return hash((self.x, self.y, self.width, self.height))

    def inflate(self, *args):
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
            raise TypeError("Invalid arguments for inflate")

    def intersect(self, rectangle: Rectangle):
        inter = Rectangle.intersect_rect(self, rectangle)
        if inter is Rectangle.EMPTY:
            self.x = self.y = self.width = self.height = 0
        else:
            self.x, self.y, self.width, self.height = inter.x, inter.y, inter.width, inter.height

    def intersects_with(self, rectangle: Rectangle) -> bool:
        return (
            rectangle.left < self.right
            and self.left < rectangle.right
            and rectangle.top < self.bottom
            and self.top < rectangle.bottom
        )

    def normalize(self):
        if self.width < 0:
            self.x += self.width
            self.width = -self.width
        if self.height < 0:
            self.y += self.height
            self.height = -self.height

    def offset(self, *args):
        if len(args) == 1 and isinstance(args[0], Point):
            point = args[0]
            self.offset(point.x, point.y)
        elif len(args) == 2:
            x, y = args
            self.x += x
            self.y += y
        else:
            raise TypeError("Invalid arguments for offset")

    def __str__(self) -> str:
        return f"{{X={self.x}, Y={self.y}, Width={self.width}, Height={self.height}}}"


Rectangle.EMPTY = Rectangle()

