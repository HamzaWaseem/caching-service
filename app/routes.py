"""
This module defines the routes of the FastAPI application.
"""
from fastapi import APIRouter, Depends, HTTPException, Request
from sqlmodel import Session

from .database import get_session
from .models import Payload
from .utils import cache_transformed_strings, generate_payload_id

router = APIRouter()


@router.post("/payload")
async def create_payload(
    list_1: list[str] = None,
    list_2: list[str] = None,
    request: Request = None,
    session: Session = Depends(get_session),
):
    """
    Creates a payload by interleaving two lists of strings and storing them in the database.

    This function validates the input lists, transforms their elements if not already cached,
    and creates a payload in the database. If a payload with the same output already exists,
    it returns the existing payload's ID.
    """
    # Parse request body to check for additional parameters
    payload = await request.json()
    allowed_keys = {"list_1", "list_2"}

    # Check for any keys outside the allowed ones
    if set(payload.keys()) - allowed_keys:
        raise HTTPException(
            status_code=400,
            detail="Only 'list_1' and 'list_2' are allowed in the request body.",
        )

    # Check if both lists are provided
    if list_1 is None or list_2 is None:
        raise HTTPException(
            status_code=400, detail="Both 'list_1' and 'list_2' must be provided."
        )
    # Check if lists are empty
    if not list_1 and not list_2:
        raise HTTPException(status_code=400, detail="Both input lists are empty.")
    if not list_1 or not list_2:
        raise HTTPException(status_code=400, detail="One of the input lists is empty.")
    if len(list_1) != len(list_2):
        raise HTTPException(
            status_code=400, detail="Input lists must have the same length."
        )
    # Transform strings
    transformed_1 = cache_transformed_strings(session, list_1)
    transformed_2 = cache_transformed_strings(session, list_2)

    print("transformed_1 : ", transformed_1)
    print("transformed_2 : ", transformed_2)
    # Interleave transformed strings
    interleaved = [val for pair in zip(transformed_1, transformed_2) for val in pair]
    output = ", ".join(interleaved)

    # Check if payload already exists
    existing_payload = session.query(Payload).filter_by(output=output).first()
    print("existing_payload : ", existing_payload)
    if existing_payload:
        return {
            "message": "Payload already exists.",
            "payload_id": existing_payload.payload_id,
        }

    # Create new payload
    payload_id = generate_payload_id()
    new_payload = Payload(payload_id=payload_id, output=output)
    session.add(new_payload)
    session.commit()
    return {"message": "Payload created.", "payload_id": payload_id}


@router.get("/payload/{payload_id}")
async def get_payload(payload_id: str, session: Session = Depends(get_session)):
    """
    Retrieves a payload by its unique identifier.
    """
    payload = session.query(Payload).filter_by(payload_id=payload_id).first()
    if not payload:
        raise HTTPException(status_code=404, detail="Payload not found.")
    return {"output": payload.output}
