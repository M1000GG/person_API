from pydantic import BaseModel


class Typedoc(BaseModel):
    code:str
    description:str
