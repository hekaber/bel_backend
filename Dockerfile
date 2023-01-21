# For more information, please refer to https://aka.ms/vscode-docker-python
FROM python:3.8-slim

EXPOSE 8000

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt
COPY ./alembic.ini /code/alembic.ini

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./alembic /code/alembic
COPY ./app /code/app
COPY ./config/.env.docker /code/config/.env

# Creates a non-root user with an explicit UID and adds permission to access the /app folder
RUN pip install debugpy -t /tmp \
    && adduser -u 5678 --disabled-password --gecos "" bebel \
    && chown -R bebel /code
USER bebel

# During debugging, this entry point will be overridden.
CMD ["uvicorn", "app.main:app", "--proxy-headers", "--reload", "--host", "0.0.0.0", "--port", "8000"]
