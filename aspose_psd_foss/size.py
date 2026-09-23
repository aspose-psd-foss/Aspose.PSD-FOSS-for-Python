class Size:
    """Represents an ordered pair of integer width and height values that defines a size."""

    def __init__(self, width=0, height=0):
        """Initializes a new instance of the Size structure with the specified dimensions.

        Args:
            width (int): The width component.
            height (int): The height component.
        """
        self.width = width
        self.height = height

    @property
    def width(self):
        """Gets or sets the width component of this Size."""
        return self._width

    @width.setter
    def width(self, value):
        self._width = value

    @property
    def height(self):
        """Gets or sets the height component of this Size."""
        return self._height

    @height.setter
    def height(self, value):
        self._height = value

    @property
    def is_empty(self):
        """Gets a value indicating whether this Size has width and height left uninitialized."""
        return self.width == 0 and self.height == 0

    @classmethod
    def empty(cls):
        """Represents a Size with width and height left uninitialized."""
        return cls()

    def equals(self, other):
        """Determines whether the specified size is equal to this size.

        Args:
            other (Size): The size to compare.

        Returns:
            bool: True if the sizes are equal; otherwise, False.
        """
        if not isinstance(other, Size):
            return False
        return self.width == other.width and self.height == other.height

    def __eq__(self, other):
        """Determines whether the specified object is equal to this size.

        Args:
            other: The object to compare.

        Returns:
            bool: True if the object is an equal size; otherwise, False.
        """
        return self.equals(other)

    def __ne__(self, other):
        """Determines whether two sizes are not equal.

        Args:
            other: The object to compare.

        Returns:
            bool: True if the sizes are not equal; otherwise, False.
        """
        return not self.__eq__(other)

    def __hash__(self):
        """Returns a hash code for this size.

        Returns:
            int: The hash code.
        """
        return hash((self.width, self.height))

    def __str__(self):
        """Returns a compact size representation.

        Returns:
            str: The size representation.
        """
        return f"{{Width={self.width}, Height={self.height}}}"

    def __repr__(self):
        return self.__str__()
