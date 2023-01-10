import sys
sys.path.insert(0, "/code/")
import requests
import json

from fastapi import status
import pytest


valid_images_list = ['images/single_channel.jpg','images/chairs-2.png', 'images/coffee-1.jpg']
invalid_images_list = [pytest.param('images/dummy_not_image.py')]

@pytest.mark.parametrize("image", valid_images_list)
def test_upload_image(image, retrieve_token):
    files = {'file': open(image, 'rb'),
             'Content-Type': 'image/jpeg',
            'filename': image}
    hed = {'Authorization': 'Bearer ' + retrieve_token,
           'accept': 'application/json'}
    r = requests.post('http://localhost:8000/predict', headers=hed, files=files)
    results = json.loads(r.content)
    assert results['success']
    assert r.status_code == status.HTTP_200_OK


@pytest.mark.parametrize("image", invalid_images_list)
def test_upload_image_no_good(image, retrieve_token):
    files = {'file': open(image, 'rb'),
             'Content-Type': 'image/jpeg',
            'filename': image}
    hed = {'Authorization': 'Bearer ' + retrieve_token,
           'accept': 'application/json'}
    r = requests.post('http://localhost:8000/predict', headers=hed, files=files)
    assert r.status_code == status.HTTP_406_NOT_ACCEPTABLE


def test_retrieve_token(retrieve_token_response):
    r = requests.post('http://localhost:8000/token',
                      headers={'accept': 'application/json', 'Content-Type': 'application/x-www-form-urlencoded'},
                      data='grant_type=&username=client_user&password=tryClassifier&scope=&client_id=&client_secret=')
    print(type(r.content))
    assert json.loads(r.content) == retrieve_token_response
    assert r.status_code == status.HTTP_200_OK
