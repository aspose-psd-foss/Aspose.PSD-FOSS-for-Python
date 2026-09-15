from enum import IntEnum


# Defines the color modes supported by PSD files.
class ColorModes(IntEnum):
    # Bitmap color mode.
    BITMAP = 0
    # Grayscale color mode.
    GRAYSCALE = 1
    # Indexed color mode (using a color palette).
    INDEXED = 2
    # RGB color mode (Red, Green, Blue).
    RGB = 3
    # CMYK color mode (Cyan, Magenta, Yellow, Black).
    CMYK = 4
    # Multichannel color mode.
    MULTICHANNEL = 7
    # Duotone color mode (two-color gradient).
    DUOTONE = 8
    # LAB color mode.
    LAB = 9
