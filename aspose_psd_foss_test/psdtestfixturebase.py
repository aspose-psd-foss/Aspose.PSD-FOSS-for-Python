import os
import shutil
import tempfile
import uuid
from pathlib import Path
import io

import pytest

from aspose_psd_foss.bigendianbitconverter import BigEndianBitConverter
from aspose_psd_foss.bigendianwriter import BigEndianWriter
from aspose_psd_foss.colormodes import ColorModes
from aspose_psd_foss.psdimage import PsdImage
from aspose_psd_foss.resources.indexedcolorpalette import IndexedColorPalette


class PsdTestFixtureBase:
    """Provides common temporary-file helpers and binary fixture builders for PSD tests."""

    @pytest.fixture(autouse=True)
    def test_dir(self, tmp_path):
        """Creates a temporary test directory for output files.

        The directory is automatically cleaned up by pytest's tmp_path fixture.
        """
        test_dir = tmp_path / f"AsposePsdTest_{uuid.uuid4()}"
        test_dir.mkdir(parents=True, exist_ok=True)
        self._test_dir = str(test_dir)
        yield self._test_dir

    def get_persistent_artifact_path(self, file_name):
        """Gets a stable artifact path for the current test under the artifacts directory.

        :param file_name: The artifact file name.
        :return: The full output path for the artifact.
        """
        test_name = os.getenv("PYTEST_CURRENT_TEST", "unknown_test")
        # Sanitize test name for use as a directory name
        test_name = self.sanitize_path_segment(test_name)
        artifact_directory = os.path.join(
            os.getcwd(),
            "artifacts",
            "PsdTestFixtureBase",
            test_name,
        )
        os.makedirs(artifact_directory, exist_ok=True)
        return os.path.join(artifact_directory, file_name)

    @staticmethod
    def get_test_data_path(file_name):
        """Resolves a test fixture path from the copied test output or the repository testdata folder.

        :param file_name: The fixture file name.
        :return: The resolved fixture path.
        """
        test_directory_path = os.path.join(os.getcwd(), "testdata", file_name)
        if os.path.isfile(test_directory_path):
            return test_directory_path

        repository_path = os.path.abspath(
            os.path.join(os.getcwd(), "../../../testdata", file_name),
        )
        return repository_path

    @staticmethod
    def log_artifact_directory(output_file):
        """Writes the artifact directory path for the current test to the output log.

        :param output_file: The saved artifact file path.
        """
        output_directory = os.path.dirname(output_file) or ""
        print(f"Saved test artifact directory: {output_directory}")

    @staticmethod
    def sanitize_path_segment(value):
        """Replaces characters that are invalid in file-system path segments.

        :param value: The path segment candidate.
        :return: A file-system-safe path segment.
        """
        invalid_characters = set(chr(c) for c in range(0, 32)) | set('<>:"/\\|?*')
        return ''.join('_' if ch in invalid_characters else ch for ch in value)

    def assert_byte_exact_round_trip(self, file_name):
        """Asserts that saving a fixture without mutations produces byte-for-byte identical output.

        :param file_name: The fixture file name.
        """
        test_file = self.get_test_data_path(file_name)
        output_file = self.get_persistent_artifact_path(file_name)
        with open(test_file, "rb") as f:
            original_bytes = f.read()

        with PsdImage.load(test_file) as image:
            image.save(output_file)
        self.log_artifact_directory(output_file)

        with open(output_file, "rb") as f:
            saved_bytes = f.read()
        assert saved_bytes == original_bytes, "Saved bytes differ from original"

    def assert_rename_save(self, file_name, layer_index, new_name):
        """Asserts that renaming a layer persists after saving and reloading a fixture.

        :param file_name: The fixture file name.
        :param layer_index: The zero-based layer index to rename.
        :param new_name: The replacement layer name.
        """
        test_file = self.get_test_data_path(file_name)
        output_file = self.get_persistent_artifact_path(
            f"renamed_{file_name}",
        )

        with PsdImage.load(test_file) as image:
            image.layers[layer_index].name = new_name
            image.save(output_file)
        self.log_artifact_directory(output_file)

        with PsdImage.load(output_file) as reloaded:
            assert (
                reloaded.layers[layer_index].name == new_name
            ), "Layer name was not persisted"

    @staticmethod
    def write_uint32_big_endian(buffer, offset, value):
        """Writes a 32-bit unsigned integer into the specified buffer in big-endian byte order.

        :param buffer: The target byte buffer.
        :param offset: The offset at which to write the value.
        :param value: The value to encode.
        """
        buffer[offset] = (value >> 24) & 0xFF
        buffer[offset + 1] = (value >> 16) & 0xFF
        buffer[offset + 2] = (value >> 8) & 0xFF
        buffer[offset + 3] = value & 0xFF

    @staticmethod
    def build_header_bytes(
        version,
        channels=3,
        width=1,
        height=1,
        bit_depth=8,
        color_mode=ColorModes.RGB,
    ):
        """Builds a minimal PSD or PSB header byte sequence for parser-boundary tests.

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

        stream.write(b"8BPS")
        writer.write_uint16(version)
        writer.write(b"\x00" * 6)
        writer.write_uint16(channels)
        writer.write_uint32(height)
        writer.write_uint32(width)
        writer.write_uint16(bit_depth)
        writer.write_uint16(int(color_mode))

        return stream.getvalue()

    @staticmethod
    def build_color_data_section(payload):
        """Builds a Color Mode Data section with a 4-byte length field and caller-provided payload.

        :param payload: The Color Mode Data payload bytes.
        :return: The encoded section bytes.
        """
        stream = io.BytesIO()
        writer = BigEndianWriter(stream, leave_open=True)
        writer.write_uint32(len(payload))
        writer.write(payload)
        return stream.getvalue()

    @staticmethod
    def build_image_data_section(compression, payload):
        """Builds an Image Data section with a compression field and caller-provided payload.

        :param compression: The compression mode to encode.
        :param payload: The image data payload bytes after the compression field.
        :return: The encoded image data section bytes.
        """
        stream = io.BytesIO()
        writer = BigEndianWriter(stream, leave_open=True)
        writer.write_uint16(int(compression))
        writer.write(payload)
        return stream.getvalue()

    @staticmethod
    def build_indexed_palette_payload():
        """Builds a deterministic 256-entry indexed palette payload for Color Mode Data tests.

        :return: The 768-byte indexed palette payload.
        """
        payload = bytearray(IndexedColorPalette.ExpectedRawLength)
        for i in range(256):
            payload[i] = i & 0xFF
            payload[i + 256] = (255 - i) & 0xFF
            payload[i + 512] = (128 + (i % 64)) & 0xFF
        return bytes(payload)

    @staticmethod
    def build_resources_payload(*resources):
        """Builds an Image Resources payload containing one or more unknown resource blocks.

        :param resources: The resource identifiers, Pascal names, and payload bytes to encode.
        :return: The encoded Image Resources payload without the outer section length field.
        """
        stream = io.BytesIO()

        def write_int16(value):
            stream.write(bytes([(value >> 8) & 0xFF, value & 0xFF]))

        def write_int32(value):
            stream.write(
                bytes(
                    [
                        (value >> 24) & 0xFF,
                        (value >> 16) & 0xFF,
                        (value >> 8) & 0xFF,
                        value & 0xFF,
                    ]
                )
            )

        for resource_id, name, data in resources:
            stream.write(b"8BIM")
            write_int16(resource_id)

            name_bytes = name.encode("ascii")
            stream.write(bytes([len(name_bytes)]))
            stream.write(name_bytes)
            if (len(name_bytes) + 1) % 2 != 0:
                stream.write(b"\x00")

            write_int32(len(data))
            stream.write(data)
            if len(data) % 2 == 1:
                stream.write(b"\x00")

        return stream.getvalue()

    @staticmethod
    def build_layer_record_bytes_with_extra_data(extra_data):
        """Builds a minimal PSD layer record with caller-controlled extra data bytes.

        :param extra_data: The layer extra data payload to append after the fixed layer record fields.
        :return: The encoded layer record bytes.
        """
        stream = io.BytesIO()
        writer = BigEndianWriter(stream, leave_open=True)

        writer.write_uint32(0)
        writer.write_uint32(0)
        writer.write_uint32(1)
        writer.write_uint32(1)
        writer.write_uint16(0)
        writer.write_uint32(0x3842494D)
        writer.write(b"norm")
        writer.write_uint8(255)
        writer.write_uint8(0)
        writer.write_uint8(0)
        writer.write_uint8(0)
        writer.write_uint32(len(extra_data))
        writer.write(extra_data)

        return stream.getvalue()

    @staticmethod
    def extract_image_resources_section(document_bytes):
        """Extracts the full Image Resources section, including its 4-byte length field.

        :param document_bytes: The complete PSD document bytes.
        :return: The raw Image Resources section bytes, including the section length field.
        """
        header_length = 26
        color_mode_length = BigEndianBitConverter.to_int32(
            document_bytes,
            header_length,
        )
        resources_length_offset = header_length + 4 + color_mode_length
        resources_payload_length = BigEndianBitConverter.to_int32(
            document_bytes,
            resources_length_offset,
        )
        total_section_length = 4 + resources_payload_length
        return document_bytes[
            resources_length_offset : resources_length_offset + total_section_length
        ]

    @staticmethod
    def read_layer_info_length(document_bytes):
        """Reads the PSD layer info payload length field from a complete document byte array.

        :param document_bytes: The complete PSD document bytes.
        :return: The stored layer info payload length.
        """
        header_length = 26
        color_mode_length = BigEndianBitConverter.to_int32(
            document_bytes,
            header_length,
        )
        resources_length_offset = header_length + 4 + color_mode_length
        resources_payload_length = BigEndianBitConverter.to_int32(
            document_bytes,
            resources_length_offset,
        )
        layer_and_mask_length_offset = resources_length_offset + 4 + resources_payload_length
        layer_info_length_offset = layer_and_mask_length_offset + 4
        return BigEndianBitConverter.to_int32(
            document_bytes,
            layer_info_length_offset,
        )

    @staticmethod
    def read_layer_and_mask_tail(document_bytes):
        """Reads the preserved Layer and Mask Information tail bytes from a complete PSD document.

        :param document_bytes: The complete PSD document bytes.
        :return: The global mask and trailing layer/mask bytes after the Layer Info subsection.
        """
        header_length = 26
        color_mode_length = BigEndianBitConverter.to_int32(
            document_bytes,
            header_length,
        )
        resources_length_offset = header_length + 4 + color_mode_length
        resources_payload_length = BigEndianBitConverter.to_int32(
            document_bytes,
            resources_length_offset,
        )
        layer_and_mask_length_offset = resources_length_offset + 4 + resources_payload_length
        layer_and_mask_length = BigEndianBitConverter.to_int32(
            document_bytes,
            layer_and_mask_length_offset,
        )
        layer_info_length = PsdTestFixtureBase.read_layer_info_length(document_bytes)
        tail_offset = (
            layer_and_mask_length_offset
            + 4
            + 4
            + layer_info_length
        )
        tail_length = (
            layer_and_mask_length_offset
            + 4
            + layer_and_mask_length
        ) - tail_offset

        if tail_length <= 0:
            return b""

        return document_bytes[tail_offset : tail_offset + tail_length]

    @staticmethod
    def build_psb_layer_record_bytes():
        """Builds a synthetic PSB layer record with 64-bit channel lengths.

        :return: The encoded PSB layer record bytes.
        """
        stream = io.BytesIO()
        writer = BigEndianWriter(stream, leave_open=True)

        writer.write_uint32(0)
        writer.write_uint32(0)
        writer.write_uint32(1)
        writer.write_uint32(1)
        writer.write_uint16(4)
        writer.write_int16(-1)
        writer.write_uint64(3)
        writer.write_int16(0)
        writer.write_uint64(3)
        writer.write_int16(1)
        writer.write_uint64(3)
        writer.write_int16(2)
        writer.write_uint64(3)
        writer.write_uint32(0x3842494D)
        writer.write(b"norm")
        writer.write_uint8(200)
        writer.write_uint8(0)
        writer.write_uint8(0)
        writer.write_uint8(0)

        extra_stream = io.BytesIO()
        extra_writer = BigEndianWriter(extra_stream, leave_open=True)
        extra_writer.write_uint32(0)
        extra_writer.write_uint32(0)
        extra_writer.write_pascal_string("Layer 1")

        extra_data = extra_stream.getvalue()
        writer.write_uint32(len(extra_data))
        writer.write(extra_data)

        return stream.getvalue()