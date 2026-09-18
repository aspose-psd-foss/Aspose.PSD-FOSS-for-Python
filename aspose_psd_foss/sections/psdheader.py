from aspose_psd_foss.bigendianreader import BigEndianReader
from aspose_psd_foss.bigendianwriter import BigEndianWriter
from aspose_psd_foss.colormodes import ColorModes
from aspose_psd_foss.psdversion import PsdVersion
from aspose_psd_foss.coreexceptions.psdloadexception import PsdLoadException


class PsdHeader:
    PSD_SIGNATURE = 0x38425053
    PSB_SIGNATURE = PSD_SIGNATURE
    PSD_VERSION = 1
    PSB_VERSION = 2

    def __init__(self):
        self.width = 0
        self.height = 0
        self.channels = 0
        self.bit_depth = 0
        self.color_mode = None
        self.format_version = None

    @property
    def version(self):
        return int(self.format_version.value)

    @property
    def is_large_document(self):
        return self.format_version == PsdVersion.PSB

    @staticmethod
    def load(reader: BigEndianReader) -> 'PsdHeader':
        signature = reader.read_uint32()
        if signature != PsdHeader.PSD_SIGNATURE:
            raise PsdLoadException(
                "Invalid PSD signature. Expected '8BPS' (0x38425053)."
            )

        raw_version = reader.read_uint16()
        if raw_version not in (PsdVersion.PSD.value, PsdVersion.PSB.value):
            raise PsdLoadException(
                f"Unsupported PSD version: {raw_version}. "
                f"Supported versions: {PsdHeader.PSD_VERSION} (PSD) and "
                f"{PsdHeader.PSB_VERSION} (PSB)."
            )
        version = PsdVersion(raw_version)

        reserved = reader.read_bytes(6)
        if any(b != 0 for b in reserved):
            raise PsdLoadException(
                "PSD header reserved bytes must be zero."
            )

        channels = reader.read_uint16()
        height = reader.read_int32()
        width = reader.read_int32()
        bit_depth = reader.read_uint16()
        color_mode = ColorModes(reader.read_uint16())

        PsdHeader._validate_header_fields(
            version, channels, height, width, bit_depth, color_mode
        )

        header = PsdHeader()
        header.width = width
        header.height = height
        header.channels = channels
        header.bit_depth = bit_depth
        header.color_mode = color_mode
        header.format_version = version
        return header

    @staticmethod
    def _validate_header_fields(
        version: PsdVersion,
        channels: int,
        height: int,
        width: int,
        bit_depth: int,
        color_mode: ColorModes,
    ):
        if not (1 <= channels <= 56):
            raise PsdLoadException(
                f"PSD header channel count {channels} is outside the supported range 1-56."
            )

        max_dimension = 300000 if version == PsdVersion.PSB else 30000
        if height < 1 or height > max_dimension:
            raise PsdLoadException(
                f"PSD header height {height} is outside the supported range "
                f"1-{max_dimension} for this document version."
            )
        if width < 1 or width > max_dimension:
            raise PsdLoadException(
                f"PSD header width {width} is outside the supported range "
                f"1-{max_dimension} for this document version."
            )
        if bit_depth not in (1, 8, 16, 32):
            raise PsdLoadException(
                "PSD header bit depth {bit_depth} is not supported. "
                "Supported values are 1, 8, 16, and 32."
            )
        if not isinstance(color_mode, ColorModes):
            raise PsdLoadException(
                f"PSD header color mode {(int(color_mode))} is not recognized by this implementation."
            )

    def save(self, writer: BigEndianWriter):
        writer.write_uint16(self.format_version.value)
        writer.write_all_bytes(b'\x00' * 6)
        writer.write_uint16(self.channels)
        writer.write_int32(self.height)
        writer.write_int32(self.width)
        writer.write_uint16(self.bit_depth)
        writer.write_uint16(self.color_mode.value)

    def set_color_mode(self, color_mode: ColorModes):
        self.color_mode = color_mode

    def set_version(self, version: int):
        if version not in (PsdVersion.PSD.value, PsdVersion.PSB.value):
            raise ValueError(
                f"Supported PSD versions are {PsdHeader.PSD_VERSION} (PSD) and "
                f"{PsdHeader.PSB_VERSION} (PSB)."
            )
        self.format_version = PsdVersion(version)
