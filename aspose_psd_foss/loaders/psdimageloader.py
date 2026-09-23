"""Loads parsed PSD/PSB document state from a stream."""

from aspose_psd_foss.bigendianreader import BigEndianReader, EndOfStreamException
from ..sections.psdheader import PsdHeader
from ..sections.colordata import ColorData
from ..sections.imageresourcessection import ImageResourcesSection
from ..sections.layerandmasksection import LayerAndMaskSection
from ..sections.imagedata import ImageData
from ..sections.psdimagedocumentstate import PsdImageDocumentState
from aspose_psd_foss.coreexceptions.psdloadexception import PsdLoadException


class PsdImageLoader:
    """Loads parsed PSD/PSB document state from a stream."""

    @classmethod
    def load(cls, stream, leave_open):
        """Loads all supported PSD/PSB sections into memory.

        Args:
            stream: The buffered PSD/PSB stream.
            leave_open: True to leave the stream open after loading; otherwise, False.

        Returns:
            The parsed document state.
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
        except EndOfStreamException as exception:
            raise PsdLoadException(
                "Unexpected end of PSD/PSB data while reading the file structure.", exception)
        except OSError as exception:
            raise PsdLoadException(
                "Failed to read PSD/PSB data from the source stream.", exception)
        finally:
            reader.close()

