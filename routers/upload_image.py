import base64

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status
from fastapi.responses import JSONResponse
from slowapi import Limiter
from slowapi.util import get_remote_address
from starlette.requests import Request

from custom_exceptions.exceptions import OpenAIRequestError, OpenAITimeoutError
from models.model import ImageUpload
from utils.vllm_utils import v_llm

limiter = Limiter(key_func=get_remote_address)
router = APIRouter()


@router.post("/upload-image/")
@limiter.limit("5/second")
async def upload_image(
    request: Request, file: UploadFile = File(...), form_data: ImageUpload = Depends()
):
    try:
        if file.content_type not in ["image/jpeg", "image/png"]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid file format. Only JPEG and PNG are allowed.",
            )

        image_data = await file.read()
        base64_image = base64.b64encode(image_data).decode("utf-8")
        response = await v_llm(base64_image, form_data.time, form_data.timezone, form_data.day)

        return JSONResponse(
            content={"status": "success", "response": response},
            status_code=status.HTTP_200_OK,
        )

    except OpenAITimeoutError as e:
        return JSONResponse(
            content={"status": "error", "detail": str(e)},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

    except OpenAIRequestError as e:
        return JSONResponse(
            content={"status": "error", "detail": str(e)},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

    except Exception as e:
        return JSONResponse(
            content={"status": "error", "detail": f"Internal server error: {str(e)}"},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
