from __future__ import annotations

from aspose_psd_foss.bigendianreader import BigEndianReader
from aspose_psd_foss.bigendianwriter import BigEndianWriter
from aspose_psd_foss.compressionmethod import CompressionMethod
from aspose_psd_foss.coreexceptions.psdloadexception import PsdLoadException
from aspose_psd_foss.psdsectionreader import PsdSectionReader
from aspose_psd_foss.sections.imagedatastructure import ImageDataStructure
from aspose_psd_foss.sections.psdimagedatainfo import PsdImageDataInfo


class ImageData:
    """Stores the PSD Image Data section as a compression header plus raw payload bytes."""

    def __init__(self, compression: CompressionMethod, raw_data: bytes, structure: ImageDataStructure):
        self._compression = compression
        self._raw_data = raw_data
        self._structure = structure

    @property
    def structure(self) -> ImageDataStructure:
        """Gets the parsed structural interpretation of the payload."""
        return self._structure

    @property
    def compression(self) -> CompressionMethod:
        """Gets the stored compression method."""
        return self._compression

    @property
    def raw_data(self) -> bytes:
        """Gets the raw image data payload after the compression field."""
        return self._raw_data

    @classmethod
    def load(
        cls,
        reader: BigEndianReader,
        is_large_document: bool,
        height: int,
        channel_count: int,
    ) -> "ImageData":
        """Loads the final Image Data section from the reader."""
        compression = CompressionMethod(reader.read_uint16())

        image_data_start = reader.position
        reader.seek(0, 2)  # SeekOrigin.End
        image_data_end = reader.position
        reader.seek(image_data_start, 0)  # SeekOrigin.Begin

        image_data_length = image_data_end - image_data_start
        raw_data = PsdSectionReader.read_bytes(reader, image_data_length, "Image Data section")
        structure = cls._parse_structure(
            compression, raw_data, is_large_document, height, channel_count
        )
        return cls(compression, raw_data, structure)

    def save(self, writer: BigEndianWriter) -> None:
        """Writes the Image Data section to the writer."""
        writer.write_uint16(self.compression.value)
        writer.write(self.raw_data)

    def to_public_info(self) -> PsdImageDataInfo:
        """Creates a read-only public summary of the parsed merged image data structure."""
        return PsdImageDataInfo(
            self.structure.kind,
            self.structure.row_length_field_size,
            self.structure.row_byte_counts,
            self.structure.compressed_payload_length,
            self.structure.uses_prediction,
        )

    @staticmethod
    def _parse_structure(
        compression: CompressionMethod,
        raw_data: bytes,
        is_large_document: bool,
        height: int,
        channel_count: int,
    ) -> ImageDataStructure:
        """Builds a structural view over the raw image-data payload without decoding pixels."""
        if compression == CompressionMethod.RAW:
            return ImageDataStructure.create_raw(len(raw_data))
        if compression == CompressionMethod.RLE:
            return ImageData._parse_rle_structure(
                raw_data, is_large_document, height, channel_count
            )
        if compression == CompressionMethod.ZIP_WITHOUT_PREDICTION:
            return ImageDataStructure.create_zip(len(raw_data), uses_prediction=False)
        if compression == CompressionMethod.ZIP_WITH_PREDICTION:
            return ImageDataStructure.create_zip(len(raw_data), uses_prediction=True)
        return ImageDataStructure.create_unknown(len(raw_data))

    @staticmethod
    def _parse_rle_structure(
        raw_data: bytes,
        is_large_document: bool,
        height: int,
        channel_count: int,
    ) -> ImageDataStructure:
        """Parses the RLE row-length table so the payload has a validated structural model."""
        if height < 0 or channel_count < 0:
            raise PsdLoadException("PSD image dimensions are invalid for RLE image data.")

        row_count = height * channel_count
        row_length_field_size = 4 if is_large_document else 2
        table_length = row_count * row_length_field_size

        if len(raw_data) < table_length:
            raise PsdLoadException(
                "PSD RLE image data is truncated before the row-length table completes."
            )

        if row_count == 0:
            return ImageDataStructure.create_rle([], row_length_field_size, 0)

        offset = 0
        row_byte_counts = []
        for _ in range(row_count):
            if is_large_document:
                count = ImageData._read_uint32_big_endian(raw_data, offset)
            else:
                count = ImageData._read_uint16_big_endian(raw_data, offset)
            row_byte_counts.append(count)
            offset += row_length_field_size

        return ImageDataStructure.create_rle(
            row_byte_counts,
            row_length_field_size,
            len(raw_data) - table_length,
        )

    @staticmethod
    def _read_uint16_big_endian(buffer: bytes, offset: int) -> int:
        """Reads a big-endian 16-bit unsigned integer from a byte span."""
        return (buffer[offset] << 8) | buffer[offset + 1]

    @staticmethod
    def _read_uint32_big_endian(buffer: bytes, offset: int) -> int:
        """Reads a big-endian 32-bit unsigned integer from a byte span."""
        return (
            (buffer[offset] << 24)
            | (buffer[offset + 1] << 16)
            | (buffer[offset + 2] << 8)
            | buffer[offset + 3]
        )
