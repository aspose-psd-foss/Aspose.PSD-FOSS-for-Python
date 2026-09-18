from __future__ import annotations

import io
import os
import typing

from .image import Image
from .size import Size
from .resourceblock import ResourceBlock
from .resources.preservedresourceblock import PreservedResourceBlock
from .layers.layerresource import LayerResource
from .layers.globallayermaskinfo import GlobalLayerMaskInfo
from .sections.psdheader import PsdHeader
from .sections.psdcolordatainfo import PsdColorDataInfo
from .resources.indexedcolorpaletteinfo import IndexedColorPaletteInfo
from .compressionmethod import CompressionMethod
from .sections.psdimagedatainfo import PsdImageDataInfo
from .sections.imagedatakind import ImageDataKind
from .sections.colordata import ColorData
from .resources.psdresourceinfo import PsdResourceInfo
from .loaders import psdimageloader as _psd_loader
from .loaders.psdimageloader import PsdImageDocumentState
from .colormodes import ColorModes
from typing import Any as Layer


class PsdImageWriter:
    """Fallback writer used when the real writer implementation is missing."""
    @staticmethod
    def save(document, stream: typing.BinaryIO, leave_open: bool) -> None:
        raise NotImplementedError("PsdImageWriter is not implemented in this build.")


class PsdImage(Image):
    def __init__(self, stream: typing.BinaryIO, leave_open: bool):
        self._stream = stream
        self._leave_open = leave_open
        self._disposed = False
        self._document: typing.Optional[PsdImageDocumentState] = None

    @property
    def width(self) -> int:
        return self._document.header.width if self._document and self._document.header else 0

    @property
    def height(self) -> int:
        return self._document.header.height if self._document and self._document.header else 0

    @property
    def _channels(self) -> int:
        return self._document.header.channels if self._document and self._document.header else 0

    @property
    def bits_per_channel(self) -> int:
        return self._document.header.bit_depth if self._document and self._document.header else 0

    @property
    def color_mode(self) -> ColorModes:
        return (
            self._document.header.color_mode
            if self._document and self._document.header
            else ColorModes.RGB
        )

    @color_mode.setter
    def color_mode(self, value: ColorModes) -> None:
        if self._document and self._document.header:
            self._document.header.set_color_mode(value)

    @property
    def version(self) -> int:
        return 6

    @version.setter
    def version(self, value: int) -> None:
        if value != 6:
            raise ValueError(
                "Supported Aspose.PSD-compatible API version is 6."
            )

    @property
    def _header(self) -> PsdHeader:
        if not self._document or not self._document.header:
            raise RuntimeError("PSD/PSB header is not loaded.")
        return self._document.header

    @property
    def _is_large_document(self) -> bool:
        return bool(
            self._document and self._document.header and self._document.header.is_large_document
        )

    @property
    def _is_psb(self) -> bool:
        return self._is_large_document

    @property
    def layers(self) -> typing.List[Layer]:
        return list(self._document.layer_and_mask_section.layers) if self._document else []

    @layers.setter
    def layers(self, value: typing.List[Layer]) -> None:
        if self._document:
            self._document.layer_and_mask_section = (
                self._document.layer_and_mask_section.with_layers(value or [])
            )

    @property
    def channels_count(self) -> int:
        return self._channels

    @property
    def size(self) -> Size:
        return Size(self.width, self.height)

    @property
    def active_layer(self) -> typing.Optional[Layer]:
        return self.layers[0] if self.layers else None

    @active_layer.setter
    def active_layer(self, value: typing.Optional[Layer]) -> None:
        raise NotImplementedError(
            "Changing the active layer is not supported by this FOSS build."
        )

    @property
    def _layer_count(self) -> int:
        return len(self.layers)

    @property
    def _has_layers(self) -> bool:
        return bool(self._document and self._document.layer_and_mask_section.layers)

    @property
    def _has_image_resources(self) -> bool:
        return bool(self._document and self._document.image_resources_section.has_resources)

    @property
    def _resource_count(self) -> int:
        return len(self._document.image_resources_section.resources) if self._document else 0

    @property
    def image_resources(self) -> typing.List[ResourceBlock]:
        return [
            PreservedResourceBlock(r)
            for r in self._document.image_resources_section.resources
        ] if self._document else []

    @image_resources.setter
    def image_resources(self, value: typing.List[ResourceBlock]) -> None:
        raise NotImplementedError(
            "Changing image resources is not supported by this FOSS build."
        )

    @property
    def global_layer_resources(self) -> typing.List[LayerResource]:
        return []

    @global_layer_resources.setter
    def global_layer_resources(self, value: typing.List[LayerResource]) -> None:
        raise NotImplementedError(
            "Changing global layer resources is not supported by this FOSS build."
        )

    @property
    def global_layer_mask_info(self) -> typing.Optional[GlobalLayerMaskInfo]:
        return GlobalLayerMaskInfo.EMPTY

    @property
    def is_flatten(self) -> bool:
        return len(self._document.layer_and_mask_section.layers) == 0 if self._document else True

    @property
    def has_transparency_data(self) -> bool:
        return False

    @has_transparency_data.setter
    def has_transparency_data(self, value: bool) -> None:
        raise NotImplementedError(
            "Changing transparency data semantics is not supported by this FOSS build."
        )

    @property
    def _resources(self) -> typing.List[PsdResourceInfo]:
        return [r.to_public_info() for r in self._document.image_resources_section.resources] if self._document else []

    @property
    def _has_color_mode_data(self) -> bool:
        return bool(self._document and len(self._document.color_data.raw_data) > 0)

    @property
    def _color_data_info(self) -> PsdColorDataInfo:
        return self._document.color_data.to_public_info() if self._document else None  # type: ignore

    @property
    def _indexed_palette(self) -> typing.Optional[IndexedColorPaletteInfo]:
        return self._color_data_info.indexed_palette if self._color_data_info else None

    @property
    def _has_merged_image_data(self) -> bool:
        return bool(self._document and len(self._document.image_data.raw_data) > 0)

    @property
    def compression(self) -> CompressionMethod:
        return self._document.image_data.compression if self._document else CompressionMethod.RLE  # type: ignore

    @property
    def _image_data_info(self) -> PsdImageDataInfo:
        return self._document.image_data.to_public_info() if self._document else None  # type: ignore

    @property
    def _image_data_kind(self) -> ImageDataKind:
        return self._document.image_data.structure.kind if self._document else None  # type: ignore

    @property
    def _uses_prediction(self) -> bool:
        return self._document.image_data.structure.uses_prediction if self._document else False

    @property
    def global_angle(self) -> int:
        return getattr(self, "_global_angle", 0)

    @global_angle.setter
    def global_angle(self, value: int) -> None:
        self._global_angle = value

    @property
    def _has_icc_profile(self) -> bool:
        return False

    @property
    def _is_icc_profile_untagged(self) -> typing.Optional[bool]:
        return None

    @property
    def _parsed_color_data(self) -> ColorData:
        return self._document.color_data if self._document else None  # type: ignore

    @property
    def _parsed_resources(self) -> typing.List:
        return self._document.image_resources_section.resources if self._document else []

    @classmethod
    def load(cls, file_path: str) -> "PsdImage":
        if file_path is None:
            raise ValueError("file_path cannot be None")
        if not os.path.isfile(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")
        with open(file_path, "rb") as stream:
            return cls._load_from_stream(stream, leave_open=False)

    @classmethod
    def load_from_stream(cls, stream: typing.BinaryIO) -> "PsdImage":
        if stream is None:
            raise ValueError("stream cannot be None")
        original_position = 0
        restore_position = stream.seekable()
        if restore_position:
            original_position = stream.tell()
        try:
            buffered = io.BytesIO(stream.read())
            buffered.seek(0)
            return cls._load_from_stream(buffered, leave_open=False)
        finally:
            if restore_position:
                stream.seek(original_position)

    @classmethod
    def _load_from_stream(cls, stream: typing.BinaryIO, leave_open: bool) -> "PsdImage":
        image = cls(stream, leave_open)
        image._document = _psd_loader.load(stream, leave_open)
        return image

    def save(self, file_path: str) -> None:
        if file_path is None:
            raise ValueError("file_path cannot be None")
        with open(file_path, "wb") as stream:
            self._save(stream, leave_open=False)

    def save_to_stream(self, stream: typing.BinaryIO) -> None:
        if stream is None:
            raise ValueError("stream cannot be None")
        self._save(stream, leave_open=True)

    def _save(self, stream: typing.BinaryIO, leave_open: bool) -> None:
        if self._disposed:
            raise RuntimeError("PsdImage is disposed")
        PsdImageWriter.save(self._document, stream, leave_open)

    def dispose(self) -> None:
        if self._disposed:
            return
        self._disposed = True
        if not self._leave_open:
            self._stream.close()

