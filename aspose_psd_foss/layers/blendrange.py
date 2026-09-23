# Represents a PSD layer blend range.


class BlendRange:
    """
    Represents a PSD layer blend range.
    """

    def __init__(self, destination=0, source=0):
        """
        Initializes a new instance of the BlendRange class.

        :param destination: The destination blend range.
        :param source: The source blend range.
        """
        self.destination = destination
        self.source = source

    @property
    def destination(self):
        """Gets or sets the destination blend range."""
        return self._destination

    @destination.setter
    def destination(self, value):
        self._destination = value

    @property
    def source(self):
        """Gets or sets the source blend range."""
        return self._source

    @source.setter
    def source(self, value):
        self._source = value
