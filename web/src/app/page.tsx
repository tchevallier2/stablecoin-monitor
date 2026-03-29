import { supabase } from "@/lib/supabase";
import Link from "next/link";

function formatUsd(n: number | null) {
  if (n == null) return "—";
  if (n >= 1e9) return `$${(n / 1e9).toFixed(2)}B`;
  if (n >= 1e6) return `$${(n / 1e6).toFixed(2)}M`;
  return `$${n.toLocaleString()}`;
}

function formatSupply(n: number | null) {
  if (n == null) return "—";
  if (n >= 1e9) return `${(n / 1e9).toFixed(2)}B`;
  if (n >= 1e6) return `${(n / 1e6).toFixed(2)}M`;
  return n.toLocaleString();
}

export const revalidate = 3600; // revalidate every hour

export default async function OverviewPage() {
  const { data: coins } = await supabase
    .from("stablecoins")
    .select("id, ticker, name, type, price_usd, market_cap_usd, circulating_supply, issuers(name)")
    .order("market_cap_usd", { ascending: false, nullsFirst: false });

  const totalMcap = coins?.reduce((sum, c) => sum + (c.market_cap_usd || 0), 0) ?? 0;
  const coinCount = coins?.length ?? 0;

  return (
    <div>
      <h1 className="text-2xl font-bold mb-6">Market Overview</h1>

      {/* Summary cards */}
      <div className="grid grid-cols-1 sm:grid-cols-3 gap-4 mb-8">
        <div className="bg-card border border-card-border rounded-lg p-5">
          <p className="text-sm text-muted">Total Market Cap</p>
          <p className="text-2xl font-bold text-accent">{formatUsd(totalMcap)}</p>
        </div>
        <div className="bg-card border border-card-border rounded-lg p-5">
          <p className="text-sm text-muted">Stablecoins Tracked</p>
          <p className="text-2xl font-bold">{coinCount}</p>
        </div>
        <div className="bg-card border border-card-border rounded-lg p-5">
          <p className="text-sm text-muted">Top Stablecoin</p>
          <p className="text-2xl font-bold">{coins?.[0]?.ticker ?? "—"}</p>
        </div>
      </div>

      {/* Table */}
      <div className="bg-card border border-card-border rounded-lg overflow-hidden">
        <table className="w-full text-sm">
          <thead>
            <tr className="border-b border-card-border text-left text-muted">
              <th className="px-4 py-3">#</th>
              <th className="px-4 py-3">Ticker</th>
              <th className="px-4 py-3">Name</th>
              <th className="px-4 py-3">Issuer</th>
              <th className="px-4 py-3 text-right">Price</th>
              <th className="px-4 py-3 text-right">Market Cap</th>
              <th className="px-4 py-3 text-right">Supply</th>
              <th className="px-4 py-3 text-right">Share</th>
            </tr>
          </thead>
          <tbody>
            {coins?.map((coin, i) => {
              const share = totalMcap > 0 && coin.market_cap_usd
                ? ((coin.market_cap_usd / totalMcap) * 100).toFixed(1)
                : "—";
              const issuerName = Array.isArray(coin.issuers)
                ? coin.issuers[0]?.name
                : (coin.issuers as any)?.name;
              return (
                <tr key={coin.id} className="border-b border-card-border/50 hover:bg-card-border/20">
                  <td className="px-4 py-3 text-muted">{i + 1}</td>
                  <td className="px-4 py-3 font-mono font-bold">
                    <Link href={`/stablecoin/${coin.ticker}`} className="text-accent hover:underline">
                      {coin.ticker}
                    </Link>
                  </td>
                  <td className="px-4 py-3">{coin.name}</td>
                  <td className="px-4 py-3 text-muted">{issuerName ?? "—"}</td>
                  <td className="px-4 py-3 text-right font-mono">
                    {coin.price_usd != null ? `$${Number(coin.price_usd).toFixed(4)}` : "—"}
                  </td>
                  <td className="px-4 py-3 text-right font-mono">{formatUsd(coin.market_cap_usd)}</td>
                  <td className="px-4 py-3 text-right font-mono">{formatSupply(coin.circulating_supply)}</td>
                  <td className="px-4 py-3 text-right font-mono">{share}%</td>
                </tr>
              );
            })}
          </tbody>
        </table>
      </div>
    </div>
  );
}
