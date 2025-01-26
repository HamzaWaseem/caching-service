"""
This module contains tests for the utility functions in the app.utils module.
"""
from unittest.mock import Mock

from app.utils import cache_transformed_strings, generate_payload_id


def test_generate_payload_id():
    """Test that generate_payload_id() returns a non-empty string."""
    payload_id = generate_payload_id()
    assert len(payload_id) > 0  # Check that it generates a non-empty string


def test_cache_transformed_strings():
    """Test that cache_transformed_strings() transforms and caches the strings as expected."""
    # Mock the session object
    session = Mock()

    # Use side_effect to alternate the return values for each call
    session.query().filter_by().first.side_effect = [
        Mock(output_value="FIRST STRING"),
        Mock(output_value="SECOND STRING"),
    ]

    strings = ["first string", "second string"]
    transformed_strings = cache_transformed_strings(session, strings)

    # Assert the transformed strings are as expected
    assert transformed_strings == ["FIRST STRING", "SECOND STRING"]
