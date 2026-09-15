# Represents a PSD layer blend range.

class BlendRange:
    """Represents a PSD layer blend range."""

    def __init__(self, destination=0, source=0):
        self.destination = destination  # destination blend range
        self.source = source  # source blend range
