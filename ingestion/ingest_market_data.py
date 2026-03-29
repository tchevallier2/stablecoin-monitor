"""
Ingest stablecoin market data from CoinGecko (free, no API key).
Updates stablecoins table and inserts daily market_snapshots.

Usage:
    pip install -r requirements.txt
    python ingestion/ingest_market_data.py
"""

import os
import sys
import time
from datetime import date

import requests
from dotenv import load_dotenv
from supabase import create_client

load_dotenv()

SUPABASE_URL = os.environ["SUPABASE_URL"]
SUPABASE_KEY = os.environ["SUPABASE_SERVICE_ROLE_KEY"]
COINGECKO_BASE = "https://api.coingecko.com/api/v3"

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)


def get_coingecko_ids():
    """Fetch all stablecoins that have a coingecko_id set."""
    result = supabase.table("stablecoins").select("id, ticker, coingecko_id").not_.is_("coingecko_id", "null").execute()
    return result.data


def fetch_market_data(cg_ids: list[str]) -> dict:
    """Fetch price + market cap for a list of CoinGecko IDs in one call."""
    ids_str = ",".join(cg_ids)
    url = f"{COINGECKO_BASE}/simple/price"
    params = {
        "ids": ids_str,
        "vs_currencies": "usd",
        "include_market_cap": "true",
        "include_24hr_change": "true",
    }
    resp = requests.get(url, params=params, timeout=30)
    resp.raise_for_status()
    return resp.json()


def fetch_coin_detail(cg_id: str) -> dict:
    """Fetch detailed data for a single coin (for circulating supply)."""
    url = f"{COINGECKO_BASE}/coins/{cg_id}"
    params = {
        "localization": "false",
        "tickers": "false",
        "community_data": "false",
        "developer_data": "false",
        "sparkline": "false",
    }
    resp = requests.get(url, params=params, timeout=30)
    resp.raise_for_status()
    return resp.json()


def run():
    coins = get_coingecko_ids()
    if not coins:
        print("No stablecoins with coingecko_id found. Run seed.py first.")
        return

    cg_id_to_coin = {}
    for c in coins:
        cg_id_to_coin[c["coingecko_id"]] = c

    cg_ids = list(cg_id_to_coin.keys())
    print(f"Fetching market data for {len(cg_ids)} coins: {cg_ids}")

    # Batch price fetch
    market = fetch_market_data(cg_ids)

    # Compute total market cap for market share
    total_mcap = sum(
        market.get(cg_id, {}).get("usd_market_cap", 0) for cg_id in cg_ids
    )

    today = date.today().isoformat()
    updates = []
    snapshots = []

    for cg_id, coin in cg_id_to_coin.items():
        data = market.get(cg_id)
        if not data:
            print(f"  No data for {coin['ticker']} ({cg_id})")
            continue

        price = data.get("usd")
        mcap = data.get("usd_market_cap")

        # Fetch circulating supply from detail endpoint
        supply = None
        try:
            time.sleep(6)  # CoinGecko free tier: ~10 req/min
            detail = fetch_coin_detail(cg_id)
            supply = detail.get("market_data", {}).get("circulating_supply")
        except Exception as e:
            print(f"  Warning: could not fetch detail for {cg_id}: {e}")

        share_pct = (mcap / total_mcap * 100) if mcap and total_mcap else None

        print(f"  {coin['ticker']}: price=${price}, mcap=${mcap}, supply={supply}")

        # Update stablecoins table
        updates.append({
            "id": coin["id"],
            "price_usd": price,
            "market_cap_usd": mcap,
            "circulating_supply": supply,
        })

        # Insert daily snapshot
        snapshots.append({
            "stablecoin_id": coin["id"],
            "date": today,
            "price_usd": price,
            "market_cap_usd": mcap,
            "circulating_supply": supply,
            "market_share_pct": round(share_pct, 4) if share_pct else None,
        })

    # Batch upsert to stablecoins
    if updates:
        for u in updates:
            supabase.table("stablecoins").update({
                "price_usd": u["price_usd"],
                "market_cap_usd": u["market_cap_usd"],
                "circulating_supply": u["circulating_supply"],
            }).eq("id", u["id"]).execute()
        print(f"\nUpdated {len(updates)} stablecoins")

    # Upsert snapshots (unique on stablecoin_id + date)
    if snapshots:
        supabase.table("market_snapshots").upsert(
            snapshots, on_conflict="stablecoin_id,date"
        ).execute()
        print(f"Upserted {len(snapshots)} market snapshots for {today}")

    print("Done.")


if __name__ == "__main__":
    run()
