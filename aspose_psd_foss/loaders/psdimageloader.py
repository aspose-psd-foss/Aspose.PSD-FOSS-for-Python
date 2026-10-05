import io

from aspose_psd_foss.bigendianreader import BigEndianReader
from aspose_psd_foss.coreexceptions.psdloadexception import PsdLoadException
from aspose_psd_foss.sections.colordata import ColorData
from aspose_psd_foss.sections.imagedata import ImageData
from aspose_psd_foss.sections.imageresourcessection import ImageResourcesSection
from aspose_psd_foss.sections.layerandmasksection import LayerAndMaskSection
from aspose_psd_foss.layerandmasksectionreader import LayerAndMaskSectionReader
from aspose_psd_foss.sections.psdheader import PsdHeader
from aspose_psd_foss.sections.psdimagedocumentstate import PsdImageDocumentState


class PsdImageLoader:
    @classmethod
    def load(cls, stream: io.BufferedIOBase, leave_open: bool):
        reader = BigEndianReader(stream, leave_open)
        try:
            header = PsdHeader.load(reader)
            color_data = ColorData.load(reader, header.color_mode)
            image_resources_section = ImageResourcesSection.load(reader)
            layer_and_mask_section = LayerAndMaskSectionReader.load(reader, header.is_large_document)
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
                "Unexpected end of PSD/PSB data while reading the file structure.", exception
            )
        except IOError as exception:
            raise PsdLoadException(
                "Failed to read PSD/PSB data from the source stream.", exception
            )
        finally:
            reader.dispose()


# Optional backward‑compatible alias
ImageLoader = PsdImageLoader

__all__ = ["PsdImageLoader", "ImageLoader"]
