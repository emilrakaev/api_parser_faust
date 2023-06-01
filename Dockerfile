FROM python:3.9.9

RUN apt update && apt install -y jq

WORKDIR /app

RUN curl -sSL https://install.python-poetry.org | python - && \
    ln -s $HOME/.local/bin/poetry /usr/local/bin/poetry

COPY ./poetry.lock /app/
COPY ./pyproject.toml /app/

RUN poetry config virtualenvs.create false
RUN poetry install --only main

COPY . /app/

EXPOSE 6066

ENTRYPOINT ["/app/docker-entrypoint.sh"]

CMD ["python", "-m", "laborer", "--loop", "uvloop", "--loglevel", "INFO", "worker"]
