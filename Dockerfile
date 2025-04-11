FROM python:3.11-slim

RUN apt-get update && apt-get install -y portaudio19-dev gcc

WORKDIR /app
COPY . /app

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

CMD ["python", "your_script.py"]
