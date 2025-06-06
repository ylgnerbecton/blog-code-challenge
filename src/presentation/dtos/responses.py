from typing import Any, Dict, List, Optional, Union

from pydantic import Field

from .base import BaseModel


class Error(BaseModel):
    field: Optional[str] = Field(None, description="Field associated with the error, if applicable")
    message: str = Field(..., description="Detailed error message")


class ResponseBase(BaseModel):
    server_unix_timestamp: int = Field(
        ...,
        description="Server's Unix timestamp at the moment of the response",
    )
    status_code: int = Field(..., description="HTTP status code of the response")


class Response(ResponseBase):
    response_data: Optional[Union[Dict[str, Any], List[Dict[str, Any]]]] = Field(
        None, description="Data returned in the response"
    )


class ErrorResponse(ResponseBase):
    errors: Optional[Union[List[Error], List[dict]]] = Field(None, description="List of errors if any")


class APIResponse(BaseModel):
    message: str = Field(..., description="The message indicating the result of the operation.")
    success: bool = Field(True, description="Indicates whether the operation was successful.")
    response_data: Optional[Union[Dict[str, Any], List[Dict[str, Any]]]] = Field(
        None, description="Data returned in the response"
    )
