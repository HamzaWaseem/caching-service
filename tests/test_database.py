import pytest
from sqlalchemy.orm import Session
from app.database import get_session, Base, engine
from app.models import Payload

# Set up and tear down the database for testing
@pytest.fixture
def db_session():
    # Create tables
    Base.metadata.create_all(bind=engine)
    session = Session(bind=engine)

    # Clean up existing records to prevent UNIQUE constraint violations
    session.query(Payload).delete()
    session.commit()
    
    yield session

    # Rollback any changes to avoid persistence across tests
    session.rollback()
    
    # Drop all tables after the test
    Base.metadata.drop_all(bind=engine)
    session.close()

def test_add_payload(db_session):
    # Create a new payload instance
    payload = Payload(payload_id="12345", output="FIRST STRING, OTHER STRING")
    
    # Add and commit the payload to the session
    db_session.add(payload)
    db_session.commit()

    # Query the database to fetch the payload
    result = db_session.query(Payload).filter_by(payload_id="12345").first()
    
    # Assertions to verify the result
    assert result is not None
    assert result.output == "FIRST STRING, OTHER STRING"
