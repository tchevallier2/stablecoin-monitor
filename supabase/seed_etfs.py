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

# ── Live ETFs (data sourced from issuer sites / SEC filings, Aug 17 2026) ──────────

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
        "pct_staked": "99%",
        "gross_yield": "6.76%",
        "net_yield": "6.36%",
        "description": "Reinvests staking rewards (no distribution). Uses Helius / Bitwise Onchain Solutions validator. 6% commission on staking rewards.",
    },
    {
        "ticker": "GSOL",
        "issuer": "Grayscale",
        "exchange": "NYSE Arca",
        "aum_usd": 195_320_000,
        "price_usd": 6.15,
        "price_source": "static",
        # Sponsor fee cut from 0.35% to 0.19% via SEC 8-K/424B3 effective Jun 25, 2026
        "exp_ratio_current": "0.19%",
        "exp_ratio_target": "0.19%",
        "exp_waiver_note": "Waiver expired Feb 5, 2026",
        "fee_waived": False,
        "staking_enabled": True,
        # Staking commission cut from 23% (post-waiver rate) to 7% effective Jun 25, 2026
        "commission_current": "7%",
        "commission_target": "7%",
        "commission_note": "Reduced to 7% on Jun 25, 2026 (was 23% after Feb 2026 waiver expiry; sponsor fee also cut from 0.35% to 0.19%)",
        "pct_staked": "100%",
        "gross_yield": "7.01%",
        # ~7.01% * 0.93 (7% commission) - 0.19% expense = ~6.33%
        "net_yield": "~6.3%",
        "description": "Formerly Grayscale Solana Trust; converted to ETF Jan 5, 2026. Fee cuts effective Jun 25, 2026: sponsor fee 0.19%, staking commission 7% (down from 23%). Pays quarterly cash distributions from staking rewards (effective Aug 7, 2026).",
    },
    {
        "ticker": "FSOL",
        "issuer": "Fidelity",
        "exchange": "NYSE Arca",
        "aum_usd": 156_230_000,
        "price_usd": 9.76,
        "price_source": "static",
        # Fee waiver expired May 18, 2026 — now at full 0.25% expense ratio
        "exp_ratio_current": "0.25%",
        "exp_ratio_target": "0.25%",
        "exp_waiver_note": "Waiver expired May 18, 2026",
        "fee_waived": False,
        "staking_enabled": True,
        # Staking commission waiver also expired May 18, 2026 — now at full 15%
        "commission_current": "15%",
        "commission_target": "15%",
        "commission_note": "15% commission on staking rewards; both fee and commission waiver expired May 18, 2026",
        "pct_staked": "N/A",
        "gross_yield": "~7.0%",
        # ~7.0% * 0.85 (15% commission) - 0.25% expense = ~5.7%
        "net_yield": "~5.7%",
        "description": "Launched Nov 18, 2025. Both management fee and staking commission waiver expired May 18, 2026. Now: 0.25% expense ratio, 15% staking commission. % staked not publicly disclosed. Coinbase staking provider.",
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
        "gross_yield": "6.03%",
        "net_yield": "5.78%",
        "description": "Uses SOL Strategies as staking provider. 88.04% of SOL staked. Net staking yield 5.78%. Commission not separately disclosed.",
    },
    {
        "ticker": "TSOL",
        "issuer": "21Shares",
        "exchange": "Cboe BZX",
        "aum_usd": 29_980_000,
        "price_usd": 8.00,
        "price_source": "static",
        # 21Shares introduced 1-year sponsor fee waiver effective Jul 28, 2026 (through Jul 2027)
        "exp_ratio_current": "0% (waived)",
        "exp_ratio_target": "0.21%",
        "exp_waiver_note": "Sponsor fee waived through July 2027",
        "fee_waived": True,
        "staking_enabled": True,
        "commission_current": "N/A",
        "commission_target": "N/A",
        "commission_note": "Distributes staking rewards to shareholders monthly",
        "pct_staked": "99.77%",
        "gross_yield": "~7.0%",
        "net_yield": "~6.7%",
        "description": "Distributes staking rewards monthly ($0.016962/share in Mar 2026). 99.77% utilization rate. CME CF Solana-Dollar Reference Rate. 0.21% sponsor fee waived through July 2027.",
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
        # Marinade Finance stakes 100% of SOL assets per prospectus
        "pct_staked": "100%",
        "gross_yield": "~7.0%",
        "net_yield": "N/A",
        "description": "Partners with Marinade Finance for liquid staking. 100% of SOL staked. Staking rewards accrue to NAV (not distributed).",
    },
    {
        "ticker": "SSK",
        "issuer": "REX-Osprey",
        "exchange": "Cboe BZX",
        "aum_usd": None,
        "price_usd": None,
        "price_source": "static",
        "exp_ratio_current": "0.75%",
        "exp_ratio_target": "0.75%",
        "exp_waiver_note": None,
        "fee_waived": False,
        "staking_enabled": True,
        "commission_current": "N/A",
        "commission_target": "N/A",
        "commission_note": None,
        "pct_staked": "N/A",
        "gross_yield": "N/A",
        "net_yield": "N/A",
        "description": "REX-Osprey SOL Staking ETF. Anchorage Digital custody. Approved and live.",
    },
    # ── New ETFs added Aug 17 2026 ──
    {
        "ticker": "SOEZ",
        "issuer": "Franklin Templeton",
        "exchange": "NYSE Arca",
        "aum_usd": None,
        "price_usd": None,
        "price_source": "static",
        "exp_ratio_current": "0.19%",
        "exp_ratio_target": "0.19%",
        "exp_waiver_note": "Fee waiver on first $5B expired May 31, 2026",
        "fee_waived": False,
        "staking_enabled": True,
        "commission_current": "N/A",
        "commission_target": "N/A",
        "commission_note": "Staking rewards distributed monthly as cash; Coinbase custody and staking provider",
        "pct_staked": "~100%",
        "gross_yield": "N/A",
        "net_yield": "N/A",
        "description": "Launched Dec 3, 2025 on NYSE Arca. Coinbase custody and staking. 0.19% expense ratio. Staking rewards distributed monthly as cash. Tracks CF Benchmarks Solana Index.",
    },
    {
        "ticker": "QSOL",
        "issuer": "Invesco Galaxy",
        "exchange": "Cboe BZX",
        "aum_usd": None,
        "price_usd": None,
        "price_source": "static",
        "exp_ratio_current": "0.25%",
        "exp_ratio_target": "0.25%",
        "exp_waiver_note": None,
        "fee_waived": False,
        "staking_enabled": True,
        "commission_current": "N/A",
        "commission_target": "N/A",
        "commission_note": "Staking via Galaxy Digital infrastructure; Coinbase Custody",
        "pct_staked": "~100%",
        "gross_yield": "N/A",
        "net_yield": "N/A",
        "description": "Launched Dec 15, 2025 on Cboe BZX. Galaxy Digital staking infrastructure, Coinbase Custody. 0.25% expense ratio. Seeks to stake substantially all SOL. Tracks Lukka Prime Solana Reference Rate.",
    },
    {
        "ticker": "MSOL",
        "issuer": "Morgan Stanley",
        "exchange": "NYSE Arca",
        "aum_usd": None,
        "price_usd": None,
        "price_source": "static",
        "exp_ratio_current": "0.14%",
        "exp_ratio_target": "0.14%",
        "exp_waiver_note": None,
        "fee_waived": False,
        "staking_enabled": True,
        # 5% retained as validator fee; 95% of staking rewards distributed to shareholders
        "commission_current": "5%",
        "commission_target": "5%",
        "commission_note": "5% validator fee on staking rewards; 95% passed to shareholders",
        "pct_staked": "~100%",
        "gross_yield": "N/A",
        "net_yield": "N/A",
        "description": "Launched Jul 28, 2026 on NYSE Arca. Lowest-fee Solana ETF at 0.14%. Staking via Figment, Galaxy, Coinbase Canada. 95% of staking rewards distributed to shareholders. Tracks CoinDesk Solana Benchmark 4PM NY Settlement Rate.",
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
        "last_verified": "2026-08-17",
        "notes": "Approved. Live on NYSE Arca as SOEZ since Dec 3, 2025. 0.19% expense ratio. Coinbase custody and staking. Staking rewards distributed monthly as cash.",
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
        "last_verified": "2026-08-17",
        "notes": "S-1 filed Mar 2025. No approval announced as of Aug 2026.",
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
        "last_verified": "2026-08-17",
        "notes": "S-1 filed Jun 2025. Spot SOL ETF still pending as of Aug 2026. ProShares separately launched leveraged futures ETF (SLON).",
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
        "last_verified": "2026-08-17",
        "notes": "Approved. Live on Cboe BZX as SSK. 0.75% expense ratio. Anchorage Digital custody.",
    },
    {
        "issuer": "Morgan Stanley",
        "etf_name": "Morgan Stanley Solana Trust",
        "ticker_proposed": "MSOL",
        "filing_type": "S-1",
        "status": "approved",
        "filing_date": "2026-01-06",
        "decision_deadline": None,
        "staking_included": True,
        "is_new": True,
        "last_verified": "2026-08-17",
        "sec_url": "https://www.sec.gov/Archives/edgar/data/2103547/000110465926000988/tm2534148d1_s1.htm",
        "notes": "Approved. Live on NYSE Arca as MSOL since Jul 28, 2026. Lowest fee at 0.14%. Staking via Figment, Galaxy, Coinbase Canada. 95% of staking rewards distributed to shareholders.",
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
        "last_verified": "2026-08-17",
        "sec_url": "https://www.sec.gov/Archives/edgar/data/2073298/000199937125014084/solana-s1a_092625.htm",
        "notes": "S-1/A filed. Planned listing on Nasdaq. Coinbase & BitGo custody. No approval announced as of Aug 2026.",
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
        "last_verified": "2026-08-17",
        "notes": "Approved. Live on Cboe BZX as QSOL since Dec 15, 2025. 0.25% expense ratio. Galaxy Digital staking, Coinbase custody.",
    },
    {
        "issuer": "Osprey Funds",
        "etf_name": "Osprey Solana Trust",
        "ticker_proposed": "OSOL",
        "filing_type": "S-1",
        "status": "withdrawn",
        "filing_date": None,
        "decision_deadline": None,
        "staking_included": None,
        "is_new": True,
        "last_verified": "2026-08-17",
        "notes": "Trust liquidated Jul 15, 2026. Filing effectively withdrawn. (Separate from the REX-Osprey SSK joint filing which launched successfully.)",
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
        "last_verified": "2026-08-17",
        "notes": "LST-based Solana ETF using Jito liquid staking token. Nasdaq filed rule change Feb 2026. SEC issued order instituting formal proceedings Jun 23, 2026. Still pending as of Aug 2026.",
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
