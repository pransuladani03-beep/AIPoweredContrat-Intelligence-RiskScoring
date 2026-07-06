# Use an official lightweight Python runtime
FROM python:3.10-slim

WORKDIR /app

# Install system dependencies needed for OCR
RUN apt-get update && apt-get install -y tesseract-ocr libtesseract-dev poppler-utils && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY ./src /app/src
COPY ./data /app/data

EXPOSE 8000

# Command to run your FastAPI application
CMD ["uvicorn", "src.week3_fastapi_app:app", "--host", "0.0.0.0", "--port", "8000"]
