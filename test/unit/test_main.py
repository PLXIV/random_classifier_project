import json
from typing import Dict

import pytest
from fastapi import status
from fastapi.testclient import TestClient

from app_classifier.main import app


client = TestClient(app)
valid_images_list = ['images/single_channel.jpg', 'images/chairs-2.png', 'images/coffee-1.jpg']
valid_results_ = [{"username": "client_user", "filename": "single_channel.jpg", "extension": "jpg", "class_id": 579,
                  "category_name": "grand piano", "score": 46, "success": True},
                  {"username": "client_user", "filename": "chairs-2.png", "extension": "png", "class_id": 532,
                  "category_name": "dining table", "score": 74, "success": True},
                  {"username": "client_user", "filename": "coffee-1.jpg", "extension": "jpg", "class_id": 505,
                  "category_name": "coffeepot", "score": 23, "success": True}]


def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {'message': 'Da warudo'}


@pytest.mark.parametrize(
    "payload, status_code",
    [
        ({"username": "client_user", "password": "tryClassifier"}, status.HTTP_200_OK),
        ({"username": "wrong_user", "password": "wrong_password"}, status.HTTP_401_UNAUTHORIZED),
        ({"username": "client_user", "password": "wrong_password"}, status.HTTP_401_UNAUTHORIZED),
        ({"username": "wrong_user", "password": "tryClassifier"}, status.HTTP_401_UNAUTHORIZED),
        ({"username": "only_user"}, status.HTTP_422_UNPROCESSABLE_ENTITY),
        ({"password": "only_password"}, status.HTTP_422_UNPROCESSABLE_ENTITY),
        ({}, status.HTTP_422_UNPROCESSABLE_ENTITY)
    ]
)
def test_get_token(payload: Dict, status_code: status) -> None:
    response = client.post("/token", data=payload)
    print(response)
    print(response.content)
    assert status_code == response.status_code


@pytest.mark.parametrize("imagepath, valid_results", [(i, j) for i, j in zip(valid_images_list, valid_results_)])
def test_upload_image_successful(retrieve_token: str, imagepath: str, valid_results: Dict) -> None:
    bearer_token = f"Bearer {retrieve_token}"
    files = {'file': open(imagepath, 'rb'),
             'Content-Type': 'image/jpeg'}
    response = client.post("/predict", headers={"Authorization": bearer_token}, files=files)
    content = json.loads(response.content)

    del(content['date'])
    assert status.HTTP_200_OK == response.status_code
    assert content == valid_results


@pytest.mark.parametrize("imagepath", ['images/dummy_not_image.py'])
def test_upload_image_unsuccessful(retrieve_token: str, imagepath: str) -> None:
    files = {'file': open(imagepath, 'rb'),
             'Content-Type': 'image/jpeg'}
    bearer_token = f"Bearer {retrieve_token}"
    response = client.post("/predict", headers={"Authorization": bearer_token}, files=files)
    content = json.loads(response.content)
    assert response.status_code == status.HTTP_406_NOT_ACCEPTABLE
    assert "something went wrong" in content['detail']


@pytest.mark.parametrize("imagepath", ['images/single_channel.jpg'])
def test_predict_wrong_token(retrieve_token: str, imagepath: str) -> None:
    files = {'file': open(imagepath, 'rb'),
             'Content-Type': 'image/jpeg'}
    bearer_token = "Bearer hello"
    response = client.post("/predict", headers={"Authorization": bearer_token}, files=files)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_predict_non_image(retrieve_token: str) -> None:
    files = {'file': '',
             'Content-Type': 'image/jpeg'}
    bearer_token = f"Bearer {retrieve_token}"
    response = client.post("/predict", headers={"Authorization": bearer_token}, files=files)
    assert response.status_code == status.HTTP_406_NOT_ACCEPTABLE
