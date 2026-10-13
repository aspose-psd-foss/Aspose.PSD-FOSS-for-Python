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
        BlendMode.Multiply
        if layer.blend_mode_key == BlendMode.Normal
        else BlendMode.Normal
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
