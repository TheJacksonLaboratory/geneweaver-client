"""Custom exceptions for the GeneWeaver client."""


class EmptyFileError(Exception):
    """Custom exception for when a file is empty.

    Attributes
    ----------
        file_path -- the path of the file that is empty
        message -- explanation of the error
    """

    def __init__(
        self: "EmptyFileError", file_path: str, message: str = "File is empty."
    ) -> None:
        """Initialize the exception."""
        self.file_path = file_path
        self.message = message
        super().__init__(self.message)

    def __str__(self: "EmptyFileError") -> str:
        """Return a string representation of the exception."""
        return f"{self.file_path} -> {self.message}"
