# Exception that is thrown when an error occurs while saving a PSD file.

class PsdSaveException(Exception):
    """
    Exception that is thrown when an error occurs while saving a PSD file.

    Initializes a new instance of the PsdSaveException class with a specified error message.
    Initializes a new instance of the PsdSaveException class with a specified error message and inner exception.
    """
    def __init__(self, message, inner_exception=None):
        super().__init__(message)
        self.inner_exception = inner_exception
