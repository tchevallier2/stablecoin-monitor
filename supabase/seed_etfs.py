"""
Seed script for Solana ETF tables.
Populates solana_etfs with the live US-listed Solana ETFs
and solana_etf_filings with known upcoming/pending filings.

Usage:
    python supabase/seed_etfs.py
"""

import os
from dotenv import load_dotenv
from supabase import create_client

load_dotenv()

SUPABASE_URL = os.environ["SUPABASE_URL"]
SUPABASE_KEY = os.environ["SUPABASE_SERVICE_ROLE_KEY"]

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# ── Live ETFs (data sourced from issuer sites / SEC filings, Aug 31 2026) ──

ETFS = [
    {
        "ticker": "BSOL",
        "issuer": "Bitwise",
        "exchange": "NYSE Arca",
        "aum_usd": 596_200_000,
        "price_usd": 11.07,
        "price_source": "static",
        "exp_ratio_current": "0.20%",
        "exp_ratio_target": "0.20%",
        "exp_waiver_note": None,
        "fee_waived": False,
        "staking_enabled": True,
        "commission_current": "6%",
        "commission_target": "6%",
        "commission_note": "6% commission on staking rewards",
        "pct_staked": "96%",
        "gross_yield": "~7.0%",
        "net_yield": "5.81%",
        "description": "Reinvests staking rewards (no distribution). Uses Helius / Bitwise Onchain Solutions validator. 6% commission on staking rewards. ~96% of SOL staked.",
    },
    {
        "ticker": "GSOL",
        "issuer": "Grayscale",
        "exchange": "NYSE Arca",
        "aum_usd": 195_320_000,
        "price_usd": 6.15,
        "price_source": "static",
        "exp_ratio_current": "0.19%",
        "exp_ratio_target": "0.19%",
        "exp_waiver_note": "Waiver expired Feb 5, 2026; sponsor fee subsequently reduced to 0.19%",
        "fee_waived": False,
        "staking_enabled": True,
        "commission_current": "7%",
        "commission_target": "7%",
        "commission_note": "Staking fee 7% (reduced from 23% at launch)",
        "pct_staked": "100%",
        "gross_yield": "7.01%",
        "net_yield": "5.63%",
        "description": "Formerly Grayscale Solana Trust; converted to ETF Jan 5, 2026. Sponsor fee reduced to 0.19% in 2026. Staking commission 7% (reduced from 23%).",
    },
    {
        "ticker": "FSOL",
        "issuer": "Fidelity",
        "exchange": "NYSE Arca",
        "aum_usd": 156_230_000,
        "price_usd": 9.76,
        "price_source": "static",
        "exp_ratio_current": "0.25%",
        "exp_ratio_target": "0.25%",
        "exp_waiver_note": "Waiver expired May 18, 2026",
        "fee_waived": False,
        "staking_enabled": True,
        "commission_current": "15%",
        "commission_target": "15%",
        "commission_note": "15% commission on staking rewards; was waived through May 18, 2026",
        "pct_staked": "N/A",
        "gross_yield": "~7.0%",
        "net_yield": "N/A",
        "description": "Launched Nov 18, 2025. Both management fee (0.25%) and staking commission (15%) were waived through May 18, 2026; both now in effect. % staked not publicly disclosed.",
    },
    {
        "ticker": "VSOL",
        "issuer": "VanEck",
        "exchange": "Cboe BZX",
        "aum_usd": 150_000_000,
        "price_usd": 10.91,
        "price_source": "static",
        "exp_ratio_current": "0.30%",
        "exp_ratio_target": "0.30%",
        "exp_waiver_note": "Waiver expired Feb 17, 2026",
        "fee_waived": False,
        "staking_enabled": True,
        "commission_current": "N/A",
        "commission_target": "N/A",
        "commission_note": "Not separately disclosed; reflected in NAV",
        "pct_staked": "88.04%",
        "gross_yield": "4.85%",
        "net_yield": "~4.55%",
        "description": "Uses SOL Strategies as staking provider. Gross staking yield 4.85% (as of Jul 31 2026); net ~4.55% after 0.30% sponsor fee. Commission not separately disclosed.",
    },
    {
        "ticker": "TSOL",
        "issuer": "21Shares",
        "exchange": "Cboe BZX",
        "aum_usd": 29_980_000,
        "price_usd": 8.00,
        "price_source": "static",
        "exp_ratio_current": "0% (waived)",
        "exp_ratio_target": "0.21%",
        "exp_waiver_note": "Sponsor fee waived through July 27, 2027 (started July 28, 2026)",
        "fee_waived": True,
        "staking_enabled": True,
        "commission_current": "N/A",
        "commission_target": "N/A",
        "commission_note": "Distributes staking rewards to shareholders monthly",
        "pct_staked": "99.77%",
        "gross_yield": "~7.0%",
        "net_yield": "~4.65%",
        "description": "Distributes staking rewards monthly. 99.77% utilization rate. CME CF Solana-Dollar Reference Rate. 0.21% sponsor fee waived for 1 year from July 28, 2026. Net staking yield ~4.65%.",
    },
    {
        "ticker": "SOLC",
        "issuer": "Canary Capital",
        "exchange": "NASDAQ",
        "aum_usd": 1_610_000,
        "price_usd": 16.27,
        "price_source": "static",
        "exp_ratio_current": "0.50%",
        "exp_ratio_target": "0.50%",
        "exp_waiver_note": None,
        "fee_waived": False,
        "staking_enabled": True,
        "commission_current": "N/A",
        "commission_target": "N/A",
        "commission_note": "Marinade Finance liquid staking; not separately disclosed",
        "pct_staked": "N/A",
        "gross_yield": "~7.0%",
        "net_yield": "N/A",
        "description": "Partners with Marinade Finance for liquid staking. Staking rewards accrued in daily NAV.",
    },
    {
        "ticker": "SSK",
        "issuer": "REX-Osprey",
        "exchange": "Cboe BZX",
        "aum_usd": 84_210_000,
        "price_usd": None,
        "price_source": "static",
        "exp_ratio_current": "0.75%",
        "exp_ratio_target": "0.75%",
        "exp_waiver_note": None,
        "fee_waived": False,
        "staking_enabled": True,
        "commission_current": "N/A",
        "commission_target": "N/A",
        "commission_note": "Distributes staking rewards monthly",
        "pct_staked": "N/A",
        "gross_yield": "N/A",
        "net_yield": "N/A",
        "description": "REX-Osprey SOL + Staking ETF. Launched Jul 2, 2025. Anchorage Digital custody. Distributes staking rewards monthly. AUM ~$84M as of Apr 2026.",
    },
    {
        "ticker": "SOEZ",
        "issuer": "Franklin Templeton",
        "exchange": "NYSE Arca",
        "aum_usd": None,
        "price_usd": None,
        "price_source": "static",
        "exp_ratio_current": "0.19%",
        "exp_ratio_target": "0.19%",
        "exp_waiver_note": "Fee waiver on first $5B AUM expired May 31, 2026",
        "fee_waived": False,
        "staking_enabled": True,
        "commission_current": "N/A",
        "commission_target": "N/A",
        "commission_note": "Staking rewards (via Coinbase Crypto) converted to cash and distributed monthly",
        "pct_staked": "N/A",
        "gross_yield": "N/A",
        "net_yield": "N/A",
        "description": "Launched Dec 3, 2025 on NYSE Arca. 0.19% expense ratio. Tracks CF Benchmarks Index. Staking rewards via Coinbase Crypto converted to cash and paid monthly to shareholders.",
    },
    {
        "ticker": "QSOL",
        "issuer": "Invesco Galaxy",
        "exchange": "Cboe BZX",
        "aum_usd": 4_300_000,
        "price_usd": None,
        "price_source": "static",
        "exp_ratio_current": "0.25%",
        "exp_ratio_target": "0.25%",
        "exp_waiver_note": None,
        "fee_waived": False,
        "staking_enabled": True,
        "commission_current": "N/A",
        "commission_target": "N/A",
        "commission_note": "Staking via Galaxy Digital Infrastructure; not separately disclosed",
        "pct_staked": "N/A",
        "gross_yield": "N/A",
        "net_yield": "N/A",
        "description": "Launched Dec 15, 2025 on Cboe BZX. Tracks Lukka Prime Solana Reference Rate. Staking via Galaxy Digital Infrastructure. AUM ~$4.3M as of Apr 2026.",
    },
]

# ── Upcoming / pending filings ───────────────────────────────────────

FILINGS = [
    {
        "issuer": "Franklin Templeton",
        "etf_name": "Franklin Solana ETF",
        "ticker_proposed": "SOEZ",
        "filing_type": "S-1",
        "status": "approved",
        "filing_date": "2025-03-12",
        "decision_deadline": None,
        "staking_included": True,
        "is_new": False,
        "last_verified": "2026-08-31",
        "notes": "Approved and live on NYSE Arca as SOEZ since Dec 3, 2025. 0.19% expense ratio. Fee waiver on first $5B AUM expired May 31, 2026.",
    },
    {
        "issuer": "WisdomTree",
        "etf_name": "WisdomTree Solana Fund",
        "ticker_proposed": None,
        "filing_type": "S-1",
        "status": "filed",
        "filing_date": "2025-03-13",
        "decision_deadline": None,
        "staking_included": None,
        "is_new": False,
        "last_verified": "2026-08-31",
        "notes": "S-1 filed Mar 2025. No approval announcement found as of Aug 2026.",
    },
    {
        "issuer": "ProShares",
        "etf_name": "ProShares Solana ETF",
        "ticker_proposed": None,
        "filing_type": "S-1",
        "status": "filed",
        "filing_date": "2025-06-17",
        "decision_deadline": None,
        "staking_included": None,
        "is_new": False,
        "last_verified": "2026-08-31",
        "notes": "S-1 filed Jun 2025. No spot ETF approval as of Aug 2026. ProShares also has live leveraged futures ETF (SLON) and UltraShort Solana ETF.",
    },
    {
        "issuer": "REX-Osprey",
        "etf_name": "REX-Osprey Solana Staking ETF",
        "ticker_proposed": "SSK",
        "filing_type": "S-1",
        "status": "approved",
        "filing_date": "2025-03-05",
        "decision_deadline": None,
        "staking_included": True,
        "is_new": False,
        "last_verified": "2026-08-31",
        "notes": "Approved. Live on Cboe BZX as SSK since Jul 2, 2025. 0.75% expense ratio. Anchorage Digital custody. AUM ~$84M as of Apr 2026.",
    },
    {
        "issuer": "Morgan Stanley",
        "etf_name": "Morgan Stanley Solana Trust",
        "ticker_proposed": "MSOL",
        "filing_type": "S-1",
        "status": "filed",
        "filing_date": "2026-01-06",
        "decision_deadline": None,
        "staking_included": True,
        "is_new": True,
        "last_verified": "2026-08-31",
        "sec_url": "https://www.sec.gov/Archives/edgar/data/2103547/000110465926000988/tm2534148d1_s1.htm",
        "notes": "S-1 filed Jan 2026 via E*TRADE Capital Management. S-1/A filed May 20, 2026 added staking; proposed ticker MSOL on NYSE Arca. Pending SEC approval as of Aug 2026.",
    },
    {
        "issuer": "CoinShares",
        "etf_name": "CoinShares Solana ETF",
        "ticker_proposed": None,
        "filing_type": "S-1",
        "status": "filed",
        "filing_date": None,
        "decision_deadline": None,
        "staking_included": None,
        "is_new": True,
        "last_verified": "2026-08-31",
        "sec_url": "https://www.sec.gov/Archives/edgar/data/2073298/000199937125014084/solana-s1a_092625.htm",
        "notes": "S-1/A filed. Planned listing on Nasdaq. Coinbase & BitGo custody. No approval as of Aug 2026.",
    },
    {
        "issuer": "Invesco Galaxy",
        "etf_name": "Invesco Galaxy Solana ETF",
        "ticker_proposed": "QSOL",
        "filing_type": "S-1",
        "status": "approved",
        "filing_date": None,
        "decision_deadline": None,
        "staking_included": True,
        "is_new": True,
        "last_verified": "2026-08-31",
        "notes": "Approved. Live on Cboe BZX as QSOL since Dec 15, 2025. 0.25% expense ratio. Staking via Galaxy Digital Infrastructure. AUM ~$4.3M as of Apr 2026.",
    },
    {
        "issuer": "Osprey Funds",
        "etf_name": "Osprey Solana Trust",
        "ticker_proposed": "OSOL",
        "filing_type": "S-1",
        "status": "filed",
        "filing_date": None,
        "decision_deadline": None,
        "staking_included": None,
        "is_new": True,
        "last_verified": "2026-08-31",
        "notes": "S-1 filed for new ETF on Cboe BZX. Coinbase custody. Separate from REX-Osprey joint filing. Note: original Osprey Solana Trust OTC product (pre-2022) was liquidated Jul 15, 2026. New ETF filing still pending as of Aug 2026.",
    },
    {
        "issuer": "VanEck",
        "etf_name": "VanEck JitoSOL ETF",
        "ticker_proposed": None,
        "filing_type": "S-1",
        "status": "filed",
        "filing_date": None,
        "decision_deadline": None,
        "staking_included": True,
        "is_new": True,
        "last_verified": "2026-08-31",
        "notes": "LST-based Solana ETF using Jito liquid staking token. Nasdaq filed to list on Cboe BZX Feb 2026. SEC instituted proceedings to approve/disapprove Jun 23, 2026. Still pending as of Aug 2026.",
    },
]


def main():
    print("Seeding Solana ETFs...")
    result = supabase.table("solana_etfs").upsert(ETFS, on_conflict="ticker").execute()
    print(f"  Upserted {len(result.data)} ETFs")

    print("Seeding Solana ETF filings...")
    # Use issuer+filing_type as dedup key (upsert not available without unique constraint)
    # Insert only if not already present
    for filing in FILINGS:
        existing = (
            supabase.table("solana_etf_filings")
            .select("id")
            .eq("issuer", filing["issuer"])
            .eq("filing_type", filing["filing_type"])
            .execute()
        )
        if existing.data:
            supabase.table("solana_etf_filings").update(filing).eq("id", existing.data[0]["id"]).execute()
            print(f"  Updated: {filing['issuer']} ({filing['filing_type']})")
        else:
            supabase.table("solana_etf_filings").insert(filing).execute()
            print(f"  Inserted: {filing['issuer']} ({filing['filing_type']})")

    print("\nDone! Check your Supabase dashboard.")


if __name__ == "__main__":
    main()
