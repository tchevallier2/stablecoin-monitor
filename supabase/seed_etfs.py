"""
Seed script for Solana ETF tables.
Populates solana_etfs with the 9 live US-listed Solana ETFs
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

# ── Live ETFs (data sourced from issuer sites, Mar 30 2026) ──────────

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
        "commission_current": "0.06%",
        "commission_target": "0.06%",
        "commission_note": None,
        "pct_staked": "99%",
        "gross_yield": "6.76%",
        "net_yield": "6.36%",
        "description": "Reinvests staking rewards (no distribution). Uses Helius / Bitwise Onchain Solutions validator. 0.06% commission on staking rewards.",
    },
    {
        "ticker": "GSOL",
        "issuer": "Grayscale",
        "exchange": "NYSE Arca",
        "aum_usd": 195_320_000,
        "price_usd": 6.15,
        "price_source": "static",
        "exp_ratio_current": "0.35%",
        "exp_ratio_target": "0.35%",
        "exp_waiver_note": "Waiver expired Feb 5, 2026",
        "fee_waived": False,
        "staking_enabled": True,
        "commission_current": "5%",
        "commission_target": "5%",
        "commission_note": "Reduced from 23% to 5% on Nov 5, 2025",
        "pct_staked": "100%",
        "gross_yield": "7.01%",
        "net_yield": "5.63%",
        "description": "Formerly Grayscale Solana Trust; converted to ETF Jan 5, 2026. 5% commission on staking rewards (reduced from 23%).",
    },
    {
        "ticker": "FSOL",
        "issuer": "Fidelity",
        "exchange": "NYSE Arca",
        "aum_usd": 156_230_000,
        "price_usd": 9.76,
        "price_source": "static",
        "exp_ratio_current": "0% (waived)",
        "exp_ratio_target": "0.25%",
        "exp_waiver_note": "Both fees waived through May 18, 2026",
        "fee_waived": True,
        "staking_enabled": True,
        "commission_current": "0% (waived)",
        "commission_target": "15%",
        "commission_note": "Waived through May 18, 2026; 15% target post-waiver",
        "pct_staked": "N/A",
        "gross_yield": "~7.0%",
        "net_yield": "~7.0%",
        "description": "Launched Nov 18, 2025. Both management fee and staking commission waived through May 18, 2026. % staked not publicly disclosed.",
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
        "commission_current": "0.28%",
        "commission_target": "0.28%",
        "commission_note": "SOL Strategies (Orangefin validator) 0.28% staking service fee; waived Nov 17, 2025 – Feb 17, 2026, active thereafter",
        "pct_staked": "N/A",
        "gross_yield": "6.03%",
        "net_yield": "N/A",
        "description": "Uses SOL Strategies (Orangefin validator) as staking provider. 0.28% staking service fee (waived through Feb 17, 2026). Staking rewards reflected in share price. Yield incorporates both staked and unstaked assets.",
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
        "exp_waiver_note": "Waived Oct 9, 2025 through Oct 8, 2026",
        "fee_waived": True,
        "staking_enabled": True,
        "commission_current": "N/A",
        "commission_target": "N/A",
        "commission_note": "Distributes rewards to shareholders quarterly",
        "pct_staked": "99.77%",
        "gross_yield": "~7.0%",
        "net_yield": "~6.7%",
        "description": "Distributes staking rewards quarterly ($0.016962/share Mar 31 2026; $0.316871/share Feb 2026 covering Oct–Jan). 0.21% expense ratio waived through Oct 8, 2026. 99.77% utilization rate. CME CF Solana-Dollar Reference Rate.",
    },
    {
        "ticker": "SOEZ",
        "issuer": "Franklin Templeton",
        "exchange": "NYSE Arca",
        "aum_usd": 10_290_000,
        "price_usd": 14.58,
        "price_source": "static",
        "exp_ratio_current": "0% (waived)",
        "exp_ratio_target": "0.19%",
        "exp_waiver_note": "Waived through May 31, 2026 on first $5B AUM",
        "fee_waived": True,
        "staking_enabled": True,
        "commission_current": "N/A",
        "commission_target": "N/A",
        "commission_note": "Validator/staking fees not separately disclosed; reflected in NAV",
        "pct_staked": "up to 100%",
        "gross_yield": "N/A",
        "net_yield": "N/A",
        "description": "Launched Nov/Dec 2025 on NYSE Arca. 0.19% expense ratio waived through May 31, 2026 on first $5B AUM. Staking up to 100% of assets; rewards accrue to NAV. Custodians: Coinbase Custody, BNY (admin).",
    },
    {
        "ticker": "SSK",
        "issuer": "REX Shares / Osprey Funds",
        "exchange": "Cboe BZX",
        "aum_usd": 86_360_000,
        "price_usd": 20.85,
        "price_source": "static",
        "exp_ratio_current": "1.40%",
        "exp_ratio_target": "1.40%",
        "exp_waiver_note": None,
        "fee_waived": False,
        "staking_enabled": True,
        "commission_current": "N/A",
        "commission_target": "N/A",
        "commission_note": "Staking rewards distributed as monthly dividends; validator commission not separately disclosed",
        "pct_staked": "N/A",
        "gross_yield": "N/A",
        "net_yield": "~5.12%",
        "description": "Launched July 2, 2025. C-corp structure enabling monthly staking dividend distributions (~5.12% dividend yield). Highest expense ratio at 1.40%. Uses Cayman subsidiary. Note: C-corp introduces double taxation at fund and investor levels.",
    },
    {
        "ticker": "QSOL",
        "issuer": "Invesco / Galaxy Asset Management",
        "exchange": "Cboe BZX",
        "aum_usd": 100_000,
        "price_usd": 25.00,
        "price_source": "static",
        "exp_ratio_current": "0.25%",
        "exp_ratio_target": "0.25%",
        "exp_waiver_note": None,
        "fee_waived": False,
        "staking_enabled": True,
        "commission_current": "N/A",
        "commission_target": "N/A",
        "commission_note": "Staking via Galaxy Blockchain Infrastructure LLC; validator commission not separately disclosed",
        "pct_staked": "substantially all",
        "gross_yield": "N/A",
        "net_yield": "N/A",
        "description": "Launched Dec 15, 2025 on Cboe BZX. Tracks Lukka Prime Solana Reference Rate. Stakes substantially all SOL via Galaxy Blockchain Infrastructure LLC (liquidity sleeve retained unstaked). Custody: Coinbase Custody Trust; admin: BNY Mellon. No formal fee waiver. AUM/price at seed ($100K, 4,000 shares).",
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
        "description": "Smallest by AUM. Partners with Marinade Finance for liquid staking. Highest expense ratio of the group.",
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
        "notes": "S-1 filed Mar 2025. Launched Nov/Dec 2025 as SOEZ on NYSE Arca. 0.19% expense ratio waived through May 31, 2026 on first $5B AUM. Staking up to 100%; rewards accrue to NAV.",
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
        "notes": "S-1 filed Mar 2025.",
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
        "notes": "S-1 filed Jun 2025. ProShares known for leveraged products; may include leveraged/inverse variants.",
    },
    {
        "issuer": "REX Shares",
        "etf_name": "REX-Osprey SOL + Staking ETF",
        "ticker_proposed": "SSK",
        "filing_type": "S-1",
        "status": "approved",
        "filing_date": "2025-03-05",
        "decision_deadline": None,
        "staking_included": True,
        "notes": "Joint filing with Osprey Funds. Launched July 2, 2025 as SSK on Cboe BZX. 1.40% expense ratio. C-corp structure with monthly staking dividend distributions (~5.12% yield). ~$86M AUM as of Mar 2026.",
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
