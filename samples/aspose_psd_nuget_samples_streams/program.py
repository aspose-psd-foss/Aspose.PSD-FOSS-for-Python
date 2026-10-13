import sys
import io

from samples.common.samplepathhelper import SamplePathHelper
from samples.common.sampleoutputhelper import SampleOutputHelper
from aspose_psd_foss.image import Image
from aspose_psd_foss.psdimage import PsdImage


def print_sample_description(
    input_path: str,
    output_path: str,
    input_byte_count: int,
    original_position: int,
    current_position: int,
) -> None:
    print("Aspose.PSD Stream Sample")
    print(
        "Description: Demonstrates Load(Stream) and Save(Stream) using an in-memory round-trip without rendering."
    )
    print(f"Input: {input_path}")
    print(f"Output: {output_path}")
    print(f"InputBytes: {input_byte_count}")
    print(f"OriginalStreamPosition: {original_position}")
    print(f"StreamPositionAfterLoad: {current_position}")
    print()


def print_usage() -> None:
    print("Usage: dotnet run --project <sample-project> -- [input.psd] [output.psd]")
    print(
        "Description: Loads a PSD/PSB from a stream and saves it to another stream using an in-memory round-trip."
    )
    print(
        "If no input path is provided, the sample tries to use the repository test fixture."
    )
    print(
        "If no output path is provided, the sample writes to the repository tmp/ folder."
    )


def run_stream_round_trip(input_path: str, output_path: str) -> None:
    with open(input_path, "rb") as f:
        input_bytes = f.read()

    input_stream = io.BytesIO(input_bytes)
    original_position = input_stream.tell()
    image = Image.load(input_stream)  # type: ignore[assignment]

    print_sample_description(
        input_path,
        output_path,
        len(input_bytes),
        original_position,
        input_stream.tell(),
    )

    output_stream = io.BytesIO()
    image.save(output_stream)  # type: ignore[call-arg]

    with open(output_path, "wb") as f:
        f.write(output_stream.getvalue())

    print(f"SavedThroughStream: {output_path}")
    print(f"OutputBytes: {output_stream.getbuffer().nbytes}")
    SampleOutputHelper.open_output_folder(output_path)


if __name__ == "__main__":
    input_path = SamplePathHelper.resolve_input_path(sys.argv[1:])
    if input_path is None:
        print_usage()
        sys.exit()

    output_path = SamplePathHelper.resolve_output_path(sys.argv[1:], 1, "streams-sample-output.psd")
    run_stream_round_trip(input_path, output_path)
