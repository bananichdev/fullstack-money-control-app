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
        super().__init__(detail="Token incorrect", status_code=status.HTTP_403_FORBIDDEN)


class TokenNotFound(TokenError):
    def __init__(self):
        super().__init__(detail="Token was not found", status_code=status.HTTP_401_UNAUTHORIZED)


class AccountError(HTTPException):
    def __init__(self, detail, status_code):
        super().__init__(
            detail=detail,
            status_code=status_code,
        )
