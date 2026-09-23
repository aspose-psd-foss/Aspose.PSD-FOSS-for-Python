"""Defines the color modes supported by PSD files."""

from enum import Enum



class ColorModes(Enum):
    """Defines the color modes supported by PSD files."""
    BITMAP = 0
    GRAYSCALE = 1
    INDEXED = 2
    RGB = 3
    CMYK = 4
    MULTICHANNEL = 7
    DUOTONE = 8
    LAB = 9
