# Exception that is thrown when an error occurs while saving a PSD file.


class PsdSaveException(Exception):
    """Initializes a new instance of the PsdSaveException class with a specified error message."""
    def __init__(self, message, inner_exception=None):
        """
        :param message: The error message that explains the reason for the exception.
        :param inner_exception: The exception that caused the current exception.
        """
        super().__init__(message)
        self.inner_exception = inner_exception
