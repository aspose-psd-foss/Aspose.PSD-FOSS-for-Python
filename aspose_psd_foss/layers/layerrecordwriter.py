from .layer import Layer

class LayerRecordWriter:
    def __init__(self, layer: Layer):
        self.layer = layer

    def write(self, writer):
        raise NotImplementedError

__all__ = ['LayerRecordWriter']
