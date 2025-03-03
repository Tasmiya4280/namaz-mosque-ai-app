from dotenv import load_dotenv
from openai import AsyncOpenAI  # Use Async client

from .constants import Const
from .models import Prayers

load_dotenv()
client = AsyncOpenAI(api_key=Const.API_KEY)


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
            response_format=Prayers,
        )

        return completion.choices[0].message.parsed.model_dump()

    except Exception:
        return {"error": "OpenAI API call failed:"}
