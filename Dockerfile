FROM python:3.12-slim

WORKDIR /app

COPY pyproject.toml ./
COPY app ./app
COPY alembic ./alembic
COPY alembic.ini ./alembic.ini
COPY scripts ./scripts

RUN pip install --upgrade pip && pip install .

CMD ["python", "scripts/import_uci_dataset.py", "--skip-docker"]
