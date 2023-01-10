FROM python:3.9-slim-buster

RUN groupadd -r user && useradd -r -g user user
WORKDIR /code
EXPOSE 8000

COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY . .
USER user

CMD ["uvicorn", "app_classifier.main:app","--reload", "--host 0.0.0.0"]