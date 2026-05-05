class DivisasException(Exception):
    """Base exception for Divisas.lat API errors."""
    
    def __init__(self, message: str, status_code: int = 0):
        super().__init__(message)
        self.status_code = status_code
