from abc import ABC, abstractmethod
from aspose_psd_foss.rectangle import Rectangle
from aspose_psd_foss.psdimage import PsdImage


class Image(ABC):
    """Provides the Aspose.PSD-compatible base image entry point for loading PSD/PSB documents."""

    @property
    @abstractmethod
    def width(self):
        """Gets the image width in pixels."""
        pass

    @property
    @abstractmethod
    def height(self):
        """Gets the image height in pixels."""
        pass

    @property
    def bounds(self):
        """Gets the image bounds."""
        return Rectangle(0, 0, self.width, self.height)

    @classmethod
    def load(cls, file_path):
        """Loads a new image from the specified file path.

        :param file_path: The file path to load image from.
        :return: The loaded image.
        """
        return PsdImage.load(file_path)

    @classmethod
    def load_stream(cls, stream):
        """Loads a new image from the specified stream.

        :param stream: The stream to load image from.
        :return: The loaded image.
        """
        return PsdImage.load_stream(stream)

    @abstractmethod
    def save(self, file_path):
        """Saves the image data to the specified file path.

        :param file_path: The destination file path.
        """
        pass

    @abstractmethod
    def save_stream(self, stream):
        """Saves the image data to the specified stream.

        :param stream: The destination stream.
        """
        pass

    @abstractmethod
    def dispose(self):
        """Releases resources used by the image."""
        pass
