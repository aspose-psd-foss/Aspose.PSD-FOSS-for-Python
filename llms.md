# Aspose.PSD FOSS – Complete Reference

**Aspose.PSD FOSS for Python** is a pure Python library for loading, inspecting, and mutating Photoshop PSD/PSB files without any rendering pipeline. Its public API mirrors the compatible subset of Aspose.PSD for .NET, exposing document level metadata, layer properties, and raw preserving save functionality.

---  

## Installation  

```bash
pip install aspose-psd-foss
```

*Requires Python 3.7+.*  
The library is pure Python; no external native dependencies are needed.

---  

## Core Usage  

```python
import sys
from aspose_psd_foss.image import Image
from aspose_psd_foss.psdimage import PsdImage
from samples.common.samplepathhelper import SamplePathHelper


def run_document_inspection(input_path):
    image = Image.load(input_path)               # returns an Image (PsdImage)
    if not isinstance(image, PsdImage):
        image = PsdImage(image)

    print("Aspose.PSD Basic Sample")
    print(f"Input: {input_path}\n")

    # Header information
    print("Header")
    print(f"  Width: {image.width}")
    print(f"  Height: {image.height}")
    print(f"  Size: {image.size}")
    print(f"  ChannelsCount: {image.channels_count}")
    print(f"  BitsPerChannel: {image.bits_per_channel}")
    print(f"  ColorMode: {image.color_mode}")
    print(f"  Version: {image.version}\n")

    # Document state
    print("Document State")
    print(f"  Layers: {len(image.layers)}")
    print(f"  ImageResources: {len(image.image_resources)}")
    print(f"  Compression: {image.compression}")
    print(f"  IsFlatten: {image.is_flatten}")
    active = image.active_layer.name if image.active_layer else "<none>"
    print(f"  ActiveLayer: {active}")

    # Close the underlying stream if needed
    close = getattr(image, "close", None)
    if callable(close):
        close()


if __name__ == "__main__":
    input_path = SamplePathHelper.resolve_input_path(sys.argv[1:])
    if input_path is None:
        print("Usage: python program.py [input.psd]")
        print("If no path is supplied the sample uses the repository test fixture.")
    else:
        run_document_inspection(input_path)
```

### What the sample shows  

| Property                | Meaning                                                                      |
|------------------------|------------------------------------------------------------------------------|
| `width` / `height`      | Document dimensions in pixels                                                |
| `size`                  | `Size(width, height)` wrapper                                               |
| `channels_count`        | Number of channels (e.g., 3 for RGB)                                        |
| `bits_per_channel`      | Bits stored per channel (usually 8)                                         |
| `color_mode`            | `ColorModes` enum (`RGB`, `CMYK`, …)                                        |
| `version`               | PSD container version (always 6 for the compatible subset)                  |
| `layers`                | List of `Layer` objects (read only unless mutated)                           |
| `image_resources`       | List of image resource blocks (preserved but immutable)                     |
| `compression`           | `CompressionMethod` (`RLE`, `RAW`, `ZIP_WITHOUT_PREDICTION`, …)            |
| `is_flatten`            | `True` when the document contains no layers                                 |
| `active_layer`          | First layer in the stack (or `None`)                                         |

---  

## Layer Sample  

```python
import sys
from aspose_psd_foss.image import Image
from aspose_psd_foss.psdimage import PsdImage
from samples.common.samplepathhelper import SamplePathHelper


def run_layer_inspection(input_path):
    image = Image.load(input_path)
    if not isinstance(image, PsdImage):
        return

    print("Aspose.PSD Layer Sample")
    print(f"Input: {input_path}")
    print(f"LayerCount: {len(image.layers)}\n")

    for i, layer in enumerate(image.layers):
        print(f"Layer [{i}]")
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
        print(f"  BlendingRangesLength: {len(layer.layer_blending_ranges_data)}\n")


if __name__ == "__main__":
    args = sys.argv[1:]
    input_path = SamplePathHelper.resolve_input_path(args)
    if input_path is None:
        print("Usage: python program.py [input.psd]")
        print("If no path is supplied the sample uses the repository test fixture.")
    else:
        run_layer_inspection(input_path)
```

### Layer properties of interest  

| Property                     | Type / Description                                             |
|------------------------------|---------------------------------------------------------------|
| `name`                       | Layer name (editable)                                          |
| `bounds`                     | `Rectangle` (left, top, width, height)                        |
| `top`, `left`, `bottom`, `right` | Individual edges (editable)                                  |
| `is_visible` / `IsVisible`  | Visibility flag (editable)                                     |
| `opacity`                    | 0 255 (editable)                                               |
| `clipping`                   | 0 = no clipping, 1 = clipping (editable)                       |
| `blend_mode_key`             | `BlendMode` enum (`NORMAL`, `MULTIPLY`, …) (editable)         |
| `channels_count`             | Number of channel entries                                      |
| `layer_mask_data`            | `LayerMaskDataShort` (read only in FOSS)                       |
| `layer_blending_ranges_data` | `LayerBlendingRangesData` (read only in FOSS)                 |

---  

## Stream (In Memory) Sample  

```python
import sys, io
from aspose_psd_foss.image import Image
from aspose_psd_foss.psdimage import PsdImage
from samples.common.samplepathhelper import SamplePathHelper
from samples.common.sampleoutputhelper import SampleOutputHelper


def run_stream_round_trip(input_path, output_path):
    # Load the file into a BytesIO buffer
    with open(input_path, "rb") as f:
        input_bytes = f.read()
    input_stream = io.BytesIO(input_bytes)

    # Load from stream (no rendering)
    image = Image.load(input_stream)          # type: PsdImage

    print("Aspose.PSD Stream Sample")
    print(f"Input: {input_path}")
    print(f"Output: {output_path}")
    print(f"InputBytes: {len(input_bytes)}")
    print(f"OriginalStreamPosition: {input_stream.tell()}")
    print(f"StreamPositionAfterLoad: {input_stream.tell()}\n")

    # Save back to another in memory stream
    output_stream = io.BytesIO()
    image.save(output_stream)
    output_bytes = output_stream.getvalue()

    # Write to disk
    with open(output_path, "wb") as f:
        f.write(output_bytes)

    print(f"SavedThroughStream: {output_path}")
    print(f"OutputBytes: {len(output_bytes)}")
    SampleOutputHelper.open_output_folder(output_path)


if __name__ == "__main__":
    args = sys.argv[1:]
    input_path = SamplePathHelper.resolve_input_path(args)
    if input_path is None:
        print("Usage: python program.py [input.psd] [output.psd]")
        sys.exit(1)

    output_path = SamplePathHelper.resolve_output_path(
        args, 1, "streams-sample-output.psd"
    )
    run_stream_round_trip(input_path, output_path)
```

*Demonstrates `Image.load(stream)` and `image.save(stream)` without ever materialising pixel data.*

---  

## Structural Editing Sample  

```python
import sys
from aspose_psd_foss.image import Image
from aspose_psd_foss.psdimage import PsdImage
from aspose_psd_foss.layers.blendmode import BlendMode
from samples.common.sampleoutputhelper import SampleOutputHelper
from samples.common.samplepathhelper import SamplePathHelper


def run_structural_editing(input_path, output_path):
    image = Image.load(input_path)   # returns a PsdImage
    print("Aspose.PSD Structural Editing Sample")
    print(f"Input: {input_path}")
    print(f"Output: {output_path}")
    print(f"LayerCount: {len(image.layers)}\n")

    if not image.layers:
        print("The document has no layers, so no supported mutations were applied.")
        return

    layer = image.layers[0]
    print("Before:")
    _print_editable_layer_state(layer)

    # Mutate supported fields
    layer.name = f"{layer.name} (edited)"
    layer.is_visible = not layer.is_visible
    layer.opacity = 128 if layer.opacity == 255 else 255
    layer.clipping = 1 if layer.clipping == 0 else 0
    layer.blend_mode_key = (
        BlendMode.MULTIPLY if layer.blend_mode_key == BlendMode.NORMAL else BlendMode.NORMAL
    )
    layer.left += 1
    layer.top += 1
    layer.bottom += 1

    print("\nAfter:")
    _print_editable_layer_state(layer)

    # Persist changes
    image.save(output_path)
    print(f"\nSavedEditedDocument: {output_path}")
    SampleOutputHelper.open_output_folder(output_path)


def _print_editable_layer_state(layer):
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


if __name__ == "__main__":
    args = sys.argv[1:]
    input_path = SamplePathHelper.resolve_input_path(args)
    if input_path is None:
        print("Usage: python program.py [input.psd] [output.psd]")
        sys.exit(1)

    output_path = SamplePathHelper.resolve_output_path(
        args, 1, "structural-editing-sample-output.psd"
    )
    run_structural_editing(input_path, output_path)
```

*Only the mutable subset of layer metadata is supported; all other structures are preserved byte for byte.*

---  

## Naming Conventions  

All public members have **snake_case** primary names and **PascalCase** aliases for .NET compatibility.

```python
# Python style
layer.is_visible = True
layer.blend_mode_key = BlendMode.MULTIPLY

# .NET style
layer.IsVisible = True
layer.BlendModeKey = BlendMode.MULTIPLY
```

---  

## Color Strings  

Color values are always exposed as **6 digit `RRGGBB` hex strings without a leading `#`**.

```python
# Correct
layer.blend_mode_key = BlendMode.MULTIPLY   # enum, not a color string
# (Color strings are used in other APIs such as font colors, not in PSD core)
```

---  

## Rectangle & Point Helpers  

* `Rectangle` – integer based rectangle with properties `x`, `y`, `width`, `height` and PascalCase aliases `X`, `Y`, `Width`, `Height`.  
* `Point` – integer coordinates `x`, `y` with `Empty` sentinel (`Point(0,0)`).  
* `Size` – `width`, `height` pair.

Common operations:  

```python
rect = Rectangle.from_left_top_right_bottom(10, 20, 40, 60)
print(rect)                     # {X=10, Y=20, Width=30, Height=40}
rect.offset(5, -3)              # move rectangle
rect.inflate(Size(2, 4))        # expand rectangle
```

---  

## Key Classes  

| Class | Description |
|---|---|
| `PsdImage` | Root object; loads, inspects, mutates, and saves PSD/PSB files. |
| `Image` (ABC) | Abstract base for image types; `Image.load()` returns a concrete `PsdImage`. |
| `Layer` | Represents a single PSD layer; mutable fields include `name`, `is_visible`, `opacity`, `clipping`, `blend_mode_key`, and bounds. |
| `Rectangle` | Integer rectangle used for layer bounds and other geometry. |
| `Point` | Integer point (x, y). |
| `Size` | Width/height pair. |
| `BlendMode` (Enum) | Supported blend modes (`NORMAL`, `MULTIPLY`, `SCREEN`, …). |
| `ColorModes` (IntEnum) | Document color modes (`BITMAP`, `GRAYSCALE`, `INDEXED`, `RGB`, `CMYK`, …). |
| `CompressionMethod` (IntEnum) | Image data compression (`RAW`, `RLE`, `ZIP_WITHOUT_PREDICTION`, `ZIP_WITH_PREDICTION`). |
| `ImageResourcesSection` | Raw preserved image resource block container. |
| `LayerAndMaskSection` | Holds layer records, channel image data, and global mask/tail bytes. |
| `ImageData` | Holds merged image data payload and structural description (`ImageDataStructure`). |
| `SamplePathHelper` / `SampleOutputHelper` | Utility classes used by the sample programs. |
| `PsdHeader` | Parsed file header (width, height, channels, bit depth, color mode, version). |
| `PsdImageDocumentState` | Internal immutable snapshot of all parsed sections. |

---  

## Typical Workflow  

1. **Load** – `image = Image.load(path_or_stream)`  
2. **Inspect** – read properties (`image.width`, `layer.bounds`, etc.)  
3. **Mutate** – modify mutable layer fields (`layer.opacity = 128`) or document level flags (`image.color_mode = ColorModes.CMYK`)  
4. **Save** – `image.save(output_path)` – preserves all untouched raw bytes, guaranteeing byte exact round trips when no mutations occur.  

---  

## Frequently Asked Questions  

* **Does the library render raster image data?**  
  No. It works purely on the file structure; pixel decoding is not performed.

* **Can I add or delete layers?**  
  The current FOSS subset only supports mutation of existing layer metadata. Adding/removing layers is not implemented.

* **Is the saved file byte identical to the source when unchanged?**  
  Yes. When no public members are mutated, the original raw sections are written back unchanged.

* **What about ICC profiles and other image resources?**  
  They are parsed as `UnknownResource` blocks, exposed read only via `image.resources`. Mutation is not supported.

---  

*End of Aspose.PSD FOSS reference.*
