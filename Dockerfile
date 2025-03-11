FROM python:3.11-slim

WORKDIR /app
COPY . .

RUN apt-get update && apt-get install -y \
    fonts-freefont-ttf \
    ttf-mscorefonts-installer \
    fontconfig

COPY arial.ttf /usr/share/fonts/truetype/arial.ttf

RUN pip install poetry && apt update -y
RUN poetry config virtualenvs.create false && apt-get update

RUN poetry install


ENTRYPOINT ["poetry", "run", "dev"]