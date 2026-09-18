# Defines the blend modes used for layers in PSD files.
from enum import Enum


class BlendMode(Enum):
    # Normal blend mode (no blending).
    NORMAL = 1852797549

    # Multiply blend mode (multiply colors, darkens image).
    MULTIPLY = 1836411936

    # Screen blend mode (screen colors, lightens image).
    SCREEN = 1935897198

    # Overlay blend mode (combines multiply and screen).
    OVERLAY = 1870030194

    # Darken blend mode (keeps darker pixels).
    DARKEN = 1684107883

    # Lighten blend mode (keeps lighter pixels).
    LIGHTEN = 1818850405

    # Color Dodge blend mode (dodges colors).
    COLOR_DODGE = 1684633120

    # Color Burn blend mode (burns colors).
    COLOR_BURN = 1768188278

    # Hard Light blend mode (hard light blending).
    HARD_LIGHT = 1749838196

    # Soft Light blend mode (soft light blending).
    SOFT_LIGHT = 1934387572

    # Difference blend mode (subtract colors).
    DIFFERENCE = 1684629094

    # Exclusion blend mode (exclude colors).
    EXCLUSION = 1936553316

    # Hue blend mode (apply hue).
    HUE = 1752524064

    # Saturation blend mode (apply saturation).
    SATURATION = 1935766560

    # Color blend mode (apply color).
    COLOR = 1668246642

    # Luminosity blend mode (apply luminosity).
    LUMINOSITY = 1819634976

    # Darker Color blend mode (darker of colors).
    DARKER_COLOR = 1684751212

    # Lighter Color blend mode (lighter of colors).
    LIGHTER_COLOR = 1818706796

    # Linear Burn blend mode (linear burn).
    LINEAR_BURN = 1818391150

    # Linear Dodge blend mode (linear dodge).
    LINEAR_DODGE = 1818518631

    # Linear Light blend mode (linear light).
    LINEAR_LIGHT = 1816947060

    # Vivid Light blend mode (vivid light).
    VIVID_LIGHT = 1984719220

    # Pin Light blend mode (pin light).
    PIN_LIGHT = 1884055924

    # Hard Mix blend mode (hard mix).
    HARD_MIX = 1749903736

    # Subtract blend mode (subtract colors).
    SUBTRACT = 1718842722

    # Divide blend mode (divide colors).
    DIVIDE = 1717856630

    # Dissolve blend mode.
    DISSOLVE = 1684632435

    # Pass-through blend mode.
    PASS_THROUGH = 1885434739

    # Blend mode is absent or not set yet.
    ABSENT = 0
