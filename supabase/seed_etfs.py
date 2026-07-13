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

# ── Live ETFs (data sourced from issuer sites / SEC filings, Jul 13 2026) ───

ETFS = [
    {
        "ticker": "BSOL",
        "issuer": "Bitwise",
        "exchange": "NYSE Arca",
        "aum_usd": 636_450_000,        # updated Jul 10 2026
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
        "pct_staked": "100%",          # updated; fund targets 100% staked via Bitwise Onchain Solutions
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
        "exp_ratio_current": "0.19%",  # cut from 0.35% effective Jun 25, 2026
        "exp_ratio_target": "0.19%",
        "exp_waiver_note": "Sponsor fee permanently cut from 0.35% to 0.19% on Jun 25, 2026",
        "fee_waived": False,
        "staking_enabled": True,
        "commission_current": "7%",    # cut from 23% effective Jun 25, 2026 (was 5% waiver Nov–Feb)
        "commission_target": "7%",
        "commission_note": "Sponsor's Staking Fee reduced from 23% to 7% effective Jun 25, 2026 (Amendment No. 3 to Trust Agreement)",
        "pct_staked": "100%",
        "gross_yield": "7.01%",
        "net_yield": "~6.3%",          # estimated: 7.01% × 0.93 − 0.19%
        "description": "Formerly Grayscale Solana Trust; converted to ETF Jan 5, 2026. Sponsor fee and staking commission both permanently cut Jun 25, 2026 to 0.19% and 7% respectively (from 0.35% / 23%).",
    },
    {
        "ticker": "FSOL",
        "issuer": "Fidelity",
        "exchange": "NYSE Arca",
        "aum_usd": 156_230_000,
        "price_usd": 9.76,
        "price_source": "static",
        "exp_ratio_current": "0.25%",  # waiver expired May 18, 2026
        "exp_ratio_target": "0.25%",
        "exp_waiver_note": "Both fees waived through May 18, 2026 (now expired)",
        "fee_waived": False,           # waiver expired May 18, 2026
        "staking_enabled": True,
        "commission_current": "15%",   # waiver expired May 18, 2026
        "commission_target": "15%",
        "commission_note": "15% staking commission; waiver expired May 18, 2026",
        "pct_staked": "N/A",
        "gross_yield": "~7.0%",
        "net_yield": "~5.7%",          # estimated: 7.0% × 0.85 − 0.25%
        "description": "Launched Nov 18, 2025. Management fee and staking commission both waived through May 18, 2026; now at 0.25% expense ratio and 15% staking commission. % staked not publicly disclosed.",
    },
    {
        "ticker": "VSOL",
        "issuer": "VanEck",
        "exchange": "Cboe BZX",
        "aum_usd": 15_060_000,         # updated Jul 10 2026 (down from earlier $150M estimate)
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
        "description": "Distributes staking rewards quarterly ($0.035949/share Jun 30, 2026). 99.77% utilization rate. CME CF Solana-Dollar Reference Rate. Anchorage Digital, BitGo, and Coinbase custody.",
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
        "description": "Partners with Marinade Finance for liquid staking. Marinade Finance is exclusive staking provider for minimum two years from first trading date.",
    },
    {
        "ticker": "SSK",
        "issuer": "REX-Osprey",
        "exchange": "Cboe BZX",
        "aum_usd": 67_000_000,         # approximate as of May 2026
        "price_usd": None,
        "price_source": "static",
        "exp_ratio_current": "0.75%",
        "exp_ratio_target": "0.75%",
        "exp_waiver_note": None,
        "fee_waived": False,
        "staking_enabled": True,
        "commission_current": "N/A",
        "commission_target": "N/A",
        "commission_note": "100% of staking rewards accrue to shareholders; no separate staking commission per prospectus",
        "pct_staked": "N/A",
        "gross_yield": "N/A",
        "net_yield": "N/A",
        "description": "REX-Osprey SOL + Staking ETF. Anchorage Digital custody. Launched Jul 2, 2025. 100% of staking rewards accrue to shareholders. CF Benchmarks pricing.",
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
        "exp_waiver_note": "Fee waived Dec 3, 2025 – May 31, 2026 on first $5B assets",
        "fee_waived": False,
        "staking_enabled": True,
        "commission_current": "N/A",
        "commission_target": "N/A",
        "commission_note": "Staking rewards reflected in NAV; commission not separately disclosed",
        "pct_staked": "N/A",
        "gross_yield": "~7.0%",
        "net_yield": "N/A",
        "description": "Launched Dec 3, 2025 on NYSE Arca. 0.19% sponsor fee (waived through May 31, 2026 on first $5B). Tracks CF Benchmarks Solana Index plus staking rewards. Franklin Holdings LLC sponsor.",
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
        "commission_note": "Stakes through Galaxy Blockchain Infrastructure LLC; rewards reflected in NAV",
        "pct_staked": "N/A",
        "gross_yield": "~7.0%",
        "net_yield": "N/A",
        "description": "Launched Dec 15, 2025 on Cboe BZX. 0.25% expense ratio. Stakes SOL through Galaxy Blockchain Infrastructure LLC. Coinbase Custody Trust Company. Lukka Inc. pricing.",
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
        "last_verified": "2026-07-13",
        "notes": "Approved and live on NYSE Arca as SOEZ since Dec 3, 2025. 0.19% expense ratio. CF Benchmarks Solana Index.",
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
        "last_verified": "2026-07-13",
        "notes": "S-1 filed Mar 2025. US spot ETF filing still pending as of Jul 2026. (Separate from European ETP SOLW.)",
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
        "last_verified": "2026-07-13",
        "notes": "S-1 filed Jun 2025. Still pending as of Jul 2026. Also has live leveraged futures ETF (SLON).",
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
        "last_verified": "2026-07-13",
        "notes": "Approved. Live on Cboe BZX as SSK since Jul 2, 2025. 0.75% expense ratio. Anchorage Digital custody. AUM ~$67M.",
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
        "last_verified": "2026-07-13",
        "sec_url": "https://www.sec.gov/Archives/edgar/data/2103547/000110465926000988/tm2534148d1_s1.htm",
        "notes": "S-1 filed Jan 2026 via E*TRADE Capital Management. S-1/A amended Jun 18, 2026 with 0.14% sponsor fee. Proposed ticker MSOL on NYSE Arca. Includes staking.",
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
        "last_verified": "2026-07-13",
        "sec_url": "https://www.sec.gov/Archives/edgar/data/2073298/000199937125014084/solana-s1a_092625.htm",
        "notes": "S-1/A filed. Planned listing on Nasdaq. Coinbase & BitGo custody. Still pending as of Jul 2026.",
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
        "last_verified": "2026-07-13",
        "notes": "Approved and live on Cboe BZX as QSOL since Dec 15, 2025. 0.25% expense ratio. Galaxy Blockchain Infrastructure staking. Coinbase custody.",
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
        "last_verified": "2026-07-13",
        "notes": "S-1 filed Oct 2025. Proposed ticker OSOL on Cboe BZX. Coinbase custody. Separate from REX-Osprey joint filing. Still pending as of Jul 2026.",
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
        "last_verified": "2026-07-13",
        "notes": "LST-based Solana ETF using Jito liquid staking token. SEC published notice Mar 2026. Nasdaq filed listing rule change (SR-NASDAQ-2026-010). Review period ongoing.",
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
