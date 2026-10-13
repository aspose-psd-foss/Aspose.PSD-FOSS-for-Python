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
