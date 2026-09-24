import io

class NonSeekableReadStream(io.BytesIO):
    _inner_stream = None

    def __init__(self, data):
        self._inner_stream = io.BytesIO(data)

    @property
    def can_read(self):
        return True

    @property
    def can_seek(self):
        return False

    @property
    def can_write(self):
        return False

    @property
    def length(self):
        return self._inner_stream.getbuffer().nbytes

    @property
    def position(self):
        return self._inner_stream.tell()

    @position.setter
    def position(self, value):
        raise NotImplementedError()

    def flush(self):
        pass

    def read(self, buffer, offset, count):
        self._inner_stream.seek(offset)
        data = self._inner_stream.read(count)
        buffer[:len(data)] = data
        return len(data)

    def seek(self, offset, origin):
        raise NotImplementedError()

    def set_length(self, value):
        raise NotImplementedError()

    def write(self, buffer, offset, count):
        raise NotImplementedError()

    def close(self):
        if self._inner_stream is not None:
            self._inner_stream.close()
        super().close()

