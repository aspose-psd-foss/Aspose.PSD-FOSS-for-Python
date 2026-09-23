from aspose_psd_foss import image
from aspose_psd_foss.coreexceptions import psdloadexception, psdsaveexception
from aspose_psd_foss.layers import globallayermaskinfo
from aspose_psd_foss.properties import assemblyinfo
from aspose_psd_foss.resources import indexedcolorpalette, indexedcolorpaletteinfo, preservedresourceblock, psdresourceinfo, psdresourcekind, unknownresource
from aspose_psd_foss.sections import colordata, imagedata, imagedatakind, imagedatastructure, imageresourcessection, psdcolordatainfo, psdcolordatakind, psdheader, psdimagedatainfo
from aspose_psd_foss import bigendianbitconverter, bigendianreader, bigendianwriter, colormodes, compressionmethod, point, psdsectionreader, psdversion, rectangle, rectanglef, resourceblock, size, streamcontainer
import io
import os

class PsdImage(image.Image):
    def __init__(self, stream, leave_open):
        self._stream = stream
        self._leave_open = leave_open
        self._disposed = False
        self._document = psdimagedatainfo.PsdImageDocumentState.empty
        self.global_angle = 0

    @property
    def width(self):
        return self._document.header.width if self._document.header else 0

    @property
    def height(self):
        return self._document.header.height if self._document.header else 0

    @property
    def channels(self):
        return self._document.header.channels if self._document.header else 0

    @property
    def bits_per_channel(self):
        return self._document.header.bit_depth if self._document.header else 0

    @property
    def color_mode(self):
        return self._document.header.color_mode if self._document.header else colormodes.ColorModes.rgb

    @color_mode.setter
    def color_mode(self, value):
        self.header.set_color_mode(value)

    @property
    def version(self):
        return 6

    @version.setter
    def version(self, value):
        if value != 6:
            raise ValueError("Supported Aspose.PSD-compatible API version is 6.")

    @property
    def header(self):
        if not self._document.header:
            raise InvalidOperationException("PSD/PSB header is not loaded.")
        return self._document.header

    @property
    def is_large_document(self):
        return self._document.header.is_large_document if self._document.header else False

    @property
    def is_psb(self):
        return self.is_large_document

    @property
    def layers(self):
        return list(self._document.layer_and_mask_section.layers)

    @layers.setter
    def layers(self, value):
        self._document = self._document.with_layer_and_mask_section(
            self._document.layer_and_mask_section.with_layers(value if value is not None else [])
        )

    @property
    def channels_count(self):
        return self.channels

    @property
    def size(self):
        return size.Size(self.width, self.height)

    @property
    def active_layer(self):
        return self.layers[0] if self.layers else None

    @active_layer.setter
    def active_layer(self, value):
        raise NotSupportedException("Changing the active layer is not supported by this FOSS build.")

    @property
    def layer_count(self):
        return len(self.layers)

    @property
    def has_layers(self):
        return len(self._document.layer_and_mask_section.layers) > 0

    @property
    def has_image_resources(self):
        return self._document.image_resources_section.has_resources

    @property
    def resource_count(self):
        return len(self._document.image_resources_section.resources)

    @property
    def image_resources(self):
        preserved = []
        for resource in self._document.image_resources_section.resources:
            preserved.append(preservedresourceblock.PreservedResourceBlock(resource))
        return preserved

    @image_resources.setter
    def image_resources(self, value):
        raise NotSupportedException("Changing image resources is not supported by this FOSS build.")

    @property
    def global_layer_resources(self):
        return []

    @global_layer_resources.setter
    def global_layer_resources(self, value):
        raise NotSupportedException("Changing global layer resources is not supported by this FOSS build.")

    @property
    def global_layer_mask_info(self):
        return globallayermaskinfo.GlobalLayerMaskInfo.empty

    @property
    def is_flatten(self):
        return len(self._document.layer_and_mask_section.layers) == 0

    @property
    def has_transparency_data(self):
        return False

    @has_transparency_data.setter
    def has_transparency_data(self, value):
        raise NotSupportedException("Changing transparency data semantics is not supported by this FOSS build.")

    @property
    def resources(self):
        return [resource.to_public_info() for resource in self._document.image_resources_section.resources]

    @property
    def has_color_mode_data(self):
        return len(self._document.color_data.raw_data) > 0

    @property
    def color_data_info(self):
        return self._document.color_data.to_public_info()

    @property
    def indexed_palette(self):
        if self.color_data_info.indexed_palette:
            return self.color_data_info.indexed_palette
        return None

    @property
    def has_merged_image_data(self):
        return len(self._document.image_data.raw_data) > 0

    @property
    def compression(self):
        return self._document.image_data.compression

    @property
    def image_data_info(self):
        return self._document.image_data.to_public_info()

    @property
    def image_data_kind(self):
        return self._document.image_data.structure.kind

    @property
    def uses_prediction(self):
        return self._document.image_data.structure.uses_prediction

    @property
    def has_icc_profile(self):
        return False

    @property
    def is_icc_profile_untagged(self):
        return None

    @property
    def parsed_color_data(self):
        return self._document.color_data

    @property
    def parsed_resources(self):
        return list(self._document.image_resources_section.resources)

    @classmethod
    def load(cls, file_path):
        if file_path is None:
            raise ValueError("file_path cannot be None")
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")

        with open(file_path, 'rb') as stream:
            return cls.load_stream(stream)

    @classmethod
    def load_stream(cls, stream):
        if stream is None:
            raise ValueError("stream cannot be None")

        original_position = 0
        restore_position = stream.seekable()
        if restore_position:
            original_position = stream.tell()

        try:
            buffered_stream = io.BytesIO()
            buffered_stream.write(stream.read())
            buffered_stream.seek(0)
            return cls._load(buffered_stream, False)
        finally:
            if restore_position:
                stream.seek(original_position)

    @classmethod
    def _load(cls, stream, leave_open):
        image = cls(stream, leave_open)
        image._document = psdimageloader.PsdImageLoader.load(stream, leave_open)
        return image

    def save(self, file_path):
        if file_path is None:
            raise ValueError("file_path cannot be None")

        with open(file_path, 'wb') as stream:
            self._save(stream, False)

    def save_stream(self, stream):
        if stream is None:
            raise ValueError("stream cannot be None")
        self._save(stream, True)

    def _save(self, stream, leave_open):
        if self._disposed:
            raise ObjectDisposedException("PsdImage")

        psdimagewriter.PsdImageWriter.save(self._document, stream, leave_open)

    def dispose(self):
        if self._disposed:
            return
        self._disposed = True
        if not self._leave_open:
            self._stream.close()
