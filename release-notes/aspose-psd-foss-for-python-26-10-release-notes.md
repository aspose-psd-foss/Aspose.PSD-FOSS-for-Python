---
id: "aspose-psd-foss-for-python-26-10-release-notes"
slug: "aspose-psd-foss-for-python-26-10-release-notes"
linktitle: "Aspose.PSD FOSS for Python 26.10 - Release Notes"
title: "Aspose.PSD FOSS for Python 26.10 - Release Notes"
description: "Aspose.PSD FOSS for Python 26.10 - Release Notes – the latest updates and examples."
---

{{% alert color="primary" %}}
This page contains release notes for [Aspose.PSD FOSS for Python 26.10](https://pypi.org/project/aspose-psd-foss/)
{{% /alert %}}

# Initial release of Aspose.PSD FOSS for Python

This is the initial release of Aspose.PSD FOSS for Python.  

The FOSS edition provides a lightweight, pure-Python library for reading and writing Photoshop© (PSD/PSB) documents. It focuses on metadata inspection and non-rendering edits, making it ideal for automation, validation, and CI pipelines.

> **Note** – For full-featured editing, rendering, AI file support and additional blend-mode operations see the commercial **Aspose.PSD** product (available for .NET, Java and Python).

## **Public API Changes**

# **Added APIs**

T:aspose_psd_foss.image.Image  
M:aspose_psd_foss.image.Image.load  

T:aspose_psd_foss.psdimage.PsdImage  
P:aspose_psd_foss.psdimage.PsdImage.width  
P:aspose_psd_foss.psdimage.PsdImage.height  
P:aspose_psd_foss.psdimage.PsdImage.channels  
P:aspose_psd_foss.psdimage.PsdImage.bits_per_channel  
P:aspose_psd_foss.psdimage.PsdImage.color_mode  
P:aspose_psd_foss.psdimage.PsdImage.version  
P:aspose_psd_foss.psdimage.PsdImage.size  
P:aspose_psd_foss.psdimage.PsdImage.layers  
P:aspose_psd_foss.psdimage.PsdImage.image_resources  
P:aspose_psd_foss.psdimage.PsdImage.compression  
P:aspose_psd_foss.psdimage.PsdImage.is_flatten  
P:aspose_psd_foss.psdimage.PsdImage.active_layer  

T:aspose_psd_foss.layers.layer.Layer  
P:aspose_psd_foss.layers.layer.Layer.name  
P:aspose_psd_foss.layers.layer.Layer.bounds  
P:aspose_psd_foss.layers.layer.Layer.width  
P:aspose_psd_foss.layers.layer.Layer.height  
P:aspose_psd_foss.layers.layer.Layer.top  
P:aspose_psd_foss.layers.layer.Layer.left  
P:aspose_psd_foss.layers.layer.Layer.bottom  
P:aspose_psd_foss.layers.layer.Layer.right  
P:aspose_psd_foss.layers.layer.Layer.is_visible  
P:aspose_psd_foss.layers.layer.Layer.opacity  
P:aspose_psd_foss.layers.layer.Layer.clipping  
P:aspose_psd_foss.layers.layer.Layer.blend_mode_key  
P:aspose_psd_foss.layers.layer.Layer.channels_count  
P:aspose_psd_foss.layers.layer.Layer.layer_mask_data  
P:aspose_psd_foss.layers.layer.Layer.layer_blending_ranges_data  

T:aspose_psd_foss.layers.blendmode.BlendMode  
F:aspose_psd_foss.layers.blendmode.BlendMode.NORMAL  
F:aspose_psd_foss.layers.blendmode.BlendMode.MULTIPLY  
F:aspose_psd_foss.layers.blendmode.BlendMode.SCREEN  
F:aspose_psd_foss.layers.blendmode.BlendMode.OVERLAY  
F:aspose_psd_foss.layers.blendmode.BlendMode.DARKEN  
F:aspose_psd_foss.layers.blendmode.BlendMode.LIGHTEN  
F:aspose_psd_foss.layers.blendmode.BlendMode.COLORDODGE  
F:aspose_psd_foss.layers.blendmode.BlendMode.COLORBURN  
F:aspose_psd_foss.layers.blendmode.BlendMode.HARDLIGHT  
F:aspose_psd_foss.layers.blendmode.BlendMode.SOFTLIGHT  
F:aspose_psd_foss.layers.blendmode.BlendMode.DIFFERENCE  
F:aspose_psd_foss.layers.blendmode.BlendMode.EXCLUSION  
F:aspose_psd_foss.layers.blendmode.BlendMode.HUE  
F:aspose_psd_foss.layers.blendmode.BlendMode.SATURATION  
F:aspose_psd_foss.layers.blendmode.BlendMode.COLOR  
F:aspose_psd_foss.layers.blendmode.BlendMode.LUMINOSITY  
F:aspose_psd_foss.layers.blendmode.BlendMode.LINEARBURN  
F:aspose_psd_foss.layers.blendmode.BlendMode.LINEARDODGE  
F:aspose_psd_foss.layers.blendmode.BlendMode.LINEARLIGHT  
F:aspose_psd_foss.layers.blendmode.BlendMode.VIVIDLIGHT  
F:aspose_psd_foss.layers.blendmode.BlendMode.PINLIGHT  
F:aspose_psd_foss.layers.blendmode.BlendMode.HARDMIX  
F:aspose_psd_foss.layers.blendmode.BlendMode.SUBTRACT  
F:aspose_psd_foss.layers.blendmode.BlendMode.DIVIDE  
F:aspose_psd_foss.layers.blendmode.BlendMode.DISSOLVE  
F:aspose_psd_foss.layers.blendmode.BlendMode.PASSTHROUGH  

T:aspose_psd_foss.colormodes.ColorModes  
F:aspose_psd_foss.colormodes.ColorModes.BITMAP  
F:aspose_psd_foss.colormodes.ColorModes.GRAYSCALE  
F:aspose_psd_foss.colormodes.ColorModes.INDEXED  
F:aspose_psd_foss.colormodes.ColorModes.RGB  
F:aspose_psd_foss.colormodes.ColorModes.CMYK  
F:aspose_psd_foss.colormodes.ColorModes.MULTICHANNEL  
F:aspose_psd_foss.colormodes.ColorModes.DUOTONE  
F:aspose_psd_foss.colormodes.ColorModes.LAB  

T:aspose_psd_foss.compressionmethod.CompressionMethod  
F:aspose_psd_foss.compressionmethod.CompressionMethod.RAW  
F:aspose_psd_foss.compressionmethod.CompressionMethod.RLE  
F:aspose_psd_foss.compressionmethod.CompressionMethod.ZIP_WITHOUT_PREDICTION  
F:aspose_psd_foss.compressionmethod.CompressionMethod.ZIP_WITH_PREDICTION  

T:aspose_psd_foss.rectangle.Rectangle  
M:aspose_psd_foss.rectangle.Rectangle.__init__  
M:aspose_psd_foss.rectangle.Rectangle.from_left_top_right_bottom  
M:aspose_psd_foss.rectangle.Rectangle.from_points  
M:aspose_psd_foss.rectangle.Rectangle.from_point_and_size  
M:aspose_psd_foss.rectangle.Rectangle.inflated_rect  
M:aspose_psd_foss.rectangle.Rectangle.intersect_rect  
M:aspose_psd_foss.rectangle.Rectangle.union_rect  
P:aspose_psd_foss.rectangle.Rectangle.x  
P:aspose_psd_foss.rectangle.Rectangle.y  
P:aspose_psd_foss.rectangle.Rectangle.width  
P:aspose_psd_foss.rectangle.Rectangle.height  
P:aspose_psd_foss.rectangle.Rectangle.bottom  
P:aspose_psd_foss.rectangle.Rectangle.left  
P:aspose_psd_foss.rectangle.Rectangle.right  
P:aspose_psd_foss.rectangle.Rectangle.top  

T:aspose_psd_foss.point.Point  
P:aspose_psd_foss.point.Point.x  
P:aspose_psd_foss.point.Point.y  
F:aspose_psd_foss.point.Point.Empty  

T:aspose_psd_foss.size.Size  

P:aspose_psd_foss.size.Size.width  
P:aspose_psd_foss.size.Size.height  

T:aspose_psd_foss.resourceblock.ResourceBlock  
M:aspose_psd_foss.resourceblock.ResourceBlock.id  
M:aspose_psd_foss.resourceblock.ResourceBlock.name  
M:aspose_psd_foss.resourceblock.ResourceBlock.data_size  
M:aspose_psd_foss.resourceblock.ResourceBlock.minimal_version  

T:aspose_psd_foss.resources.unknownresource.UnknownResource  
M:aspose_psd_foss.resources.unknownresource.UnknownResource.resource_id  
M:aspose_psd_foss.resources.unknownresource.UnknownResource.name  
M:aspose_psd_foss.resources.unknownresource.UnknownResource.data  

T:aspose_psd_foss.coreexceptions.psdloadexception.PsdLoadException  
T:aspose_psd_foss.coreexceptions.psdsaveexception.PsdSaveException  
T:aspose_psd_foss.coreexceptions.notsupportedexception.NotSupportedException  
T:aspose_psd_foss.coreexceptions.argumentnullexception.ArgumentNullException  

## **Usage examples**

### Basic document inspection – prints document-level metadata

{{< highlight python >}}
import sys
from aspose_psd_foss.image import Image
from aspose_psd_foss.psdimage import PsdImage
from samples.common.samplepathhelper import SamplePathHelper


def run_document_inspection(input_path):
    image = Image.load(input_path)
    if not isinstance(image, PsdImage):
        image = PsdImage(image)
    try:
        print_sample_description(input_path)
        print_header_info(image)
        print_document_state(image)
    finally:
        close = getattr(image, "close", None)
        if callable(close):
            close()


def print_sample_description(input_path):
    print("Aspose.PSD Basic Sample")
    print("Description: Loads a PSD/PSB file and prints document-level metadata without rendering pixel data.")
    print(f"Input: {input_path}")
    print()


def print_header_info(image):
    print("Header")
    print(f"  Width: {image.width}")
    print(f"  Height: {image.height}")
    print(f"  Size: {image.size}")
    print(f"  ChannelsCount: {image.channels_count}")
    print(f"  BitsPerChannel: {image.bits_per_channel}")
    print(f"  ColorMode: {image.color_mode}")
    print(f"  Version: {image.version}")
    print()


def print_document_state(image):
    print("Document State")
    print(f"  Layers: {len(image.layers)}")
    print(f"  ImageResources: {len(image.image_resources)}")
    print(f"  Compression: {image.compression}")
    print(f"  IsFlatten: {image.is_flatten}")
    active_layer_name = (
        image.active_layer.name if getattr(image, "active_layer", None) else "<none>"
    )
    print(f"  ActiveLayer: {active_layer_name}")


def print_usage():
    print("Usage: python program.py [input.psd]")
    print("Description: Prints document-level metadata exposed by the compatible public API subset.")
    print("If no input path is provided, the sample tries to use the repository test fixture.")


if __name__ == "__main__":
    input_path = SamplePathHelper.resolve_input_path(sys.argv[1:])
    if input_path is None:
        print_usage()
    else:
        run_document_inspection(input_path)
{{< /highlight >}}

### Layer inspection – prints supported layer metadata for all layers

{{< highlight python >}}
import sys

from aspose_psd_foss.image import Image
from aspose_psd_foss.psdimage import PsdImage
from samples.common.samplepathhelper import SamplePathHelper


def main(args):
    input_path = SamplePathHelper.resolve_input_path(args)
    if input_path is None:
        print_usage()
        return
    run_layer_inspection(input_path)


def run_layer_inspection(input_path):
    image = Image.load(input_path)
    if not isinstance(image, PsdImage):
        return
    print_sample_description(input_path, len(image.layers))
    for i, layer in enumerate(image.layers):
        print_layer(layer, i)


def print_sample_description(input_path, layer_count):
    print("Aspose.PSD Layer Sample")
    print("Description: Loads a PSD/PSB file and prints supported layer metadata.")
    print(f"Input: {input_path}")
    print(f"LayerCount: {layer_count}")
    print()


def print_layer(layer, index):
    print(f"Layer [{index}]")
    print(f"  Name: {layer.name}")
    print(f"  Bounds: {layer.bounds}")
    print(f"  Width: {layer.width}")
    print(f"  Height: {layer.height}")
    print(f"  Top: {layer.top}")
    print(f"  Left: {layer.left}")
    print(f"  Bottom: {layer.bottom}")
    print(f"  Right: {layer.right}")
    print(f"  IsVisible: {layer.is_visible}")
    print(f"  Opacity: {layer.opacity}")
    print(f"  Clipping: {layer.clipping}")
    print(f"  BlendModeKey: {layer.blend_mode_key}")
    print(f"  ChannelsCount: {layer.channels_count}")
    print(f"  HasLayerMaskData: {layer.layer_mask_data is not None}")
    print(f"  BlendingRangesLength: {len(layer.layer_blending_ranges_data)}")
    print()


def print_usage():
    print("Usage: python program.py [input.psd]")
    print("Description: Prints supported layer metadata.")
    print("If no input path is provided, the sample tries to use the repository test fixture.")


if __name__ == "__main__":
    main(sys.argv[1:])
{{< /highlight >}}

### Stream round-trip – demonstrates `Load(stream)` and `Save(stream)`

{{< highlight python >}}
import sys
import io
from aspose_psd_foss.image import Image
from aspose_psd_foss.psdimage import PsdImage
from samples.common.samplepathhelper import SamplePathHelper
from samples.common.sampleoutputhelper import SampleOutputHelper


def runStreamRoundTrip(input_path, output_path):
    with open(input_path, "rb") as f:
        input_bytes = f.read()

    input_stream = io.BytesIO(input_bytes)
    original_position = input_stream.tell()
    image = Image.load(input_stream)  # type: PsdImage

    printSampleDescription(
        input_path,
        output_path,
        len(input_bytes),
        original_position,
        input_stream.tell(),
    )

    output_stream = io.BytesIO()
    image.save(output_stream)
    output_bytes = output_stream.getvalue()
    with open(output_path, "wb") as f:
        f.write(output_bytes)

    print(f"SavedThroughStream: {output_path}")
    print(f"OutputBytes: {len(output_bytes)}")
    SampleOutputHelper.open_output_folder(output_path)


def printSampleDescription(
    input_path,
    output_path,
    input_byte_count,
    original_position,
    current_position,
):
    print("Aspose.PSD Stream Sample")
    print(
        "Description: Demonstrates Load(Stream) and Save(Stream) using an "
        "in-memory round-trip without rendering."
    )
    print(f"Input: {input_path}")
    print(f"Output: {output_path}")
    print(f"InputBytes: {input_byte_count}")
    print(f"OriginalStreamPosition: {original_position}")
    print(f"StreamPositionAfterLoad: {current_position}")
    print()


def print_usage():
    print("Usage: python program.py [input.psd] [output.psd]")
    print(
        "Description: Loads a PSD/PSB from a stream and saves it to another "
        "stream using an in-memory round-trip."
    )
    print(
        "If no input path is provided, the sample tries to use the repository "
        "test fixture."
    )
    print(
        "If no output path is provided, the sample writes to the repository tmp/ folder."
    )


if __name__ == "__main__":
    args = sys.argv[1:]

    input_path = SamplePathHelper.resolve_input_path(args)
    if input_path is None:
        print_usage()
    else:
        output_path = SamplePathHelper.resolve_output_path(
            args, 1, "streams-sample-output.psd"
        )
        runStreamRoundTrip(input_path, output_path)
{{< /highlight >}}

### Structural editing – applies supported non-rendering edits to the first layer and saves

{{< highlight python >}}
import sys
from aspose_psd_foss.image import Image
from aspose_psd_foss.psdimage import PsdImage
from aspose_psd_foss.layers.layer import Layer
from aspose_psd_foss.layers.blendmode import BlendMode
from samples.common.sampleoutputhelper import SampleOutputHelper
from samples.common.samplepathhelper import SamplePathHelper


def run_structural_editing(input_path, output_path):
    image = Image.load(input_path)  # returns a PsdImage instance
    print_sample_description(input_path, output_path, len(image.layers))

    if len(image.layers) == 0:
        print(
            "The document has no layers, so no supported mutations were applied."
        )
        return

    layer = image.layers[0]
    print("Before:")
    print_editable_layer_state(layer)

    apply_supported_edits(layer)

    print("After:")
    print_editable_layer_state(layer)

    image.save(output_path)
    print(f"SavedEditedDocument: {output_path}")
    SampleOutputHelper.open_output_folder(output_path)


def print_sample_description(input_path, output_path, layer_count):
    print("Aspose.PSD Structural Editing Sample")
    print(
        "Description: Applies supported non-rendering edits to layer metadata and saves the document."
    )
    print(f"Input: {input_path}")
    print(f"Output: {output_path}")
    print(f"LayerCount: {layer_count}")
    print()


def apply_supported_edits(layer):
    layer.name = f"{layer.name} (edited)"
    layer.is_visible = not layer.is_visible
    layer.opacity = 128 if layer.opacity == 255 else 255
    layer.clipping = 1 if layer.clipping == 0 else 0
    layer.blend_mode_key = (
        BlendMode.MULTIPLY
        if layer.blend_mode_key == BlendMode.NORMAL
        else BlendMode.NORMAL
    )

    layer.left += 1
    layer.top += 1
    layer.bottom += 1


def print_editable_layer_state(layer):
    print(f"  Name: {layer.name}")
    print(f"  IsVisible: {layer.is_visible}")
    print(f"  Opacity: {layer.opacity}")
    print(f"  Clipping: {layer.clipping}")
    print(f"  BlendModeKey: {layer.blend_mode_key}")
    print(f"  Bounds: {layer.bounds}")
    print(f"  Top: {layer.top}")
    print(f"  Left: {layer.left}")
    print(f"  Bottom: {layer.bottom}")
    print(f"  Right: {layer.right}")
    print()


def print_usage():
    print("Usage: python program.py [input.psd] [output.psd]")
    print(
        "Description: Applies supported layer metadata edits and saves the result without any rendering pipeline."
    )
    print(
        "If no input path is provided, the sample tries to use the repository test fixture."
    )
    print(
        "If no output path is provided, the sample writes to the repository tmp/ folder."
    )


if __name__ == "__main__":
    args = sys.argv[1:]
    input_path = SamplePathHelper.resolve_input_path(args)
    if input_path is None:
        print_usage()
    else:
        output_path = SamplePathHelper.resolve_output_path(
            args, 1, "structural-editing-sample-output.psd"
        )
        run_structural_editing(input_path, output_path)
{{< /highlight >}}
