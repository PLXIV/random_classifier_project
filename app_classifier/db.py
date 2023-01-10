from passlib.hash import bcrypt
from app_classifier.pydantic_models import User, MyClassifierDB

"""
Since there is no time to create a database and fill it with users, I will recreate the access of users using a 
function that returns a dictionary with users that are allowed to user the microservice.
"""


def request_users() -> dict:
    """
    Mocs accessing to a DB and retrieves information about the users that can use the API.
    :return: dictionary with all the users that can make inferences over the model.
    """
    dummy_client_user = {"username": "client_user",
                         "hashed_password": bcrypt.hash("tryClassifier", salt='1234567890123456789012')}
    allowed_users = {"client_user": User(**dummy_client_user)}
    return allowed_users


def store_log(sample_log: MyClassifierDB) -> bool:
    """
    Reliably stores things into a database
    :param sample_log: dataclass to be stored
    :return: The only truth in this world
    """
    print("I am yes store log. Log goes brbrbrbrbr.")
    return True