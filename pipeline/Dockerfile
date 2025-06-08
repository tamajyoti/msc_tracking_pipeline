# pipeline/Dockerfile
FROM python:3.12-slim

WORKDIR /pipeline

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

RUN chmod +x wait-for-it.sh

CMD ["sh", "-c", "./wait-for-it.sh postgres:5432 -- ./wait-for-it.sh prefect-server:4200 -- python flow.py"]