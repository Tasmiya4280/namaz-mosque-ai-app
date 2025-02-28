import asyncio
import base64

from fastapi import Depends, FastAPI, File, HTTPException, UploadFile, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from slowapi import Limiter
from slowapi.errors import RateLimitExceeded
from slowapi.util import get_remote_address
from starlette.requests import Request

from .models import ImageUpload
from .utils import v_llm

app = FastAPI()

limiter = Limiter(key_func=get_remote_address)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

TIMEOUT_SECONDS = 300


@app.exception_handler(RateLimitExceeded)
async def rate_limit_exceeded_handler(request: Request, exc: RateLimitExceeded):
    return JSONResponse(
        status_code=status.HTTP_429_TOO_MANY_REQUESTS,
        content={"detail": "Rate limit exceeded. Try again later."},
    )


@app.post("/upload-image/")
@limiter.limit("5/second")
async def upload_image(
    request: Request, file: UploadFile = File(...), form_data: ImageUpload = Depends()
):
    """
    Upload an image of a clock and extract prayer times using OpenAI.

    This endpoint accepts an image file (JPEG or PNG) along with additional
    form data containing time and timezone information. The image is encoded
    in Base64 format and sent to an AI model (`v_llm`) for processing. The model
    extracts the prayer times from the image and returns the result.

    Rate Limiting:
        - Maximum 5 requests per second.

    Parameters:
        request (Request): The FastAPI request object.
        file (UploadFile): The image file uploaded by the user. Must be JPEG or PNG format.
        form_data (ImageUpload): Additional form data containing:
            - time (str): The time information provided by the user.
            - timezone (str): The timezone associated with the provided time.

    Returns:
        JSONResponse:
            - 200 OK: If the extraction is successful, returns the extracted prayer times.
            - 400 Bad Request: If the uploaded file is not in JPEG or PNG format.
            - 504 Gateway Timeout: If the processing takes too long and times out.
            - 500 Internal Server Error: If an unexpected error occurs during processing.
    """
    try:
        # Check if the file is an image
        if file.content_type not in ["image/jpeg", "image/png"]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid file format. Only JPEG and PNG are allowed.",
            )

        image_data = await file.read()
        base64_image = base64.b64encode(image_data).decode("utf-8")
        response = await asyncio.wait_for(
            v_llm(base64_image, form_data.time, form_data.timezone),
            timeout=TIMEOUT_SECONDS,
        )

        return JSONResponse(
            content={"status": "success", "response": response},
            status_code=status.HTTP_200_OK,
        )

    except asyncio.TimeoutError:
        return JSONResponse(
            content={
                "status": "error",
                "detail": "Request timed out. Please try again.",
            },
            status_code=status.HTTP_504_GATEWAY_TIMEOUT,
        )

    except Exception as e:
        return JSONResponse(
            content={"status": "error", "detail": f"Internal server error: {str(e)}"},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
