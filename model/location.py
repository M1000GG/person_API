from pydantic import BaseModel, Optional


class Location(BaseModel):
    city: str
    country: str
    state_code: Optional[str] = None
    is_capital: Optional[bool] = False