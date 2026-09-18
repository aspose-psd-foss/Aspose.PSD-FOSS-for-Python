"""Defines PSD layer mask flags."""

from enum import IntFlag


class LayerMaskFlags(IntFlag):
    """Defines PSD layer mask flags."""
    NONE = 0
    RELATIVE_TO_LAYER = 1
    DISABLED = 2
    INVERTED_WHEN_BLENDING = 4
    USER_MASK_FROM_RENDERING_OTHER_DATA = 8
    USER_OR_VECTOR_MASKS_HAVE_PARAMETERS = 16
