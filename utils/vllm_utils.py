import logging

from openai import APITimeoutError, AsyncOpenAI  # Use Async client

from config.config import OPENAI_API_KEY, TIMEOUT_SECONDS
from custom_exceptions.exceptions import (  # Import custom exceptions
    OpenAIRequestError, OpenAITimeoutError)
from models.model import Prayers
from utils.constant import Const

client = AsyncOpenAI(api_key=OPENAI_API_KEY)


# Configure logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Create a file handler
file_handler = logging.FileHandler("openai_requests.log")
file_handler.setLevel(logging.ERROR)

# Create a console handler
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)

# Create a formatter and add it to the handlers
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
file_handler.setFormatter(formatter)
console_handler.setFormatter(formatter)

# Add handlers to logger
logger.addHandler(file_handler)
logger.addHandler(console_handler)


async def v_llm(base64_image: str, time: str, timezone: str):
    """Sends an image and time-related prompt to OpenAI API asynchronously."""
    prompt = f"{Const.PROMT} ```Time: {time}``` and ```Time Zone: {timezone}```"

    try:
        # Directly await the API request
        completion = await client.beta.chat.completions.parse(
            model="gpt-4o",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt},
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{base64_image}"
                            },
                        },
                    ],
                }
            ],
            timeout=int(TIMEOUT_SECONDS) if TIMEOUT_SECONDS is not None else 300,
            response_format=Prayers,
        )
        logger.info("Request to OpenAI API successful.")
        return completion.choices[0].message.parsed.model_dump()

    except APITimeoutError:
        logger.error("OpenAI API request timed out.")
        raise OpenAITimeoutError("The request timed out. Please try again.")

    except Exception:
        logger.exception("Exception occurred while processing OpenAI request.")
        raise OpenAIRequestError("Internal server error")
