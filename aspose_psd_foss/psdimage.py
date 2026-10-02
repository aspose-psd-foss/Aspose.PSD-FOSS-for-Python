from .loaders.psdimageloader import PsdImageLoader as ImageLoader

class Image(ImageLoader):
    """Legacy alias for the loader class to keep backward compatibility."""
    pass

# Export under the name expected by other modules
PsdImage = Image

__all__ = ["PsdImage", "Image", "ImageLoader"]
