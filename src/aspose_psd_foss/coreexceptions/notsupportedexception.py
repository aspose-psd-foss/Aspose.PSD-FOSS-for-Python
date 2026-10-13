class NotSupportedException(Exception):
    """Exception that is thrown when operation is not supported."""

    def __init__(self, message, inner_exception=None):
        """
        Initializes a new instance of the NotSupportedException class.

        :param message: The error message that explains the reason for the exception.
        :param inner_exception: The exception that caused the current exception (optional).
        """
        super().__init__(message)
        self.inner_exception = inner_exception
