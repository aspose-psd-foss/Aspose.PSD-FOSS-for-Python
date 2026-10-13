import os


class SamplePathHelper:
    # Provides shared path resolution helpers for sample projects.
    _repository_root = os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            '../../../../../'
        )
    )

    @classmethod
    def resolve_input_path(cls, args):
        # Resolves the input PSD path from command-line arguments or the repository fixture.
        # args: The command-line arguments.
        # Returns: The resolved PSD path, or None when no input can be found.
        if len(args) > 0 and os.path.isfile(args[0]):
            return os.path.abspath(args[0])

        repository_fixture = os.path.abspath(
            os.path.join(
                os.path.dirname(__file__),
                '../../src/aspose_psd_foss_test/testdata/test.psd'
            )
        )
        return repository_fixture if os.path.isfile(repository_fixture) else None

    @classmethod
    def resolve_output_path(cls, args, output_argument_index, default_file_name):
        # Resolves the output PSD path from command-line arguments or a default file name.
        # args: The command-line arguments.
        # output_argument_index: The zero-based argument index that may contain the output path.
        # default_file_name: The default output file name to use when no explicit path is provided.
        # Returns: The resolved output path.
        if len(args) > output_argument_index and args[output_argument_index].strip():
            return os.path.abspath(args[output_argument_index])

        output_directory = os.path.join(cls._repository_root, "tmp")
        os.makedirs(output_directory, exist_ok=True)
        return os.path.join(output_directory, default_file_name)
