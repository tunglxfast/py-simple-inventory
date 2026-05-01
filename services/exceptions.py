"""Domain exceptions for warehouse services."""


class ServiceError(Exception):
    """Base exception for domain-level service errors."""


class ValidationError(ServiceError):
    """Raised when user input is invalid."""


class NotFoundError(ServiceError):
    """Raised when target entities do not exist."""


class InsufficientStockError(ServiceError):
    """Raised when export/hold exceeds available quantity."""
