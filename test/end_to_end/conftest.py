import pytest


@pytest.fixture
def retrieve_token():
    return "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6ImNsaWVudF91c2VyIiwiaGFzaGVkX3Bhc3N3b3JkIjoiJDJiJDEyJ" \
            "DEyMzQ1Njc4OTAxMjM0NTY3ODkwMXVSeFQvb2dYTkVVTGYxbnhSNC5IMTh1MTE4ZVllMld1In0.PqONjMIGhLn9LGTWVltA0K1GhihH5Wd" \
            "HvvvKbP0VIBU"


@pytest.fixture
def retrieve_token_response():
    return {"access_token":"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6ImNsaWVudF91c2VyIiwiaGFzaGVkX3Bhc3N"
                           "3b3JkIjoiJDJiJDEyJDEyMzQ1Njc4OTAxMjM0NTY3ODkwMXVSeFQvb2dYTkVVTGYxbnhSNC5IMTh1MTE4ZVllMld"
                           "1In0.PqONjMIGhLn9LGTWVltA0K1GhihH5WdHvvvKbP0VIBU","token_type":"bearer"}