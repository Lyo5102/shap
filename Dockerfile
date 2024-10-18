ARG PYTHON_VERSION=3.8.10
FROM python:${PYTHON_VERSION}-slim as base

RUN pip install poetry==1.4.2

ENV POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=1 \
    POETRY_VIRTUALENVS_CREATE=1 \
    POETRY_CACHE_DIR=/tmp/poetry_cache

WORKDIR /app

COPY pyproject.toml poetry.lock ./
RUN touch README.md

RUN poetry install --without dev --no-root && rm -rf $POETRY_CACHE_DIR

COPY fake_face_test_web ./fake_face_test_web
COPY images ./images
COPY questions ./questions
COPY results ./results
COPY sessions.json ./sessions.json
COPY logininfo.csv ./logininfo.csv

RUN poetry install --without dev

EXPOSE 8080

ENTRYPOINT ["poetry", "run", "python", "fake_face_test_web/main.py"]
