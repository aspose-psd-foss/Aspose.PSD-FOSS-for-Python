from typing import ClassVar

class Size:
    """Represents an ordered pair of integer width and height values that defines a size."""

    # Represents a Size with width and height left uninitialized.
    EMPTY: ClassVar["Size"]

    def __init__(self, width: int, height: int):
        """
        Initializes a new instance of the Size structure with the specified dimensions.

        :param width: The width component.
        :param height: The height component.
        """
        self.width = width
        self.height = height

    @property
    def width(self) -> int:
        """Gets or sets the width component of this Size."""
        return self._width

    @width.setter
    def width(self, value: int):
        self._width = value

    @property
    def height(self) -> int:
        """Gets or sets the height component of this Size."""
        return self._height

    @height.setter
    def height(self, value: int):
        self._height = value

    @property
    def is_empty(self) -> bool:
        """Gets a value indicating whether this Size has width and height left uninitialized."""
        return self.width == 0 and self.height == 0

    def __eq__(self, other):
        """Determines whether the specified size is equal to this size."""
        if isinstance(other, Size):
            return self.width == other.width and self.height == other.height
        return False

    def __ne__(self, other):
        """Determines whether two sizes are not equal."""
        return not self.__eq__(other)

    def __hash__(self):
        """Returns a hash code for this size."""
        return hash((self.width, self.height))

    def __repr__(self):
        """Returns a compact size representation."""
        return f'{{Width={self.width}, Height={self.height}}}'


# Initialize the static EMPTY field
Size.EMPTY = Size(0, 0)
