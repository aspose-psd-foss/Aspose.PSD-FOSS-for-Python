from aspose_psd_foss.colormodes import ColorModes
from aspose_psd_foss.coreexceptions.psdloadexception import PsdLoadException


class PsdVersion:
    """PSD container version values."""
    PSD = 1
    PSB = 2


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

    # --- properties ---

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
    def color_mode(self) -> int:
        """Gets the color mode of the image."""
        return self._color_mode

    @property
    def version(self) -> int:
        """Gets the raw PSD container version: 1 for PSD and 2 for PSB."""
        return int(self._format_version)

    @property
    def format_version(self) -> int:
        """Gets the strongly typed PSD container version."""
        return self._format_version

    @property
    def is_large_document(self) -> bool:
        """Gets a value indicating whether the document uses the PSB large-document container."""
        return self._format_version == PsdVersion.PSB

    # --- loading ---

    @staticmethod
    def load(reader) -> "PsdHeader":
        """
        Loads the fixed PSD/PSB file header from the reader.

        :param reader: The reader positioned at the start of the file header.
        :return: The parsed :class:`PsdHeader` instance.
        """
        signature = reader.read_uint32()
        if signature != PsdHeader.PSD_SIGNATURE:
            raise PsdLoadException(
                "Invalid PSD signature. Expected '8BPS' (0x38425053)."
            )

        raw_version = reader.read_uint16()
        if raw_version != PsdVersion.PSD and raw_version != PsdVersion.PSB:
            raise PsdLoadException(
                f"Unsupported PSD version: {raw_version}. "
                f"Supported versions: {PsdHeader.PSD_VERSION} (PSD) and "
                f"{PsdHeader.PSB_VERSION} (PSB)."
            )

        version = raw_version

        reserved = reader.read_bytes(6)
        if any(value != 0 for value in reserved):
            raise PsdLoadException("PSD header reserved bytes must be zero.")

        channels = reader.read_uint16()
        height = reader.read_int32()
        width = reader.read_int32()
        bit_depth = reader.read_uint16()
        color_mode = reader.read_uint16()

        PsdHeader._validate_header_fields(
            version, channels, height, width, bit_depth, color_mode
        )

        header = PsdHeader()
        header._width = width
        header._height = height
        header._channels = channels
        header._bit_depth = bit_depth
        header._color_mode = color_mode
        header._format_version = version
        return header

    @staticmethod
    def _validate_header_fields(
        version: int,
        channels: int,
        height: int,
        width: int,
        bit_depth: int,
        color_mode: int,
    ) -> None:
        """
        Validates PSD/PSB header invariants before exposing the parsed document state.

        :raises PsdLoadException: Thrown when a header field is outside the supported PSD/PSB range.
        """
        if channels < 1 or channels > 56:
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
                f"PSD header bit depth {bit_depth} is not supported. "
                f"Supported values are 1, 8, 16, and 32."
            )

        if not PsdHeader._is_color_mode_defined(color_mode):
            raise PsdLoadException(
                f"PSD header color mode {color_mode} is not recognized by this implementation."
            )

    @staticmethod
    def _is_color_mode_defined(color_mode: int) -> bool:
        return color_mode in (
            ColorModes.BITMAP,
            ColorModes.GRAYSCALE,
            ColorModes.INDEXED,
            ColorModes.RGB,
            ColorModes.CMYK,
            ColorModes.MULTICHANNEL,
            ColorModes.DUOTONE,
            ColorModes.LAB,
        )

    # --- saving ---

    def save(self, writer) -> None:
        """
        Writes the fixed PSD/PSB file header to the writer.

        :param writer: The destination writer.
        """
        writer.write_uint16(self._format_version)
        writer.write_bytes(bytes(6))
        writer.write_uint16(self._channels)
        writer.write_int32(self._height)
        writer.write_int32(self._width)
        writer.write_uint16(self._bit_depth)
        writer.write_uint16(self._color_mode)

    def set_color_mode(self, color_mode: int) -> None:
        """
        Updates the header color mode for the compatibility subset that rewrites header metadata.

        :param color_mode: The color mode to store.
        """
        self._color_mode = color_mode

    def set_version(self, version: int) -> None:
        """
        Updates the PSD container version.

        :param version: The PSD container version to store.
        """
        if version != PsdVersion.PSD and version != PsdVersion.PSB:
            raise ValueError(
                f"Supported PSD versions are 1 (PSD) and 2 (PSB). Got: {version}"
            )

        self._format_version = version