import re

from fastapi import HTTPException, status
from pydantic import BaseModel, validator


class Prayers(BaseModel):
    Fajar: str
    Zohar: str
    Asar: str
    Maghrib: str
    Isha: str
    Jumma: str
    Next_Prayer_Time: str


Prayers.model_rebuild()


class ImageUpload(BaseModel):
    time: str
    timezone: str

    @validator("time")
    def validate_time(cls, value):
        time_pattern = re.compile(r"^(0?[1-9]|1[0-2]):[0-5][0-9]\s?(AM|PM|am|pm)$")
        if not time_pattern.match(value):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid time format. Time should be in HH:MM AM/PM format.",
            )
        return value
