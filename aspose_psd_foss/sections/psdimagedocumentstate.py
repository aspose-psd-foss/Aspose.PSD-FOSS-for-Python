from aspose_psd_foss.sections.colordata import ColorData, PsdColorDataKind as ColorDataKind
from aspose_psd_foss.sections.imagedata import ImageData
from ..compressionmethod import CompressionMethod
from aspose_psd_foss.sections.imageresourcessection import ImageResourcesSection
from aspose_psd_foss.sections.layerandmasksection import LayerAndMaskSection
from aspose_psd_foss.sections.psdheader import PsdHeader
from .imagedatastructure import ImageDataStructure


class PsdImageDocumentState:
    """
    Stores parsed PSD/PSB document sections used by :py:class:`PsdImage`.
    """

    Empty = None  # type: PsdImageDocumentState

    def __init__(self, header, color_data, image_resources_section, layer_and_mask_section, image_data):
        """
        Initializes a new instance of the :py:class:`PsdImageDocumentState` class.

        :param header: The parsed PSD/PSB header.
        :type header: PsdHeader or None
        :param color_data: The parsed Color Mode Data section.
        :type color_data: ColorData
        :param image_resources_section: The parsed Image Resources section.
        :type image_resources_section: ImageResourcesSection
        :param layer_and_mask_section: The parsed Layer and Mask Information section.
        :type layer_and_mask_section: LayerAndMaskSection
        :param image_data: The parsed merged Image Data section.
        :type image_data: ImageData
        """
        self._header = header
        self._color_data = color_data
        self._image_resources_section = image_resources_section
        self._layer_and_mask_section = layer_and_mask_section
        self._image_data = image_data

    @property
    def header(self):
        """
        Gets the parsed PSD/PSB header.

        :return: The parsed PSD/PSB header.
        :rtype: PsdHeader or None
        """
        return self._header

    @property
    def color_data(self):
        """
        Gets the parsed Color Mode Data section.

        :return: The parsed Color Mode Data section.
        :rtype: ColorData
        """
        return self._color_data

    @property
    def image_resources_section(self):
        """
        Gets the parsed and raw-preserved Image Resources section.

        :return: The parsed and raw-preserved Image Resources section.
        :rtype: ImageResourcesSection
        """
        return self._image_resources_section

    @property
    def layer_and_mask_section(self):
        """
        Gets the parsed and raw-preserved Layer and Mask Information section.

        :return: The parsed and raw-preserved Layer and Mask Information section.
        :rtype: LayerAndMaskSection
        """
        return self._layer_and_mask_section

    @property
    def image_data(self):
        """
        Gets the parsed merged Image Data section.

        :return: The parsed merged Image Data section.
        :rtype: ImageData
        """
        return self._image_data

    def with_layer_and_mask_section(self, layer_and_mask_section):
        """
        Creates a state copy with a replaced Layer and Mask Information section.

        :param layer_and_mask_section: The replacement Layer and Mask Information section.
        :type layer_and_mask_section: LayerAndMaskSection
        :return: The updated document state.
        :rtype: PsdImageDocumentState
        """
        return PsdImageDocumentState(
            self._header,
            self._color_data,
            self._image_resources_section,
            layer_and_mask_section,
            self._image_data)


# Initialize Empty static field
PsdImageDocumentState.Empty = PsdImageDocumentState(
    None,
    ColorData(raw_data=b"", kind=ColorDataKind(0)),
    ImageResourcesSection.Empty,
    LayerAndMaskSection.Empty,
    ImageData(CompressionMethod.RAW, b"", structure=ImageDataStructure(
        kind=0,
        row_length_field_size=0,
        row_byte_counts=[],
        compressed_payload_length=0,
        uses_prediction=False
    ))
)
