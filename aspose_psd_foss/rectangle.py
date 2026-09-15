from __future__ import annotations

import math

from aspose_psd_foss.point import Point
from aspose_psd_foss.rectanglef import RectangleF
from aspose_psd_foss.size import Size


class Rectangle:
    """Stores a set of four integers that represent the location and size of a rectangle."""

    EMPTY = None  # will be set after class definition

    def __init__(self, x: int = 0, y: int = 0, width: int = 0, height: int = 0):
        self._x = x
        self._y = y
        self._width = width
        self._height = height

    @classmethod
    def from_location_size(cls, location: Point, size: Size) -> Rectangle:
        return cls(location.x, location.y, size.width, size.height)

    @property
    def x(self) -> int:
        return self._x

    @x.setter
    def x(self, value: int):
        self._x = value

    @property
    def y(self) -> int:
        return self._y

    @y.setter
    def y(self, value: int):
        self._y = value

    @property
    def width(self) -> int:
        return self._width

    @width.setter
    def width(self, value: int):
        self._width = value

    @property
    def height(self) -> int:
        return self._height

    @height.setter
    def height(self, value: int):
        self._height = value

    @property
    def bottom(self) -> int:
        return self._y + self._height

    @bottom.setter
    def bottom(self, value: int):
        self._height = value - self._y

    @property
    def is_empty(self) -> bool:
        return (
            self._x == 0
            and self._y == 0
            and self._width == 0
            and self._height == 0
        )

    @property
    def left(self) -> int:
        return self._x

    @left.setter
    def left(self, value: int):
        right = self.right
        self._x = value
        self._width = right - value

    @property
    def right(self) -> int:
        return self._x + self._width

    @right.setter
    def right(self, value: int):
        self._width = value - self._x

    @property
    def top(self) -> int:
        return self._y

    @top.setter
    def top(self, value: int):
        bottom = self.bottom
        self._y = value
        self._height = bottom - value

    @property
    def location(self) -> Point:
        return Point(self._x, self._y)

    @location.setter
    def location(self, value: Point):
        self._x = value.x
        self._y = value.y

    @property
    def size(self) -> Size:
        return Size(self._width, self._height)

    @size.setter
    def size(self, value: Size):
        self._width = value.width
        self._height = value.height

    @staticmethod
    def ceiling(value: RectangleF) -> Rectangle:
        return Rectangle(
            int(math.ceil(value.x)),
            int(math.ceil(value.y)),
            int(math.ceil(value.width)),
            int(math.ceil(value.height)),
        )

    @staticmethod
    def round_(value: RectangleF) -> Rectangle:
        return Rectangle(
            int(round(value.x)),
            int(round(value.y)),
            int(round(value.width)),
            int(round(value.height)),
        )

    @staticmethod
    def truncate(value: RectangleF) -> Rectangle:
        return Rectangle(int(value.x), int(value.y), int(value.width), int(value.height))

    @staticmethod
    def from_left_top_right_bottom(
        left: int, top: int, right: int, bottom: int
    ) -> Rectangle:
        return Rectangle(left, top, right - left, bottom - top)

    @staticmethod
    def from_ltrb(left: int, top: int, right: int, bottom: int) -> Rectangle:
        return Rectangle.from_left_top_right_bottom(left, top, right, bottom)

    @staticmethod
    def from_points(point1: Point, point2: Point) -> Rectangle:
        left = min(point1.x, point2.x)
        top = min(point1.y, point2.y)
        right = max(point1.x, point2.x)
        bottom = max(point1.y, point2.y)
        return Rectangle.from_left_top_right_bottom(left, top, right, bottom)

    @staticmethod
    def inflate(rectangle: Rectangle, x: int, y: int) -> Rectangle:
        result = Rectangle(rectangle.x, rectangle.y, rectangle.width, rectangle.height)
        result.inflate(x, y)
        return result

    @staticmethod
    def intersect(a: Rectangle, b: Rectangle) -> Rectangle:
        left = max(a.left, b.left)
        top = max(a.top, b.top)
        right = min(a.right, b.right)
        bottom = min(a.bottom, b.bottom)

        if right > left and bottom > top:
            return Rectangle.from_left_top_right_bottom(left, top, right, bottom)
        return Rectangle.EMPTY

    @staticmethod
    def union(a: Rectangle, b: Rectangle) -> Rectangle:
        left = min(a.left, b.left)
        top = min(a.top, b.top)
        right = max(a.right, b.right)
        bottom = max(a.bottom, b.bottom)
        return Rectangle.from_left_top_right_bottom(left, top, right, bottom)

    def contains(self, point_or_x, y: int = None) -> bool:
        if isinstance(point_or_x, Point):
            return self.contains(point_or_x.x, point_or_x.y)
        if isinstance(point_or_x, Rectangle):
            rect = point_or_x
            return (
                self.left <= rect.left
                and rect.right <= self.right
                and self.top <= rect.top
                and rect.bottom <= self.bottom
            )
        x = point_or_x
        return (
            x >= self.left
            and x < self.right
            and y >= self.top
            and y < self.bottom
        )

    def equals(self, other: Rectangle) -> bool:
        return (
            self._x == other._x
            and self._y == other._y
            and self._width == other._width
            and self._height == other._height
        )

    def __eq__(self, other) -> bool:
        if isinstance(other, Rectangle):
            return self.equals(other)
        return False

    def __ne__(self, other) -> bool:
        return not self == other

    def __hash__(self) -> int:
        return hash((self._x, self._y, self._width, self._height))

    def __repr__(self) -> str:
        return f"{{X={self._x}, Y={self._y}, Width={self._width}, Height={self._height}}}"

    def inflate(self, arg1, arg2=None):
        if isinstance(arg1, Size):
            self.inflate(arg1.width, arg1.height)
        else:
            width = arg1
            height = arg2
            self._x -= width
            self._y -= height
            self._width += width * 2
            self._height += height * 2

    def intersect_self(self, rectangle: Rectangle):
        intersected = Rectangle.intersect(self, rectangle)
        self._x = intersected._x
        self._y = intersected._y
        self._width = intersected._width
        self._height = intersected._height

    def intersects_with(self, rectangle: Rectangle) -> bool:
        return (
            rectangle.left < self.right
            and self.left < rectangle.right
            and rectangle.top < self.bottom
            and self.top < rectangle.bottom
        )

    def normalize(self):
        if self._width < 0:
            self._x += self._width
            self._width = -self._width
        if self._height < 0:
            self._y += self._height
            self._height = -self._height

    def offset(self, arg1, arg2=None):
        if isinstance(arg1, Point):
            self.offset(arg1.x, arg1.y)
        else:
            self._x += arg1
            self._y += arg2

    def to_string(self) -> str:
        return self.__repr__()


Rectangle.EMPTY = Rectangle(0, 0, 0, 0)
