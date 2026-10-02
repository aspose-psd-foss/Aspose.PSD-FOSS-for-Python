from __future__ import annotations
import io
import os
from typing import Union
from abc import ABC, abstractmethod

class Image(ABC):
    """
    Abstract base class for image objects.
    Concrete image implementations should inherit from this class
    and implement the required interface.
    """
    @abstractmethod
    def some_method(self):
        """Placeholder abstract method for concrete implementations."""
        pass

    @staticmethod
    def Load(source: Union[str, io.BytesIO, io.BufferedIOBase]) -> "Image":
        """
        Load an image using the ImageLoader factory.

        Parameters
        ----------
        source : str or io.BytesIO or io.BufferedIOBase
            Path to the image file or a binary stream containing image data.

        Returns
        -------
        Image
            An instance of a subclass of `Image` representing the loaded image.
        """
        return ImageLoader.load(source)

class ImageLoader:
    """
    Factory class responsible for loading images from file paths or streams.
    The `load` method inspects the source type and dispatches to the appropriate
    concrete Image subclass. Currently only a generic placeholder implementation
    is provided; extend it with actual image format handling as needed.
    """
    @staticmethod
    def load(source: Union[str, io.BytesIO, io.BufferedIOBase]) -> "Image":
        """
        Load an image from a file path or a binary stream.

        Parameters
        ----------
        source : str or io.BytesIO or io.BufferedIOBase
            Path to the image file or a binary stream containing image data.

        Returns
        -------
        Image
            An instance of a subclass of `Image` representing the loaded image.

        Raises
        ------
        FileNotFoundError
            If a file path is provided but the file does not exist.
        NotImplementedError
            If the loader does not recognize the format or the concrete
            Image subclass is not implemented.
        """
        # Handle file path strings
        if isinstance(source, str):
            if not os.path.isfile(source):
                raise FileNotFoundError(f"Image file not found: {source}")

            # Determine format by file extension (simple heuristic)
            _, ext = os.path.splitext(source)
            ext = ext.lower()

            # Dispatch to concrete loaders based on extension.
            # Replace the following placeholders with actual implementations.
            if ext in {".psd"}:
                # return PsdImage.load(source)
                raise NotImplementedError("PSD image loading not implemented.")
            elif ext in {".png"}:
                # return PngImage.load(source)
                raise NotImplementedError("PNG image loading not implemented.")
            elif ext in {".jpg", ".jpeg"}:
                # return JpegImage.load(source)
                raise NotImplementedError("JPEG image loading not implemented.")
            else:
                raise NotImplementedError(f"Unsupported image format: {ext}")

        # Handle binary streams (BytesIO, BufferedIOBase, etc.)
        elif isinstance(source, (io.BytesIO, io.BufferedIOBase)):
            # Peek at the first few bytes to guess format if needed.
            # This is a placeholder; actual implementation should inspect the stream.
            raise NotImplementedError("Loading from streams is not implemented yet.")

        else:
            raise TypeError("source must be a file path string or a binary stream")

# Optional convenience alias if external code expects a factory called ImageFactory
ImageFactory = ImageLoader

# Export the Image, ImageLoader, and ImageFactory classes when using `from .image import *`
__all__ = ["Image", "ImageLoader", "ImageFactory"]
