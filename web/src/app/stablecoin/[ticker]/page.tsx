import { supabase } from "@/lib/supabase";
import Link from "next/link";
import { notFound } from "next/navigation";

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

export const revalidate = 3600;

export default async function StablecoinPage({
  params,
}: {
  params: Promise<{ ticker: string }>;
}) {
  const { ticker } = await params;

  const { data: coin } = await supabase
    .from("stablecoins")
    .select("*, issuers(name, headquarters, website, regulatory_status)")
    .eq("ticker", ticker.toUpperCase())
    .single();

  if (!coin) notFound();

  // Fetch chain breakdown
  const { data: chainLinks } = await supabase
    .from("stablecoin_chains")
    .select("supply_on_chain, contract_address, chains(name, slug)")
    .eq("stablecoin_id", coin.id)
    .order("supply_on_chain", { ascending: false, nullsFirst: false });

  // Fetch recent snapshots
  const { data: snapshots } = await supabase
    .from("market_snapshots")
    .select("date, price_usd, market_cap_usd, circulating_supply, market_share_pct")
    .eq("stablecoin_id", coin.id)
    .order("date", { ascending: false })
    .limit(30);

  const issuer = Array.isArray(coin.issuers) ? coin.issuers[0] : coin.issuers;
  const totalChainSupply = chainLinks?.reduce((s, cl) => s + (cl.supply_on_chain || 0), 0) ?? 0;

  return (
    <div>
      <Link href="/" className="text-sm text-muted hover:text-foreground mb-4 inline-block">&larr; Back to overview</Link>

      <div className="flex items-baseline gap-3 mb-6">
        <h1 className="text-3xl font-bold font-mono text-accent">{coin.ticker}</h1>
        <span className="text-xl text-muted">{coin.name}</span>
      </div>

      {/* Key metrics */}
      <div className="grid grid-cols-2 sm:grid-cols-4 gap-4 mb-8">
        <div className="bg-card border border-card-border rounded-lg p-4">
          <p className="text-xs text-muted">Price</p>
          <p className="text-xl font-mono font-bold">
            {coin.price_usd != null ? `$${Number(coin.price_usd).toFixed(4)}` : "—"}
          </p>
        </div>
        <div className="bg-card border border-card-border rounded-lg p-4">
          <p className="text-xs text-muted">Market Cap</p>
          <p className="text-xl font-mono font-bold">{formatUsd(coin.market_cap_usd)}</p>
        </div>
        <div className="bg-card border border-card-border rounded-lg p-4">
          <p className="text-xs text-muted">Circulating Supply</p>
          <p className="text-xl font-mono font-bold">{formatSupply(coin.circulating_supply)}</p>
        </div>
        <div className="bg-card border border-card-border rounded-lg p-4">
          <p className="text-xs text-muted">Type</p>
          <p className="text-xl font-bold capitalize">{coin.type ?? "—"}</p>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        {/* Info */}
        <section>
          <h2 className="text-lg font-semibold mb-3">Details</h2>
          <div className="bg-card border border-card-border rounded-lg divide-y divide-card-border">
            {[
              ["Peg", coin.peg_currency?.toUpperCase()],
              ["Issuer", issuer?.name],
              ["Headquarters", issuer?.headquarters],
              ["Regulatory Status", issuer?.regulatory_status ?? coin.regulator_charter],
              ["Reserve Assets", coin.reserve_assets],
              ["Reserve Manager", coin.reserve_manager],
              ["Custodians", coin.custodians],
              ["Audit / Attestation", coin.attestation_audit],
              ["Website", coin.website],
            ]
              .filter(([, v]) => v)
              .map(([label, value]) => (
                <div key={label as string} className="flex justify-between px-4 py-2.5 text-sm">
                  <span className="text-muted">{label}</span>
                  <span className="text-right max-w-[60%]">
                    {String(value).startsWith("http") ? (
                      <a href={String(value)} target="_blank" rel="noopener noreferrer" className="text-accent hover:underline">
                        {String(value).replace(/^https?:\/\//, "")}
                      </a>
                    ) : (
                      value
                    )}
                  </span>
                </div>
              ))}
          </div>
        </section>

        {/* Chain breakdown */}
        <section>
          <h2 className="text-lg font-semibold mb-3">Chain Breakdown</h2>
          {chainLinks && chainLinks.length > 0 ? (
            <div className="bg-card border border-card-border rounded-lg overflow-hidden">
              <table className="w-full text-sm">
                <thead>
                  <tr className="border-b border-card-border text-left text-muted">
                    <th className="px-4 py-2.5">Chain</th>
                    <th className="px-4 py-2.5 text-right">Supply</th>
                    <th className="px-4 py-2.5 text-right">Share</th>
                  </tr>
                </thead>
                <tbody>
                  {chainLinks.map((cl) => {
                    const chain = Array.isArray(cl.chains) ? cl.chains[0] : cl.chains;
                    const share = totalChainSupply > 0 && cl.supply_on_chain
                      ? ((cl.supply_on_chain / totalChainSupply) * 100).toFixed(1)
                      : "—";
                    return (
                      <tr key={chain?.slug} className="border-b border-card-border/50">
                        <td className="px-4 py-2.5">{chain?.name ?? "Unknown"}</td>
                        <td className="px-4 py-2.5 text-right font-mono">{formatSupply(cl.supply_on_chain)}</td>
                        <td className="px-4 py-2.5 text-right font-mono">{share}%</td>
                      </tr>
                    );
                  })}
                </tbody>
              </table>
            </div>
          ) : (
            <p className="text-muted text-sm">No chain data available yet.</p>
          )}
        </section>
      </div>

      {/* Recent snapshots */}
      {snapshots && snapshots.length > 0 && (
        <section className="mt-8">
          <h2 className="text-lg font-semibold mb-3">Recent History (last 30 days)</h2>
          <div className="bg-card border border-card-border rounded-lg overflow-x-auto">
            <table className="w-full text-sm">
              <thead>
                <tr className="border-b border-card-border text-left text-muted">
                  <th className="px-4 py-2.5">Date</th>
                  <th className="px-4 py-2.5 text-right">Price</th>
                  <th className="px-4 py-2.5 text-right">Market Cap</th>
                  <th className="px-4 py-2.5 text-right">Supply</th>
                  <th className="px-4 py-2.5 text-right">Market Share</th>
                </tr>
              </thead>
              <tbody>
                {snapshots.map((s) => (
                  <tr key={s.date} className="border-b border-card-border/50">
                    <td className="px-4 py-2.5 font-mono">{s.date}</td>
                    <td className="px-4 py-2.5 text-right font-mono">
                      {s.price_usd != null ? `$${Number(s.price_usd).toFixed(4)}` : "—"}
                    </td>
                    <td className="px-4 py-2.5 text-right font-mono">{formatUsd(s.market_cap_usd)}</td>
                    <td className="px-4 py-2.5 text-right font-mono">{formatSupply(s.circulating_supply)}</td>
                    <td className="px-4 py-2.5 text-right font-mono">
                      {s.market_share_pct != null ? `${Number(s.market_share_pct).toFixed(2)}%` : "—"}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </section>
      )}
    </div>
  );
}
