"""
Ingest Solana ETF market data from Yahoo Finance.
Updates AUM and price for each ETF in the solana_etfs table.
Also fetches SOL spot price.

Runs twice daily: 12:00 UTC (8 AM ET) and 21:00 UTC (5 PM ET).

Usage:
    python ingestion/ingest_etf_data.py
"""

import os
import time

import requests
from dotenv import load_dotenv
from supabase import create_client

load_dotenv()

SUPABASE_URL = os.environ["SUPABASE_URL"]
SUPABASE_KEY = os.environ["SUPABASE_SERVICE_ROLE_KEY"]

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

YAHOO_SUMMARY_URL = "https://query2.finance.yahoo.com/v10/finance/quoteSummary/{ticker}?modules=defaultKeyStatistics,price"
YAHOO_CHART_URL = "https://query1.finance.yahoo.com/v8/finance/chart/{ticker}?interval=1d&range=1d"

HEADERS = {"Accept": "application/json", "User-Agent": "StablecoinMonitor/1.0"}


def fetch_yahoo(ticker: str) -> dict:
    """Fetch AUM + price from Yahoo Finance for an ETF ticker."""
    result = {"source": "static", "aum": None, "price": None}

    # Try quoteSummary first (has both AUM and price)
    try:
        resp = requests.get(
            YAHOO_SUMMARY_URL.format(ticker=ticker),
            headers=HEADERS,
            timeout=15,
        )
        if resp.ok:
            data = resp.json()
            r = data.get("quoteSummary", {}).get("result", [{}])[0]
            aum = r.get("defaultKeyStatistics", {}).get("totalAssets", {}).get("raw")
            price = r.get("price", {}).get("regularMarketPrice", {}).get("raw")
            if aum or price:
                result["aum"] = aum
                result["price"] = price
                result["source"] = "live"
                return result
    except Exception as e:
        print(f"    quoteSummary failed for {ticker}: {e}")

    # Fallback: chart endpoint for price only
    try:
        resp = requests.get(
            YAHOO_CHART_URL.format(ticker=ticker),
            headers=HEADERS,
            timeout=15,
        )
        if resp.ok:
            data = resp.json()
            meta = data.get("chart", {}).get("result", [{}])[0].get("meta", {})
            price = meta.get("regularMarketPrice")
            if price:
                result["price"] = price
                result["source"] = "price-only"
    except Exception as e:
        print(f"    chart failed for {ticker}: {e}")

    return result


def fetch_sol_price() -> float | None:
    """Fetch SOL spot price from Yahoo Finance."""
    try:
        resp = requests.get(
            YAHOO_CHART_URL.format(ticker="SOL-USD"),
            headers=HEADERS,
            timeout=15,
        )
        if resp.ok:
            data = resp.json()
            return data.get("chart", {}).get("result", [{}])[0].get("meta", {}).get("regularMarketPrice")
    except Exception as e:
        print(f"  SOL price fetch failed: {e}")
    return None


def run():
    # Get all ETFs from DB
    result = supabase.table("solana_etfs").select("id, ticker, aum_usd, price_usd").order("aum_usd", desc=True).execute()
    etfs = result.data

    if not etfs:
        print("No ETFs found in database. Run seed_etfs.py first.")
        return

    print(f"Fetching Yahoo Finance data for {len(etfs)} Solana ETFs...")

    sol_price = fetch_sol_price()
    if sol_price:
        print(f"  SOL price: ${sol_price:.2f}")

    for etf in etfs:
        time.sleep(1)  # Be polite to Yahoo
        data = fetch_yahoo(etf["ticker"])

        updates = {"price_source": data["source"]}
        if data["price"] is not None:
            updates["price_usd"] = data["price"]
        if data["aum"] is not None:
            updates["aum_usd"] = data["aum"]

        source_label = data["source"]
        aum_str = f"${data['aum']:,.0f}" if data["aum"] else "unchanged"
        price_str = f"${data['price']:.2f}" if data["price"] else "unchanged"

        print(f"  {etf['ticker']}: price={price_str}, aum={aum_str} ({source_label})")

        supabase.table("solana_etfs").update(updates).eq("id", etf["id"]).execute()

    print(f"\nUpdated {len(etfs)} ETFs.")
    print("Done.")


if __name__ == "__main__":
    run()
