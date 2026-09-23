"""Represents global layer mask information."""

from typing import ClassVar


class GlobalLayerMaskInfo:
    """Represents global layer mask information."""
    Empty: ClassVar['GlobalLayerMaskInfo']


# Empty global layer mask info instance
GlobalLayerMaskInfo.Empty = GlobalLayerMaskInfo()

