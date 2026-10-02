import os
import io
import uuid
from typing import Tuple, List

from aspose_psd_foss.psdimage import PsdImage
from aspose_psd_foss.bigendianwriter import BigEndianWriter
from aspose_psd_foss.bigendianbitconverter import BigEndianBitConverter
from aspose_psd_foss.colormodes import ColorModes
from aspose_psd_foss.resources.indexedcolorpalette import IndexedColorPalette


class PsdTestFixtureBase:
    """
    Provides common temporary-file helpers and binary fixture builders for PSD tests.
    """

    ''' def __init__(self):
        """
        Initializes a new instance of the PsdTestFixtureBase class.
        Creates a temporary test directory for output files.
        """
        self._test_dir = os.path.join(
            os.path.abspath(os.getenv('TMP', '/tmp')),
            f'AsposePsdTest_{uuid.uuid4()}'
        )
        os.makedirs(self._test_dir, exist_ok=True)

    def __del__(self):
        """
        Releases all resources used by the test fixture.
        Deletes the temporary test directory and its contents.
        """
        try:
            if os.path.isdir(self._test_dir):
                for root, dirs, files in os.walk(self._test_dir, topdown=False):
                    for name in files:
                        os.remove(os.path.join(root, name))
                    for name in dirs:
                        os.rmdir(os.path.join(root, name))
                os.rmdir(self._test_dir)
        except Exception:
            pass'''

    @classmethod
    def get_persistent_artifact_path(cls, file_name: str) -> str:
        """
        Gets a stable artifact path for the current test under the NUnit work directory.

        :param file_name: The artifact file name.
        :return: The full output path for the artifact.
        """
        test_context = os.getenv('PYTEST_CURRENT_TEST', 'test')
        test_name = test_context.split('::')[-1] if '::' in test_context else test_context
        test_name = cls.sanitize_path_segment(test_name)
        artifact_directory = os.path.join(
            os.getcwd(),
            'artifacts',
            cls.__name__,
            test_name
        )
        os.makedirs(artifact_directory, exist_ok=True)
        return os.path.join(artifact_directory, file_name)

    @classmethod
    def get_test_data_path(cls, file_name: str) -> str:
        """
        Resolves a test fixture path from the copied test output or the repository testdata folder.

        :param file_name: The fixture file name.
        :return: The resolved fixture path.
        """
        test_dir = os.path.abspath(os.getenv('PYTEST_CURRENT_TEST', ''))
        test_directory_path = os.path.join(test_dir, 'testdata', file_name)
        if os.path.isfile(test_directory_path):
            return test_directory_path

        repository_path = os.path.abspath(
            os.path.join(test_dir, '../testdata', file_name)
        )
        return repository_path

    @classmethod
    def log_artifact_directory(cls, output_file: str) -> None:
        """
        Writes the artifact directory path for the current test to the NUnit output log.

        :param output_file: The saved artifact file path.
        """
        output_directory = os.path.dirname(output_file) or ''
        print(f'Saved test artifact directory: {output_directory}')

    @classmethod
    def sanitize_path_segment(cls, value: str) -> str:
        """
        Replaces characters that are invalid in file-system path segments.

        :param value: The path segment candidate.
        :return: A file-system-safe path segment.
        """
        invalid_characters = set(chr(i) for i in range(0, 32)) | set('<>:"/\\|?*')
        return ''.join('_' if c in invalid_characters else c for c in value)

    @classmethod
    def assert_byte_exact_round_trip(cls, file_name: str) -> None:
        """
        Asserts that saving a fixture without mutations produces byte-for-byte identical output.

        :param file_name: The fixture file name.
        """
        test_file = cls.get_test_data_path(file_name)
        output_file = cls.get_persistent_artifact_path(file_name)
        with open(test_file, 'rb') as f:
            original_bytes = f.read()

        image = PsdImage.load(test_file)
        image.save(output_file)
        cls.log_artifact_directory(output_file)

        with open(output_file, 'rb') as f:
            saved_bytes = f.read()

        assert saved_bytes == original_bytes

    @classmethod
    def assert_rename_save(cls, file_name: str, layer_index: int, new_name: str) -> None:
        """
        Asserts that renaming a layer persists after saving and reloading a fixture.

        :param file_name: The fixture file name.
        :param layer_index: The zero-based layer index to rename.
        :param new_name: The replacement layer name.
        """
        test_file = cls.get_test_data_path(file_name)
        output_file = cls.get_persistent_artifact_path(f'renamed_{file_name}')

        image = PsdImage.load(test_file)
        image.layers[layer_index].name = new_name
        image.save(output_file)
        cls.log_artifact_directory(output_file)

        reloaded = PsdImage.load(output_file)
        assert reloaded.layers[layer_index].name == new_name

    @classmethod
    def write_uint32_big_endian(cls, buffer: bytearray, offset: int, value: int) -> None:
        """
        Writes a 32-bit unsigned integer into the specified buffer in big-endian byte order.

        :param buffer: The target byte buffer.
        :param offset: The offset at which to write the value.
        :param value: The value to encode.
        """
        buffer[offset] = (value >> 24) & 0xFF
        buffer[offset + 1] = (value >> 16) & 0xFF
        buffer[offset + 2] = (value >> 8) & 0xFF
        buffer[offset + 3] = value & 0xFF

    @classmethod
    def build_header_bytes(
        cls,
        version: int,
        channels: int = 3,
        width: int = 1,
        height: int = 1,
        bit_depth: int = 8,
        color_mode: ColorModes = ColorModes.RGB
    ) -> bytearray:
        """
        Builds a minimal PSD or PSB header byte sequence for parser-boundary tests.

        :param version: The PSD container version to encode.
        :param channels: The channel count to encode.
        :param width: The document width to encode.
        :param height: The document height to encode.
        :param bit_depth: The bits per channel to encode.
        :param color_mode: The color mode to encode.
        :return: The encoded header bytes.
        """
        stream = io.BytesIO()
        writer = BigEndianWriter(stream, leave_open=True)

        stream.write(b'8BPS')
        writer.write_ushort(version)
        writer.write_bytes(b'\x00' * 6)
        writer.write_ushort(channels)
        writer.write_uint(height)
        writer.write_uint(width)
        writer.write_ushort(bit_depth)
        writer.write_ushort(int(color_mode))

        return bytearray(stream.getvalue())

    @classmethod
    def build_color_data_section(cls, payload: bytes) -> bytes:
        """
        Builds a Color Mode Data section with a 4-byte length field and caller-provided payload.

        :param payload: The Color Mode Data payload bytes.
        :return: The encoded section bytes.
        """
        stream = io.BytesIO()
        writer = BigEndianWriter(stream, leave_open=True)
        writer.write_uint(len(payload))
        writer.write_bytes(payload)
        return stream.getvalue()

    @classmethod
    def build_image_data_section(cls, compression, payload: bytes) -> bytes:
        """
        Builds an Image Data section with a compression field and caller-provided payload.

        :param compression: The compression mode to encode.
        :param payload: The image data payload bytes after the compression field.
        :return: The encoded image data section bytes.
        """
        stream = io.BytesIO()
        writer = BigEndianWriter(stream, leave_open=True)
        writer.write_ushort(int(compression))
        writer.write_bytes(payload)
        return stream.getvalue()

    @classmethod
    def build_indexed_palette_payload(cls) -> bytes:
        """
        Builds a deterministic 256-entry indexed palette payload for Color Mode Data tests.

        :return: The 768-byte indexed palette payload.
        """
        payload = bytearray(IndexedColorPalette.expected_raw_length)
        for i in range(256):
            payload[i] = i
            payload[i + 256] = 255 - i
            payload[i + 512] = 128 + (i % 64)
        return bytes(payload)

    @classmethod
    def build_resources_payload(cls, *resources: Tuple[int, str, bytes]) -> bytes:
        """
        Builds an Image Resources payload containing one or more unknown resource blocks.

        :param resources: The resource identifiers, Pascal names, and payload bytes to encode.
        :return: The encoded Image Resources payload without the outer section length field.
        """
        stream = io.BytesIO()

        def write_int16(value: int) -> None:
            stream.write(bytes([(value >> 8) & 0xFF, value & 0xFF]))

        def write_int32(value: int) -> None:
            stream.write(bytes([
                (value >> 24) & 0xFF,
                (value >> 16) & 0xFF,
                (value >> 8) & 0xFF,
                value & 0xFF
            ]))

        for resource_id, name, data in resources:
            stream.write(b'8BIM')
            write_int16(resource_id)

            name_bytes = name.encode('ascii')
            stream.write(bytes([len(name_bytes)]))
            stream.write(name_bytes)
            if (len(name_bytes) + 1) % 2 != 0:
                stream.write(b'\x00')

            write_int32(len(data))
            stream.write(data)
            if len(data) % 2 == 1:
                stream.write(b'\x00')

        return stream.getvalue()

    @classmethod
    def build_layer_record_bytes_with_extra_data(cls, extra_data: bytes) -> bytes:
        """
        Builds a minimal PSD layer record with caller-controlled extra data bytes.

        :param extra_data: The layer extra data payload to append after the fixed layer record fields.
        :return: The encoded layer record bytes.
        """
        stream = io.BytesIO()
        writer = BigEndianWriter(stream, leave_open=True)

        writer.write_uint(0)
        writer.write_uint(0)
        writer.write_uint(1)
        writer.write_uint(1)
        writer.write_ushort(0)
        writer.write_uint(0x3842494D)
        writer.write_bytes(b'norm')
        writer.write_byte(255)
        writer.write_byte(0)
        writer.write_byte(0)
        writer.write_byte(0)
        writer.write_uint(len(extra_data))
        writer.write_bytes(extra_data)

        return stream.getvalue()

    @classmethod
    def extract_image_resources_section(cls, document_bytes: bytes) -> bytes:
        """
        Extracts the full Image Resources section, including its 4-byte length field.

        :param document_bytes: The complete PSD document bytes.
        :return: The raw Image Resources section bytes, including the section length field.
        """
        header_length = 26
        color_mode_length = BigEndianBitConverter.to_int32(document_bytes, header_length)
        resources_length_offset = header_length + 4 + color_mode_length
        resources_payload_length = BigEndianBitConverter.to_int32(document_bytes, resources_length_offset)
        total_section_length = 4 + resources_payload_length
        return document_bytes[resources_length_offset:resources_length_offset + total_section_length]

    @classmethod
    def read_layer_info_length(cls, document_bytes: bytes) -> int:
        """
        Reads the PSD layer info payload length field from a complete document byte array.

        :param document_bytes: The complete PSD document bytes.
        :return: The stored layer info payload length.
        """
        header_length = 26
        color_mode_length = BigEndianBitConverter.to_int32(document_bytes, header_length)
        resources_length_offset = header_length + 4 + color_mode_length
        resources_payload_length = BigEndianBitConverter.to_int32(document_bytes, resources_length_offset)
        layer_and_mask_length_offset = resources_length_offset + 4 + resources_payload_length
        layer_info_length_offset = layer_and_mask_length_offset + 4
        return BigEndianBitConverter.to_int32(document_bytes, layer_info_length_offset)

    @classmethod
    def read_layer_and_mask_tail(cls, document_bytes: bytes) -> bytes:
        """
        Reads the preserved Layer and Mask Information tail bytes from a complete PSD document.

        :param document_bytes: The complete PSD document bytes.
        :return: The global mask and trailing layer/mask bytes after the Layer Info subsection.
        """
        header_length = 26
        color_mode_length = BigEndianBitConverter.to_int32(document_bytes, header_length)
        resources_length_offset = header_length + 4 + color_mode_length
        resources_payload_length = BigEndianBitConverter.to_int32(document_bytes, resources_length_offset)
        layer_and_mask_length_offset = resources_length_offset + 4 + resources_payload_length
        layer_and_mask_length = BigEndianBitConverter.to_int32(document_bytes, layer_and_mask_length_offset)
        layer_info_length = cls.read_layer_info_length(document_bytes)
        tail_offset = layer_and_mask_length_offset + 4 + 4 + layer_info_length
        tail_length = (layer_and_mask_length_offset + 4 + layer_and_mask_length) - tail_offset

        if tail_length <= 0:
            return b''

        return document_bytes[tail_offset:tail_offset + tail_length]

    @classmethod
    def build_psb_layer_record_bytes(cls) -> bytes:
        """
        Builds a synthetic PSB layer record with 64-bit channel lengths.

        :return: The encoded PSB layer record bytes.
        """
        stream = io.BytesIO()
        writer = BigEndianWriter(stream, leave_open=True)

        writer.write_uint(0)
        writer.write_uint(0)
        writer.write_uint(1)
        writer.write_uint(1)
        writer.write_ushort(4)
        writer.write_short(-1)
        writer.write_ulong(3)
        writer.write_short(0)
        writer.write_ulong(3)
        writer.write_short(1)
        writer.write_ulong(3)
        writer.write_short(2)
        writer.write_ulong(3)
        writer.write_uint(0x3842494D)
        writer.write_bytes(b'norm')
        writer.write_byte(200)
        writer.write_byte(0)
        writer.write_byte(0)
        writer.write_byte(0)

        extra_stream = io.BytesIO()
        extra_writer = BigEndianWriter(extra_stream, leave_open=True)
        extra_writer.write_uint(0)
        extra_writer.write_uint(0)
        extra_writer.write_pascal_string('Layer 1')

        extra_data = extra_stream.getvalue()
        writer.write_uint(len(extra_data))
        writer.write_bytes(extra_data)

        return stream.getvalue()

