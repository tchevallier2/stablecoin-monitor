import { supabase } from "@/lib/supabase";
import Link from "next/link";

function formatUsd(n: number | null) {
  if (n == null) return "—";
  if (n >= 1e9) return `$${(n / 1e9).toFixed(2)}B`;
  if (n >= 1e6) return `$${(n / 1e6).toFixed(2)}M`;
  return `$${n.toLocaleString()}`;
}

export const revalidate = 3600;

export default async function RankingsPage() {
  const { data: coins } = await supabase
    .from("stablecoins")
    .select("id, ticker, name, price_usd, market_cap_usd, circulating_supply, issuers(name)")
    .order("market_cap_usd", { ascending: false, nullsFirst: false });

  const totalMcap = coins?.reduce((sum, c) => sum + (c.market_cap_usd || 0), 0) ?? 0;

  return (
    <div>
      <h1 className="text-2xl font-bold mb-2">Rankings</h1>
      <p className="text-muted mb-6">Stablecoins ranked by market capitalization</p>

      <div className="space-y-3">
        {coins?.map((coin, i) => {
          const share = totalMcap > 0 && coin.market_cap_usd
            ? (coin.market_cap_usd / totalMcap) * 100
            : 0;
          const issuerName = Array.isArray(coin.issuers)
            ? coin.issuers[0]?.name
            : (coin.issuers as any)?.name;
          return (
            <Link
              key={coin.id}
              href={`/stablecoin/${coin.ticker}`}
              className="block bg-card border border-card-border rounded-lg p-4 hover:border-accent/50 transition-colors"
            >
              <div className="flex items-center justify-between mb-2">
                <div className="flex items-center gap-3">
                  <span className="text-muted text-sm w-6">{i + 1}</span>
                  <span className="font-mono font-bold text-accent">{coin.ticker}</span>
                  <span className="text-muted text-sm">{coin.name}</span>
                  {issuerName && <span className="text-xs text-muted bg-card-border/50 px-2 py-0.5 rounded">{issuerName}</span>}
                </div>
                <span className="font-mono font-bold">{formatUsd(coin.market_cap_usd)}</span>
              </div>
              {/* Market share bar */}
              <div className="w-full bg-card-border/50 rounded-full h-2">
                <div
                  className="bg-accent rounded-full h-2 transition-all"
                  style={{ width: `${Math.min(share, 100)}%` }}
                />
              </div>
              <p className="text-xs text-muted mt-1">{share.toFixed(1)}% market share</p>
            </Link>
          );
        })}
      </div>
    </div>
  );
}
