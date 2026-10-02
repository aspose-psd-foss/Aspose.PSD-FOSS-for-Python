"""
Python port of Aspose.PSD.FileFormats.Psd.PsdImage

Represents a PSD image that can be loaded, inspected, and saved without rendering.
"""

from __future__ import annotations

import os
from typing import List, Optional

from aspose_psd_foss.colormodes import ColorModes
from aspose_psd_foss.compressionmethod import CompressionMethod
from aspose_psd_foss.coreexceptions.argumentnullexception import ArgumentNullException
from aspose_psd_foss.coreexceptions.notsupportedexception import NotSupportedException
from aspose_psd_foss.image import Image
from aspose_psd_foss.layers.globallayermaskinfo import GlobalLayerMaskInfo
from aspose_psd_foss.layers.layer import Layer
from aspose_psd_foss.layers.layerresource import LayerResource
from aspose_psd_foss.resourceblock import ResourceBlock
from aspose_psd_foss.resources.indexedcolorpaletteinfo import IndexedColorPaletteInfo
from aspose_psd_foss.resources.preservedresourceblock import PreservedResourceBlock
from aspose_psd_foss.resources.unknownresource import UnknownResource
from aspose_psd_foss.sections.colordata import ColorData
from aspose_psd_foss.sections.imagedatakind import ImageDataKind
from aspose_psd_foss.sections.psdcolordatainfo import PsdColorDataInfo
from aspose_psd_foss.sections.psdheader import PsdHeader
from aspose_psd_foss.sections.psdimagedatainfo import PsdImageDataInfo
from aspose_psd_foss.sections.psdimagedocumentstate import PsdImageDocumentState
from aspose_psd_foss.size import Size



# ---------------------------------------------------------------------------
# PsdImage
# ---------------------------------------------------------------------------

class PsdImage(Image):
    """
    Represents a PSD image that can be loaded, inspected, and saved without rendering.
    """

    def __init__(self, stream, leave_open: bool):
        # Stores the underlying source or destination stream.
        self._stream = stream
        # Indicates whether the underlying stream must remain open after disposal.
        self._leave_open = leave_open
        # Tracks whether the instance has already been disposed.
        self._disposed = False
        # Stores the parsed PSD/PSB document sections.
        self._document = PsdImageDocumentState.empty()

    # -- Properties ---------------------------------------------------------

    @property
    def width(self) -> int:
        """Gets the document width in pixels."""
        header = self._document.header
        return header.width if header else 0

    @property
    def height(self) -> int:
        """Gets the document height in pixels."""
        header = self._document.header
        return header.height if header else 0

    @property
    def channels(self) -> int:
        """Gets the document channel count from the PSD header."""
        header = self._document.header
        return header.channels if header else 0

    @property
    def bits_per_channel(self) -> int:
        """Gets the number of bits stored per channel."""
        header = self._document.header
        return header.bit_depth if header else 0

    @property
    def color_mode(self) -> ColorModes:
        """Gets the PSD color mode reported by the header."""
        header = self._document.header
        return header.color_mode if header else ColorModes.RGB

    @color_mode.setter
    def color_mode(self, value: ColorModes):
        self.header.set_color_mode(value)

    @property
    def version(self) -> int:
        """Gets or sets the Aspose.PSD-compatible API version number."""
        return 6

    @version.setter
    def version(self, value: int):
        if value != 6:
            raise ValueError(
                f"Supported Aspose.PSD-compatible API version is 6. (value={value})"
            )

    @property
    def header(self) -> PsdHeader:
        """Gets the parsed PSD/PSB header object."""
        if self._document.header is None:
            raise RuntimeError("PSD/PSB header is not loaded.")
        return self._document.header

    @property
    def is_large_document(self) -> bool:
        """Gets whether the loaded document uses the PSB large-document container."""
        header = self._document.header
        return bool(header and header.is_large_document)

    @property
    def is_psb(self) -> bool:
        """Equivalent to :attr:`is_large_document`."""
        return self.is_large_document

    @property
    def layers(self) -> List[Layer]:
        """Gets the parsed layer collection."""
        return list(self._document.layer_and_mask_section.layers)

    @layers.setter
    def layers(self, value: List[Layer]):
        value = value or []
        self._document = self._document.with_layer_and_mask_section(
            self._document.layer_and_mask_section.with_layers(value)
        )

    @property
    def channels_count(self) -> int:
        """Gets the PSD channels count."""
        return self.channels

    @property
    def size(self) -> Size:
        """Gets the image size."""
        return Size(self.width, self.height)

    @property
    def active_layer(self) -> Optional[Layer]:
        """Gets the active layer."""
        layers = self.layers
        return layers[0] if layers else None

    @active_layer.setter
    def active_layer(self, value):
        raise NotSupportedException(
            "Changing the active layer is not supported by this FOSS build."
        )

    @property
    def layer_count(self) -> int:
        """Gets the number of parsed layers in the document."""
        return len(self.layers)

    @property
    def has_layers(self) -> bool:
        """Gets whether the document contains at least one parsed layer."""
        return len(self._document.layer_and_mask_section.layers) > 0

    @property
    def has_image_resources(self) -> bool:
        """Gets whether the document contains any parsed image resources."""
        return self._document.image_resources_section.has_resources

    @property
    def resource_count(self) -> int:
        """Gets the number of parsed image resource blocks."""
        return len(self._document.image_resources_section.resources)

    @property
    def image_resources(self) -> List[ResourceBlock]:
        """Gets or sets the PSD image resources."""
        return [
            PreservedResourceBlock(resource)
            for resource in self._document.image_resources_section.resources
        ]

    @image_resources.setter
    def image_resources(self, value):
        raise NotSupportedException(
            "Changing image resources is not supported by this FOSS build."
        )

    @property
    def global_layer_resources(self) -> List[LayerResource]:
        """Gets or sets the global layer resources."""
        return []

    @global_layer_resources.setter
    def global_layer_resources(self, value):
        raise NotSupportedException(
            "Changing global layer resources is not supported by this FOSS build."
        )

    @property
    def global_layer_mask_info(self) -> GlobalLayerMaskInfo:
        """Gets the global layer mask info."""
        return GlobalLayerMaskInfo.empty()

    @property
    def is_flatten(self) -> bool:
        """Gets whether the PSD image is flattened."""
        return len(self._document.layer_and_mask_section.layers) == 0

    @property
    def has_transparency_data(self) -> bool:
        """Gets or sets whether the first alpha channel contains transparency data."""
        return False

    @has_transparency_data.setter
    def has_transparency_data(self, value):
        raise NotSupportedException(
            "Changing transparency data semantics is not supported by this FOSS build."
        )

    @property
    def resources(self):
        """Gets a read-only summary of the parsed image resource blocks."""
        return [
            resource.to_public_info()
            for resource in self._document.image_resources_section.resources
        ]

    @property
    def has_color_mode_data(self) -> bool:
        """Gets whether the document contains Color Mode Data bytes."""
        return len(self._document.color_data.raw_data) > 0

    @property
    def color_data_info(self) -> PsdColorDataInfo:
        """Gets a read-only summary of the parsed Color Mode Data section."""
        return self._document.color_data.to_public_info()

    @property
    def indexed_palette(self) -> Optional[IndexedColorPaletteInfo]:
        """Gets the parsed indexed palette summary, when present."""
        return self.color_data_info.indexed_palette

    @property
    def has_merged_image_data(self) -> bool:
        """Gets whether the document contains merged image data payload bytes."""
        return len(self._document.image_data.raw_data) > 0

    @property
    def compression(self) -> CompressionMethod:
        """Gets the compression method used by the merged image data section."""
        return self._document.image_data.compression

    @property
    def image_data_info(self) -> PsdImageDataInfo:
        """Gets a read-only summary of the parsed merged image data structure."""
        return self._document.image_data.to_public_info()

    @property
    def image_data_kind(self) -> ImageDataKind:
        """Gets the structural kind of the merged image data payload."""
        return self._document.image_data.structure.kind

    @property
    def uses_prediction(self) -> bool:
        """Gets whether ZIP prediction is used by the merged image data payload."""
        return self._document.image_data.structure.uses_prediction

    # GlobalAngle: lightweight unknown-only parser does not reconstruct
    # ID-specific semantic values, so this is a simple pass-through property.
    global_angle: int = 0

    @property
    def has_icc_profile(self) -> bool:
        """Gets whether an embedded ICC profile resource is present."""
        return False

    @property
    def is_icc_profile_untagged(self) -> Optional[bool]:
        """Gets the parsed untagged ICC profile flag, when present."""
        return None

    @property
    def parsed_color_data(self) -> ColorData:
        """Gets the parsed color mode data details for internal verification/tests."""
        return self._document.color_data

    @property
    def parsed_resources(self) -> List[UnknownResource]:
        """Gets the parsed image resources for internal verification/tests."""
        return self._document.image_resources_section.resources

    # -- Loading ------------------------------------------------------------

    @staticmethod
    def load(file_path_or_stream) -> PsdImage:
        """
        Loads a PSD image from a file path or a readable stream.

        Mirrors the two overloads ``Load(string)`` and ``Load(Stream)``.
        """
        if isinstance(file_path_or_stream, (str, bytes, os.PathLike)):
            file_path = file_path_or_stream
            if file_path is None:
                raise ValueError("file_path must not be None")
            if not os.path.isfile(file_path):
                raise FileNotFoundError(f"File not found: {file_path}")
            with open(file_path, "rb") as stream:
                return PsdImage._load_from_stream(stream)

        stream = file_path_or_stream
        if stream is None:
            raise ArgumentNullException("stream must not be None")
        return PsdImage._load_from_stream(stream)

    @staticmethod
    def _load_from_stream(stream) -> "PsdImage":
        original_position = 0
        restore_position = getattr(stream, "seekable", lambda: False)()
        if restore_position:
            original_position = stream.tell()

        try:
            import io

            buffered_stream = io.BytesIO()
            buffered_stream.write(stream.read())
            buffered_stream.seek(0)
            return PsdImage._load(buffered_stream, leave_open=False)
        finally:
            if restore_position:
                stream.seek(original_position)

    @staticmethod
    def _load(stream, leave_open: bool) -> "PsdImage":
        from aspose_psd_foss.loaders.psdimageloader import PsdImageLoader
        image = PsdImage(stream, leave_open)
        image._document = PsdImageLoader.load(stream, leave_open)
        return image

    # -- Saving -------------------------------------------------------------

    def save(self, file_path_or_stream):
        """
        Saves the image to a file path or a writable stream.

        Mirrors the ``Save(string)`` and ``Save(Stream)`` overloads.
        """
        if isinstance(file_path_or_stream, (str, bytes, os.PathLike)):
            file_path = file_path_or_stream
            if file_path is None:
                raise ValueError("file_path must not be None")
            with open(file_path, "wb") as stream:
                self._save(stream, leave_open=False)
            return

        stream = file_path_or_stream
        if stream is None:
            raise ValueError("stream must not be None")
        self._save(stream, leave_open=True)

    def _save(self, stream, leave_open: bool):
        from aspose_psd_foss.writedescriptors.psdimagewriter import PsdImageWriter
        if self._disposed:
            raise RuntimeError("PsdImage has been disposed.")
        PsdImageWriter.save(self._document, stream, leave_open)

    # -- Disposal -----------------------------------------------------------

    def dispose(self):
        """Releases the image and optionally the underlying stream."""
        if self._disposed:
            return
        self._disposed = True
        if not self._leave_open:
            self._stream.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.dispose()
        return False