class Size:
    """Represents an ordered pair of integer width and height values that defines a size."""
    __slots__ = ("width", "height")

    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height

    @property
    def is_empty(self) -> bool:
        return self.width == 0 and self.height == 0

    def __eq__(self, other):
        if isinstance(other, Size):
            return self.width == other.width and self.height == other.height
        return False

    def __hash__(self):
        return hash((self.width, self.height))

    def __str__(self):
        return f"{{Width={self.width}, Height={self.height}}}"

    def __repr__(self):
        return self.__str__()

    def __ne__(self, other):
        return not self.__eq__(other)


# Represents a Size with width and height left uninitialized.
Size.EMPTY = Size(0, 0)
