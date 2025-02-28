from pydantic import BaseModel

class Prayers(BaseModel):
    Fajar: str
    Zohar: str
    Asar: str
    Maghrib: str
    Isha: str
    Jumma: str

Prayers.model_rebuild()
