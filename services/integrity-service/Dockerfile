from python:3.12-slim

WORKDIR /app

COPY pyproject.toml uv.lock ./

RUN apt-get update && apt-get install -y --no-install-recommends git \
  && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir uv \
  && uv sync --no-cache

COPY app/ ./app/

ENV PYTHONUNBUFFERED=1
CMD ["uv", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
