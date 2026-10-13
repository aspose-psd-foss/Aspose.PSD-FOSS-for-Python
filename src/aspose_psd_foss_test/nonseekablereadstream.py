import io


class NonSeekableReadStream(io.RawIOBase):
    """Wraps a readable in‑memory stream and intentionally disables seeking."""

    def __init__(self, data):
        """
        Initializes a new instance of the NonSeekableReadStream class.

        :param data: The bytes exposed by the stream.
        """
        self._inner_stream = io.BytesIO(data)

    @property
    def length(self):
        """Gets the total length of the stream."""
        current = self._inner_stream.tell()
        self._inner_stream.seek(0, io.SEEK_END)
        length = self._inner_stream.tell()
        self._inner_stream.seek(current, io.SEEK_SET)
        return length

    @property
    def position(self):
        """Gets or sets the current stream position."""
        return self._inner_stream.tell()

    @position.setter
    def position(self, value):
        raise OSError("Seek not supported")

    def readable(self):
        """Gets a value indicating whether the stream supports reading."""
        return True

    def writable(self):
        """Gets a value indicating whether the stream supports writing."""
        return False

    def seekable(self):
        """Gets a value indicating whether the stream supports seeking."""
        return False

    def flush(self):
        """Flushes buffered state."""
        pass

    def read(self, size=-1):
        """Reads bytes from the stream."""
        return self._inner_stream.read(size)

    def seek(self, offset, whence=io.SEEK_SET):
        """Seeks within the stream."""
        raise OSError("Seek not supported")

    def set_length(self, value):
        """Changes the stream length."""
        raise OSError("SetLength not supported")

    def write(self, b):
        """Writes bytes to the stream."""
        raise OSError("Write not supported")

    def close(self):
        """Releases resources used by the wrapped stream."""
        self._inner_stream.close()
        super().close()

