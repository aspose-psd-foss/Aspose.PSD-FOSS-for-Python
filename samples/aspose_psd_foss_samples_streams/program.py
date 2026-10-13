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
        "If no output path is provided, the sample writes to the repository "
        "tmp/ folder."
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
