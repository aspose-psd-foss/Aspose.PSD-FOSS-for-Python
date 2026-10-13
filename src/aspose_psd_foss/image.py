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


    @staticmethod
    def load(source: Union[str, io.BytesIO, io.BufferedIOBase]) -> "Image":
        from aspose_psd_foss.imageloader import ImageLoader

        """
        Loads a new image from the specified file path or stream.

        :param source: The file path (str) or stream (io.BytesIO) to load image from.
        :return: The loaded image.
        """
        if isinstance(source, str):
            return ImageLoader.load_from_path(source)
        elif isinstance(source, (io.BytesIO, io.BufferedIOBase)):
            return ImageLoader.load_from_stream(source)

        raise TypeError(f"Unsupported type {type(source)}")

