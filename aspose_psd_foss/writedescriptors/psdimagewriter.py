from aspose_psd_foss.bigendianwriter import BigEndianWriter
from aspose_psd_foss.sections.psdheader import PsdHeader


class PsdImageWriter:
    @classmethod
    def save(cls, document, stream, leave_open):
        writer = BigEndianWriter(stream, leave_open)
        try:
            writer.Write(int(PsdHeader.PsdSignature) & 0xFFFFFFFF)
            if document.Header is not None:
                document.Header.Save(writer)
            document.ColorData.Save(writer)
            document.ImageResourcesSection.Save(writer)
            is_large = getattr(document.Header, 'IsLargeDocument', False) == True
            document.LayerAndMaskSection.Save(writer, is_large)
            document.ImageData.Save(writer)
        finally:
            writer.Dispose()

