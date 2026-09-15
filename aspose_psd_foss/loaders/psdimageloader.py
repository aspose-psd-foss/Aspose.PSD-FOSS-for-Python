# loads parsed psd/psb document state from a stream.
import sys
from aspose_psd_foss.sections.psd_image_document_state import PsdImageDocumentState
from aspose_psd_foss.big_endian_reader import BigEndianReader
from aspose_psd_foss.sections.psd_header import PsdHeader
from aspose_psd_foss.sections.color_data import ColorData
from aspose_psd_foss.sections.image_resources_section import ImageResourcesSection
from aspose_psd_foss.sections.layer_and_mask_section import LayerAndMaskSection
from aspose_psd_foss.sections.image_data import ImageData
from aspose_psd_foss.core_exceptions.psd_load_exception import PsdLoadException


def load(stream, leave_open):
    """
    loads all supported psd/psb sections into memory.

    :param stream: the buffered psd/psb stream.
    :param leave_open: true to leave the stream open after loading; otherwise, false.
    :return: the parsed document state.
    """
    reader = BigEndianReader(stream, leave_open)
    try:
        header = PsdHeader.load(reader)
        color_data = ColorData.load(reader, header.color_mode)
        image_resources_section = ImageResourcesSection.load(reader)
        layer_and_mask_section = LayerAndMaskSection.load(reader, header.is_large_document)
        image_data = ImageData.load(
            reader,
            header.is_large_document,
            header.height,
            header.channels)

        return PsdImageDocumentState(
            header,
            color_data,
            image_resources_section,
            layer_and_mask_section,
            image_data)
    except PsdLoadException:
        raise
    except EOFError as exception:
        raise PsdLoadException("Unexpected end of PSD/PSB data while reading the file structure.", exception) from exception
    except OSError as exception:
        raise PsdLoadException("Failed to read PSD/PSB data from the source stream.", exception) from exception
    finally:
        # dispose of the reader
        dispose = getattr(reader, "dispose", None)
        if callable(dispose):
            dispose()
        else:
            close = getattr(reader, "close", None)
            if callable(close):
                close()

