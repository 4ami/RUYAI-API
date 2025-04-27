FROM python:3.12

WORKDIR /model-services

COPY . .

EXPOSE 3002

RUN pip install --no-cache-dir -r requirements.txt

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "3002"]