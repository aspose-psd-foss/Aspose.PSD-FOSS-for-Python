from aspose_psd_foss.colormodes import ColorModes
from aspose_psd_foss.psdversion import PsdVersion
from aspose_psd_foss.bigendianreader import BigEndianReader
from aspose_psd_foss.bigendianwriter import BigEndianWriter
from aspose_psd_foss.coreexceptions.psdloadexception import PsdLoadException


class PsdHeader:
    """
    Contains the header information of a Photoshop document.
    """
    # Shared PSD/PSB file signature value (0x38425053 = '8BPS').
    PSD_SIGNATURE = 0x38425053

    # Shared PSD/PSB file signature value (0x38425053 = '8BPS').
    PSB_SIGNATURE = PSD_SIGNATURE

    # PSD version value.
    PSD_VERSION = 1

    # PSB large-document version value.
    PSB_VERSION = 2

    def __init__(self):
        self._width = 0
        self._height = 0
        self._channels = 0
        self._bit_depth = 0
        self._color_mode = ColorModes.RGB
        self._format_version = PsdVersion.PSD

    @property
    def width(self) -> int:
        """Gets the width of the image in pixels."""
        return self._width

    @property
    def height(self) -> int:
        """Gets the height of the image in pixels."""
        return self._height

    @property
    def channels(self) -> int:
        """Gets the number of channels in the image (e.g., 3 for RGB)."""
        return self._channels

    @property
    def bit_depth(self) -> int:
        """Gets the bit depth per channel (e.g., 8, 16, 32)."""
        return self._bit_depth

    @property
    def color_mode(self) -> ColorModes:
        """Gets the color mode of the image."""
        return self._color_mode

    @property
    def version(self) -> int:
        """Gets the raw PSD container version: 1 for PSD and 2 for PSB."""
        return int(self._format_version)

    @property
    def format_version(self) -> PsdVersion:
        """Gets the strongly typed PSD container version."""
        return self._format_version

    @property
    def is_large_document(self) -> bool:
        """Gets a value indicating whether the document uses the PSB large-document container."""
        return self._format_version == PsdVersion.PSB

    @classmethod
    def load(cls, reader: BigEndianReader) -> 'PsdHeader':
        """Loads the fixed PSD/PSB file header from the reader."""
        signature = reader.read_uint32()
        if signature != cls.PSD_SIGNATURE:
            raise PsdLoadException("Invalid PSD signature. Expected '8BPS' (0x38425053).")

        raw_version = reader.read_uint16()
        if raw_version not in (cls.PSD_VERSION, cls.PSB_VERSION):
            raise PsdLoadException(
                f"Unsupported PSD version: {raw_version}. Supported versions: {cls.PSD_VERSION} (PSD) and {cls.PSB_VERSION} (PSB)."
            )

        version = PsdVersion.PSB if raw_version == cls.PSB_VERSION else PsdVersion.PSD

        reserved = reader.read_bytes(6)
        if any(value != 0 for value in reserved):
            raise PsdLoadException("PSD header reserved bytes must be zero.")

        channels = reader.read_uint16()
        height = reader.read_int32()
        width = reader.read_int32()
        bit_depth = reader.read_uint16()
        color_mode = ColorModes(reader.read_uint16())

        cls._validate_header_fields(version, channels, height, width, bit_depth, color_mode)

        header = cls()
        header._width = width
        header._height = height
        header._channels = channels
        header._bit_depth = bit_depth
        header._color_mode = color_mode
        header._format_version = version
        return header

    @staticmethod
    def _validate_header_fields(version: int, channels: int, height: int, width: int,
                                bit_depth: int, color_mode: ColorModes) -> None:
        if not (1 <= channels <= 56):
            raise PsdLoadException(f"PSD header channel count {channels} is outside the supported range 1-56.")

        max_dimension = 300000 if version == PsdVersion.PSB else 30000
        if not (1 <= height <= max_dimension):
            raise PsdLoadException(
                f"PSD header height {height} is outside the supported range 1-{max_dimension} for this document version."
            )
        if not (1 <= width <= max_dimension):
            raise PsdLoadException(
                f"PSD header width {width} is outside the supported range 1-{max_dimension} for this document version."
            )

        if bit_depth not in (1, 8, 16, 32):
            raise PsdLoadException(
                f"PSD header bit depth {bit_depth} is not supported. Supported values are 1, 8, 16, and 32."
            )

        if not isinstance(color_mode, ColorModes):
            raise PsdLoadException(
                f"PSD header color mode {int(color_mode)} is not recognized by this implementation."
            )

    def save(self, writer: BigEndianWriter) -> None:
        """Writes the fixed PSD/PSB file header to the writer."""
        writer.write_uint(int(self._format_version))
        writer.write_all_bytes(bytes(6))
        writer.write_uint(self._channels)
        writer.write_int(self._height)
        writer.write_int(self._width)
        writer.write_uint(self._bit_depth)
        writer.write_uint(int(self._color_mode))

    def set_color_mode(self, color_mode: ColorModes) -> None:
        """Updates the header color mode for the compatibility subset that rewrites header metadata."""
        self._color_mode = color_mode

    def set_version(self, version: int) -> None:
        """Updates the PSD container version."""
        if version not in (PsdVersion.PSD, PsdVersion.PSB):
            raise ValueError("Supported PSD versions are 1 (PSD) and 2 (PSB).")

        self._format_version = version
