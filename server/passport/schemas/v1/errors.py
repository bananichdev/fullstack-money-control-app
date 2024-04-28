from fastapi import HTTPException, status


class DBAPICallError(HTTPException):
    def __init__(self, msg: str = "..."):
        super().__init__(
            detail=f"DB api call failed: {msg}",
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


class TokenError(HTTPException):
    def __init__(self, detail, status_code):
        super().__init__(
            detail=detail,
            status_code=status_code,
        )


class TokenIncorrect(TokenError):
    def __init__(self):
        super().__init__(
            detail="Token incorrect", status_code=status.HTTP_403_FORBIDDEN
        )


class TokenNotFound(TokenError):
    def __init__(self):
        super().__init__(
            detail="Token was not found", status_code=status.HTTP_401_UNAUTHORIZED
        )


class AccountError(HTTPException):
    def __init__(self, detail, status_code):
        super().__init__(
            detail=detail,
            status_code=status_code,
        )


class AccountNotFound(AccountError):
    def __init__(self):
        super().__init__(
            detail="Account does not exists", status_code=status.HTTP_404_NOT_FOUND
        )


class AccountWrongPassword(AccountError):
    def __init__(self):
        super().__init__(detail="Wrong password", status_code=status.HTTP_403_FORBIDDEN)


class AccountReplenishmentForbidden(AccountError):
    def __init__(self):
        super().__init__(
            detail="You can not top up your balance today",
            status_code=status.HTTP_403_FORBIDDEN,
        )


class RequestError(HTTPException):
    def __init__(self, detail, status_code):
        super().__init__(
            detail=detail,
            status_code=status_code,
        )


class RequestAuthDataError(RequestError):
    def __init__(self):
        super().__init__(
            detail="Insufficient information for authentication",
            status_code=status.HTTP_400_BAD_REQUEST,
        )
