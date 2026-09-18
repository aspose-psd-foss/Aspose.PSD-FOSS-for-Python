# layers/layerblendmodmapper.py
from aspose_psd_foss.layers.blendmode import BlendMode

# Maps between PSD blend mode keys and the public BlendMode enum.
# Gets the PSD blend mode key for the normal blend mode.
NORMAL_BLEND_MODE_KEY = "norm"


def parse_blend_mode_key(key):
    """
    Maps a PSD blend mode key to the public BlendMode enum.

    :param key: The 4-byte PSD blend mode key (bytes).
    :return: The mapped blend mode value.
    """
    if len(key) < 4:
        return BlendMode.Normal

    mode_key = key.decode("ascii")
    return {
        NORMAL_BLEND_MODE_KEY: BlendMode.Normal,
        "mul ": BlendMode.Multiply,
        "scrn": BlendMode.Screen,
        "diss": BlendMode.Dissolve,
        "over": BlendMode.Overlay,
        "dark": BlendMode.Darken,
        "lite": BlendMode.Lighten,
        "div ": BlendMode.ColorDodge,
        "idiv": BlendMode.ColorBurn,
        "burn": BlendMode.ColorBurn,
        "hLit": BlendMode.HardLight,
        "hlit": BlendMode.HardLight,
        "sLit": BlendMode.SoftLight,
        "slit": BlendMode.SoftLight,
        "diff": BlendMode.Difference,
        "smud": BlendMode.Exclusion,
        "hue ": BlendMode.Hue,
        "sat ": BlendMode.Saturation,
        "colr": BlendMode.Color,
        "lum ": BlendMode.Luminosity,
        "lbrn": BlendMode.LinearBurn,
        "lddg": BlendMode.LinearDodge,
        "vLit": BlendMode.VividLight,
        "lLit": BlendMode.LinearLight,
        "pLit": BlendMode.PinLight,
        "hMix": BlendMode.HardMix,
        "pass": BlendMode.PassThrough,
        "dkCl": BlendMode.DarkerColor,
        "lgCl": BlendMode.LighterColor,
        "fsub": BlendMode.Subtract,
        "fdiv": BlendMode.Divide,
    }.get(mode_key, BlendMode.Normal)


def get_blend_mode_key(mode):
    """
    Maps the public BlendMode value back to a 4-byte PSD blend mode key.

    :param mode: The blend mode value to encode.
    :return: The encoded PSD blend mode key.
    """
    return {
        BlendMode.Normal: NORMAL_BLEND_MODE_KEY,
        BlendMode.Multiply: "mul ",
        BlendMode.Screen: "scrn",
        BlendMode.Dissolve: "diss",
        BlendMode.Overlay: "over",
        BlendMode.Darken: "dark",
        BlendMode.Lighten: "lite",
        BlendMode.ColorDodge: "div ",
        BlendMode.ColorBurn: "idiv",
        BlendMode.HardLight: "hLit",
        BlendMode.SoftLight: "sLit",
        BlendMode.Difference: "diff",
        BlendMode.Exclusion: "smud",
        BlendMode.Hue: "hue ",
        BlendMode.Saturation: "sat ",
        BlendMode.Color: "colr",
        BlendMode.Luminosity: "lum ",
        BlendMode.LinearBurn: "lbrn",
        BlendMode.LinearDodge: "lddg",
        BlendMode.VividLight: "vLit",
        BlendMode.LinearLight: "lLit",
        BlendMode.PinLight: "pLit",
        BlendMode.HardMix: "hMix",
        BlendMode.PassThrough: "pass",
        BlendMode.DarkerColor: "dkCl",
        BlendMode.LighterColor: "lgCl",
        BlendMode.Subtract: "fsub",
        BlendMode.Divide: "fdiv",
    }.get(mode, NORMAL_BLEND_MODE_KEY)
