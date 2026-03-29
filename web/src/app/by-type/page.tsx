import { supabase } from "@/lib/supabase";
import Link from "next/link";

function formatUsd(n: number | null) {
  if (n == null) return "—";
  if (n >= 1e9) return `$${(n / 1e9).toFixed(2)}B`;
  if (n >= 1e6) return `$${(n / 1e6).toFixed(2)}M`;
  return `$${n.toLocaleString()}`;
}

export const revalidate = 3600;

export default async function ByTypePage() {
  const { data: coins } = await supabase
    .from("stablecoins")
    .select("id, ticker, name, type, market_cap_usd")
    .order("market_cap_usd", { ascending: false, nullsFirst: false });

  // Group by type
  const groups: Record<string, typeof coins> = {};
  for (const coin of coins ?? []) {
    const type = coin.type || "Unknown";
    if (!groups[type]) groups[type] = [];
    groups[type]!.push(coin);
  }

  // Sort groups by total market cap
  const sortedGroups = Object.entries(groups).sort((a, b) => {
    const mcapA = a[1]!.reduce((s, c) => s + (c.market_cap_usd || 0), 0);
    const mcapB = b[1]!.reduce((s, c) => s + (c.market_cap_usd || 0), 0);
    return mcapB - mcapA;
  });

  return (
    <div>
      <h1 className="text-2xl font-bold mb-2">By Type</h1>
      <p className="text-muted mb-6">Stablecoins grouped by backing mechanism</p>

      <div className="space-y-8">
        {sortedGroups.map(([type, typeCoins]) => {
          const typeMcap = typeCoins!.reduce((s, c) => s + (c.market_cap_usd || 0), 0);
          return (
            <section key={type}>
              <div className="flex items-baseline justify-between mb-3">
                <h2 className="text-lg font-semibold capitalize">{type}</h2>
                <span className="text-sm text-muted">
                  {typeCoins!.length} coin{typeCoins!.length > 1 ? "s" : ""} &middot; {formatUsd(typeMcap)} total
                </span>
              </div>
              <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-3">
                {typeCoins!.map((coin) => (
                  <Link
                    key={coin.id}
                    href={`/stablecoin/${coin.ticker}`}
                    className="bg-card border border-card-border rounded-lg p-4 hover:border-accent/50 transition-colors"
                  >
                    <div className="flex items-center justify-between">
                      <span className="font-mono font-bold text-accent">{coin.ticker}</span>
                      <span className="font-mono text-sm">{formatUsd(coin.market_cap_usd)}</span>
                    </div>
                    <p className="text-sm text-muted mt-1">{coin.name}</p>
                  </Link>
                ))}
              </div>
            </section>
          );
        })}
      </div>
    </div>
  );
}
