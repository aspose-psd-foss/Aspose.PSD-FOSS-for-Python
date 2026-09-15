from aspose_psd_foss.colormodes import ColorModes
from aspose_psd_foss.coreexceptions.psdloadexception import PsdLoadException
from aspose_psd_foss.psdversion import PsdVersion


class PsdHeader:
    """Contains the header information of a Photoshop document."""

    # Shared PSD/PSB file signature value (0x38425053 = '8BPS').
    PSD_SIGNATURE = 0x38425053
    # Shared PSD/PSB file signature value (0x38425053 = '8BPS').
    PSB_SIGNATURE = PSD_SIGNATURE

    # PSD version value.
    PSD_VERSION = 1
    # PSB large-document version value.
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
        """Gets the raw PSD container version: 1 for PSD and 2 for PSB."""
        return int(self.format_version)

    @property
    def is_large_document(self):
        """Gets a value indicating whether the document uses the PSB large-document container."""
        return self.format_version == PsdVersion.Psb

    @staticmethod
    def load(reader):
        """Loads the fixed PSD/PSB file header from the reader."""
        signature = reader.read_uint32()
        if signature != PsdHeader.PSD_SIGNATURE:
            raise PsdLoadException(
                "Invalid PSD signature. Expected '8BPS' (0x38425053)."
            )

        raw_version = reader.read_uint16()
        if raw_version != PsdVersion.Psd.value and raw_version != PsdVersion.Psb.value:
            raise PsdLoadException(
                f"Unsupported PSD version: {raw_version}. Supported versions: "
                f"{PsdHeader.PSD_VERSION} (PSD) and {PsdHeader.PSB_VERSION} (PSB)."
            )

        version = PsdVersion(raw_version)

        reserved = reader.read_bytes(6)
        if any(value != 0 for value in reserved):
            raise PsdLoadException("PSD header reserved bytes must be zero.")

        channels = reader.read_uint16()
        height = reader.read_int32()
        width = reader.read_int32()
        bit_depth = reader.read_uint16()
        color_mode = ColorModes(reader.read_uint16())

        PsdHeader.validate_header_fields(
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
    def validate_header_fields(
        version, channels, height, width, bit_depth, color_mode
    ):
        """Validates PSD/PSB header invariants before exposing the parsed document state."""
        if channels < 1 or channels > 56:
            raise PsdLoadException(
                f"PSD header channel count {channels} is outside the supported range 1-56."
            )

        max_dimension = 300000 if version == PsdVersion.Psb else 30000
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
                f"PSD header bit depth {bit_depth} is not supported. "
                "Supported values are 1, 8, 16, and 32."
            )
        if not isinstance(color_mode, ColorModes):
            raise PsdLoadException(
                f"PSD header color mode {int(color_mode)} is not recognized by this implementation."
            )

    def save(self, writer):
        """Writes the fixed PSD/PSB file header to the writer."""
        writer.write_uint16(int(self.format_version))
        writer.write_bytes(b'\x00' * 6)
        writer.write_uint16(self.channels)
        writer.write_int32(self.height)
        writer.write_int32(self.width)
        writer.write_uint16(self.bit_depth)
        writer.write_uint16(int(self.color_mode))

    def set_color_mode(self, color_mode):
        """Updates the header color mode for the compatibility subset that rewrites header metadata."""
        self.color_mode = color_mode

    def set_version(self, version):
        """Updates the PSD container version."""
        if version != PsdVersion.Psd.value and version != PsdVersion.Psb.value:
            raise ValueError("Supported PSD versions are 1 (PSD) and 2 (PSB).")
        self.format_version = PsdVersion(version)
