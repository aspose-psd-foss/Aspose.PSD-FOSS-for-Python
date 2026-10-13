class ArgumentNullException(Exception):
    """Exception that is thrown when argument is null."""

    def __init__(self, message, inner_exception=None):
        """
        Initializes a new instance of the ArgumentNullException class.

        :param message: The error message that explains the reason for the exception.
        :param inner_exception: The exception that caused the current exception (optional).
        """
        super().__init__(message)
        self.inner_exception = inner_exception
