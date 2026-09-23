from enum import Flag, auto


class LayerMaskFlags(Flag):
    """
    Defines PSD layer mask flags.
    """
    none = 0
    relative_to_layer = 1
    disabled = 2
    inverted_when_blending = 4
    user_mask_from_rendering_other_data = 8
    user_or_vector_masks_have_parameters = 16
