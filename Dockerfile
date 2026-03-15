FROM python:3.9.10-slim AS base

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

WORKDIR /app

RUN apt-get update && \
    apt-get install -y --no-install-recommends netcat gcc libc6-dev libpq-dev && \
    rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

COPY poetry.lock pyproject.toml ./
RUN pip install --no-cache-dir "poetry>=1.1,<1.2" "poetry-core<1.1" setuptools && \
    poetry config virtualenvs.in-project true

# --- Production stage ---
FROM base AS production

RUN poetry install --no-dev && \
    poetry run pip install --no-cache-dir "setuptools<67.5"

COPY . ./

EXPOSE 8000

CMD poetry run alembic upgrade head && \
    poetry run uvicorn --host=0.0.0.0 app.main:app

# --- Test stage ---
FROM base AS test

RUN poetry install && \
    poetry run pip install --no-cache-dir "setuptools<67.5"

COPY . ./

CMD poetry run alembic upgrade head && \
    poetry run pytest --tb=short -q
