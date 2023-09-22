from pydantic import BaseModel, Field


class GetMainModel(BaseModel):
    result: str
