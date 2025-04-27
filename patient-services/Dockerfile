FROM python:latest

WORKDIR /patient-services

COPY . .

EXPOSE 3003

RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "3003"]