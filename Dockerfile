FROM python:3.10-slim
ENV POETRY_VIRTUALENVS_CREATE=false
WORKDIR /code
RUN pip install --no-cache-dir poetry
COPY pyproject.toml poetry.lock ./
RUN poetry install --only main --no-interaction
COPY app ./app
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]