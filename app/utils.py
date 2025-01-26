"""
Utility functions for the application.
"""
import uuid

from .models import TransformedString


def transformer_function(string: str) -> str:
    """
    Simulates an external service transforming strings.
    """
    return string.upper()


def cache_transformed_strings(session, strings):
    """
    Cache transformed strings or retrieve them from the cache.

    This function checks whether a string has been transformed previously.
    If so, it returns the cached result. Otherwise, it transforms the string
    and stores the result in the database for future use.
    """
    results = []
    for string in strings:
        cached = session.query(TransformedString).filter_by(input_value=string).first()

        if cached:
            results.append(cached.output_value)
        else:
            transformed = transformer_function(string)
            new_entry = TransformedString(input_value=string, output_value=transformed)
            session.add(new_entry)
            session.commit()
            results.append(transformed)
    return results


def generate_payload_id() -> str:
    """
    Generates a unique payload identifier.
    """
    return str(uuid.uuid4())
