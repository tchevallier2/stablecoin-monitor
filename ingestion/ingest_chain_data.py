"""
Ingest stablecoin chain-level supply data from DeFiLlama (free, no API key).
Updates stablecoin_chains.supply_on_chain.

Usage:
    pip install -r requirements.txt
    python ingestion/ingest_chain_data.py
"""

import os
import time

import requests
from dotenv import load_dotenv
from supabase import create_client

load_dotenv()

SUPABASE_URL = os.environ["SUPABASE_URL"]
SUPABASE_KEY = os.environ["SUPABASE_SERVICE_ROLE_KEY"]
DEFILLAMA_BASE = "https://stablecoins.llama.fi"

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# Map DeFiLlama chain names to our chain slugs
LLAMA_CHAIN_MAP = {
    "Ethereum": "ethereum",
    "Solana": "solana",
    "Tron": "tron",
    "Arbitrum": "arbitrum",
    "Base": "base",
    "Avalanche": "avalanche",
    "Polygon": "polygon",
    "Optimism": "optimism",
    "BSC": "bnb-chain",
    "Stellar": "stellar",
    "Ripple": "xrp-ledger",
    "Sui": "sui",
    "Aptos": "aptos",
    "Near": "near",
    "TON": "ton",
    "Algorand": "algorand",
}


def get_defillama_coins():
    """Fetch stablecoins that have a defillama_id set."""
    result = supabase.table("stablecoins").select("id, ticker, defillama_id").not_.is_("defillama_id", "null").execute()
    return result.data


def get_chain_map():
    """Get slug -> chain_id mapping."""
    result = supabase.table("chains").select("id, slug").execute()
    return {c["slug"]: c["id"] for c in result.data}


def fetch_stablecoin_chains(defillama_id: str) -> dict:
    """Fetch chain breakdown from DeFiLlama stablecoins API."""
    # DeFiLlama uses numeric IDs; we need to find the right one
    # First, get the full list to map name -> id
    resp = requests.get(f"{DEFILLAMA_BASE}/stablecoins?includePrices=false", timeout=30)
    resp.raise_for_status()
    data = resp.json()

    # Find the stablecoin by matching gecko_id or name
    for coin in data.get("peggedAssets", []):
        if coin.get("gecko_id") == defillama_id or coin.get("symbol", "").upper() == defillama_id.upper():
            llama_id = coin["id"]
            # Now fetch chain breakdown
            detail_resp = requests.get(f"{DEFILLAMA_BASE}/stablecoin/{llama_id}", timeout=30)
            detail_resp.raise_for_status()
            return detail_resp.json()

    return {}


def run():
    coins = get_defillama_coins()
    if not coins:
        print("No stablecoins with defillama_id found. Run seed.py first.")
        return

    chain_map = get_chain_map()
    print(f"Processing {len(coins)} coins with DeFiLlama IDs")

    # Fetch the full stablecoin list once
    print("Fetching DeFiLlama stablecoin list...")
    resp = requests.get(f"{DEFILLAMA_BASE}/stablecoins?includePrices=false", timeout=30)
    resp.raise_for_status()
    llama_data = resp.json()
    llama_assets = llama_data.get("peggedAssets", [])

    # Build a lookup: gecko_id -> llama_id
    gecko_to_llama = {}
    for asset in llama_assets:
        gid = asset.get("gecko_id")
        if gid:
            gecko_to_llama[gid] = asset["id"]

    updates = []

    for coin in coins:
        llama_id = gecko_to_llama.get(coin["defillama_id"])
        if not llama_id:
            print(f"  {coin['ticker']}: no DeFiLlama match for '{coin['defillama_id']}'")
            continue

        print(f"  Fetching chain data for {coin['ticker']} (llama_id={llama_id})...")
        time.sleep(0.5)  # Be polite

        try:
            detail_resp = requests.get(f"{DEFILLAMA_BASE}/stablecoin/{llama_id}", timeout=30)
            detail_resp.raise_for_status()
            detail = detail_resp.json()
        except Exception as e:
            print(f"    Error fetching {coin['ticker']}: {e}")
            continue

        # Extract current chain supplies from chainBalances
        chain_balances = detail.get("chainBalances", {})
        for llama_chain_name, chain_data in chain_balances.items():
            slug = LLAMA_CHAIN_MAP.get(llama_chain_name)
            if not slug or slug not in chain_map:
                continue

            # Get the most recent token entry
            tokens = chain_data.get("tokens", [])
            if not tokens:
                continue

            latest = tokens[-1]
            supply = latest.get("circulating", {}).get("peggedUSD")
            if supply is None:
                continue

            updates.append({
                "stablecoin_id": coin["id"],
                "chain_id": chain_map[slug],
                "supply_on_chain": supply,
            })

    # Upsert chain supply data
    if updates:
        supabase.table("stablecoin_chains").upsert(
            updates, on_conflict="stablecoin_id,chain_id"
        ).execute()
        print(f"\nUpserted {len(updates)} chain supply records")
    else:
        print("\nNo chain supply data to update")

    print("Done.")


if __name__ == "__main__":
    run()
