import yfinance as yf
import pandas as pd


def fetch_stock(symbol="RELIANCE.NS", period="1y"):
    print(f"📥 Downloading data for {symbol}...")

    df = yf.download(symbol, period=period)

    # Keep only close price
    df = df[["Close"]].dropna().reset_index()
    df.columns = ["date", "close"]

    # Save
    df.to_csv("data/sample_data.csv", index=False)

    print("✅ Data saved to data/sample_data.csv")
    print(f"📊 Rows: {len(df)}")


if __name__ == "__main__":
    fetch_stock()