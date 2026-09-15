import enum


# Represents the supported PSD container versions.
class PsdVersion(enum.Enum):
    # Standard PSD document format.
    PSD = 1

    # Large-document PSB format.
    PSB = 2
