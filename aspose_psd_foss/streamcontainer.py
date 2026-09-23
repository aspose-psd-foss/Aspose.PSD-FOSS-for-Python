import io


class StreamContainer:
    """Represents a stream container used by resource save APIs."""

    def __init__(self, stream):
        """Initializes a new instance of the <see cref="StreamContainer"/> class."""
        if stream is None:
            raise ValueError("Stream cannot be null")
        self._stream = stream

    @property
    def stream(self):
        """Gets the wrapped stream."""
        return self._stream
