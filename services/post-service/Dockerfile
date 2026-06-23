FROM python:3.11

WORKDIR /app

RUN pip install uv

COPY pyproject.toml .
COPY uv.lock .

RUN uv sync

COPY . .

CMD ["uv", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]

# Test stage – runs integration tests with testcontainers
FROM python:3.11 AS test

WORKDIR /app

RUN pip install uv

COPY pyproject.toml .
COPY uv.lock .

# Install runtime + test dependencies (the `test` optional group)
RUN uv sync --extra test

COPY . .

# Override the command for tests (can be overridden in compose)
CMD ["uv", "run", "--extra", "test", "pytest", "tests/integration"]