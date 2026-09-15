import abc
from aspose_psd_foss.rectangle import Rectangle
from aspose_psd_foss.psd_image import PsdImage


# Provides the Aspose.PSD-compatible base image entry point for loading PSD/PSB documents.

class Image(abc.ABC):
    @property
    @abc.abstractmethod
    def width(self):
        # Gets the image width in pixels.
        ...

    @property
    @abc.abstractmethod
    def height(self):
        # Gets the image height in pixels.
        ...

    @property
    def bounds(self):
        # Gets the image bounds.
        return Rectangle(0, 0, self.width, self.height)

    @staticmethod
    def load(*args):
        # Loads a new image from the specified file path or stream.
        if len(args) != 1:
            raise TypeError("load() takes exactly one argument")
        return PsdImage.load(args[0])

    @abc.abstractmethod
    def save(self, destination):
        # Saves the image data to the specified file path or stream.
        ...

    @abc.abstractmethod
    def dispose(self):
        # Releases resources used by the image.
        ...
