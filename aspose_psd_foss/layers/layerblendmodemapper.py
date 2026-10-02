from aspose_psd_foss.layers.blendmode import BlendMode


class LayerBlendModeMapper:
    NORMAL_BLEND_MODE_KEY = "norm"

    @classmethod
    def parse_blend_mode_key(cls, key):
        if len(key) < 4:
            return BlendMode.Normal
        mode_key = key.decode('ascii')
        return {
            cls.NORMAL_BLEND_MODE_KEY: BlendMode.Normal,
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

    @classmethod
    def get_blend_mode_key(cls, mode):
        return {
            BlendMode.Normal: cls.NORMAL_BLEND_MODE_KEY,
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
        }.get(mode, cls.NORMAL_BLEND_MODE_KEY)
