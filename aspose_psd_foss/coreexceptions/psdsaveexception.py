# Exception that is thrown when an error occurs while saving a PSD file.
class PsdSaveException(Exception):
    """
    Initializes a new instance of the PsdSaveException class with a specified error message.

    :param message: The error message that explains the reason for the exception.
    """
    def __init__(self, message, inner_exception=None):
        super().__init__(message)
        self.inner_exception = inner_exception
