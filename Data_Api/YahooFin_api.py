from fastapi import FastAPI, Query
import yfinance as yf

app = FastAPI()

@app.get('/stock-data')
async def get_stock_data(
    tickers: str = Query(..., description="Stock ticker symbol (e.g., AAPL)"),
    time_period: str = Query("1mo", description="Time period (e.g., 1mo, 1y)"),
    data_intervals: str = Query("1d", description="Data interval (e.g., 1d, 1wk, 1mo)")
):
    # Corrected interval validation
    valid_intervals = ["1d", "5d", "1wk", "1mo", "3mo"]

    if data_intervals not in valid_intervals:
        return {"error": f"Invalid data interval. Choose from {valid_intervals}."}

    try:
        ticker_data = yf.Ticker(tickers)
        data = ticker_data.history(period=time_period, interval=data_intervals)

        # Check if data is empty
        if data.empty:
            return {"error": "No stock data available for the selected parameters."}

        return data.to_dict()

    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(stock_Detail, host="127.0.0.1", port=8000, reload=True)



# run api uvicorn main:app --reload
