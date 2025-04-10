# exceptions.py

class DeribitAPIException(Exception):
    """Base exception for Deribit API errors."""
    def __init__(self, message: str):
        self.message = message
        super().__init__(message)


# Mapping of Deribit error codes to specific exceptions

class InvalidRequest(DeribitAPIException):
    def __init__(self, message: str = ""):
        super().__init__(message or "Invalid request (missing or invalid fields).")


class AuthenticationError(DeribitAPIException):
    def __init__(self, message: str = ""):
        super().__init__(message or "Authentication failed.")


class AuthorizationError(DeribitAPIException):
    def __init__(self, message: str = ""):
        super().__init__(message or "Client is not authorized to access the requested resource.")


class NotFoundError(DeribitAPIException):
    def __init__(self, message: str = ""):
        super().__init__(message or "Requested resource was not found.")


class MethodNotFoundError(DeribitAPIException):
    def __init__(self, message: str = ""):
        super().__init__(message or "Requested method was not found.")


class InvalidParamsError(DeribitAPIException):
    def __init__(self, message: str = ""):
        super().__init__(message or "Invalid method parameters.")


class InternalError(DeribitAPIException):
    def __init__(self, message: str = ""):
        super().__init__(message or "Internal error.")


class ServiceUnavailableError(DeribitAPIException):
    def __init__(self, message: str = ""):
        super().__init__(message or "Service temporarily unavailable.")


class RequestLimitExceeded(DeribitAPIException):
    def __init__(self, message: str = ""):
        super().__init__(message or "Request rate limit exceeded.")


class InvalidSession(DeribitAPIException):
    def __init__(self, message: str = ""):
        super().__init__(message or "Session is invalid or expired.")


class UnsupportedError(DeribitAPIException):
    def __init__(self, message: str = ""):
        super().__init__(message or "Feature not supported.")


# Error code to exception mapping
ERROR_CODE_MAP = {
    -32600: InvalidRequest,
    -32601: MethodNotFoundError,
    -32602: InvalidParamsError,
    -32603: InternalError,
    -32000: AuthenticationError,
    -32001: AuthorizationError,
    -32002: NotFoundError,
    -32003: InvalidSession,
    -32004: UnsupportedError,
    -32005: RequestLimitExceeded,
    -32099: ServiceUnavailableError,
}


def raise_deribit_exception(code: int, message: str = ""):
    exc_class = ERROR_CODE_MAP.get(code, DeribitAPIException)
    raise exc_class(message)
