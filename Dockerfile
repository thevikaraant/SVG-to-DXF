# syntax=docker/dockerfile:1
FROM python:3.10-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PORT=5000

WORKDIR /app

# Install Inkscape, pstoedit, Ghostscript
RUN apt-get update && apt-get install -y --no-install-recommends \
    inkscape \
    pstoedit \
    ghostscript \
    && rm -rf /var/lib/apt/lists/*

# Copy and install Python deps
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY app.py .

# Listen on port
EXPOSE 5000

# Serve with Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]
