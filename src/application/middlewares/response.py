import json
import re

from fastapi import Request, Response, status
from fastapi.responses import JSONResponse
from pydantic import ValidationError
from starlette.concurrency import iterate_in_threadpool
from starlette.exceptions import HTTPException as StarletteHTTPException
from starlette.middleware.base import BaseHTTPMiddleware

from src.application.utils.general import build_error_response, get_current_time
from src.logger import logger
from src.presentation.dtos.responses import Error, ErrorResponse
from src.presentation.dtos.responses import Response as ApiResponse


class ResponseMiddleware(BaseHTTPMiddleware):

    async def dispatch(self, request: Request, call_next) -> Response:
        if request.url.path in ["/openapi.json", "/docs", "/redoc"]:
            return await call_next(request)

        try:
            response = await call_next(request)

            if response.headers.get("content-type") == "application/json":
                response_body = [chunk async for chunk in response.body_iterator]
                response.body_iterator = iterate_in_threadpool(iter(response_body))

                if response.status_code == status.HTTP_204_NO_CONTENT:
                    return response

                content = b"".join(response_body).decode("utf-8")
                content_data = json.loads(content)

                if response.status_code < status.HTTP_400_BAD_REQUEST:
                    metadata = ApiResponse(
                        server_unix_timestamp=int(get_current_time().timestamp()),
                        status_code=response.status_code,
                        response_data=content_data,
                    )
                else:
                    errors = content_data.get("errors", [content_data])
                    error_details = self._process_errors(errors)

                    metadata = ErrorResponse(
                        server_unix_timestamp=int(get_current_time().timestamp()),
                        status_code=response.status_code,
                        errors=error_details,
                    )

                response = JSONResponse(content=metadata.model_dump(), status_code=response.status_code)

            return response

        except StarletteHTTPException as exc:
            error_message, field = self._parse_error_message(
                exc.detail if isinstance(exc.detail, str) else json.dumps(exc.detail)
            )
            logger.error(context="StarletteHTTPException", message=error_message)
            return build_error_response(
                status_code=exc.status_code,
                error_message=error_message,
                field=field,
            )

        except ValidationError as exc:
            error_details = self._process_validation_errors(exc.errors())
            logger.error(context="ValidationError", message=str(exc.errors()))
            return build_error_response(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                error_message="Validation error",
                field=None,
                errors=error_details,
            )

        except ValueError as exc:
            error_message = str(exc)
            logger.error(context="ValueError", message=error_message)
            return build_error_response(
                status_code=status.HTTP_400_BAD_REQUEST,
                error_message=error_message,
                field=None,
            )

        except Exception as exc:
            parsed_message, field = self._parse_error_message(str(exc))
            logger.error(context="Exception", message=parsed_message)
            return build_error_response(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                error_message="An unexpected error occurred.",
                field=field,
            )

    def _process_errors(self, errors):
        error_details = []

        for error in errors:
            if isinstance(error, dict):
                if "loc" in error and "msg" in error:
                    field = ".".join(str(loc) for loc in error["loc"])
                    error_message = error["msg"]
                    error_details.append(Error(message=error_message, field=field))
                else:
                    try:
                        error_details.append(Error(**error))
                    except ValidationError as ve:
                        logger.error(context="ValidationError", message=str(ve))
                        error_message, field = self._parse_error_message(error.get("detail", json.dumps(error)))
                        error_details.append(Error(message=error_message, field=field))
            else:
                error_message, field = self._parse_error_message(str(error))
                error_details.append(Error(message=error_message, field=field))
        return error_details

    def _parse_error_message(self, error_message: str) -> tuple:
        try:
            if isinstance(error_message, (list, dict)):
                error_message = json.dumps(error_message)
            error_message = error_message.replace('"', "'").replace("\\", "")
            field = None

            match = re.search(r"column '([^']+)'", error_message)
            if match:
                field = match.group(1)

            error_message = re.sub(r"\(psycopg2\.errors\.[^)]+\)\s*", "", error_message)
            error_message = re.split(r"\n|\(Background on this error at:", error_message)[0].strip()
            return error_message, field
        except Exception as parse_exc:
            logger.error(
                context="ErrorParsing",
                message=f"Error parsing error message: {parse_exc}",
            )
            return error_message, None
