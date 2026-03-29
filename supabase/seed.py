"""
Seed script for Stablecoin Monitor database.
Reads crypto_reference.xlsx and populates Supabase tables.

Usage:
    pip install supabase python-dotenv pandas openpyxl
    python supabase/seed.py
"""

import os
import re
import pandas as pd
from dotenv import load_dotenv
from supabase import create_client

load_dotenv()

SUPABASE_URL = os.environ["SUPABASE_URL"]
SUPABASE_KEY = os.environ["SUPABASE_SERVICE_ROLE_KEY"]
EXCEL_PATH = os.path.join(os.path.dirname(__file__), "..", "csv", "crypto_reference.xlsx")

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# Chain columns in the Excel (column name -> chain slug)
CHAIN_COLUMNS = {
    "Ethereum": "ethereum",
    "Solana": "solana",
    "Tron": "tron",
    "Arbitrum": "arbitrum",
    "Base": "base",
    "Avalanche": "avalanche",
    "Polygon": "polygon",
    "Optimism": "optimism",
    "BNB Chain": "bnb-chain",
    "Stellar": "stellar",
    "XRP Ledger": "xrp-ledger",
    "Sui": "sui",
    "Aptos": "aptos",
    "Near": "near",
    "TON": "ton",
    "Algorand": "algorand",
}

# Known CoinGecko IDs for stablecoins
COINGECKO_IDS = {
    "USDT": "tether",
    "USDC": "usd-coin",
    "DAI/USDS": "dai",
    "PYUSD": "paypal-usd",
    "USDP": "paxos-standard",
    "FDUSD": "first-digital-usd",
    "GUSD": "gemini-dollar",
    "USDe": "ethena-usde",
    "RLUSD": "ripple-usd",
    "USD1": "world-liberty-financial-usd",
    "EURC": "euro-coin",
    "USDG": "global-dollar",
    "M": "m-by-m0",
    "USDtb": "usdtb",
}

# Known DeFiLlama IDs
DEFILLAMA_IDS = {
    "USDT": "tether",
    "USDC": "usd-coin",
    "DAI/USDS": "dai",
    "PYUSD": "paypal-usd",
    "FDUSD": "first-digital-usd",
    "USDe": "ethena-usde",
    "GUSD": "gemini-dollar",
    "USDP": "paxos-standard",
}


def parse_supply(val):
    """Parse supply strings like '$187B', '$4.1B', '$300M', '~300M+' into numeric."""
    if pd.isna(val) or val in ("Pre-launch", "TBD", "New (Jan 2026)", "New (Mar 2026)"):
        return None
    s = str(val).replace("$", "").replace(",", "").replace("+", "").replace("~", "").replace("≈", "").strip()
    s = re.sub(r"\s*\(.*\)", "", s)  # remove parenthetical notes
    multiplier = 1
    if s.upper().endswith("B"):
        multiplier = 1_000_000_000
        s = s[:-1]
    elif s.upper().endswith("M"):
        multiplier = 1_000_000
        s = s[:-1]
    elif s.upper().endswith("K"):
        multiplier = 1_000
        s = s[:-1]
    try:
        return float(s) * multiplier
    except ValueError:
        return None


def safe_str(val):
    """Return string or None for NaN."""
    if pd.isna(val):
        return None
    return str(val).strip()


def seed_chains():
    """Insert all blockchain records."""
    print("Seeding chains...")
    chains = [{"name": name, "slug": slug} for name, slug in CHAIN_COLUMNS.items()]
    result = supabase.table("chains").upsert(chains, on_conflict="slug").execute()
    print(f"  Inserted/updated {len(result.data)} chains")
    # Return mapping of slug -> id
    all_chains = supabase.table("chains").select("id, slug").execute()
    return {c["slug"]: c["id"] for c in all_chains.data}


def seed_issuers(df_companies):
    """Insert issuers from Companies sheet (filtered to stablecoin-related)."""
    print("Seeding issuers...")

    # Get unique issuers from the Stablecoins sheet
    df_stable = pd.read_excel(EXCEL_PATH, sheet_name="Stablecoins")
    issuer_names = set()
    for val in df_stable["Issuer"].dropna():
        issuer_names.add(str(val).strip())

    issuers = []
    for _, row in df_companies.iterrows():
        company = safe_str(row["Company"])
        if company is None:
            continue
        # Check if this company is an issuer of a stablecoin
        is_issuer = company in issuer_names
        # Also include companies in the Stablecoin category
        is_stablecoin_co = safe_str(row.get("Category")) == "Stablecoin"
        if is_issuer or is_stablecoin_co:
            issuers.append({
                "name": company,
                "website": safe_str(row.get("Website")),
                "description": safe_str(row.get("Notes")),
            })

    # Also add issuers that appear in Stablecoins sheet but not in Companies
    existing_names = {i["name"] for i in issuers}
    for name in issuer_names:
        if name not in existing_names:
            issuers.append({"name": name})

    if issuers:
        result = supabase.table("issuers").upsert(issuers, on_conflict="name").execute()
        print(f"  Inserted/updated {len(result.data)} issuers")

    # Return mapping of name -> id
    all_issuers = supabase.table("issuers").select("id, name").execute()
    return {i["name"]: i["id"] for i in all_issuers.data}


def seed_stablecoins(df_stablecoins, issuer_map, chain_map):
    """Insert stablecoins and their chain mappings."""
    print("Seeding stablecoins...")

    stablecoins = []
    for _, row in df_stablecoins.iterrows():
        ticker = safe_str(row["Ticker"])
        if ticker is None or ticker == "TBD":
            continue

        issuer_name = safe_str(row["Issuer"])
        issuer_id = issuer_map.get(issuer_name)

        supply = parse_supply(row.get("Approx Circ. Supply"))
        third_party = safe_str(row.get("Third-Party Issuance"))

        stablecoins.append({
            "ticker": ticker,
            "name": safe_str(row["Stablecoin"]) or ticker,
            "issuer_id": issuer_id,
            "peg_currency": safe_str(row.get("Peg")) or "USD",
            "type": safe_str(row.get("Type")),
            "description": safe_str(row.get("Notes")),
            "market_cap_usd": supply,
            "circulating_supply": supply,  # approximate — will be updated by ingestion
            "reserve_assets": safe_str(row.get("Reserve Assets")),
            "reserve_manager": safe_str(row.get("Reserve Manager")),
            "custodians": safe_str(row.get("Custodian(s)")),
            "attestation_audit": safe_str(row.get("Attestation / Audit")),
            "regulator_charter": safe_str(row.get("Regulator / Charter")),
            "third_party_issuance": third_party == "Yes" if third_party else False,
            "sponsor": safe_str(row.get("Sponsor / Principal")),
            "coingecko_id": COINGECKO_IDS.get(ticker),
            "defillama_id": DEFILLAMA_IDS.get(ticker),
        })

    result = supabase.table("stablecoins").upsert(stablecoins, on_conflict="ticker").execute()
    print(f"  Inserted/updated {len(result.data)} stablecoins")

    # Get stablecoin id mapping
    all_coins = supabase.table("stablecoins").select("id, ticker").execute()
    coin_map = {c["ticker"]: c["id"] for c in all_coins.data}

    # Seed chain mappings
    print("Seeding stablecoin-chain mappings...")
    chain_links = []
    for _, row in df_stablecoins.iterrows():
        ticker = safe_str(row["Ticker"])
        if ticker is None or ticker == "TBD" or ticker not in coin_map:
            continue
        coin_id = coin_map[ticker]
        for chain_col, chain_slug in CHAIN_COLUMNS.items():
            if chain_col in row and row[chain_col] == 1:
                chain_links.append({
                    "stablecoin_id": coin_id,
                    "chain_id": chain_map[chain_slug],
                })

    if chain_links:
        result = supabase.table("stablecoin_chains").upsert(
            chain_links, on_conflict="stablecoin_id,chain_id"
        ).execute()
        print(f"  Inserted/updated {len(result.data)} chain mappings")


def main():
    print(f"Reading Excel from: {EXCEL_PATH}")
    df_stablecoins = pd.read_excel(EXCEL_PATH, sheet_name="Stablecoins")
    df_companies = pd.read_excel(EXCEL_PATH, sheet_name="Companies")

    print(f"Found {len(df_stablecoins)} stablecoins, {len(df_companies)} companies")
    print()

    chain_map = seed_chains()
    issuer_map = seed_issuers(df_companies)
    seed_stablecoins(df_stablecoins, issuer_map, chain_map)

    print()
    print("Done! Check your Supabase dashboard to verify the data.")


if __name__ == "__main__":
    main()
