"""
Seed script for Solana ETF tables.
Populates solana_etfs with the 10 live US-listed Solana ETFs
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

# ── Live ETFs (data sourced from issuer sites, Sep 7 2026) ──────────

ETFS = [
    {
        "ticker": "BSOL",
        "issuer": "Bitwise",
        "exchange": "NYSE Arca",
        "aum_usd": 1_018_000_000,
        "price_usd": None,
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
        "gross_yield": "~6.4%",
        "net_yield": "5.80%",
        "description": "Surpassed $1B AUM Aug 28, 2026 (launched Oct 28, 2025). Uses Helius / Bitwise Onchain Solutions validator. 6% commission on staking rewards. Reinvests rewards in NAV.",
    },
    {
        "ticker": "GSOL",
        "issuer": "Grayscale",
        "exchange": "NYSE Arca",
        "aum_usd": 99_700_000,
        "price_usd": None,
        "price_source": "static",
        "exp_ratio_current": "0.19%",
        "exp_ratio_target": "0.19%",
        "exp_waiver_note": "Waiver expired Feb 5, 2026; fee permanently cut to 0.19% on Jun 25, 2026",
        "fee_waived": False,
        "staking_enabled": True,
        "commission_current": "7%",
        "commission_target": "7%",
        "commission_note": "Cut to 7% on Jun 25, 2026 (permanent; was 23% originally)",
        "pct_staked": "100%",
        "gross_yield": "~7.0%",
        "net_yield": "~5.8%",
        "description": "Formerly Grayscale Solana Trust; converted to ETF Jan 5, 2026. Fee cuts Jun 25, 2026: sponsor fee 0.19% (from 0.35%), staking commission 7% (from 23%).",
    },
    {
        "ticker": "FSOL",
        "issuer": "Fidelity",
        "exchange": "NYSE Arca",
        "aum_usd": 156_230_000,
        "price_usd": None,
        "price_source": "static",
        "exp_ratio_current": "0.25%",
        "exp_ratio_target": "0.25%",
        "exp_waiver_note": "Waiver expired May 18, 2026",
        "fee_waived": False,
        "staking_enabled": True,
        "commission_current": "15%",
        "commission_target": "15%",
        "commission_note": "15% post-waiver (waiver expired May 18, 2026)",
        "pct_staked": "N/A",
        "gross_yield": "~7.0%",
        "net_yield": "~5.7% (est.)",
        "description": "Launched Nov 18, 2025. Both management fee and staking commission waived through May 18, 2026; now 0.25% expense ratio and 15% staking commission. % staked not publicly disclosed.",
    },
    {
        "ticker": "VSOL",
        "issuer": "VanEck",
        "exchange": "Cboe BZX",
        "aum_usd": 150_000_000,
        "price_usd": None,
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
        "net_yield": "~4.55% (est.)",
        "description": "Uses SOL Strategies as staking provider. 88.04% of SOL staked. Gross staking yield 4.85% as of Jul 31, 2026. Commission not separately disclosed.",
    },
    {
        "ticker": "TSOL",
        "issuer": "21Shares",
        "exchange": "Cboe BZX",
        "aum_usd": 29_980_000,
        "price_usd": None,
        "price_source": "static",
        "exp_ratio_current": "0% (waived)",
        "exp_ratio_target": "0.21%",
        "exp_waiver_note": "Fee waived Jul 28, 2026 through Jul 27, 2027",
        "fee_waived": True,
        "staking_enabled": True,
        "commission_current": "N/A",
        "commission_target": "N/A",
        "commission_note": "Distributes rewards to shareholders quarterly",
        "pct_staked": "99.77%",
        "gross_yield": "~7.0%",
        "net_yield": "~6.7%",
        "description": "Distributes staking rewards quarterly. 99.77% utilization rate. CME CF Solana-Dollar Reference Rate. Management fee waived Jul 28, 2026 – Jul 27, 2027.",
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
        "aum_usd": 9_600_000,
        "price_usd": None,
        "price_source": "static",
        "exp_ratio_current": "0.19%",
        "exp_ratio_target": "0.19%",
        "exp_waiver_note": "Fee waiver on first $5B AUM expired May 31, 2026",
        "fee_waived": False,
        "staking_enabled": True,
        "commission_current": "N/A",
        "commission_target": "N/A",
        "commission_note": "Staking rewards reflected in NAV; no separate commission disclosed",
        "pct_staked": "N/A",
        "gross_yield": "~5-7%",
        "net_yield": "N/A",
        "description": "Launched Dec 3, 2025 on NYSE Arca. 0.19% expense ratio. Staking rewards flow back into NAV. Fee waiver on first $5B AUM expired May 31, 2026.",
    },
    {
        "ticker": "QSOL",
        "issuer": "Invesco Galaxy",
        "exchange": "Cboe BZX",
        "aum_usd": 5_107_357,
        "price_usd": None,
        "price_source": "static",
        "exp_ratio_current": "0.25%",
        "exp_ratio_target": "0.25%",
        "exp_waiver_note": None,
        "fee_waived": False,
        "staking_enabled": True,
        "commission_current": "N/A",
        "commission_target": "N/A",
        "commission_note": "Staking rewards reflected in NAV via Lukka Prime benchmark",
        "pct_staked": "N/A",
        "gross_yield": "N/A",
        "net_yield": "N/A",
        "description": "Launched Dec 15, 2025 on Cboe BZX. 0.25% expense ratio. Tracks Lukka Prime Solana Reference Rate plus staking rewards. Coinbase custody. AUM as of Jun 30, 2026.",
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
        "commission_note": "5% of staking yields retained as institutional validator fees; 95% returned to shareholders",
        "pct_staked": "100%",
        "gross_yield": "~7%",
        "net_yield": "N/A",
        "description": "Launched Jul 28, 2026 on NYSE Arca. 0.14% expense ratio (lowest-cost Solana ETF). Stakes 100% of SOL; 95% of staking rewards distributed to shareholders. Via E*TRADE Capital Management (Morgan Stanley subsidiary).",
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
        "last_verified": "2026-09-07",
        "notes": "Approved and live. Launched Dec 3, 2025 on NYSE Arca as SOEZ. 0.19% expense ratio. Fee waiver on first $5B AUM expired May 31, 2026.",
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
        "last_verified": "2026-09-07",
        "notes": "S-1 filed Mar 2025. Still pending as of Sep 2026. (SOLW is a separate European ETP.)",
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
        "last_verified": "2026-09-07",
        "notes": "Spot Solana S-1 still pending as of Sep 2026. Also has live leveraged futures ETF (SLON).",
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
        "last_verified": "2026-09-07",
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
        "last_verified": "2026-09-07",
        "sec_url": "https://www.sec.gov/Archives/edgar/data/2103547/000110465926000988/tm2534148d1_s1.htm",
        "notes": "Approved and live. NYSE Arca certified Jul 24, 2026; launched Jul 28, 2026 as MSOL. 0.14% expense ratio (lowest-cost Solana ETF). Stakes 100% of SOL.",
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
        "last_verified": "2026-09-07",
        "sec_url": "https://www.sec.gov/Archives/edgar/data/2073298/000199937125014084/solana-s1a_092625.htm",
        "notes": "S-1/A filed. Still pending as of Sep 2026. Planned listing on Nasdaq. Coinbase & BitGo custody.",
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
        "last_verified": "2026-09-07",
        "notes": "Approved and live. Launched Dec 15, 2025 on Cboe BZX as QSOL. 0.25% expense ratio. Coinbase custody.",
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
        "last_verified": "2026-09-07",
        "notes": "Underlying Osprey Solana Trust (OSOL) liquidated Jul 15, 2026. ETF conversion plan abandoned. Separate from REX-Osprey joint SSK filing.",
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
        "last_verified": "2026-09-07",
        "notes": "LST-based Solana ETF using Jito liquid staking token. Still pending as of Apr 2026. Separate from VSOL spot ETF.",
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
