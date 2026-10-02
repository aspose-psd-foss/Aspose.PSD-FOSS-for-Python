from __future__ import annotations

from typing import TYPE_CHECKING

from aspose_psd_foss.sections.psdheader import PsdHeader
from aspose_psd_foss.sections.colordata import ColorData
from aspose_psd_foss.sections.imageresourcessection import ImageResourcesSection
from aspose_psd_foss.sections.layerandmasksection import LayerAndMaskSection
from aspose_psd_foss.sections.imagedata import ImageData, ImageDataStructure
from aspose_psd_foss.compressionmethod import CompressionMethod

if TYPE_CHECKING:
    from aspose_psd_foss.sections.layerandmasksection import LayerAndMaskSection


class PsdImageDocumentState:
    """Stores parsed PSD/PSB document sections used by PsdImage."""

    Empty: "PsdImageDocumentState"

    @classmethod
    def empty(cls) -> "PsdImageDocumentState":
        """Gets an empty document state before a PSD/PSB stream has been parsed."""
        return cls(
            None,
            ColorData.empty(),
            ImageResourcesSection.empty(),
            LayerAndMaskSection.empty(),
            ImageData(
                CompressionMethod.RAW,
                b"",               # empty bytes for raw image data
                structure=ImageDataStructure.create_raw(0)
            ),
        )

    def __init__(
        self,
        header: PsdHeader | None,
        color_data: ColorData,
        image_resources_section: ImageResourcesSection,
        layer_and_mask_section: LayerAndMaskSection,
        image_data: ImageData,
    ) -> None:
        self.header = header
        self.color_data = color_data
        self.image_resources_section = image_resources_section
        self._layer_and_mask_section = layer_and_mask_section
        self.image_data = image_data

    @property
    def Header(self) -> PsdHeader | None:
        return self.header

    @property
    def ColorData(self) -> ColorData:
        return self.color_data

    @property
    def ImageResourcesSection(self) -> ImageResourcesSection:
        return self.image_resources_section

    @property
    def layer_and_mask_section(self) -> LayerAndMaskSection:
        return self._layer_and_mask_section

    @property
    def ImageData(self) -> ImageData:
        return self.image_data

    def with_layer_and_mask_section(
        self, layer_and_mask_section: LayerAndMaskSection
    ) -> "PsdImageDocumentState":
        """Creates a state copy with a replaced Layer and Mask Information section."""
        return PsdImageDocumentState(
            self.header,
            self.color_data,
            self.image_resources_section,
            layer_and_mask_section,
            self.image_data,
        )


PsdImageDocumentState.Empty = PsdImageDocumentState.empty()

