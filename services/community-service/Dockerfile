FROM python:3.12-slim

WORKDIR /app

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

# Install dependencies first (better layer caching)
COPY pyproject.toml README.md uv.lock ./
RUN uv sync --no-dev

# Copy source
COPY . .

# Generate gRPC stubs from proto
RUN uv run python -m grpc_tools.protoc \
  -I app/grpc \
  --python_out=app/grpc \
  --grpc_python_out=app/grpc \
  app/grpc/community.proto

EXPOSE 8003 50051

CMD ["uv", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8003"]
