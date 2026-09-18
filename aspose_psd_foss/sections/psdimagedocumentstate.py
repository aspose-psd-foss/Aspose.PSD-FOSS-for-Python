from __future__ import annotations

from typing import Optional

from ..compressionmethod import CompressionMethod
from .colordata import ColorData
from .imagedata import ImageData
from .imagedatastructure import ImageDataStructure
from .imagedatakind import ImageDataKind
from .imageresourcessection import ImageResourcesSection
from .layerandmasksection import LayerAndMaskSection
from .psdheader import PsdHeader

# Ensure the EMPTY attribute exists on the classes before we assign actual values
setattr(ImageResourcesSection, "EMPTY", None)  # type: ignore[attr-defined]
setattr(LayerAndMaskSection, "EMPTY", None)  # type: ignore[attr-defined]

ImageResourcesSection.EMPTY = ImageResourcesSection(b"", {})  # type: ignore[attr-defined]
LayerAndMaskSection.EMPTY = LayerAndMaskSection()  # type: ignore[attr-defined]

class PsdImageDocumentState:
    Empty: Optional["PsdImageDocumentState"] = None

    def __init__(
        self,
        header: Optional[PsdHeader],
        color_data: ColorData,
        image_resources_section: ImageResourcesSection,
        layer_and_mask_section: LayerAndMaskSection,
        image_data: ImageData,
    ):
        self._header = header
        self._color_data = color_data
        self._image_resources_section = image_resources_section
        self._layer_and_mask_section = layer_and_mask_section
        self._image_data = image_data

    @property
    def header(self) -> Optional[PsdHeader]:
        return self._header

    @property
    def color_data(self) -> ColorData:
        return self._color_data

    @property
    def image_resources_section(self) -> ImageResourcesSection:
        return self._image_resources_section

    @property
    def layer_and_mask_section(self) -> LayerAndMaskSection:
        return self._layer_and_mask_section

    @property
    def image_data(self) -> ImageData:
        return self._image_data

    def with_layer_and_mask_section(self, layer_and_mask_section: LayerAndMaskSection) -> "PsdImageDocumentState":
        return PsdImageDocumentState(
            self.header,
            self.color_data,
            self.image_resources_section,
            layer_and_mask_section,
            self.image_data,
        )

PsdImageDocumentState.Empty = PsdImageDocumentState(
    None,
    ColorData.EMPTY,
    ImageResourcesSection.EMPTY,
    LayerAndMaskSection.EMPTY,  # type: ignore[attr-defined]
    ImageData(
        CompressionMethod.RAW,
        b"",
        ImageDataStructure(
            kind=ImageDataKind.RAW,
            row_length_field_size=0,
            row_byte_counts=[],
            compressed_payload_length=0,
            uses_prediction=False,
        ),
    ),
)
