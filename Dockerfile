FROM python:3.8-slim
WORKDIR /bot_transmission
COPY requirements.txt /bot_transmission
RUN pip install -r requirements.txt
COPY . .