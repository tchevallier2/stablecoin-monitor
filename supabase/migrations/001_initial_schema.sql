-- ============================================
-- Stablecoin Monitor — Initial Schema
-- ============================================

-- Issuers (companies behind stablecoins)
CREATE TABLE issuers (
  id SERIAL PRIMARY KEY,
  name TEXT NOT NULL UNIQUE,
  founded_year INTEGER,
  headquarters TEXT,
  website TEXT,
  description TEXT,
  regulatory_status TEXT,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Blockchains
CREATE TABLE chains (
  id SERIAL PRIMARY KEY,
  name TEXT NOT NULL UNIQUE,
  slug TEXT NOT NULL UNIQUE
);

-- Stablecoins
CREATE TABLE stablecoins (
  id SERIAL PRIMARY KEY,
  ticker TEXT NOT NULL UNIQUE,
  name TEXT NOT NULL,
  issuer_id INTEGER REFERENCES issuers(id),
  peg_currency TEXT DEFAULT 'USD',
  type TEXT, -- fiat-backed, crypto-backed, algorithmic, commodity-backed, etc.
  description TEXT,
  market_cap_usd NUMERIC,
  circulating_supply NUMERIC,
  price_usd NUMERIC,
  reserve_assets TEXT,
  reserve_manager TEXT,
  custodians TEXT,
  attestation_audit TEXT,
  regulator_charter TEXT,
  third_party_issuance BOOLEAN DEFAULT FALSE,
  sponsor TEXT,
  website TEXT,
  coingecko_id TEXT,
  defillama_id TEXT,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Many-to-many: stablecoins <-> chains
CREATE TABLE stablecoin_chains (
  id SERIAL PRIMARY KEY,
  stablecoin_id INTEGER NOT NULL REFERENCES stablecoins(id) ON DELETE CASCADE,
  chain_id INTEGER NOT NULL REFERENCES chains(id) ON DELETE CASCADE,
  contract_address TEXT,
  supply_on_chain NUMERIC,
  updated_at TIMESTAMPTZ DEFAULT NOW(),
  UNIQUE (stablecoin_id, chain_id)
);

-- Time-series market data (one row per coin per day)
CREATE TABLE market_snapshots (
  id SERIAL PRIMARY KEY,
  stablecoin_id INTEGER NOT NULL REFERENCES stablecoins(id) ON DELETE CASCADE,
  date DATE NOT NULL,
  market_cap_usd NUMERIC,
  circulating_supply NUMERIC,
  price_usd NUMERIC,
  market_share_pct NUMERIC,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  UNIQUE (stablecoin_id, date)
);

-- User-defined monitoring alerts
CREATE TABLE alerts (
  id SERIAL PRIMARY KEY,
  stablecoin_id INTEGER REFERENCES stablecoins(id) ON DELETE CASCADE,
  condition_type TEXT NOT NULL, -- 'mcap_below', 'mcap_above', 'share_change', 'depeg'
  threshold_value NUMERIC NOT NULL,
  is_active BOOLEAN DEFAULT TRUE,
  last_triggered_at TIMESTAMPTZ,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- News items
CREATE TABLE news_items (
  id SERIAL PRIMARY KEY,
  title TEXT NOT NULL,
  url TEXT,
  source TEXT,
  published_at TIMESTAMPTZ,
  stablecoin_ids INTEGER[], -- array of stablecoin IDs this news relates to
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Indexes for common queries
CREATE INDEX idx_stablecoins_ticker ON stablecoins(ticker);
CREATE INDEX idx_stablecoins_market_cap ON stablecoins(market_cap_usd DESC);
CREATE INDEX idx_market_snapshots_date ON market_snapshots(stablecoin_id, date DESC);
CREATE INDEX idx_alerts_active ON alerts(is_active) WHERE is_active = TRUE;
CREATE INDEX idx_news_published ON news_items(published_at DESC);

-- Updated_at trigger function
CREATE OR REPLACE FUNCTION update_updated_at()
RETURNS TRIGGER AS $$
BEGIN
  NEW.updated_at = NOW();
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Apply trigger to tables with updated_at
CREATE TRIGGER set_updated_at BEFORE UPDATE ON issuers
  FOR EACH ROW EXECUTE FUNCTION update_updated_at();

CREATE TRIGGER set_updated_at BEFORE UPDATE ON stablecoins
  FOR EACH ROW EXECUTE FUNCTION update_updated_at();

CREATE TRIGGER set_updated_at BEFORE UPDATE ON stablecoin_chains
  FOR EACH ROW EXECUTE FUNCTION update_updated_at();

-- Enable Row Level Security (public read for now)
ALTER TABLE issuers ENABLE ROW LEVEL SECURITY;
ALTER TABLE chains ENABLE ROW LEVEL SECURITY;
ALTER TABLE stablecoins ENABLE ROW LEVEL SECURITY;
ALTER TABLE stablecoin_chains ENABLE ROW LEVEL SECURITY;
ALTER TABLE market_snapshots ENABLE ROW LEVEL SECURITY;
ALTER TABLE alerts ENABLE ROW LEVEL SECURITY;
ALTER TABLE news_items ENABLE ROW LEVEL SECURITY;

-- Public read policies
CREATE POLICY "Public read issuers" ON issuers FOR SELECT USING (true);
CREATE POLICY "Public read chains" ON chains FOR SELECT USING (true);
CREATE POLICY "Public read stablecoins" ON stablecoins FOR SELECT USING (true);
CREATE POLICY "Public read stablecoin_chains" ON stablecoin_chains FOR SELECT USING (true);
CREATE POLICY "Public read market_snapshots" ON market_snapshots FOR SELECT USING (true);
CREATE POLICY "Public read alerts" ON alerts FOR SELECT USING (true);
CREATE POLICY "Public read news_items" ON news_items FOR SELECT USING (true);
