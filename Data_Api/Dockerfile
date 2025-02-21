FROM python:3.9-slim

WORKDIR /app

COPY . /app

RUN pip install fastapi yfinance 

EXPOSE 5000

CMD [ "python", "YahooFin_api.py" ]