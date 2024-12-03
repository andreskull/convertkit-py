class ConvertKitError(Exception):
    """Base exception for ConvertKit API errors"""
    pass

class ConvertKitAPIError(ConvertKitError):
    """Exception raised for API errors"""
    def __init__(self, message, response=None):
        self.message = message
        self.response = response
        super().__init__(self.message)