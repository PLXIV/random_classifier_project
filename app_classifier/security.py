import os
from typing import Union, Dict

import jwt
from passlib.hash import bcrypt
from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer

from app_classifier.pydantic_models import User


oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')


def verify_password(password: str, hashed_password: str) -> bool:
    """
    Checks if the hashed password with the password introduced by the client match.
    :param password: password typed by the user
    :param hashed_password: hashed password using the function bcrypt.hash
    :return: bool value that determines the validity of the password
    """
    return bcrypt.verify(password, hashed_password)


async def authenticate_user(username: str, password: str, allowed_users: Dict) -> Union[User, bool]:
    """
    Authenticates the user given a username and a password. The password passes through a decoding hash H256 algorithm.

    :param username: username of the client.
    :param password: unhashed password of the user.
    :param allowed_users: users that can have access to the locked services.
    :return: pydantic model which contains basic information about the user.
    """

    if username not in allowed_users.keys():
        return False
    user = allowed_users[username]
    if not verify_password(password, user.hashed_password):
        return False
    return user


async def get_current_user(token: str = Depends(oauth2_scheme)) -> User:
    """
    Determines if the token matches with any of the users that are allowed to use the endpoint.

    :param token: str in which contains the token that should contain the users information.
    :return: User instance with the users information.
    """
    try:
        payload = jwt.decode(token, os.environ['JWT_SECRET'], algorithms=[os.environ['BASE_ENCODING_ALGORITHM']])
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Invalid token')
    return payload


def encode_user(user: Dict) -> str:
    """
    Encodes user into a token, returns all the data, even the hashed_password. Which is a vulnerability which should be
    fixed as soon as possible. It uses the constants JWT_SECRET as key and encodes using the constant
    BASE_ENCODING_ALGORITHM, both are defined previously within the docker image
    :param user: dictionary of the user in which will be encoded into a token
    :return: str which is the token of the desired user
    """
    return jwt.encode(user, key=os.environ['JWT_SECRET'], algorithm=os.environ['BASE_ENCODING_ALGORITHM'])
