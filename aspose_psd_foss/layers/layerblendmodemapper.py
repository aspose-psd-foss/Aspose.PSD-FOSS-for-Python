from aspose_psd_foss.layers.blendmode import BlendMode

# Maps between PSD blend mode keys and the public BlendMode enum.
# internal static class LayerBlendModeMapper

# Gets the PSD blend mode key for the normal blend mode.
NORMAL_BLEND_MODE_KEY = "norm"


def parse_blend_mode_key(key: bytes):
    """
    Maps a PSD blend mode key to the public BlendMode enum.
    :param key: The 4-byte PSD blend mode key.
    :return: The mapped blend mode value.
    """
    if len(key) < 4:
        return BlendMode.Normal

    mode_key = key.decode('ascii')
    if mode_key == NORMAL_BLEND_MODE_KEY:
        return BlendMode.Normal
    elif mode_key == "mul ":
        return BlendMode.Multiply
    elif mode_key == "scrn":
        return BlendMode.Screen
    elif mode_key == "diss":
        return BlendMode.Dissolve
    elif mode_key == "over":
        return BlendMode.Overlay
    elif mode_key == "dark":
        return BlendMode.Darken
    elif mode_key == "lite":
        return BlendMode.Lighten
    elif mode_key == "div ":
        return BlendMode.ColorDodge
    elif mode_key == "idiv":
        return BlendMode.ColorBurn
    elif mode_key == "burn":
        return BlendMode.ColorBurn
    elif mode_key == "hLit":
        return BlendMode.HardLight
    elif mode_key == "hlit":
        return BlendMode.HardLight
    elif mode_key == "sLit":
        return BlendMode.SoftLight
    elif mode_key == "slit":
        return BlendMode.SoftLight
    elif mode_key == "diff":
        return BlendMode.Difference
    elif mode_key == "smud":
        return BlendMode.Exclusion
    elif mode_key == "hue ":
        return BlendMode.Hue
    elif mode_key == "sat ":
        return BlendMode.Saturation
    elif mode_key == "colr":
        return BlendMode.Color
    elif mode_key == "lum ":
        return BlendMode.Luminosity
    elif mode_key == "lbrn":
        return BlendMode.LinearBurn
    elif mode_key == "lddg":
        return BlendMode.LinearDodge
    elif mode_key == "vLit":
        return BlendMode.VividLight
    elif mode_key == "lLit":
        return BlendMode.LinearLight
    elif mode_key == "pLit":
        return BlendMode.PinLight
    elif mode_key == "hMix":
        return BlendMode.HardMix
    elif mode_key == "pass":
        return BlendMode.PassThrough
    elif mode_key == "dkCl":
        return BlendMode.DarkerColor
    elif mode_key == "lgCl":
        return BlendMode.LighterColor
    elif mode_key == "fsub":
        return BlendMode.Subtract
    elif mode_key == "fdiv":
        return BlendMode.Divide
    else:
        return BlendMode.Normal


def get_blend_mode_key(mode):
    """
    Maps the public BlendMode value back to a 4-byte PSD blend mode key.
    :param mode: The blend mode value to encode.
    :return: The encoded PSD blend mode key.
    """
    if mode == BlendMode.Normal:
        return NORMAL_BLEND_MODE_KEY
    elif mode == BlendMode.Multiply:
        return "mul "
    elif mode == BlendMode.Screen:
        return "scrn"
    elif mode == BlendMode.Dissolve:
        return "diss"
    elif mode == BlendMode.Overlay:
        return "over"
    elif mode == BlendMode.Darken:
        return "dark"
    elif mode == BlendMode.Lighten:
        return "lite"
    elif mode == BlendMode.ColorDodge:
        return "div "
    elif mode == BlendMode.ColorBurn:
        return "idiv"
    elif mode == BlendMode.HardLight:
        return "hLit"
    elif mode == BlendMode.SoftLight:
        return "sLit"
    elif mode == BlendMode.Difference:
        return "diff"
    elif mode == BlendMode.Exclusion:
        return "smud"
    elif mode == BlendMode.Hue:
        return "hue "
    elif mode == BlendMode.Saturation:
        return "sat "
    elif mode == BlendMode.Color:
        return "colr"
    elif mode == BlendMode.Luminosity:
        return "lum "
    elif mode == BlendMode.LinearBurn:
        return "lbrn"
    elif mode == BlendMode.LinearDodge:
        return "lddg"
    elif mode == BlendMode.VividLight:
        return "vLit"
    elif mode == BlendMode.LinearLight:
        return "lLit"
    elif mode == BlendMode.PinLight:
        return "pLit"
    elif mode == BlendMode.HardMix:
        return "hMix"
    elif mode == BlendMode.PassThrough:
        return "pass"
    elif mode == BlendMode.DarkerColor:
        return "dkCl"
    elif mode == BlendMode.LighterColor:
        return "lgCl"
    elif mode == BlendMode.Subtract:
        return "fsub"
    elif mode == BlendMode.Divide:
        return "fdiv"
    else:
        return NORMAL_BLEND_MODE_KEY
