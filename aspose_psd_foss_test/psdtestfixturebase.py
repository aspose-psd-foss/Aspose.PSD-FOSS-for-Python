import os
import tempfile
import shutil
from io import BytesIO
from aspose_psd_foss.psdimage import PsdImage
from aspose_psd_foss.colormodes import ColorModes
from aspose_psd_foss.compressionmethod import CompressionMethod
from aspose_psd_foss.bigendianwriter import BigEndianWriter
from aspose_psd_foss.resources.indexedcolorpalette import IndexedColorPalette
from aspose_psd_foss.bigendianbitconverter import BigEndianBitConverter
import unittest
import pathlib
import array
import struct
import uuid


class PsdTestFixtureBase:
    """
    Provides common temporary-file helpers and binary fixture builders for PSD tests.
    """

    def __init__(self):
        self._test_dir = os.path.join(tempfile.gettempdir(), f"AsposePsdTest_{str(uuid.uuid4())}")
        os.makedirs(self._test_dir)

    def dispose(self):
        try:
            shutil.rmtree(self._test_dir)
        except Exception:
            pass

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.dispose()

    @staticmethod
    def get_persistent_artifact_path(file_name):
        test_name = PsdTestFixtureBase.sanitize_path_segment(unittest.TestCase().id().split('.')[-1] if hasattr(unittest.TestCase(), 'id') else 'test')
        artifact_directory = os.path.join(
            os.environ.get('NUNIT_WORK_DIRECTORY', os.getcwd()),
            "artifacts",
            "PsdTestFixtureBase",
            test_name
        )
        os.makedirs(artifact_directory, exist_ok=True)
        return os.path.join(artifact_directory, file_name)

    @staticmethod
    def get_test_data_path(file_name):
        test_directory_path = os.path.join(unittest.TestCase().testDirectory if hasattr(unittest.TestCase(), 'testDirectory') else os.getcwd(), "testdata", file_name)
        if os.path.isfile(test_directory_path):
            return test_directory_path

        repository_path = os.path.abspath(os.path.join(unittest.TestCase().testDirectory if hasattr(unittest.TestCase(), 'testDirectory') else os.getcwd(), "..", "..", "testdata", file_name))
        return repository_path

    @staticmethod
    def log_artifact_directory(output_file):
        output_directory = os.path.dirname(output_file) or ""
        print(f"Saved test artifact directory: {output_directory}")

    @staticmethod
    def sanitize_path_segment(value):
        invalid_characters = set('\\/:*?"<>|')
        return ''.join('_' if c in invalid_characters else c for c in value)

    @staticmethod
    def assert_byte_exact_round_trip(file_name):
        test_file = PsdTestFixtureBase.get_test_data_path(file_name)
        output_file = PsdTestFixtureBase.get_persistent_artifact_path(file_name)
        with open(test_file, 'rb') as f:
            original_bytes = f.read()

        with PsdImage.load(test_file) as image:
            image.save(output_file)
        PsdTestFixtureBase.log_artifact_directory(output_file)

        with open(output_file, 'rb') as f:
            saved_bytes = f.read()
        assert saved_bytes == original_bytes

    @staticmethod
    def assert_rename_save(file_name, layer_index, new_name):
        test_file = PsdTestFixtureBase.get_test_data_path(file_name)
        output_file = PsdTestFixtureBase.get_persistent_artifact_path(f"renamed_{file_name}")

        with PsdImage.load(test_file) as image:
            image.layers[layer_index].name = new_name
            image.save(output_file)
        PsdTestFixtureBase.log_artifact_directory(output_file)

        with PsdImage.load(output_file) as reloaded:
            assert reloaded.layers[layer_index].name == new_name

    @staticmethod
    def write_uint32_big_endian(buffer, offset, value):
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
            color_mode=ColorModes.Rgb):
        stream = BytesIO()
        writer = BigEndianWriter(stream)

        stream.write(b'8BPS')
        writer.write_uint16(version)
        writer.write_bytes(b'\x00' * 6)
        writer.write_uint16(channels)
        writer.write_int32(height)
        writer.write_int32(width)
        writer.write_uint16(bit_depth)
        writer.write_uint16(color_mode.value)

        return stream.getvalue()

    @staticmethod
    def build_color_data_section(payload):
        stream = BytesIO()
        writer = BigEndianWriter(stream)
        writer.write_uint32(len(payload))
        writer.write_bytes(payload)
        return stream.getvalue()

    @staticmethod
    def build_image_data_section(compression, payload):
        stream = BytesIO()
        writer = BigEndianWriter(stream)
        writer.write_uint16(compression.value)
        writer.write_bytes(payload)
        return stream.getvalue()

    @staticmethod
    def build_indexed_palette_payload():
        payload = bytearray(IndexedColorPalette.expected_raw_length)
        for i in range(256):
            payload[i] = i
            payload[i + 256] = 255 - i
            payload[i + 512] = 128 + (i % 64)
        return bytes(payload)

    @staticmethod
    def build_resources_payload(*resources):
        stream = BytesIO()

        def write_int16(value):
            stream.write(struct.pack('>H', value))

        def write_int32(value):
            stream.write(struct.pack('>I', value))

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

    @staticmethod
    def build_layer_record_bytes_with_extra_data(extra_data):
        stream = BytesIO()
        writer = BigEndianWriter(stream)

        writer.write_int32(0)
        writer.write_int32(0)
        writer.write_int32(1)
        writer.write_int32(1)
        writer.write_uint16(0)
        writer.write_uint32(0x3842494D)
        writer.write_bytes(b'norm')
        writer.write_byte(255)
        writer.write_byte(0)
        writer.write_byte(0)
        writer.write_byte(0)
        writer.write_uint32(len(extra_data))
        writer.write_bytes(extra_data)

        return stream.getvalue()

    @staticmethod
    def extract_image_resources_section(document_bytes):
        header_length = 26
        color_mode_length = BigEndianBitConverter.to_int32(document_bytes, header_length)
        resources_length_offset = header_length + 4 + color_mode_length
        resources_payload_length = BigEndianBitConverter.to_int32(document_bytes, resources_length_offset)
        total_section_length = 4 + resources_payload_length
        section_bytes = bytearray(total_section_length)
        section_bytes[:] = document_bytes[resources_length_offset:resources_length_offset + total_section_length]
        return bytes(section_bytes)

    @staticmethod
    def read_layer_info_length(document_bytes):
        header_length = 26
        color_mode_length = BigEndianBitConverter.to_int32(document_bytes, header_length)
        resources_length_offset = header_length + 4 + color_mode_length
        resources_payload_length = BigEndianBitConverter.to_int32(document_bytes, resources_length_offset)
        layer_and_mask_length_offset = resources_length_offset + 4 + resources_payload_length
        layer_info_length_offset = layer_and_mask_length_offset + 4
        return BigEndianBitConverter.to_int32(document_bytes, layer_info_length_offset)

    @staticmethod
    def read_layer_and_mask_tail(document_bytes):
        header_length = 26
        color_mode_length = BigEndianBitConverter.to_int32(document_bytes, header_length)
        resources_length_offset = header_length + 4 + color_mode_length
        resources_payload_length = BigEndianBitConverter.to_int32(document_bytes, resources_length_offset)
        layer_and_mask_length_offset = resources_length_offset + 4 + resources_payload_length
        layer_and_mask_length = BigEndianBitConverter.to_int32(document_bytes, layer_and_mask_length_offset)
        layer_info_length = PsdTestFixtureBase.read_layer_info_length(document_bytes)
        tail_offset = layer_and_mask_length_offset + 4 + 4 + layer_info_length
        tail_length = (layer_and_mask_length_offset + 4 + layer_and_mask_length) - tail_offset

        if tail_length <= 0:
            return b''

        tail_bytes = bytearray(tail_length)
        tail_bytes[:] = document_bytes[tail_offset:tail_offset + tail_length]
        return bytes(tail_bytes)

    @staticmethod
    def build_psb_layer_record_bytes():
        stream = BytesIO()
        writer = BigEndianWriter(stream)

        writer.write_int32(0)
        writer.write_int32(0)
        writer.write_int32(1)
        writer.write_int32(1)
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
        writer.write_bytes(b'norm')
        writer.write_byte(200)
        writer.write_byte(0)
        writer.write_byte(0)
        writer.write_byte(0)

        extra_stream = BytesIO()
        extra_writer = BigEndianWriter(extra_stream)
        extra_writer.write_uint32(0)
        extra_writer.write_uint32(0)
        extra_writer.write_pascal_string("Layer 1")

        extra_data = extra_stream.getvalue()
        writer.write_uint32(len(extra_data))
        writer.write_bytes(extra_data)

        return stream.getvalue()

