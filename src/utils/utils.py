from pydantic import BaseModel


class Record(BaseModel):
    prompt: str
    speech: str
    time: str