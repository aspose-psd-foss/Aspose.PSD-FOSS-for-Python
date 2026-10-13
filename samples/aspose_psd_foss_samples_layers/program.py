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
