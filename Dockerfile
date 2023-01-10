FROM python:3.9-slim-buster as builder

# Installs required libraries for the installation
RUN apt-get update && \
    apt-get install -y sudo curl git build-essential gcc

# Download wheels for the installation of the dependencies
WORKDIR /usr/app
COPY requirements.txt .
RUN pip wheel --wheel-dir /usr/app/wheels -r requirements.txt


FROM python:3.9-slim-buster

RUN groupadd -r user && useradd -r -g user user
WORKDIR /code

# Good practices with python3 docker creation
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=on \
    PIP_DISABLE_PIP_VERSION_CHECK=on

# Install dependencies
COPY --from=builder /usr/app/wheels /wheels
COPY --from=builder /usr/app/requirements.txt .
RUN pip install --no-cache /wheels/*

# Copy files
COPY . .

# Expose port and change user to non-root user
EXPOSE 8000
USER user

CMD ["uvicorn", "app_classifier.main:app","--reload", "--host 0.0.0.0"]