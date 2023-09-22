from pydantic import BaseModel, Field, Json


class CreateIndexModel(BaseModel):
    indexname: str = Field(description="인덱스 이름")


class CreateIndexDataModel(BaseModel):
    data: dict = Json
