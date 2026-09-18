import io


class StreamContainer:
    """Represents a stream container used by resource save APIs."""

    def __init__(self, stream):
        if stream is None:
            raise ValueError("stream")
        self._stream = stream

    @property
    def stream(self):
        """Gets the wrapped stream."""
        return self._stream
