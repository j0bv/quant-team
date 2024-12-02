FROM python:3.9-slim

WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY src/ ./src/

# Create directory for shared volume
RUN mkdir -p /app/shared

# Set Python path
ENV PYTHONPATH=/app

CMD ["python", "src/main.py"]
