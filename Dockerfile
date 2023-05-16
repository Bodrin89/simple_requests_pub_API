FROM python:3.10-slim
WORKDIR /code
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY main.py .
COPY . .

CMD flask run -h 127.0.0.1 -p 8000