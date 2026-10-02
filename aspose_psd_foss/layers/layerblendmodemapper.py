from aspose_psd_foss.layers.blendmode import BlendMode


class LayerBlendModeMapper:
    NORMAL_BLEND_MODE_KEY = "norm"

    @classmethod
    def parse_blend_mode_key(cls, key):
        if len(key) < 4:
            return BlendMode.NORMAL
        mode_key = key.decode('ascii')
        return {
            cls.NORMAL_BLEND_MODE_KEY: BlendMode.NORMAL,
            "mul ": BlendMode.MULTIPLY,
            "scrn": BlendMode.SCREEN,
            "diss": BlendMode.DISSOLVE,
            "over": BlendMode.OVERLAY,
            "dark": BlendMode.DARKEN,
            "lite": BlendMode.LIGHTEN,
            "div ": BlendMode.COLORDODGE,
            "idiv": BlendMode.COLORBURN,
            "burn": BlendMode.COLORBURN,
            "hLit": BlendMode.HARDLIGHT,
            "hlit": BlendMode.HARDLIGHT,
            "sLit": BlendMode.SOFTLIGHT,
            "slit": BlendMode.SOFTLIGHT,
            "diff": BlendMode.DIFFERENCE,
            "smud": BlendMode.EXCLUSION,
            "hue ": BlendMode.HUE,
            "sat ": BlendMode.SATURATION,
            "colr": BlendMode.COLOR,
            "lum ": BlendMode.LUMINOSITY,
            "lbrn": BlendMode.LINEARBURN,
            "lddg": BlendMode.LINEARDODGE,
            "vLit": BlendMode.VIVIDLIGHT,
            "lLit": BlendMode.LINEARLIGHT,
            "pLit": BlendMode.PINLIGHT,
            "hMix": BlendMode.HARDMIX,
            "pass": BlendMode.PASSTHROUGH,
            "dkCl": BlendMode.DARKERCOLOR,
            "lgCl": BlendMode.LIGHTERCOLOR,
            "fsub": BlendMode.SUBTRACT,
            "fdiv": BlendMode.DIVIDE,
        }.get(mode_key, BlendMode.NORMAL)

    @classmethod
    def get_blend_mode_key(cls, mode):
        return {
            BlendMode.NORMAL: cls.NORMAL_BLEND_MODE_KEY,
            BlendMode.MULTIPLY: "mul ",
            BlendMode.SCREEN: "scrn",
            BlendMode.DISSOLVE: "diss",
            BlendMode.OVERLAY: "over",
            BlendMode.DARKEN: "dark",
            BlendMode.LIGHTEN: "lite",
            BlendMode.COLORDODGE: "div ",
            BlendMode.COLORBURN: "idiv",
            BlendMode.HARDLIGHT: "hLit",
            BlendMode.SOFTLIGHT: "sLit",
            BlendMode.DIFFERENCE: "diff",
            BlendMode.EXCLUSION: "smud",
            BlendMode.HUE: "hue ",
            BlendMode.SATURATION: "sat ",
            BlendMode.COLOR: "colr",
            BlendMode.LUMINOSITY: "lum ",
            BlendMode.LINEARBURN: "lbrn",
            BlendMode.LINEARDODGE: "lddg",
            BlendMode.VIVIDLIGHT: "vLit",
            BlendMode.LINEARLIGHT: "lLit",
            BlendMode.PINLIGHT: "pLit",
            BlendMode.HARDMIX: "hMix",
            BlendMode.PASSTHROUGH: "pass",
            BlendMode.DARKERCOLOR: "dkCl",
            BlendMode.LIGHTERCOLOR: "lgCl",
            BlendMode.SUBTRACT: "fsub",
            BlendMode.DIVIDE: "fdiv",
        }.get(mode, cls.NORMAL_BLEND_MODE_KEY)
