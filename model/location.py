from pydantic import BaseModel

class Location(BaseModel):
    city: str
    country: str