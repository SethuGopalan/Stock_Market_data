FROM python:3.9-slim

WORKDIR /app

COPY . /app

RUN pip install fastapi yfinance 

EXPOSE 5000

CMD [ "uvicorn", "YahooFin_Api:app", "--host", "0.0.0.0", "--port", "5000" ]