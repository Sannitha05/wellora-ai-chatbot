FROM python:3.10-slim

WORKDIR /app

# Install dependencies first (layer caching)
COPY backend/requirements.txt .

RUN python -m pip install --upgrade pip --no-cache-dir && \
    pip install --no-cache-dir -r requirements.txt

# Copy only the backend code (heavy folders excluded by .dockerignore)
COPY backend/ .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
