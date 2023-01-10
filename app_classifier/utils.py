#import requests
import datetime
import os
from typing import Optional, Tuple, Dict, List

from PIL import Image
from torch import TensorType

from app_classifier.pydantic_models import MyClassifierClient, MyClassifierDB


def read_image(img: str) -> Image.Image:
    """
    Reads an image and converts it into a three-dimensional image.
    If it has an alpha channel, removes the channel.
    If it is a one dimensional image, converts it into a 3 dimensional image.

    :param img:
    :return: three dimensinoal PIL.image
    """
    img = Image.open(img)
    if len(img.split()) == 4:
        r, g, b, a = img.split()
        img = Image.merge("RGB", (r, g, b))
    if len(img.split()) == 1:
        img = Image.merge("RGB", (img, img, img))

    return img


def generate_log_sample(sample_client: Dict) -> Dict:
    """
    Generate log sample dictionary from the sample client. This dictionary will be used to create an object from the
    data class MyClassifierDB, which contains information we want to keep track from our model.
    :param sample_client: dictionary in which contains the information that will be sent to the user
    :return: returns dictionary that will fill the datamodel MyClassifierDB
    """
    S3_PATH = os.environ["S3_PATH"]
    s3_filename = sample_client['filename'].split('.')[0] + str(sample_client['date']) + sample_client['filename'].split('.')[-1]
    sample_log = sample_client.copy()
    sample_log.update(
        {"file_location": f"{S3_PATH}{sample_client['username']}/{s3_filename}", "model_version": str(os.environ['VERSION'])})
    return sample_log


def generate_samples(user: dict, file, decoded_results: Optional[dict] = None) -> Tuple[MyClassifierClient,
                                                                                        MyClassifierDB]:
    """
    Generate Pydantic objects to return to the user and to store logs of the sample
    :param user: dictionary with data related to the user
    :param file: object with data related to the
    :param decoded_results:
    :return: Pydantic models in which the first one will be sent to the user, and the second one will be uploaded to a DB
    """

    current_date = datetime.datetime.now()
    sample_client = {"username": user['username'],
                     "filename": file.filename,
                     "extension": file.filename.split('.')[-1],
                     "date": current_date,
                     "success": bool(decoded_results)
                     }
    if decoded_results:
        sample_client.update({"class_id": decoded_results["class_id"],
                              "category_name": decoded_results["category_name"],
                              "score": decoded_results["score"]})
    sample_log = generate_log_sample(sample_client)
    return MyClassifierClient(**sample_client), MyClassifierDB(**sample_log)


def decode_result(inference: TensorType, labels: List) -> Dict:
    """
    Parses the inference into a humanly readable dictionary.

    :param inference: prediction made by the classifier
    :param labels: list of label names from the classifier
    :return: dictionary which contains the result of the prediction, class_id, label name and confidence score
    """
    class_id = inference.argmax().item()
    score = inference[class_id].item()
    category_name = labels[class_id]
    return {'class_id': class_id, 'category_name': category_name, 'score': 100 * score}


# def upload_image(filepath: str, url: str, content_type: str):
#     """
#     Function created for debugging purposes. Uploads an image and retrieves and prints the response.
#
#     :param filepath: file in which will be uploaded
#     :param url: url in which the service is hosted
#     :param content_type: type of file
#     :return: information related to the execution
#     """
#     image_content_types = ['image/gif', 'image/jpeg', 'image/png', 'image/tiff', 'image/vnd.microsoft.icon',
#                            'image/x-icon', 'image/vnd.djvu', 'image/svg+xml']
#     assert (content_type in image_content_types)
#     files = {'file': open(filepath, 'rb'),
#              'Content-Type': content_type}
#     r = requests.post(url, files=files)
#     print(r.content)
# filename = '../images/chairs.jpg'
# upload_image(filename, 'http://127.0.0.1:8000/predict', 'image/jpeg')