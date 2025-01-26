"""
This module defines the database models using SQLModel,
including the TransformedString and Payload models.
"""
from typing import Optional

from sqlmodel import Field, SQLModel


class TransformedString(SQLModel, table=True):
    """
    A model representing a transformed string in the database.
    """

    id: Optional[int] = Field(default=None, primary_key=True)
    input_value: str = Field(unique=True)
    output_value: str


class Payload(SQLModel, table=True):
    """
    A model representing a payload containing transformed strings.
    """

    id: Optional[int] = Field(default=None, primary_key=True)
    payload_id: str = Field(unique=True)
    output: str
