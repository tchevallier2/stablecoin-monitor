-- Track when each filing was last manually verified as accurate
ALTER TABLE solana_etf_filings ADD COLUMN last_verified DATE;
