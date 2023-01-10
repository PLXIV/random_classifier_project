from datetime import datetime
from typing import Optional
import sys

from app_classifier.pydantic_models import MyClassifierClient, MyClassifierDB

sys.path.insert(0, "/code/")

import pytest

from app_classifier.utils import read_image, generate_log_sample, generate_samples, decode_result


class MockFile:
    def __init__(self, filename):
        self.filename = filename


@pytest.mark.parametrize("image", ['images/single_channel.jpg', 'images/chairs-2.png', 'images/chairs.jpg',
                                   'images/abstract.jpg', 'images/coffee-1.jpg', 'images/coffee-2.jpg',
                                   'images/hd-wallpaper.jpg', 'images/living-room.jpg', 'images/white-wine.jpg',
                                   pytest.param('images/dummy_not_image.py', marks=pytest.mark.xfail)])
def test_read_image_successful(image: str) -> None:
    img = read_image(image)
    assert(len(img.split()) == 3)


@pytest.mark.parametrize("user, file, decoded_results",
                         [pytest.param({"username": "hello-world", "hashed_password": "fj982098jfipo"},
                                       MockFile("s.jpg"), {'class_id': "1", 'category_name': "s", 'score': "69"}),
                          pytest.param({"username": "hello-world", "hashed_password": "fj982098jfipo"},
                                       MockFile("s.jpg"), None),
                          pytest.param({"username": "hello-world", "hashed_password": "fj982098jfipo"},
                                       MockFile("s.jpg"), None),
                          pytest.param({"user": "hello-world", "hashed_password": "fj982098jfipo"}, MockFile("s"),
                                        None, marks=pytest.mark.xfail)
                          ])
def test_generate_successful_sample(user: dict, file: dict, decoded_results: Optional[dict]) -> None:
    results_client, results_db = generate_samples(user, file, decoded_results)
    assert(type(results_client) == MyClassifierClient)
    assert(type(results_db) == MyClassifierDB)


@pytest.mark.parametrize("sample_client", [{"username": "Hello", "filename": "file.jpg", "extension": ".jpg",
                                            "date": datetime.now(), "success": True}])
def test_generate_log_sample(sample_client: dict) -> None:
    sample_log = generate_log_sample(sample_client)
    results_db = MyClassifierDB(**sample_log)
    assert(type(results_db) == MyClassifierDB)


def test_decode_inference(classifier,) -> None:
    pass
