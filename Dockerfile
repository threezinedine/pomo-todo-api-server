FROM python:3.9-alpine

WORKDIR /app

COPY requirements.txt .

RUN pip install -U pip && \
    pip install -r requirements.txt 

COPY . .

EXPOSE 8000

CMD ["python3", "server.py", "run"]