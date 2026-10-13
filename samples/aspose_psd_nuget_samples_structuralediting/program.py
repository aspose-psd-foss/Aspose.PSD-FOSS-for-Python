import sys

from aspose_psd_foss.image import Image
from aspose_psd_foss.layers.blendmode import BlendMode
from samples.common.samplepathhelper import SamplePathHelper
from samples.common.sampleoutputhelper import SampleOutputHelper


def main():
    args = sys.argv[1:]
    input_path = SamplePathHelper.resolve_input_path(args)
    if input_path is None:
        _print_usage()
        return

    output_path = SamplePathHelper.resolve_output_path(
        args, 1, "structural-editing-sample-output.psd"
    )
    _run_structural_editing(input_path, output_path)


def _run_structural_editing(input_path, output_path):
    image = Image.load(input_path)  # type: ignore

    _print_sample_description(
        input_path, output_path, len(image.layers) if hasattr(image, "layers") else 0
    )

    if not hasattr(image, "layers") or len(image.layers) == 0:
        print("The document has no layers, so no supported mutations were applied.")
        return

    layer = image.layers[0]
    print("Before:")
    _print_editable_layer_state(layer)

    _apply_supported_edits(layer)

    print("After:")
    _print_editable_layer_state(layer)

    image.save(output_path)
    print(f"SavedEditedDocument: {output_path}")
    SampleOutputHelper.open_output_folder(output_path)


def _print_sample_description(input_path, output_path, layer_count):
    print("Aspose.PSD Structural Editing Sample")
    print(
        "Description: Applies supported non-rendering edits to layer metadata and saves the document."
    )
    print(f"Input: {input_path}")
    print(f"Output: {output_path}")
    print(f"LayerCount: {layer_count}")
    print()


def _apply_supported_edits(layer):
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
    print()


def _print_usage():
    print("Usage: python program.py [input.psd] [output.psd]")
    print(
        "Description: Applies supported layer metadata edits and saves the result without any rendering pipeline."
    )
    print(
        "If no input path is provided, the sample tries to use the repository test fixture."
    )
    print("If no output path is provided, the sample writes to the repository tmp/ folder.")


if __name__ == "__main__":
    main()

