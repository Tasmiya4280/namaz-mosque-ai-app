import base64
from openai import OpenAI
import os
from dotenv import load_dotenv
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
from utils import  Prayers

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
app = FastAPI()


@app.post("/upload-image/")
async def upload_image(file: UploadFile = File(...)):
    """
    Uploads an image of a clock, extracts prayer times using OpenAI, and returns them.

    Args:
        file (UploadFile): The image file uploaded by the user.

    Returns:
        JSONResponse: A JSON object containing extracted prayer times.
    """
    image_data = await file.read()
    base64_image = base64.b64encode(image_data).decode("utf-8")
    prompt = """
    - You are provided with an image of a Clock and pydantic model having Prayers names.
    - Your role is to extract the prayes times from the image and return
    """

    completion = client.beta.chat.completions.parse(
        model="gpt-4o",
        messages=[
            {
            "role": "user",
            "content": [
                {
                "type": "text",
                "text":prompt
                },
                {
                "type": "image_url",
                "image_url": {
                    "url":  f"data:image/jpeg;base64,{base64_image}"
                },
                },
            ],
            }
        ],
        response_format=Prayers,
    )
    response = completion.choices[0].message.parsed
    response_dict = response.model_dump()
    
    return JSONResponse(
        content={"status": "success", "response": response_dict},
        status_code=200
    )
