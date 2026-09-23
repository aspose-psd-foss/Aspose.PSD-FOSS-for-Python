from .layers.layer import Layer
from .layers.layerrecordwriter import LayerRecordWriter
from .sections.layerandmasksection import LayerAndMaskSection
from .bigendianwriter import BigEndianWriter


def save(section, writer, is_large_document):
    if section.raw_section_bytes and len(section.raw_section_bytes) > 0 \
            and not section.has_layer_collection_mutated \
            and not any(layer.has_mutated for layer in section.layers):
        write_section_length(writer, len(section.raw_section_bytes), is_large_document)
        writer.write(section.raw_section_bytes)
        return

    if len(section.layers) == 0:
        write_section_length(writer, 0, is_large_document)
        return

    write_layer_section_with_mutations(section, writer, is_large_document)


def write_layer_section_with_mutations(section, writer, is_large_document):
    layer_info_payload_stream = bytearray()
    layer_info_payload_writer = BigEndianWriter(layer_info_payload_stream, leave_open=True)
    layer_count = -len(section.layers) if section.layer_count_raw < 0 else len(section.layers)
    layer_info_payload_writer.write(layer_count)

    for layer in section.layers:
        LayerRecordWriter.write(layer, layer_info_payload_writer, is_large_document)

    layer_info_payload_writer.write(section.layer_channel_image_data_raw)
    layer_info_payload = layer_info_payload_stream

    section_stream = bytearray()
    section_writer = BigEndianWriter(section_stream, leave_open=True)
    if is_large_document:
        section_writer.write(len(layer_info_payload))
    else:
        section_writer.write(len(layer_info_payload))

    section_writer.write(layer_info_payload)
    section_writer.write(get_layer_global_mask_and_tail_bytes_for_write(section))

    section_bytes = section_stream
    write_section_length(writer, len(section_bytes), is_large_document)
    writer.write(section_bytes)


def get_layer_global_mask_and_tail_bytes_for_write(section):
    return section.layer_global_mask_and_tail_raw if section.layer_global_mask_and_tail_raw else [0, 0, 0, 0]


def write_section_length(writer, length, is_large_document):
    if is_large_document:
        writer.write(length)
    else:
        writer.write(length)
