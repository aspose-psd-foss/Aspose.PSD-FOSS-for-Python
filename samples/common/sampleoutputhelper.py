import os
import sys
import subprocess
from pathlib import Path


class SampleOutputHelper:
    @classmethod
    def open_output_folder(cls, output_path):
        full_output_path = Path(output_path).resolve()
        output_directory = full_output_path.parent

        try:
            if sys.platform.startswith('win'):
                os.startfile(output_directory)
            elif sys.platform == "darwin":
                subprocess.Popen([
                    "open",
                    "-R",
                    str(output_directory)
                ])
            else:
                subprocess.Popen([
                    "xdg-open",
                    str(output_directory)
                ])

            print(f"OpenedOutputFolder: {output_directory}")
        except Exception as exception:
            print(f"FailedToOpenOutputFolder: {exception}")


def main():
    if len(sys.argv) < 2:
        print("Usage: script.py <output_path>")
        return
    SampleOutputHelper.open_output_folder(sys.argv[1])


if __name__ == "__main__":
    main()

