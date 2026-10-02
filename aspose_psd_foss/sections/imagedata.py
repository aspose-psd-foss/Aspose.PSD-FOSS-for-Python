import io

from aspose_psd_foss.compressionmethod import CompressionMethod
from aspose_psd_foss.bigendianreader import BigEndianReader
from aspose_psd_foss.bigendianwriter import BigEndianWriter
from aspose_psd_foss.psdsectionreader import PsdSectionReader
from aspose_psd_foss.sections.imagedatastructure import ImageDataStructure
from aspose_psd_foss.sections.psdimagedatainfo import PsdImageDataInfo
from aspose_psd_foss.coreexceptions.psdloadexception import PsdLoadException


class ImageData:
    """
    Stores the PSD Image Data section as a compression header plus raw payload bytes.
    """

    def __init__(self, compression: CompressionMethod, raw_data: bytes, structure: ImageDataStructure):
        self.compression = compression
        self.raw_data = raw_data
        self.structure = structure

    @classmethod
    def from_raw(cls, compression: CompressionMethod, raw_data: bytes):
        """
        Initializes a new instance for callers that only preserve raw payload bytes.
        """
        structure = cls._parse_structure(compression, raw_data, False, 0, 0)
        return cls(compression, raw_data, structure)

    @classmethod
    def load(cls, reader: BigEndianReader, is_large_document: bool, height: int, channel_count: int):
        """
        Loads the final Image Data section from the reader.
        """
        compression = CompressionMethod(reader.read_uint16())

        image_data_start = reader.position
        reader.seek(0, io.SEEK_END)
        image_data_end = reader.position
        reader.seek(image_data_start, io.SEEK_SET)

        image_data_length = image_data_end - image_data_start
        raw_data = PsdSectionReader.read_bytes(reader, image_data_length, "Image Data section")
        structure = cls._parse_structure(compression, raw_data, is_large_document, height, channel_count)
        return cls(compression, raw_data, structure)

    def save(self, writer: BigEndianWriter):
        """
        Writes the Image Data section to the writer.
        """
        writer.write_uint16(self.compression.value)
        writer.write(self.raw_data)

    def to_public_info(self) -> PsdImageDataInfo:
        """
        Creates a read‑only public summary of the parsed merged image data structure.
        """
        return PsdImageDataInfo(
            self.structure.Kind,
            self.structure.RowLengthFieldSize,
            self.structure.RowByteCounts,
            self.structure.CompressedPayloadLength,
            self.structure.UsesPrediction,
        )

    @classmethod
    def _parse_structure(cls, compression: CompressionMethod, raw_data: bytes, is_large_document: bool,
                         height: int, channel_count: int) -> ImageDataStructure:
        """
        Builds a structural view over the raw image‑data payload without decoding pixels.
        """
        if compression == CompressionMethod.Raw:
            return ImageDataStructure.create_raw(len(raw_data))
        if compression == CompressionMethod.RLE:
            return cls._parse_rle_structure(raw_data, is_large_document, height, channel_count)
        if compression == CompressionMethod.ZipWithoutPrediction:
            return ImageDataStructure.create_zip(len(raw_data), uses_prediction=False)
        if compression == CompressionMethod.ZipWithPrediction:
            return ImageDataStructure.create_zip(len(raw_data), uses_prediction=True)
        return ImageDataStructure.create_unknown(len(raw_data))

    @classmethod
    def _parse_rle_structure(cls, raw_data: bytes, is_large_document: bool, height: int,
                             channel_count: int) -> ImageDataStructure:
        """
        Parses the RLE row‑length table so the payload has a validated structural model.
        """
        if height < 0 or channel_count < 0:
            raise PsdLoadException("PSD image dimensions are invalid for RLE image data.")

        row_count = height * channel_count
        row_length_field_size = 4 if is_large_document else 2
        table_length = row_count * row_length_field_size

        if len(raw_data) < table_length:
            raise PsdLoadException("PSD RLE image data is truncated before the row‑length table completes.")

        if row_count == 0:
            return ImageDataStructure.create_rle([], row_length_field_size, 0)

        offset = 0
        row_byte_counts = [0] * row_count
        for i in range(row_count):
            if is_large_document:
                row_byte_counts[i] = cls._read_uint32_big_endian(raw_data, offset)
            else:
                row_byte_counts[i] = cls._read_uint16_big_endian(raw_data, offset)
            offset += row_length_field_size

        payload_length = len(raw_data) - table_length
        return ImageDataStructure.create_rle(row_byte_counts, row_length_field_size, payload_length)

    @classmethod
    def _read_uint16_big_endian(cls, buffer: bytes, offset: int) -> int:
        """
        Reads a big‑endian 16‑bit unsigned integer from a byte span.
        """
        return (buffer[offset] << 8) | buffer[offset + 1]

    @classmethod
    def _read_uint32_big_endian(cls, buffer: bytes, offset: int) -> int:
        """
        Reads a big‑endian 32‑bit unsigned integer from a byte span.
        """
        return (buffer[offset] << 24) | (buffer[offset + 1] << 16) | (buffer[offset + 2] << 8) | buffer[offset + 3]
