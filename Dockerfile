# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Install system dependencies needed for PyAudio
RUN apt-get update && apt-get install -y \
    portaudio19-dev \
    libasound-dev \
    libffi-dev \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory in the container
WORKDIR /app

# Copy requirements first to cache dependencies
COPY requirements.txt .

# Install Python dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copy the current directory contents into the container at /app
COPY . .

# Run the application
CMD ["python", "main.py"]
