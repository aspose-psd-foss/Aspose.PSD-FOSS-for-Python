"""Writes parsed PSD/PSB document state to a stream."""
from aspose_psd_foss.sections.psdimagedocumentstate import PsdImageDocumentState
from aspose_psd_foss.bigendianwriter import BigEndianWriter
from aspose_psd_foss.sections.psdheader import PsdHeader
from aspose_psd_foss.sections.layerandmasksection import LayerAndMaskSection


def save(document: PsdImageDocumentState, stream, leave_open: bool):
    """Saves a parsed document state to a writable stream.

    Args:
        document: The parsed document state to write.
        stream: The destination stream.
        leave_open: True to leave the stream open after saving; otherwise, False.
    """
    writer = BigEndianWriter(stream, leave_open)
    try:
        writer.write(b'8BPS')
        if document.header is not None:
            document.header.save(writer)
        document.color_data.save(writer)
        document.image_resources_section.save(writer)
        is_large = (
            document.header.is_large_document
            if document.header is not None and getattr(document.header, "is_large_document", False)
            else False
        )
        LayerAndMaskSection.save(document.layer_and_mask_section, writer, is_large)
        document.image_data.save(writer)
    finally:
        writer.dispose()

