from datetime import datetime
from typing import List, Optional, Union

import pytz
from fastapi import status
from fastapi.responses import JSONResponse

from src import settings
from src.presentation.dtos.responses import Error, ErrorResponse

local_timezone = pytz.timezone(settings.settings.TIMEZONE)


def get_current_time() -> datetime:
    return datetime.now().replace(tzinfo=None)


def ensure_timezone_aware(dt: Union[datetime, str]) -> datetime:
    if isinstance(dt, str):
        dt = datetime.fromisoformat(dt)
    if dt.tzinfo is None:
        return local_timezone.localize(dt)
    return dt.astimezone(local_timezone)


def build_error_response(
    status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR,
    error_message: Optional[str] = None,
    field: Optional[str] = None,
    errors: Optional[List[Error]] = None,
) -> JSONResponse:
    if not errors:
        errors = [Error(message=error_message, field=field)]

    error_response_content = ErrorResponse(
        server_unix_timestamp=int(get_current_time().timestamp()),
        status_code=status_code,
        errors=errors,
    )
    return JSONResponse(
        status_code=status_code,
        content=error_response_content.model_dump(),
    )
