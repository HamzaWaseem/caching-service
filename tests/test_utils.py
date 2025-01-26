from app.utils import generate_payload_id, cache_transformed_strings
from unittest.mock import Mock

def test_generate_payload_id():
    payload_id = generate_payload_id()
    assert len(payload_id) > 0  # Check that it generates a non-empty string

def test_cache_transformed_strings():
    # Mock the session object
    session = Mock()
    
    # Use side_effect to alternate the return values for each call to session.query().filter_by().first()
    session.query().filter_by().first.side_effect = [
        Mock(output_value="FIRST STRING"),
        Mock(output_value="SECOND STRING")
    ]
    
    strings = ["first string", "second string"]
    transformed_strings = cache_transformed_strings(session, strings)
    
    # Assert the transformed strings are as expected
    assert transformed_strings == ["FIRST STRING", "SECOND STRING"]
