FROM python:3.11

# Install system dependencies including PortAudio
RUN apt-get update && apt-get install -y \
    portaudio19-dev \
    libffi-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy code
COPY . .

# Upgrade pip and install Python dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Start the app
CMD ["python", "main.py"]
