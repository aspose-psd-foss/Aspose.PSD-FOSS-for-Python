import abc
from .rectangle import Rectangle


class PsdImage:
    """Fallback placeholder for missing PsdImage implementation."""

    @staticmethod
    def load(_):
        raise NotImplementedError("PsdImage.load is not implemented because the module is missing.")

    @staticmethod
    def load_stream(_):
        raise NotImplementedError("PsdImage.load_stream is not implemented because the module is missing.")


class Image(abc.ABC):
    """Provides the Aspose.PSD-compatible base image entry point for loading PSD/PSB documents."""

    @property
    @abc.abstractmethod
    def width(self) -> int:
        """Gets the image width in pixels."""
        ...

    @property
    @abc.abstractmethod
    def height(self) -> int:
        """Gets the image height in pixels."""
        ...

    @property
    def bounds(self) -> Rectangle:
        """Gets the image bounds."""
        return Rectangle(0, 0, self.width, self.height)

    @staticmethod
    def load(file_path):
        """Loads a new image from the specified file path."""
        return PsdImage.load(file_path)

    @staticmethod
    def load_stream(stream):
        """Loads a new image from the specified stream."""
        return PsdImage.load_stream(stream)

    @abc.abstractmethod
    def save(self, file_path):
        """Saves the image data to the specified file path."""
        ...

    @abc.abstractmethod
    def save_stream(self, stream):
        """Saves the image data to the specified stream."""
        ...

    @abc.abstractmethod
    def dispose(self):
        """Releases resources used by the image."""
        ...
