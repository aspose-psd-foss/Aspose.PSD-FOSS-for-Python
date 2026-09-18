from typing import Optional

# Represents global layer mask information.

class GlobalLayerMaskInfo:
    """Represents global layer mask information."""
    EMPTY: Optional["GlobalLayerMaskInfo"] = None


# Initialize the static EMPTY instance
GlobalLayerMaskInfo.EMPTY = GlobalLayerMaskInfo()

