FROM python:3.12

WORKDIR /opt/mp-fsm

# Install Poetry
RUN set eux; \
    curl -sSL https://install.python-poetry.org | POETRY_HOME=/opt/poetry python; \
    cd /usr/local/bin; \
    ln -s /opt/poetry/bin/poetry; \
    poetry config virtualenvs.create false; \
    poetry self add poetry-plugin-sort

COPY ./pyproject.toml ./poetry.lock /opt/mp-fsm/

RUN poetry install --no-root

COPY . /opt/mp-fsm
ENV PYTHONPATH=/opt/mp-fsm