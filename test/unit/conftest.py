import os
import sys
sys.path.insert(0, "/code/")

import pytest

from app_classifier.model import MyClassifier
from app_classifier.utils import read_image


@pytest.fixture
def classifier():
    model_path = os.environ["MODEL_PATH"]
    return MyClassifier(model_path, mode='script')

@pytest.fixture
def load_sample():

    def _load_sample(image):
        return read_image(image)

    return _load_sample

@pytest.fixture
def retrieve_token():
    return "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6ImNsaWVudF91c2VyIiwiaGFzaGVkX3Bhc3N3b3JkIjoiJDJiJDEyJ" \
            "DEyMzQ1Njc4OTAxMjM0NTY3ODkwMXVSeFQvb2dYTkVVTGYxbnhSNC5IMTh1MTE4ZVllMld1In0.PqONjMIGhLn9LGTWVltA0K1GhihH5Wd" \
            "HvvvKbP0VIBU"