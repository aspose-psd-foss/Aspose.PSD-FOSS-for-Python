"""Loads parsed PSD/PSB document state from a stream."""

from ..bigendianreader import BigEndianReader
from ..sections.psdheader import PsdHeader
from ..sections.colordata import ColorData
from ..sections.imageresourcessection import ImageResourcesSection
from ..layerandmasksectionreader import LayerAndMaskSectionReader as LayerAndMaskSection
from ..sections.imagedata import ImageData
from ..coreexceptions.psdloadexception import PsdLoadException


class PsdImageDocumentState:
    def __init__(self, header, color_data, image_resources_section, layer_and_mask_section, image_data):
        self.header = header
        self.color_data = color_data
        self.image_resources_section = image_resources_section
        self.layer_and_mask_section = layer_and_mask_section
        self.image_data = image_data


def load(stream, leave_open):
    """Loads all supported PSD/PSB sections into memory.

    Args:
        stream: The buffered PSD/PSB stream.
        leave_open (bool): True to leave the stream open after loading; otherwise, False.

    Returns:
        PsdImageDocumentState: The parsed document state.
    """
    reader = BigEndianReader(stream, leave_open)
    try:
        header = PsdHeader.load(reader)
        color_data = ColorData.load(reader, header.color_mode)
        image_resources_section = ImageResourcesSection.load(reader)
        layer_and_mask_section = LayerAndMaskSection.load(
            reader, header.is_large_document
        )
        image_data = ImageData.load(
            reader,
            header.is_large_document,
            header.height,
            header.channels,
        )
        return PsdImageDocumentState(
            header,
            color_data,
            image_resources_section,
            layer_and_mask_section,
            image_data,
        )
    except PsdLoadException:
        raise
    except EOFError as exception:
        raise PsdLoadException(
            "Unexpected end of PSD/PSB data while reading the file structure."
        ) from exception
    except OSError as exception:
        raise PsdLoadException(
            "Failed to read PSD/PSB data from the source stream."
        ) from exception
    finally:
        reader.close()

