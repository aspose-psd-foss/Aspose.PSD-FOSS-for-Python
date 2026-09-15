from aspose_psd_foss.layers.layer import Layer
from aspose_psd_foss.big_endian_reader import BigEndianReader
from aspose_psd_foss.big_endian_writer import BigEndianWriter
from aspose_psd_foss.layer_and_mask_section_reader import LayerAndMaskSectionReader
from aspose_psd_foss.layer_and_mask_section_writer import LayerAndMaskSectionWriter


class LayerAndMaskSection:
    # Gets an empty Layer and Mask Information section.
    Empty = None  # will be initialized after the class definition

    # Initializes a new instance of the LayerAndMaskSection class.
    # raw_section_bytes: The raw section payload without the outer length field.
    # layer_channel_image_data_raw: The raw channel image data payload after layer records.
    # layer_global_mask_and_tail_raw: The raw global mask and trailing section bytes.
    # layer_count_raw: The original signed layer count value.
    # layers: The parsed layer records.
    # has_layer_collection_mutated: true when the public layer collection was replaced; otherwise, false.
    def __init__(
        self,
        raw_section_bytes,
        layer_channel_image_data_raw,
        layer_global_mask_and_tail_raw,
        layer_count_raw,
        layers,
        has_layer_collection_mutated=False,
    ):
        self.raw_section_bytes = raw_section_bytes
        self.layer_channel_image_data_raw = layer_channel_image_data_raw
        self.layer_global_mask_and_tail_raw = layer_global_mask_and_tail_raw
        self.layer_count_raw = layer_count_raw
        self.layers = layers
        self.has_layer_collection_mutated = has_layer_collection_mutated

    # Gets the raw section payload without the outer length field.
    @property
    def raw_section_bytes(self):
        return self._raw_section_bytes

    @raw_section_bytes.setter
    def raw_section_bytes(self, value):
        self._raw_section_bytes = value

    # Gets the raw layer channel image data payload after layer records.
    @property
    def layer_channel_image_data_raw(self):
        return self._layer_channel_image_data_raw

    @layer_channel_image_data_raw.setter
    def layer_channel_image_data_raw(self, value):
        self._layer_channel_image_data_raw = value

    # Gets the raw global mask info and trailing section bytes.
    @property
    def layer_global_mask_and_tail_raw(self):
        return self._layer_global_mask_and_tail_raw

    @layer_global_mask_and_tail_raw.setter
    def layer_global_mask_and_tail_raw(self, value):
        self._layer_global_mask_and_tail_raw = value

    # Gets the original signed layer count so transparency-protected layers can preserve sign.
    @property
    def layer_count_raw(self):
        return self._layer_count_raw

    @layer_count_raw.setter
    def layer_count_raw(self, value):
        self._layer_count_raw = value

    # Gets the parsed layer records.
    @property
    def layers(self):
        return self._layers

    @layers.setter
    def layers(self, value):
        self._layers = value

    # Gets a value indicating whether the public layer collection was replaced.
    @property
    def has_layer_collection_mutated(self):
        return self._has_layer_collection_mutated

    @has_layer_collection_mutated.setter
    def has_layer_collection_mutated(self, value):
        self._has_layer_collection_mutated = value

    # Loads the section using PSD- or PSB-sized outer and layer-info lengths.
    # reader: The reader positioned at the outer section length field.
    # is_large_document: true for PSB-sized lengths; otherwise, false.
    @staticmethod
    def load(reader: BigEndianReader, is_large_document: bool):
        return LayerAndMaskSectionReader.load(reader, is_large_document)

    # Writes the section while preserving raw bytes for no-mutation saves.
    # writer: The destination writer.
    # is_large_document: true for PSB-sized lengths; otherwise, false.
    def save(self, writer: BigEndianWriter, is_large_document: bool):
        LayerAndMaskSectionWriter.save(self, writer, is_large_document)

    # Creates a section copy with a replacement layer collection and marks it for rewriting on save.
    # layers: The replacement layer collection.
    def with_layers(self, layers):
        return LayerAndMaskSection(
            self.raw_section_bytes,
            self.layer_channel_image_data_raw,
            self.layer_global_mask_and_tail_raw,
            self.layer_count_raw,
            list(layers),
            has_layer_collection_mutated=True,
        )


# Initialize the Empty static property
LayerAndMaskSection.Empty = LayerAndMaskSection([], [], [], 0, [])
