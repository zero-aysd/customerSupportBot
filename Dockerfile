# Use official Python image as base
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose port for FastAPI backend
EXPOSE 8000

# Default command to run FastAPI backend with uvicorn
CMD ["uvicorn", "chatbot_api_backend:app", "--host", "0.0.0.0", "--port", "8000"]