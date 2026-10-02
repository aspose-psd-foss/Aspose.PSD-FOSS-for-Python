from __future__ import annotations

from typing import List

from aspose_psd_foss.bigendianreader import BigEndianReader
from aspose_psd_foss.bigendianwriter import BigEndianWriter
from aspose_psd_foss.coreexceptions.psdloadexception import PsdLoadException
from aspose_psd_foss.psdversion import PsdVersion
from aspose_psd_foss.colormodes import ColorModes


class PsdHeader:
    """
    Contains the header information of a Photoshop document.
    """

    PSD_SIGNATURE: int = 0x38425053
    PSB_SIGNATURE: int = PSD_SIGNATURE
    PSD_VERSION: int = 1
    PSB_VERSION: int = 2

    def __init__(self) -> None:
        self.width: int = 0
        self.height: int = 0
        self.channels: int = 0
        self.bit_depth: int = 0
        self.color_mode: ColorModes = ColorModes.BITMAP
        self.format_version: PsdVersion = PsdVersion.Psd

    @property
    def version(self) -> int:
        """Gets the raw PSD container version: 1 for PSD and 2 for PSB."""
        return int(self.format_version)

    @property
    def is_large_document(self) -> bool:
        """Gets a value indicating whether the document uses the PSB large-document container."""
        return self.format_version == PsdVersion.Psb

    @classmethod
    def load(cls, reader: BigEndianReader) -> "PsdHeader":
        """Loads the fixed PSD/PSB file header from the reader."""
        signature = reader.read_uint32()
        if signature != cls.PSD_SIGNATURE:
            raise PsdLoadException("Invalid PSD signature. Expected '8BPS' (0x38425053).")

        raw_version = reader.read_uint16()
        if raw_version not in (cls.PSD_VERSION, cls.PSB_VERSION):
            raise PsdLoadException(
                f"Unsupported PSD version: {raw_version}. Supported versions: {cls.PSD_VERSION} (PSD) and {cls.PSB_VERSION} (PSB)."
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

        cls._validate_header_fields(version, channels, height, width, bit_depth, color_mode)

        header = cls()
        header.width = width
        header.height = height
        header.channels = channels
        header.bit_depth = bit_depth
        header.color_mode = color_mode
        header.format_version = version
        return header

    @classmethod
    def _validate_header_fields(
        cls,
        version: PsdVersion,
        channels: int,
        height: int,
        width: int,
        bit_depth: int,
        color_mode: ColorModes,
    ) -> None:
        """Validates PSD/PSB header invariants before exposing the parsed document state."""
        if not (1 <= channels <= 56):
            raise PsdLoadException(f"PSD header channel count {channels} is outside the supported range 1-56.")

        max_dimension = 300000 if version == PsdVersion.Psb else 30000
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
                f"PSD header color mode {(int(color_mode) if isinstance(color_mode, int) else color_mode)} is not recognized by this implementation."
            )

    def save(self, writer: BigEndianWriter) -> None:
        """Writes the fixed PSD/PSB file header to the writer."""
        writer.write_uint16(self.format_version.value)
        writer.write(bytes(6))
        writer.write_uint16(self.channels)
        writer.write_int32(self.height)
        writer.write_int32(self.width)
        writer.write_uint16(self.bit_depth)
        writer.write_uint16(self.color_mode.value)

    def set_color_mode(self, color_mode: ColorModes) -> None:
        """Updates the header color mode for the compatibility subset that rewrites header metadata."""
        self.color_mode = color_mode

    def set_version(self, version: int) -> None:
        """Updates the PSD container version."""
        if version not in (int(PsdVersion.Psd), int(PsdVersion.Psb)):
            raise ValueError(
                f"Supported PSD versions are {int(PsdVersion.Psd)} (PSD) and {int(PsdVersion.Psb)} (PSB)."
            )
        self.format_version = PsdVersion(version)
