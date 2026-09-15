from __future__ import annotations


from aspose_psd_foss.compression_method import CompressionMethod
from aspose_psd_foss.color_data import ColorData
from aspose_psd_foss.image_data import ImageData
from aspose_psd_foss.image_resources_section import ImageResourcesSection
from aspose_psd_foss.layer_and_mask_section import LayerAndMaskSection
from aspose_psd_foss.psd_header import PsdHeader


class PsdImageDocumentState:
    """
    Stores parsed PSD/PSB document sections used by PsdImage.
    """

    # Gets an empty document state before a PSD/PSB stream has been parsed.
    empty = None  # will be initialized after class definition

    def __init__(
        self,
        header: PsdHeader | None,
        color_data: ColorData,
        image_resources_section: ImageResourcesSection,
        layer_and_mask_section: LayerAndMaskSection,
        image_data: ImageData,
    ):
        """
        Initializes a new instance of the PsdImageDocumentState class.

        :param header: The parsed PSD/PSB header.
        :param color_data: The parsed Color Mode Data section.
        :param image_resources_section: The parsed Image Resources section.
        :param layer_and_mask_section: The parsed Layer and Mask
            Information section.
        :param image_data: The parsed merged Image Data section.
        """
        self.header = header
        self.color_data = color_data
        self.image_resources_section = image_resources_section
        self.layer_and_mask_section = layer_and_mask_section
        self.image_data = image_data

    # Gets the parsed PSD/PSB header.
    @property
    def header(self) -> PsdHeader | None:
        return self._header

    @header.setter
    def header(self, value: PsdHeader | None) -> None:
        self._header = value

    # Gets the parsed Color Mode Data section.
    @property
    def color_data(self) -> ColorData:
        return self._color_data

    @color_data.setter
    def color_data(self, value: ColorData) -> None:
        self._color_data = value

    # Gets the parsed and raw-preserved Image Resources section.
    @property
    def image_resources_section(self) -> ImageResourcesSection:
        return self._image_resources_section

    @image_resources_section.setter
    def image_resources_section(self, value: ImageResourcesSection) -> None:
        self._image_resources_section = value

    # Gets the parsed and raw-preserved Layer and Mask Information section.
    @property
    def layer_and_mask_section(self) -> LayerAndMaskSection:
        return self._layer_and_mask_section

    @layer_and_mask_section.setter
    def layer_and_mask_section(self, value: LayerAndMaskSection) -> None:
        self._layer_and_mask_section = value

    # Gets the parsed merged Image Data section.
    @property
    def image_data(self) -> ImageData:
        return self._image_data

    @image_data.setter
    def image_data(self, value: ImageData) -> None:
        self._image_data = value

    def with_layer_and_mask_section(
        self,
        layer_and_mask_section: LayerAndMaskSection,
    ) -> "PsdImageDocumentState":
        """
        Creates a state copy with a replaced Layer and Mask Information
        section.

        :param layer_and_mask_section: The replacement Layer and Mask
            Information section.
        :return: The updated document state.
        """
        return PsdImageDocumentState(
            self.header,
            self.color_data,
            self.image_resources_section,
            layer_and_mask_section,
            self.image_data,
        )


# Initialize the static empty instance
PsdImageDocumentState.empty = PsdImageDocumentState(
    None,
    ColorData.empty,
    ImageResourcesSection.empty,
    LayerAndMaskSection.empty,
    ImageData(CompressionMethod.Raw, []),
)
