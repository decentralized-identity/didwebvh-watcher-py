FROM python:3.13-slim

WORKDIR /fastapi

ENV VIRTUAL_ENV=/opt/venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

COPY README.md poetry.lock pyproject.toml ./

RUN pip install --upgrade pip
RUN pip install poetry
RUN poetry install --no-root

COPY app ./app
COPY config.py main.py ./

CMD [ "python", "main.py" ]
