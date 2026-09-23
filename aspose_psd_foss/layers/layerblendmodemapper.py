from aspose_psd_foss.layers.blendmode import BlendMode


class LayerBlendModeMapper:
    """Maps between PSD blend mode keys and the public BlendMode enum."""

    # Gets the PSD blend mode key for the normal blend mode.
    NORMAL_BLEND_MODE_KEY = "norm"

    @classmethod
    def parse_blend_mode_key(cls, key):
        """Maps a PSD blend mode key to the public BlendMode enum.

        :param key: The 4-byte PSD blend mode key.
        :return: The mapped blend mode value.
        """
        if len(key) < 4:
            return BlendMode.NORMAL

        mode_key = key[:4].decode('ascii', errors='ignore')
        return {
            cls.NORMAL_BLEND_MODE_KEY: BlendMode.NORMAL,
            "mul ": BlendMode.MULTIPLY,
            "scrn": BlendMode.SCREEN,
            "diss": BlendMode.DISSOLVE,
            "over": BlendMode.OVERLAY,
            "dark": BlendMode.DARKEN,
            "lite": BlendMode.LIGHTEN,
            "div ": BlendMode.COLOR_DODGE,
            "idiv": BlendMode.COLOR_BURN,
            "burn": BlendMode.COLOR_BURN,
            "hLit": BlendMode.HARD_LIGHT,
            "hlit": BlendMode.HARD_LIGHT,
            "sLit": BlendMode.SOFT_LIGHT,
            "slit": BlendMode.SOFT_LIGHT,
            "diff": BlendMode.DIFFERENCE,
            "smud": BlendMode.EXCLUSION,
            "hue ": BlendMode.HUE,
            "sat ": BlendMode.SATURATION,
            "colr": BlendMode.COLOR,
            "lum ": BlendMode.LUMINOSITY,
            "lbrn": BlendMode.LINEAR_BURN,
            "lddg": BlendMode.LINEAR_DODGE,
            "vLit": BlendMode.VIVID_LIGHT,
            "lLit": BlendMode.LINEAR_LIGHT,
            "pLit": BlendMode.PIN_LIGHT,
            "hMix": BlendMode.HARD_MIX,
            "pass": BlendMode.PASS_THROUGH,
            "dkCl": BlendMode.DARKER_COLOR,
            "lgCl": BlendMode.LIGHTER_COLOR,
            "fsub": BlendMode.SUBTRACT,
            "fdiv": BlendMode.DIVIDE
        }.get(mode_key, BlendMode.NORMAL)

    @classmethod
    def get_blend_mode_key(cls, mode):
        """Maps the public BlendMode value back to a 4-byte PSD blend mode key.

        :param mode: The blend mode value to encode.
        :return: The encoded PSD blend mode key.
        """
        return {
            BlendMode.NORMAL: cls.NORMAL_BLEND_MODE_KEY,
            BlendMode.MULTIPLY: "mul ",
            BlendMode.SCREEN: "scrn",
            BlendMode.DISSOLVE: "diss",
            BlendMode.OVERLAY: "over",
            BlendMode.DARKEN: "dark",
            BlendMode.LIGHTEN: "lite",
            BlendMode.COLOR_DODGE: "div ",
            BlendMode.COLOR_BURN: "idiv",
            BlendMode.HARD_LIGHT: "hLit",
            BlendMode.SOFT_LIGHT: "sLit",
            BlendMode.DIFFERENCE: "diff",
            BlendMode.EXCLUSION: "smud",
            BlendMode.HUE: "hue ",
            BlendMode.SATURATION: "sat ",
            BlendMode.COLOR: "colr",
            BlendMode.LUMINOSITY: "lum ",
            BlendMode.LINEAR_BURN: "lbrn",
            BlendMode.LINEAR_DODGE: "lddg",
            BlendMode.VIVID_LIGHT: "vLit",
            BlendMode.LINEAR_LIGHT: "lLit",
            BlendMode.PIN_LIGHT: "pLit",
            BlendMode.HARD_MIX: "hMix",
            BlendMode.PASS_THROUGH: "pass",
            BlendMode.DARKER_COLOR: "dkCl",
            BlendMode.LIGHTER_COLOR: "lgCl",
            BlendMode.SUBTRACT: "fsub",
            BlendMode.DIVIDE: "fdiv"
        }.get(mode, cls.NORMAL_BLEND_MODE_KEY)
