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

# ── Live ETFs (data sourced from issuer sites / SEC filings, Sep 14 2026) ────

ETFS = [
    {
        "ticker": "BSOL",
        "issuer": "Bitwise",
        "exchange": "NYSE Arca",
        "aum_usd": 1_000_000_000,  # Surpassed $1B on Aug 28, 2026
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
        "gross_yield": "6.76%",
        "net_yield": "5.80%",
        "description": "Reinvests staking rewards (no distribution). Uses Helius / Bitwise Onchain Solutions validator. 6% commission on staking rewards. Surpassed $1B AUM on Aug 28, 2026.",
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
        "exp_waiver_note": "Waiver expired Feb 5, 2026",
        "fee_waived": False,
        "staking_enabled": True,
        "commission_current": "7%",
        "commission_target": "7%",
        "commission_note": "Reduced to 7% (from 23%) on Jun 25, 2026; distributes quarterly cash rewards",
        "pct_staked": "100%",
        "gross_yield": "6.1%",
        "net_yield": "~5.5%",
        "description": "Formerly Grayscale Solana Trust; converted to ETF Jan 5, 2026. Sponsor fee cut to 0.19% on Jun 25, 2026. Staking commission cut to 7% on Jun 25, 2026. Distributes quarterly cash staking rewards starting Aug 2026.",
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
        "commission_note": "Waiver expired May 18, 2026; 15% staking commission now in effect",
        "pct_staked": "N/A",
        "gross_yield": "~7.0%",
        "net_yield": "N/A",
        "description": "Launched Nov 18, 2025. Both management fee and staking commission waived through May 18, 2026 (now expired). 0.25% expense ratio; 15% staking commission. % staked not publicly disclosed.",
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
        "net_yield": "~4.6%",
        "description": "Uses SOL Strategies as staking provider. 88.04% of SOL staked. Gross staking yield 4.85% as of Jul 2026. Commission not separately disclosed.",
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
        "exp_waiver_note": "Waived Jul 28, 2026 – Jul 27, 2027",
        "fee_waived": True,
        "staking_enabled": True,
        "commission_current": "N/A",
        "commission_target": "N/A",
        "commission_note": "Distributes rewards to shareholders monthly; 1-year fee waiver from Jul 28, 2026",
        "pct_staked": "99.77%",
        "gross_yield": "~7.0%",
        "net_yield": "~4.65%",
        "description": "Distributes staking rewards monthly. 99.77% utilization rate. CME CF Solana-Dollar Reference Rate. 21Shares introduced 1-year management fee waiver effective Jul 28, 2026 through Jul 27, 2027 (expense ratio 0% during waiver). Net staking yield ~4.65%.",
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
        "commission_note": "Marinade Finance liquid staking; no staking fee charged",
        "pct_staked": "N/A",
        "gross_yield": "~7.0%",
        "net_yield": "N/A",
        "description": "Partners with Marinade Finance for liquid staking. Sponsor does not charge staking fees; rewards flow to NAV.",
    },
    {
        "ticker": "SSK",
        "issuer": "REX-Osprey",
        "exchange": "Cboe BZX",
        "aum_usd": 88_640_000,
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
        "description": "REX-Osprey SOL Staking ETF. Anchorage Digital custody. AUM ~$88.6M.",
    },
    {
        "ticker": "SOEZ",
        "issuer": "Franklin Templeton",
        "exchange": "NYSE Arca",
        "aum_usd": 8_513_040,  # As of Jun 30, 2026
        "price_usd": None,
        "price_source": "static",
        "exp_ratio_current": "0.19%",
        "exp_ratio_target": "0.19%",
        "exp_waiver_note": "Waiver expired May 31, 2026",
        "fee_waived": False,
        "staking_enabled": True,
        "commission_current": "N/A",
        "commission_target": "N/A",
        "commission_note": "Distributes staking rewards monthly; Coinbase Crypto as staking provider",
        "pct_staked": "N/A",
        "gross_yield": "N/A",
        "net_yield": "N/A",
        "description": "Franklin Solana ETF. Launched Dec 3, 2025 on NYSE Arca. 0.19% expense ratio. Fee waived Dec 3, 2025–May 31, 2026 (now expired). Stakes up to 100% through Coinbase Crypto; distributes rewards monthly.",
    },
    {
        "ticker": "QSOL",
        "issuer": "Invesco Galaxy",
        "exchange": "Cboe BZX",
        "aum_usd": 6_190_000,
        "price_usd": None,
        "price_source": "static",
        "exp_ratio_current": "0.25%",
        "exp_ratio_target": "0.25%",
        "exp_waiver_note": None,
        "fee_waived": False,
        "staking_enabled": True,
        "commission_current": "N/A",
        "commission_target": "N/A",
        "commission_note": "Stakes substantially all assets; rewards reinvested in SOL",
        "pct_staked": "N/A",
        "gross_yield": "N/A",
        "net_yield": "N/A",
        "description": "Invesco Galaxy Solana ETF. Launched Dec 15, 2025 on Cboe BZX. 0.25% expense ratio. Coinbase custody. Tracks Lukka Prime Solana Reference Rate. Stakes substantially all assets.",
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
        "commission_note": "5% commission to validators; 95% of staking yields returned to shareholders",
        "pct_staked": "100%",
        "gross_yield": "~3.4%",
        "net_yield": "N/A",
        "description": "Morgan Stanley Solana Trust. Launched Jul 28, 2026 on NYSE Arca. Lowest-cost Solana ETF at 0.14%. Stakes 100% through Figment, Galaxy Digital, and Coinbase Canada. 5% validator commission; 95% of rewards distributed to shareholders.",
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
        "last_verified": "2026-09-14",
        "notes": "Approved and live on NYSE Arca as SOEZ since Dec 3, 2025. 0.19% expense ratio. Fee waiver expired May 31, 2026.",
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
        "last_verified": "2026-09-14",
        "notes": "S-1 filed Mar 2025. No approval announcement found as of Sep 2026.",
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
        "last_verified": "2026-09-14",
        "notes": "S-1 filed Jun 2025. Spot ETF still pending as of Sep 2026. Also has live leveraged futures ETF (SLON).",
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
        "last_verified": "2026-09-14",
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
        "last_verified": "2026-09-14",
        "sec_url": "https://www.sec.gov/Archives/edgar/data/2103547/000110465926000988/tm2534148d1_s1.htm",
        "notes": "Approved and live on NYSE Arca as MSOL since Jul 28, 2026. 0.14% expense ratio (lowest-cost). Stakes 100% through Figment, Galaxy Digital, Coinbase Canada.",
    },
    {
        "issuer": "CoinShares",
        "etf_name": "CoinShares Solana ETF",
        "ticker_proposed": None,
        "filing_type": "S-1",
        "status": "withdrawn",
        "filing_date": None,
        "decision_deadline": None,
        "staking_included": None,
        "is_new": True,
        "last_verified": "2026-09-14",
        "sec_url": "https://www.sec.gov/Archives/edgar/data/2073298/000199937125014084/solana-s1a_092625.htm",
        "notes": "Withdrawn Nov 28, 2025. Filed Form RW to withdraw S-1 for XRP, Solana, and Litecoin ETFs. Required asset-purchase deal was never completed.",
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
        "last_verified": "2026-09-14",
        "notes": "Approved. Registration effective Dec 9, 2025. Live on Cboe BZX as QSOL since Dec 15, 2025. 0.25% expense ratio. Coinbase custody.",
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
        "last_verified": "2026-09-14",
        "notes": "Osprey Solana Trust (OSOL) was liquidated Jul 15, 2026. Trust never converted to a fully operational ETF. Separate from REX-Osprey joint SSK product.",
    },
    {
        "issuer": "VanEck",
        "etf_name": "VanEck JitoSOL ETF",
        "ticker_proposed": None,
        "filing_type": "S-1",
        "status": "filed",
        "filing_date": None,
        "decision_deadline": "2026-11-15",
        "staking_included": True,
        "is_new": True,
        "last_verified": "2026-09-14",
        "notes": "LST-based Solana ETF using Jito liquid staking token. Nasdaq filed rule change Mar 10, 2026. SEC extended deadline to Nov 15, 2026. Separate from VSOL spot ETF.",
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
