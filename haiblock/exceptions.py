"""
Exception classes for HaiBlock SDK
"""


class HaiBlockError(Exception):
    """Base exception class for HaiBlock SDK"""
    pass


class AuthenticationError(HaiBlockError):
    """Raised when authentication fails"""
    pass


class APIError(HaiBlockError):
    """Raised when API request fails"""
    def __init__(self, message, status_code=None, response=None):
        super().__init__(message)
        self.status_code = status_code
        self.response = response


class ValidationError(HaiBlockError):
    """Raised when input validation fails"""
    pass


class ContentNotFoundError(HaiBlockError):
    """Raised when content is not found"""
    pass


class TransformationError(HaiBlockError):
    """Raised when content transformation fails"""
    pass