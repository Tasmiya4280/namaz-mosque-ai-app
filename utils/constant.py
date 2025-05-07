class Const:
    PROMPT = """
    - You are provided with an image of a clock and a Pydantic model containing prayer names.
    - You are also given the user's current time, time zone, and day.
    - Your role is to extract the prayer times from the image.
    - You must **correctly predict the next prayer** according to the given day, time, and extracted prayer times.
    - **Ensure proper reasoning before deciding the next prayer**:
      - If the provided time is **before** a prayer time, return that as the next prayer.
      - If the provided time is **after Isha**, return Fajar as the next prayer for the next day.
      - On **Friday**, if the time is between Fajar and Zohar, **return Jumma instead of Zohar**.
    - The response should be **valid JSON** as per the Pydantic model, with AM/PM formatting.
    - If unable to extract timings from the image, return `"None"` in time values.
    - **Important:** Use reasoning before selecting the next prayer to **avoid hallucination**.

    Here is the time and time zone given in triple backticks:
    ```
    """
