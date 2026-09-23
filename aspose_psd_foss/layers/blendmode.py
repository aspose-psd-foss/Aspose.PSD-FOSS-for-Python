# layers/blendmode.py
from enum import Enum


class BlendMode(Enum):
    """Defines the blend modes used for layers in PSD files."""

    NORMAL = 1852797549  # Normal blend mode (no blending).
    MULTIPLY = 1836411936  # Multiply blend mode (darkens image).
    SCREEN = 1935897198  # Screen blend mode (lightens image).
    OVERLAY = 1870030194  # Overlay blend mode (mix of multiply and screen).
    DARKEN = 1684107883  # Darken blend mode (keeps darker pixels).
    LIGHTEN = 1818850405  # Lighten blend mode (keeps lighter pixels).
    COLORDODGE = 1684633120  # Color Dodge blend mode.
    COLORBURN = 1768188278  # Color Burn blend mode.
    HARDLIGHT = 1749838196  # Hard Light blend mode.
    SOFTLIGHT = 1934387572  # Soft Light blend mode.
    DIFFERENCE = 1684629094  # Difference blend mode (subtract colors).
    EXCLUSION = 1936553316  # Exclusion blend mode.
    HUE = 1752524064  # Hue blend mode (apply hue).
    SATURATION = 1935766560  # Saturation blend mode (apply saturation).
    COLOR = 1668246642  # Color blend mode (apply color).
    LUMINOSITY = 1819634976  # Luminosity blend mode (apply luminosity).
    DARKERCOLOR = 1684751212  # Darker Color blend mode.
    LIGHTERCOLOR = 1818706796  # Lighter Color blend mode.
    LINEARBURN = 1818391150  # Linear Burn blend mode.
    LINEARDODGE = 1818518631  # Linear Dodge blend mode.
    LINEARLIGHT = 1816947060  # Linear Light blend mode.
    VIVIDLIGHT = 1984719220  # Vivid Light blend mode.
    PINLIGHT = 1884055924  # Pin Light blend mode.
    HARDMIX = 1749903736  # Hard Mix blend mode.
    SUBTRACT = 1718842722  # Subtract blend mode.
    DIVIDE = 1717856630  # Divide blend mode.
    DISSOLVE = 1684632435  # Dissolve blend mode.
    PASSTHROUGH = 1885434739  # Pass‑through blend mode.
    ABSENT = 0  # Blend mode is absent or not set yet.
