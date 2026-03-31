-- Add is_new flag to highlight recently discovered filings on the dashboard
ALTER TABLE solana_etf_filings ADD COLUMN is_new BOOLEAN DEFAULT FALSE;
