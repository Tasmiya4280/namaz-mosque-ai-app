import os

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()


class Const:
    PROMT = """
    - You are provided with an image of a Clock and a Pydantic model having Prayer names.
    - You are also provided with the user's recent time and time zone.
    - Your role is to extract the prayer times from the image and also predict the next prayer name and time according to the user's recent time/time zone and the Prayers times that extracted from the Clock.
    - Return the response in JSON format as mention in pydantic model
    - If you are unable to extract the timings from image then return "None" in time value
    - Here is the time and time zone given in triple backticks:
    """
    CLIENT = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
