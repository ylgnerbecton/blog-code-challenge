from datetime import datetime

from pydantic import BaseModel as PydanticBaseModel


class BaseModel(PydanticBaseModel):
    model_config = {"model_dump_json": {datetime: lambda v: v.isoformat()}}
