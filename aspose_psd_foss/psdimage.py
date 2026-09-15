import io
from typing import List, Optional, Sequence

from aspose_psd_foss.image import Image
from aspose_psd_foss.color_modes import ColorModes
from aspose_psd_foss.sections.psd_header import PsdHeader
from aspose_psd_foss.layers.layer import Layer
from aspose_psd_foss.size import Size
from aspose_psd_foss.resource_block import ResourceBlock
from aspose_psd_foss.resources.preserved_resource_block import PreservedResourceBlock
from aspose_psd_foss.layers.layer_resource import LayerResource
from aspose_psd_foss.layers.global_layer_mask_info import GlobalLayerMaskInfo
from aspose_psd_foss.resources.psd_resource_info import PsdResourceInfo
from aspose_psd_foss.sections.psd_color_data_info import PsdColorDataInfo
from aspose_psd_foss.resources.indexed_color_palette_info import IndexedColorPaletteInfo
from aspose_psd_foss.compression_method import CompressionMethod
from aspose_psd_foss.sections.psd_image_data_info import PsdImageDataInfo
from aspose_psd_foss.sections.image_data_kind import ImageDataKind
from aspose_psd_foss.sections.color_data import ColorData
from aspose_psd_foss.resources.unknown_resource import UnknownResource
from aspose_psd_foss.sections.psd_image_document_state import PsdImageDocumentState
from aspose_psd_foss.loaders.psd_image_loader import PsdImageLoader
from aspose_psd_foss.write_descriptors.psd_image_writer import PsdImageWriter


class PsdImage(Image):
    """Represents a PSD image that can be loaded, inspected, and saved without rendering."""

    def __init__(self, stream: io.BytesIO, leave_open: bool):
        """Initializes a new instance of the PsdImage class over an internal working stream."""
        self._stream = stream
        self._leave_open = leave_open
        self._disposed = False
        self._document: PsdImageDocumentState = PsdImageDocumentState.empty()

    @property
    def width(self) -> int:
        """Gets the document width in pixels."""
        return self._document.header.width if self._document.header else 0

    @property
    def height(self) -> int:
        """Gets the document height in pixels."""
        return self._document.header.height if self._document.header else 0

    @property
    def _channels(self) -> int:
        """Gets the document channel count from the PSD header."""
        return self._document.header.channels if self._document.header else 0

    @property
    def bits_per_channel(self) -> int:
        """Gets the number of bits stored per channel."""
        return self._document.header.bit_depth if self._document.header else 0

    @property
    def color_mode(self) -> ColorModes:
        """Gets the PSD color mode reported by the header."""
        return self._document.header.color_mode if self._document.header else ColorModes.RGB

    @color_mode.setter
    def color_mode(self, value: ColorModes):
        if self._document.header:
            self._document.header.set_color_mode(value)

    @property
    def version(self) -> int:
        """Gets or sets the Aspose.PSD-compatible API version number."""
        return 6

    @version.setter
    def version(self, value: int):
        if value != 6:
            raise ValueError(
                f"Supported Aspose.PSD-compatible API version is 6, got {value}"
            )

    @property
    def _header(self) -> PsdHeader:
        """Gets the parsed PSD/PSB header object."""
        if not self._document.header:
            raise RuntimeError("PSD/PSB header is not loaded.")
        return self._document.header

    @property
    def _is_large_document(self) -> bool:
        """Gets a value indicating whether the loaded document uses the PSB large-document container."""
        return (
            self._document.header.is_large_document
            if self._document.header
            else False
        )

    @property
    def _is_psb(self) -> bool:
        """Gets a value indicating whether the loaded document is a PSB file; this is equivalent to IsLargeDocument."""
        return self._is_large_document

    @property
    def layers(self) -> List[Layer]:
        """Gets the parsed layer collection."""
        return list(self._document.layer_and_mask_section.layers)

    @layers.setter
    def layers(self, value: Sequence[Layer]):
        self._document = self._document.with_layer_and_mask_section(
            self._document.layer_and_mask_section.with_layers(
                value if value is not None else []
            )
        )

    @property
    def channels_count(self) -> int:
        """Gets the PSD channels count."""
        return self._channels

    @property
    def size(self) -> Size:
        """Gets the image size."""
        return Size(self.width, self.height)

    @property
    def active_layer(self) -> Optional[Layer]:
        """Gets or sets the active layer."""
        return self.layers[0] if self.layers else None

    @active_layer.setter
    def active_layer(self, value: Optional[Layer]):
        raise NotImplementedError(
            "Changing the active layer is not supported by this FOSS build."
        )

    @property
    def _layer_count(self) -> int:
        """Gets the number of parsed layers in the document."""
        return len(self.layers)

    @property
    def _has_layers(self) -> bool:
        """Gets a value indicating whether the document contains at least one parsed layer."""
        return len(self._document.layer_and_mask_section.layers) > 0

    @property
    def _has_image_resources(self) -> bool:
        """Gets a value indicating whether the document contains any parsed image resources."""
        return self._document.image_resources_section.has_resources

    @property
    def _resource_count(self) -> int:
        """Gets the number of parsed image resource blocks."""
        return len(self._document.image_resources_section.resources)

    @property
    def image_resources(self) -> List[ResourceBlock]:
        """Gets or sets the PSD image resources."""
        return [
            PreservedResourceBlock(r)
            for r in self._document.image_resources_section.resources
        ]

    @image_resources.setter
    def image_resources(self, value: List[ResourceBlock]):
        raise NotImplementedError(
            "Changing image resources is not supported by this FOSS build."
        )

    @property
    def global_layer_resources(self) -> List[LayerResource]:
        """Gets or sets the global layer resources."""
        return []

    @global_layer_resources.setter
    def global_layer_resources(self, value: List[LayerResource]):
        raise NotImplementedError(
            "Changing global layer resources is not supported by this FOSS build."
        )

    @property
    def global_layer_mask_info(self) -> GlobalLayerMaskInfo:
        """Gets the global layer mask info."""
        return GlobalLayerMaskInfo.empty()

    @property
    def is_flatten(self) -> bool:
        """Gets a value indicating whether the PSD image is flattened."""
        return len(self._document.layer_and_mask_section.layers) == 0

    @property
    def has_transparency_data(self) -> bool:
        """Gets or sets a value indicating whether first alpha channel contains the transparency data for the merged result when specifying layers data."""
        return False

    @has_transparency_data.setter
    def has_transparency_data(self, value: bool):
        raise NotImplementedError(
            "Changing transparency data semantics is not supported by this FOSS build."
        )

    @property
    def _resources(self) -> List[PsdResourceInfo]:
        """Gets a read-only summary of the parsed image resource blocks."""
        return [r.to_public_info() for r in self._document.image_resources_section.resources]

    @property
    def _has_color_mode_data(self) -> bool:
        """Gets a value indicating whether the document contains Color Mode Data bytes."""
        return len(self._document.color_data.raw_data) > 0

    @property
    def _color_data_info(self) -> PsdColorDataInfo:
        """Gets a read-only summary of the parsed Color Mode Data section."""
        return self._document.color_data.to_public_info()

    @property
    def _indexed_palette(self) -> Optional[IndexedColorPaletteInfo]:
        """Gets the parsed indexed palette summary, when the Color Mode Data section contains one."""
        return self._color_data_info.indexed_palette

    @property
    def _has_merged_image_data(self) -> bool:
        """Gets a value indicating whether the document contains merged image data payload bytes."""
        return len(self._document.image_data.raw_data) > 0

    @property
    def compression(self) -> CompressionMethod:
        """Gets the compression method used by the merged image data section."""
        return self._document.image_data.compression

    @property
    def _image_data_info(self) -> PsdImageDataInfo:
        """Gets a read-only summary of the parsed merged image data structure."""
        return self._document.image_data.to_public_info()

    @property
    def _image_data_kind(self) -> ImageDataKind:
        """Gets the structural kind of the merged image data payload."""
        return self._document.image_data.structure.kind

    @property
    def _uses_prediction(self) -> bool:
        """Gets a value indicating whether ZIP prediction is used by the merged image data payload."""
        return self._document.image_data.structure.uses_prediction

    @property
    def global_angle(self) -> int:
        """Gets the parsed global angle from the image resources, when present."""
        return getattr(self, "_global_angle", 0)

    @global_angle.setter
    def global_angle(self, value: int):
        self._global_angle = value

    @property
    def _has_icc_profile(self) -> bool:
        """Gets a value indicating whether an embedded ICC profile resource is present."""
        return False

    @property
    def _is_icc_profile_untagged(self) -> Optional[bool]:
        """Gets the parsed untagged ICC profile flag, when the corresponding resource is present."""
        return None

    @property
    def _parsed_color_data(self) -> ColorData:
        """Gets the parsed color mode data details for internal verification and tests."""
        return self._document.color_data

    @property
    def _parsed_resources(self) -> List[UnknownResource]:
        """Gets the parsed image resources for internal verification and tests."""
        return self._document.image_resources_section.resources

    @classmethod
    def load(cls, file_path: str) -> "PsdImage":
        """Loads a PSD image from a file path."""
        if file_path is None:
            raise ValueError("file_path is None")
        try:
            with open(file_path, "rb") as f:
                return cls.load_stream(f)
        except FileNotFoundError as e:
            raise FileNotFoundError(f"File not found: {file_path}") from e

    @classmethod
    def load_stream(cls, stream: io.BytesIO) -> "PsdImage":
        """Loads a PSD image from a readable stream."""
        if stream is None:
            raise ValueError("stream is None")

        original_position = 0
        restore_position = stream.seekable()
        if restore_position:
            original_position = stream.tell()

        try:
            buffered = io.BytesIO()
            buffered.write(stream.read())
            buffered.seek(0)
            return cls._load(buffered, leave_open=False)
        finally:
            if restore_position:
                stream.seek(original_position)

    @classmethod
    def _load(cls, stream: io.BytesIO, leave_open: bool) -> "PsdImage":
        image = cls(stream, leave_open)
        image._document = PsdImageLoader.load(stream, leave_open)
        return image

    def save(self, file_path: str):
        """Saves the image to a file path."""
        if file_path is None:
            raise ValueError("file_path is None")
        with open(file_path, "wb") as f:
            self._save(f, leave_open=False)

    def save_stream(self, stream: io.BytesIO):
        """Saves the image to a writable stream."""
        if stream is None:
            raise ValueError("stream is None")
        self._save(stream, leave_open=True)

    def _save(self, stream: io.BytesIO, leave_open: bool):
        """Saves the current document to a stream with configurable stream ownership."""
        if self._disposed:
            raise RuntimeError("PsdImage has been disposed")
        PsdImageWriter.save(self._document, stream, leave_open)

    def dispose(self):
        """Releases the image and optionally the underlying stream."""
        if self._disposed:
            return
        self._disposed = True
        if not self._leave_open:
            self._stream.close()

