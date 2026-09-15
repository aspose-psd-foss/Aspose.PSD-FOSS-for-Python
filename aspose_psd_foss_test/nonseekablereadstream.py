import io


class NonSeekableReadStream(io.RawIOBase):
    """Wraps a readable in-memory stream and intentionally disables seeking."""

    def __init__(self, data):
        """
        Initializes a new instance of the NonSeekableReadStream class.

        :param data: The bytes exposed by the stream.
        """
        self._inner_stream = io.BytesIO(data)

    def readable(self):
        return True

    def seekable(self):
        return False

    def writable(self):
        return False

    @property
    def length(self):
        return len(self._inner_stream.getbuffer())

    @property
    def position(self):
        return self._inner_stream.tell()

    @position.setter
    def position(self, value):
        raise io.UnsupportedOperation()

    def flush(self):
        pass

    def read(self, size=-1):
        """
        Reads bytes from the stream.

        :param size: The requested byte count. -1 reads to the end.
        :return: The bytes actually read.
        """
        return self._inner_stream.read(size)

    def seek(self, offset, whence=io.SEEK_SET):
        """
        Seeks within the stream.

        :param offset: The byte offset relative to the origin.
        :param whence: The reference origin.
        :return: The new stream position.
        """
        raise io.UnsupportedOperation()

    def truncate(self, size=None):
        """
        Changes the stream length.

        :param size: The new stream length.
        """
        raise io.UnsupportedOperation()

    def write(self, b):
        """
        Writes bytes to the stream.

        :param b: The source buffer.
        """
        raise io.UnsupportedOperation()

    def close(self):
        """
        Releases resources used by the wrapped stream.
        """
        self._inner_stream.close()
        super().close()

