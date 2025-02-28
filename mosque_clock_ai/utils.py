import asyncio

from .constants import Const
from .models import Prayers

client = Const.CLIENT


async def v_llm(base64_image, time, timezone):
    prompt = Const.PROMT + f""" ```Time:{time}``` and ```Time Zone:{timezone}```"""

    def sync_openai_request():
        return client.beta.chat.completions.parse(
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

    # Run the OpenAI API call in a separate thread
    completion = await asyncio.to_thread(sync_openai_request)
    response_data = completion.choices[0].message.parsed
    response = response_data.model_dump()
    return response
