from aspose_psd_foss.bigendianwriter import BigEndianWriter
from aspose_psd_foss.sections.psdheader import PsdHeader
from aspose_psd_foss.sections.psdimagedocumentstate import PsdImageDocumentState


class PsdImageWriter:
    @classmethod
    def save(cls, document: PsdImageDocumentState, stream, leave_open):
        writer = BigEndianWriter(stream, leave_open)
        try:
            writer.write(int(PsdHeader.PSD_SIGNATURE) & 0xFFFFFFFF)
            if document.Header is not None:
                document.Header.save(writer)
            document.ColorData.save(writer)
            document.ImageResourcesSection.save(writer)
            is_large = getattr(document.Header, 'IsLargeDocument', False) == True
            document.layer_and_mask_section.save(writer, is_large)
            document.ImageData.save(writer)
        finally:
            writer.dispose()

