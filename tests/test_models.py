from app.models import Payload

def test_payload_model():
    payload = Payload(payload_id="12345", output="FIRST STRING, OTHER STRING")
    assert payload.payload_id == "12345"
    assert payload.output == "FIRST STRING, OTHER STRING"
