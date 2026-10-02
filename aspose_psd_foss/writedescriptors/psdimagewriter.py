from aspose_psd_foss.bigendianwriter import BigEndianWriter
from aspose_psd_foss.sections.psdheader import PsdHeader
from aspose_psd_foss.sections.psdimagedocumentstate import PsdImageDocumentState


class PsdImageWriter:
    """
    Writes parsed PSD/PSB document state to a stream.
    """

    @staticmethod
    def save(document: PsdImageDocumentState, stream, leave_open: bool) -> None:
        """
        Saves a parsed document state to a writable stream.

        :param document: The parsed document state to write.
        :param stream: The destination stream.
        :param leave_open: true to leave the stream open after saving; otherwise, false.
        """
        writer = BigEndianWriter(stream, leave_open)
        try:
            writer.write_uint32(int(PsdHeader.PSD_SIGNATURE))
            if document.header is not None:
                document.header.save(writer)
            document.color_data.save(writer)
            document.image_resources_section.save(writer)
            document.layer_and_mask_section.save(
                writer, document.header is not None and document.header.is_large_document
            )
            document.image_data.save(writer)
        finally:
            writer.dispose()