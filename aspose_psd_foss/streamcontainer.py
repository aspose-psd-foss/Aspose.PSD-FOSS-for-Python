class StreamContainer:
    """Represents a stream container used by resource save APIs.

    Args:
        stream: The wrapped stream.
    """
    def __init__(self, stream):
        if stream is None:
            raise ValueError("stream")
        self._stream = stream

    @property
    def stream(self):
        """Gets the wrapped stream."""
        return self._stream

    @property
    def Stream(self):
        """Gets the wrapped stream (C# property name)."""
        return self._stream
