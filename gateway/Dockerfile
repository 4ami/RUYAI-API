FROM python:latest

WORKDIR /gateway

COPY . .

EXPOSE 8000

RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

CMD ["uvicorn", "main:gateway", "--host", "0.0.0.0", "--port", "8000"]