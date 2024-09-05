from fastapi import HTTPException, status


class APIError(HTTPException):
    def __init__(self, status_code: int, error_type: str, detail: str):
        error_detail = {"type": error_type, "message": detail}
        super().__init__(status_code=status_code, detail=[error_detail])


def handle_exception(
    e: Exception,
    status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR,
    error_type: str = "server_error",
):
    error_detail = f"Internal Server Error: {str(e)}"
    return APIError(status_code=status_code, error_type=error_type, detail=error_detail)


def conflict_error(field: str):
    return APIError(
        status_code=status.HTTP_409_CONFLICT,
        error_type="conflict_error",
        detail=f"{field.capitalize()} already exists!",
    )


def not_found_error(field: str):
    return APIError(
        status_code=status.HTTP_404_NOT_FOUND,
        error_type="not_found_error",
        detail=f"{field.capitalize()} not found!",
    )


def validation_error(field: str):
    return APIError(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        error_type="validation_error",
        detail=f"Invalid {field.capitalize()}!",
    )


def credential_error():
    return APIError(
        status_code=status.HTTP_401_UNAUTHORIZED,
        error_type="credential_error",
        detail="Invalid Credentials!",
    )


def unauthorized_error():
    return APIError(
        status_code=status.HTTP_401_UNAUTHORIZED,
        error_type="unauthorized_error",
        detail="You are not authorized!",
    )