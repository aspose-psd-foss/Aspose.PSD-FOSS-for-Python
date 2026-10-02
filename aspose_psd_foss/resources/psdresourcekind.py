from enum import Enum


# Identifies the semantic classification exposed for an image resource block.
class PsdResourceKind(Enum):
    # The resource is not parsed semantically and remains raw-preserved only.
    UNKNOWN = 0

    # Reserved for future semantic parsing of the global layer-effects lighting angle resource.
    GLOBAL_ANGLE = 1

    # Reserved for future semantic parsing of an embedded ICC profile payload.
    ICC_PROFILE = 2

    # Reserved for future semantic parsing of the intentionally-untagged ICC profile flag.
    ICC_UNTAGGED_PROFILE = 3
