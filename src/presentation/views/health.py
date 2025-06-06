from fastapi import APIRouter
from starlette import status
from starlette.responses import JSONResponse

router = APIRouter()


@router.get("", status_code=status.HTTP_200_OK)
def health_check():
    return JSONResponse(content={"status": "ok"})
