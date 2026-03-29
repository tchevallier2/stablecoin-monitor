-- ============================================
-- Solana ETF Tables
-- ============================================

-- Live US-listed Solana spot ETFs & ETPs
CREATE TABLE solana_etfs (
  id SERIAL PRIMARY KEY,
  ticker TEXT NOT NULL UNIQUE,
  issuer TEXT NOT NULL,
  exchange TEXT,
  aum_usd NUMERIC,
  price_usd NUMERIC,
  price_source TEXT DEFAULT 'static', -- 'live', 'price-only', 'static'
  exp_ratio_current TEXT,
  exp_ratio_target TEXT,
  exp_waiver_note TEXT,
  fee_waived BOOLEAN DEFAULT FALSE,
  staking_enabled BOOLEAN DEFAULT TRUE,
  commission_current TEXT,
  commission_target TEXT,
  commission_note TEXT,
  pct_staked TEXT,
  gross_yield TEXT,
  net_yield TEXT,
  description TEXT,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Upcoming / pending Solana ETF filings
CREATE TABLE solana_etf_filings (
  id SERIAL PRIMARY KEY,
  issuer TEXT NOT NULL,
  etf_name TEXT NOT NULL,
  ticker_proposed TEXT,
  filing_type TEXT NOT NULL, -- '19b-4', 'S-1', 'S-1/A', etc.
  status TEXT NOT NULL DEFAULT 'filed', -- 'filed', 'acknowledged', 'comment_period', 'effective', 'withdrawn', 'approved'
  filing_date DATE,
  decision_deadline DATE,
  staking_included BOOLEAN,
  sec_url TEXT,
  notes TEXT,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Indexes
CREATE INDEX idx_solana_etfs_aum ON solana_etfs(aum_usd DESC NULLS LAST);
CREATE INDEX idx_solana_etf_filings_status ON solana_etf_filings(status);

-- Updated_at triggers
CREATE TRIGGER set_updated_at BEFORE UPDATE ON solana_etfs
  FOR EACH ROW EXECUTE FUNCTION update_updated_at();

CREATE TRIGGER set_updated_at BEFORE UPDATE ON solana_etf_filings
  FOR EACH ROW EXECUTE FUNCTION update_updated_at();

-- RLS + public read
ALTER TABLE solana_etfs ENABLE ROW LEVEL SECURITY;
ALTER TABLE solana_etf_filings ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Public read solana_etfs" ON solana_etfs FOR SELECT USING (true);
CREATE POLICY "Public read solana_etf_filings" ON solana_etf_filings FOR SELECT USING (true);
