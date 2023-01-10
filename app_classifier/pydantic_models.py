from typing import List, Optional
import datetime

from pydantic import BaseModel, Field


class User(BaseModel):
    username: str = Field(description='Name of the users allowed to use the classifier')
    hashed_password: str = Field(description='Hashed password of the user')


class Sample(BaseModel):
    username: str = Field(description="User which uploaded the sample")
    filename: str = Field(description="filename of the requested inference")
    extension: str = Field(description="Extension of the file updated")
    date: datetime.datetime = Field(description="Date and time in which the sample has been requested")


class MyClassifierClient(Sample):
    class_id: Optional[int] = Field(description="ID of the label predicted by the model")
    category_name: Optional[str] = Field(description="Label of the prediction made by the model")
    score: Optional[int] = Field(description="Confidence score related to the label selected")
    success: bool = Field(description="Stores if the sample run through the inference successfully or not")


class MyClassifierDB(MyClassifierClient):
    file_location: str = Field(description="S3 in which the file is been stored.")
    model_version: str = Field(description="model version")
    inference_result: Optional[List] = Field(description="Model output")
