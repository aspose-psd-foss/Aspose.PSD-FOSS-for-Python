class RectangleF:
    """Stores a set of four floating-point numbers that represent the location and size of a rectangle."""

    Empty: RectangleF = RectangleF()

    def __init__(self, x=0.0, y=0.0, width=0.0, height=0.0):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    @property
    def bottom(self):
        return self.y + self.height

    @property
    def is_empty(self):
        return self.x == 0 and self.y == 0 and self.width == 0 and self.height == 0

    @property
    def left(self):
        return self.x

    @property
    def right(self):
        return self.x + self.width

    @property
    def top(self):
        return self.y

    def equals(self, other):
        if not isinstance(other, RectangleF):
            return False
        return (self.x == other.x and self.y == other.y and
                self.width == other.width and self.height == other.height)

    def __eq__(self, other):
        if not isinstance(other, RectangleF):
            return False
        return self.equals(other)

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return hash((self.x, self.y, self.width, self.height))

    def __str__(self):
        return (f"Left={self.left}, Top={self.top}, Right={self.right}, "
                f"Bottom={self.bottom}, Width={self.width}, Height={self.height}")
