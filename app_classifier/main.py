import os
from typing import Dict

from fastapi import FastAPI, BackgroundTasks, UploadFile, File, Depends, status, HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from app_classifier.db import request_users, store_log
from app_classifier.model import MyClassifier
from app_classifier.pydantic_models import MyClassifierClient
from app_classifier.utils import decode_result, read_image
from app_classifier.security import authenticate_user, get_current_user, encode_user
from app_classifier.utils import generate_samples


app = FastAPI(
    title="MyClassifierServer",
    description="Servers classifications of companies models",
    version=str(os.environ['VERSION']),
    terms_of_service=None,
    contact=None,
    license_info=None
)


MODEL_PATH = os.environ['MODEL_PATH']
classifier = MyClassifier(MODEL_PATH, mode='script')
allowed_users = request_users()


@app.get('/')
def main():
    return {'message': 'Da warudo'}


@app.post('/token')
async def generate_token(form_data: OAuth2PasswordRequestForm = Depends()) -> Dict:
    """
    Authentificates the user. It also creates a string token that will be used to perform the inferences.
    :param form_data: contains the information necessary to login. It only checks for the fields username and
    password. IMPORTANT: I am encoding the password along side, which should be changed in the future.
    :return: Dictionary which contains the token and the type of token that is been encoded.
    """
    user = await authenticate_user(form_data.username, form_data.password, allowed_users)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Invalid username of password')
    token = encode_user(user.dict())
    return {'access_token': token, 'token_type': 'bearer'}


@app.post("/predict")
async def predict(background_tasks: BackgroundTasks,
                  user: Dict = Depends(get_current_user),
                  file: UploadFile =
                  File(default=..., title="Best ResNet classifier",
                       description="Takes as input a http post request which sends an object"
                                   "from the data model NewSample. The response returns a dictionary"
                                   "with the corresponding result. In case of an error it returns"
                                   " different kinds of exceptions.  ")) -> MyClassifierClient:
    """

    :param background_tasks: BackgroundTasks object that will write to a database after returning the results
    :param user: contains basic information of the user, such as username and access information.
    :param file: contains informatino about the image updated, such the file itself or the content-type
    :return: MyClassifierClient dataclass
    """

    try:
        await file.read()
        img = read_image(file.file)
        inference = classifier(img)
        decoded_results = decode_result(inference, classifier.labels)
        results_client, results_db = generate_samples(user, file, decoded_results)
        background_tasks.add_task(store_log, results_db)
        return results_client
    except:
        results_client, results_db = generate_samples(user, file)
        background_tasks.add_task(store_log, results_db)
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE,
                            detail=f"something went wrong, please check the extension or the validity of the image."
                                   f"More details: {str(results_client)}")
