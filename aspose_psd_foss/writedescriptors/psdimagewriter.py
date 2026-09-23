from aspose_psd_foss.sections.psdimagedocumentstate import PsdImageDocumentState
from aspose_psd_foss.bigendianwriter import BigEndianWriter
from aspose_psd_foss.sections.psdheader import PsdHeader


def save(document: PsdImageDocumentState, stream, leave_open: bool):
    writer = BigEndianWriter(stream, leave_open)
    try:
        writer.write(PsdHeader.PSD_SIGNATURE)
        document.header.save(writer) if document.header is not None else None
        document.color_data.save(writer)
        document.image_resources_section.save(writer)
        document.layer_and_mask_section.save(writer, document.header.is_large_document if document.header is not None else False)
        document.image_data.save(writer)
    finally:
        writer.dispose()
