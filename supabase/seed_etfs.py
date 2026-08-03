"""
Seed script for Solana ETF tables.
Populates solana_etfs with the 6 live US-listed Solana ETFs
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

# ── Live ETFs (data last reviewed Aug 3, 2026) ──────────────────────

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
        "aum_usd": 97_000_000,
        "price_usd": 6.15,
        "price_source": "static",
        "exp_ratio_current": "0.19%",
        "exp_ratio_target": "0.19%",
        "exp_waiver_note": "Sponsor fee permanently reduced to 0.19% effective June 25, 2026 (from 0.35%)",
        "fee_waived": False,
        "staking_enabled": True,
        "commission_current": "7%",
        "commission_target": "7%",
        "commission_note": "7% staking commission per June 2026 SEC filing (reduced from original 23%)",
        "pct_staked": "100%",
        "gross_yield": "~6.10%",
        "net_yield": "~5.03%",
        "description": "Formerly Grayscale Solana Trust; converted to ETF Jan 5, 2026. Sponsor fee cut from 0.35% to 0.19% in June 2026. 7% staking commission. Shifting to direct cash distributions of staking rewards (SEC filing Jul 2026).",
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
        "commission_note": "15% commission on staking rewards (waiver expired May 18, 2026)",
        "pct_staked": "N/A",
        "gross_yield": "~7.0%",
        "net_yield": "~5.70%",
        "description": "Launched Nov 18, 2025. Fee waiver (management fee + staking commission) expired May 18, 2026. Now 0.25% expense ratio and 15% staking commission. % staked not publicly disclosed.",
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
        "exp_ratio_current": "0% (waived)",
        "exp_ratio_target": "0.21%",
        "exp_waiver_note": "1-year sponsor fee waiver starting July 28, 2026",
        "fee_waived": True,
        "staking_enabled": True,
        "commission_current": "N/A",
        "commission_target": "N/A",
        "commission_note": "Distributes rewards to shareholders monthly",
        "pct_staked": "99.77%",
        "gross_yield": "~7.0%",
        "net_yield": "~4.65%",
        "description": "21Shares introduced 1-year sponsor fee waiver starting July 28, 2026. 99.77% utilization rate. Monthly staking reward distributions. Net staking yield ~4.65% as of late July 2026.",
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
        "description": "Partners with Marinade Finance for liquid staking.",
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
        "commission_note": "Up to 100% staked via Coinbase Crypto; monthly distributions with 3-month lag",
        "pct_staked": "~100%",
        "gross_yield": "N/A",
        "net_yield": "N/A",
        "description": "Launched Dec 3, 2025 on NYSE Arca. Stakes up to 100% via Coinbase Crypto. Monthly staking distributions with 3-month lag. 0.19% expense ratio; initial waiver expired May 31, 2026.",
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
        "commission_note": "Stakes substantially all holdings; quarterly distributions",
        "pct_staked": "~100%",
        "gross_yield": "N/A",
        "net_yield": "N/A",
        "description": "Launched Dec 15, 2025 on Cboe BZX. Invesco and Galaxy Digital collaboration. Stakes substantially all SOL holdings. 0.25% expense ratio.",
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
        "commission_current": "5%",
        "commission_target": "5%",
        "commission_note": "95% of staking rewards distributed; staking via Figment, Galaxy Blockchain, Coinbase Canada",
        "pct_staked": "~100%",
        "gross_yield": "N/A",
        "net_yield": "N/A",
        "description": "Launched July 28, 2026 on NYSE Arca. Lowest expense ratio at 0.14%. Stakes up to 100% via Figment, Galaxy Blockchain, Coinbase Canada. 95% of staking rewards distributed to shareholders.",
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
        "last_verified": "2026-08-03",
        "notes": "Approved. Live on NYSE Arca as SOEZ (launched Dec 3, 2025). 0.19% expense ratio. Staking via Coinbase Crypto; monthly distributions.",
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
        "last_verified": "2026-08-03",
        "notes": "S-1 filed Mar 2025. No evidence of US approval as of Aug 2026. WisdomTree operates a European physical Solana ETP (WSOL) separately.",
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
        "last_verified": "2026-08-03",
        "notes": "S-1 filed Jun 2025. No approval evidence as of Aug 2026. Also has live leveraged futures ETF (SLON).",
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
        "last_verified": "2026-08-03",
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
        "is_new": False,
        "last_verified": "2026-08-03",
        "sec_url": "https://www.sec.gov/Archives/edgar/data/2103547/000110465926000988/tm2534148d1_s1.htm",
        "notes": "Approved. Launched July 28, 2026 on NYSE Arca as MSOL. 0.14% expense ratio. Stakes up to 100% via Figment, Galaxy Blockchain, Coinbase Canada. 95% of staking rewards distributed.",
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
        "last_verified": "2026-08-03",
        "sec_url": "https://www.sec.gov/Archives/edgar/data/2073298/000199937125014084/solana-s1a_092625.htm",
        "notes": "S-1/A filed. Planned listing on Nasdaq. Coinbase & BitGo custody. No approval evidence as of Aug 2026.",
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
        "is_new": False,
        "last_verified": "2026-08-03",
        "notes": "Approved. Launched Dec 15, 2025 on Cboe BZX as QSOL. 0.25% expense ratio. Galaxy Digital collaboration.",
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
        "is_new": False,
        "last_verified": "2026-08-03",
        "notes": "OSOL OTC trust liquidated July 15, 2026 (announced June 4, 2026). ETF conversion S-1 for Cboe BZX listing appears abandoned. Separate from REX-Osprey SSK.",
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
        "last_verified": "2026-08-03",
        "notes": "LST-based Solana ETF using Jito liquid staking token. Separate from VSOL spot ETF. Still pending SEC review as of Aug 2026.",
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
