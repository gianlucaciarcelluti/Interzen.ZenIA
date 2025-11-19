# SP04 - Classifier Service
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the FastAPI app
COPY app.py .

# Set Python path
ENV PYTHONPATH=/app

# Expose port
EXPOSE 5004

# Run the FastAPI app
CMD ["python", "app.py"]