FROM python:3.11-slim

WORKDIR /app
COPY . .

RUN pip install poetry && apt update -y
RUN poetry config virtualenvs.create false && apt-get update

RUN poetry install


ENTRYPOINT ["poetry", "run", "dev"]