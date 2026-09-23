from typing import Optional
from ..layerandmasksectionreader import LayerAndMaskSectionReader
from ..layers.layerrecordwriter import LayerRecordWriter

class LayerAndMaskSection:
    """
    Represents the PSD/PSB Layer and Mask Information section and its raw-preserved save state.
    """

    Empty: "LayerAndMaskSection"

    def __init__(self, raw_section_bytes, layer_channel_image_data_raw, layer_global_mask_and_tail_raw, layer_count_raw, layers, has_layer_collection_mutated=False):
        self.raw_section_bytes = raw_section_bytes
        self.layer_channel_image_data_raw = layer_channel_image_data_raw
        self.layer_global_mask_and_tail_raw = layer_global_mask_and_tail_raw
        self.layer_count_raw = layer_count_raw
        self.layers = layers
        self.has_layer_collection_mutated = has_layer_collection_mutated

    @property
    def raw_section_bytes(self):
        """
        Gets the raw section payload without the outer length field.
        """
        return self._raw_section_bytes

    @raw_section_bytes.setter
    def raw_section_bytes(self, value):
        self._raw_section_bytes = value

    @property
    def layer_channel_image_data_raw(self):
        """
        Gets the raw layer channel image data payload after layer records.
        """
        return self._layer_channel_image_data_raw

    @layer_channel_image_data_raw.setter
    def layer_channel_image_data_raw(self, value):
        self._layer_channel_image_data_raw = value

    @property
    def layer_global_mask_and_tail_raw(self):
        """
        Gets the raw global mask info and trailing section bytes.
        """
        return self._layer_global_mask_and_tail_raw

    @layer_global_mask_and_tail_raw.setter
    def layer_global_mask_and_tail_raw(self, value):
        self._layer_global_mask_and_tail_raw = value

    @property
    def layer_count_raw(self):
        """
        Gets the original signed layer count so transparency-protected layers can preserve sign.
        """
        return self._layer_count_raw

    @layer_count_raw.setter
    def layer_count_raw(self, value):
        self._layer_count_raw = value

    @property
    def layers(self):
        """
        Gets the parsed layer records.
        """
        return self._layers

    @layers.setter
    def layers(self, value):
        self._layers = value

    @property
    def has_layer_collection_mutated(self):
        """
        Gets a value indicating whether the public layer collection was replaced.
        """
        return self._has_layer_collection_mutated

    @has_layer_collection_mutated.setter
    def has_layer_collection_mutated(self, value):
        self._has_layer_collection_mutated = value

    @classmethod
    def load(cls, reader, is_large_document):
        """
        Loads the section using PSD- or PSB-sized outer and layer-info lengths.
        """
        return LayerAndMaskSectionReader.load(reader, is_large_document)

    def save(self, writer, is_large_document):
        """
        Writes the section while preserving raw bytes for no-mutation saves.
        """
        LayerRecordWriter.save(self, writer, is_large_document)

    def with_layers(self, layers):
        """
        Creates a section copy with a replaced layer collection and marks it for rewriting on save.
        """
        return LayerAndMaskSection(
            self.raw_section_bytes,
            self.layer_channel_image_data_raw,
            self.layer_global_mask_and_tail_raw,
            self.layer_count_raw,
            list(layers),
            has_layer_collection_mutated=True
        )


# Initialize static empty instance
LayerAndMaskSection.Empty = LayerAndMaskSection([], [], [], 0, [], False)
