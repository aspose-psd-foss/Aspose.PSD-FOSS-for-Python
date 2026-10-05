from io import BytesIO

from .psdimage import PsdImage


class ImageLoader:
    """
    Provides the load functionality for images.
    """


    @staticmethod
    def load_from_path(file_path: str) -> object:
        return PsdImage.load(file_path)

    @staticmethod
    def load_from_stream(stream: BytesIO) -> object:
        return PsdImage.load(stream)
