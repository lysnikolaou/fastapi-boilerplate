from firebase_admin.exceptions import FirebaseError
from starlette import status


class RookException(Exception):
    status_code: int
    code: str
    detail: str


class NotAuthenticated(RookException):
    status_code: int = status.HTTP_401_UNAUTHORIZED
    code: str = "NOT_AUTHENTICATED"
    detail: str = "Not authenticated"


class AuthenticationFailed(RookException):
    status_code: int = status.HTTP_403_FORBIDDEN
    code: str = "AUTHENTICATION_FAILED"
    detail: str

    def __init__(self, detail: str) -> None:
        self.detail = detail


class AuthenticationTokenExpired(AuthenticationFailed):
    code: str = "AUTHENTICATION_TOKEN_EXPIRED"
    detail: str = "Authentication token expired"


class FirebaseException(RookException):
    """Exception for requests, where the method is not allowed"""

    status_code: int
    code: str
    detail: str

    def __init__(self, error: FirebaseError):
        """The error handling here stems from https://cloud.google.com/apis/design/errors#handling_errors"""
        codes = {
            "OK": 200,
            "INVALID_ARGUMENT": 400,
            "FAILED_PRECONDITION": 400,
            "OUT_OF_RANGE": 400,
            "UNAUTHENTICATED": 401,
            "PERMISSION_DENIED": 403,
            "NOT_FOUND": 404,
            "ABORTED": 409,
            "ALREADY_EXISTS": 409,
            "RESOURCE_EXHAUSTED": 429,
            "CANCELLED": 499,
            "DATA_LOSS": 500,
            "UNKNOWN": 500,
            "INTERNAL": 500,
            "NOT_IMPLEMENTED": 501,
            "N/A": 502,
            "UNAVAILABLE": 503,
            "DEADLINE_EXCEEDED": 504,
        }
        self.status_code = codes[error.code]
        self.code = error.code
        self.detail = str(error)
        self.args = error.args


class NonUniqueEmailException(RookException):
    status_code: int = status.HTTP_409_CONFLICT
    code: str = "NON_UNIQUE_EMAIL"
    detail: str = "A user with this email already exists"
