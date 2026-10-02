from enum import Enum, IntEnum


class ColorModes(IntEnum):
    """Defines the color modes supported by PSD files."""
    BITMAP = 0  # Bitmap color mode.
    GRAYSCALE = 1  # Grayscale color mode.
    INDEXED = 2  # Indexed color mode (using a color palette).
    RGB = 3  # RGB color mode (Red, Green, Blue).
    CMYK = 4  # CMYK color mode (Cyan, Magenta, Yellow, Black).
    MULTICHANNEL = 7  # Multichannel color mode.
    DUOTONE = 8  # Duotone color mode (two-color gradient).
    LAB = 9  # LAB color mode.
