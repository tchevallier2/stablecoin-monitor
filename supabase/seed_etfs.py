"""
Seed script for Solana ETF tables.
Populates solana_etfs with live US-listed Solana ETFs
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

# ── Live ETFs (data sourced from issuer sites, Jul 27 2026) ──────────

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
        "exp_ratio_current": "0.19%",
        "exp_ratio_target": "0.19%",
        "exp_waiver_note": None,
        "fee_waived": False,
        "staking_enabled": True,
        "commission_current": "7%",
        "commission_target": "7%",
        "commission_note": "Reduced from 23% to 7% effective June 25, 2026 (prior 5% temporary reduction Nov 2025 expired)",
        "pct_staked": "100%",
        "gross_yield": "6.10%",
        "net_yield": "5.03%",
        "description": "Formerly Grayscale Solana Trust; converted to ETF Jan 5, 2026. 7% staking commission (permanently reduced from 23% on June 25, 2026). 0.19% expense ratio (reduced from 0.35% on June 25, 2026). Distributes staking rewards quarterly in cash.",
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
        "commission_note": "15% staking commission (waiver expired May 18, 2026)",
        "pct_staked": "N/A",
        "gross_yield": "~7.0%",
        "net_yield": "~5.7%",
        "description": "Launched Nov 18, 2025. Management fee (0.25%) and staking commission (15%) waivers both expired May 18, 2026. % staked not publicly disclosed.",
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
        "exp_ratio_current": "0.21%",
        "exp_ratio_target": "0.21%",
        "exp_waiver_note": None,
        "fee_waived": False,
        "staking_enabled": True,
        "commission_current": "N/A",
        "commission_target": "N/A",
        "commission_note": "Distributes rewards to shareholders quarterly",
        "pct_staked": "99.77%",
        "gross_yield": "~7.0%",
        "net_yield": "~6.7%",
        "description": "Distributes staking rewards quarterly ($0.016962/share in Mar 2026; Jun 30 distribution confirmed). 99.77% utilization rate. CME CF Solana-Dollar Reference Rate.",
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
        "commission_note": "Marinade Finance liquid staking; rewards reinvested into NAV",
        "pct_staked": "100%",
        "gross_yield": "~7.0%",
        "net_yield": "N/A",
        "description": "Partners with Marinade Finance (Marinade Select) for liquid staking. Stakes 100% of assets; rewards compound into NAV.",
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
    {
        "ticker": "SOEZ",
        "issuer": "Franklin Templeton",
        "exchange": "NYSE Arca",
        "aum_usd": 9_280_000,
        "price_usd": None,
        "price_source": "static",
        "exp_ratio_current": "0.19%",
        "exp_ratio_target": "0.19%",
        "exp_waiver_note": "Fee waiver on first $5B AUM expired May 31, 2026",
        "fee_waived": False,
        "staking_enabled": True,
        "commission_current": "N/A",
        "commission_target": "N/A",
        "commission_note": "No separate staking commission; rewards distributed monthly in cash (3-month lag)",
        "pct_staked": "~100%",
        "gross_yield": "~7.0%",
        "net_yield": "N/A",
        "description": "Launched December 2025 on NYSE Arca. Stakes up to 100% of SOL through Coinbase. Distributes staking rewards monthly in cash. 0.19% expense ratio (fee waiver on first $5B AUM expired May 31, 2026).",
    },
    {
        "ticker": "QSOL",
        "issuer": "Invesco Galaxy",
        "exchange": "Cboe BZX",
        "aum_usd": 5_980_000,
        "price_usd": None,
        "price_source": "static",
        "exp_ratio_current": "0.25%",
        "exp_ratio_target": "0.25%",
        "exp_waiver_note": None,
        "fee_waived": False,
        "staking_enabled": True,
        "commission_current": "N/A",
        "commission_target": "N/A",
        "commission_note": "Distributes staking rewards; commission not separately disclosed",
        "pct_staked": "~100%",
        "gross_yield": "N/A",
        "net_yield": "N/A",
        "description": "Launched December 10, 2025 on Cboe BZX. Stakes substantially all SOL through Galaxy Digital Infrastructure. Coinbase custody. 0.25% expense ratio.",
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
        "last_verified": "2026-07-27",
        "notes": "Approved and live on NYSE Arca as SOEZ (launched Dec 2025). 0.19% expense ratio. Stakes up to 100% via Coinbase. Fee waiver on first $5B AUM expired May 31, 2026.",
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
        "last_verified": "2026-07-27",
        "notes": "S-1 filed Mar 2025. US spot ETF still pending (separate from European SOLW ETP).",
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
        "last_verified": "2026-07-27",
        "notes": "S-1 filed Jun 2025 for spot Solana ETF. Still pending. Also has live leveraged futures ETF (SLON).",
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
        "last_verified": "2026-07-27",
        "notes": "Approved. Live on Cboe BZX as SSK. 0.75% expense ratio. Anchorage Digital custody.",
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
        "last_verified": "2026-07-27",
        "sec_url": "https://www.sec.gov/Archives/edgar/data/2103547/000110465926000988/tm2534148d1_s1.htm",
        "notes": "S-1 filed Jan 2026; amended S-1 filed June 18, 2026. Ticker MSOL proposed on NYSE Arca. 0.14% annual sponsor fee. Stakes up to 100%. Still pending SEC approval.",
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
        "last_verified": "2026-07-27",
        "sec_url": "https://www.sec.gov/Archives/edgar/data/2073298/000199937125014084/solana-s1a_092625.htm",
        "notes": "S-1/A filed. Planned listing on Nasdaq. Coinbase & BitGo custody. Still pending.",
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
        "last_verified": "2026-07-27",
        "notes": "Approved and live on Cboe BZX as QSOL (launched Dec 10, 2025). 0.25% expense ratio. Stakes substantially all SOL via Galaxy Digital Infrastructure.",
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
        "last_verified": "2026-07-27",
        "notes": "ETF filing withdrawn. Osprey Solana Trust (OSOL OTC trust) was liquidated July 15, 2026. Separate from REX-Osprey joint filing (SSK).",
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
        "last_verified": "2026-07-27",
        "notes": "LST-based Solana ETF using Jito liquid staking token. In exchange-review phase (Nasdaq/SEC). Separate from VSOL spot ETF.",
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
