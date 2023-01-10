import sys
import asyncio
sys.path.insert(0, "/code/")

import pytest
from passlib.hash import bcrypt

from app_classifier.security import verify_password, authenticate_user, get_current_user, encode_user


sec_data = [({"username": "client_user", "hashed_password": bcrypt.hash("tryClassifier", salt='1234567890123456789012')},
              "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6ImNsaWVudF91c2VyIiwiaGFzaGVkX3Bhc3N3b3JkIjoiJDJiJD"
              "EyJDEyMzQ1Njc4OTAxMjM0NTY3ODkwMXVSeFQvb2dYTkVVTGYxbnhSNC5IMTh1MTE4ZVllMld1In0.PqONjMIGhLn9LGTWVltA0K1Gh"
              "ihH5WdHvvvKbP0VIBU"),
             pytest.param({"username": "client_user",
                           "hashed_password": bcrypt.hash("tryClassifier", salt='1234567890123456789012')},
                           "234yJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6ImNsaWVudF91c2VyIiwiaGFzaGVkX3Bhc3N"
                           "3b3JkIjoiJDJiJDEyJDEyMzQ1Njc4OTAxMjM0NTY3ODkwMXVSeFQvb2dYTkVVTGYxbnhSNC5IMTh1MTE4ZVllMld1In"
                           "0.PqONjMIGhLn9LGTWVltA0K1GhihH5WdHvvvKbP0VIBU",
                           marks=pytest.mark.xfail)]


@pytest.mark.parametrize("user, token", sec_data)
def test_encode_user(user: dict, token: str) -> None:
    encoded_token = encode_user(user)
    assert encoded_token == token


@pytest.mark.parametrize("user, token", sec_data)
def test_decode_token(user, token) -> None:
    payload = asyncio.run(get_current_user(token))
    assert type(payload) == dict
    assert user == payload

@pytest.mark.parametrize("password, hashed_password",
                         [("tryClassifier", "$2b$12$123456789012345678901uRxT/ogXNEULf1nxR4.H18u118eYe2Wu"),
                          pytest.param("CryClassifier", "$2b$12$123456789012345678901uRxT/ogXNEULf1nxR4.H18u118eYe2Wu",
                                       marks=pytest.mark.xfail),
                          pytest.param("TryClassifier", "C2b$12$123456789012345678901uRxT/ogXNEULf1nxR4.H18u118eYe2Wu",
                                       marks=pytest.mark.xfail),
                          pytest.param("TryClassifier", None,
                                       marks=pytest.mark.xfail),
                          pytest.param(None, "$2b$12$123456789012345678901uRxT/ogXNEULf1nxR4.H18u118eYe2Wu",
                                       marks=pytest.mark.xfail)
                          ])
def verify_password(password, hashed_password) -> None:
    assert verify_password(password, hashed_password)
