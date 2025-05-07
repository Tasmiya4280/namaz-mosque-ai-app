# Stage 1: Build
FROM python:3.11-slim AS builder

WORKDIR /app

# Install Poetry
RUN pip install poetry

# Copy dependency files first
COPY pyproject.toml poetry.lock ./

# Disable virtualenv creation and install dependencies system-wide
RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi --no-root

# Copy the rest of the source code
COPY . .

# Stage 2: Run
FROM python:3.11-slim

WORKDIR /app

# Copy installed packages and source from builder stage
COPY --from=builder /usr/local /usr/local
COPY --from=builder /app /app

# Set environment variables (if needed)
ENV PYTHONUNBUFFERED=1

# Expose the FastAPI port
EXPOSE 8000

# Final command
CMD ["gunicorn", "--worker-class", "uvicorn.workers.UvicornWorker", "--bind", "0.0.0.0:8000", "main:app"]
