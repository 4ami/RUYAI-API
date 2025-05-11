FROM python:3.12-slim

WORKDIR /model-services

RUN apt-get update && apt-get install -y build-essential

COPY requirements.txt .

RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

RUN apt-get update && apt-get install -y libgl1-mesa-glx

COPY . .

EXPOSE 3002

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "3002"]