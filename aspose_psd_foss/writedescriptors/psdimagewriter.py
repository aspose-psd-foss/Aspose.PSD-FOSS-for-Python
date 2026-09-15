# Writes parsed PSD/PSB document state to a stream.
import sys

from aspose_psd_foss.bigendianwriter import BigEndianWriter
from aspose_psd_foss.sections.psdheader import PsdHeader


class PsdImageWriter:
    """Saves a parsed document state to a writable stream.

    Args:
        document: The parsed document state to write.
        stream: The destination stream.
        leave_open: True to leave the stream open after saving; otherwise, False.
    """

    @staticmethod
    def save(document, stream, leave_open):
        writer = BigEndianWriter(stream, leave_open)
        try:
            writer.write(int(PsdHeader.PSD_SIGNATURE) & 0xFFFFFFFF)
            if getattr(document, "header", None) is not None:
                document.header.save(writer)
            document.color_data.save(writer)
            document.image_resources_section.save(writer)
            is_large = getattr(document.header, "is_large_document", False)
            document.layer_and_mask_section.save(writer, is_large)
            document.image_data.save(writer)
        finally:
            writer.dispose()

