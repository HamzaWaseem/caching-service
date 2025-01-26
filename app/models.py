from sqlmodel import SQLModel, Field
from typing import Optional


class TransformedString(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    input_value: str = Field(unique=True)
    output_value: str


class Payload(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    payload_id: str = Field(unique=True)
    output: str
