import { supabase } from "@/lib/supabase";

function formatUsd(n: number | null) {
  if (n == null) return "—";
  if (n >= 1e9) return `$${(n / 1e9).toFixed(2)}B`;
  if (n >= 1e6) return `$${(n / 1e6).toFixed(1)}M`;
  return `$${n.toLocaleString()}`;
}

function formatPrice(n: number | null) {
  if (n == null) return "—";
  return `$${Number(n).toFixed(2)}`;
}

export const revalidate = 1800; // 30 min

export default async function SolanaEtfsPage() {
  const { data: etfs } = await supabase
    .from("solana_etfs")
    .select("*")
    .order("aum_usd", { ascending: false, nullsFirst: false });

  const { data: filings } = await supabase
    .from("solana_etf_filings")
    .select("*")
    .order("filing_date", { ascending: true });

  const totalAum = etfs?.reduce((s, e) => s + (e.aum_usd || 0), 0) ?? 0;
  const stakingEnabled = etfs?.filter((e) => e.staking_enabled).length ?? 0;
  const etfCount = etfs?.length ?? 0;

  return (
    <div>
      {/* Header */}
      <div className="mb-6">
        <h1 className="text-2xl font-bold">
          <span className="bg-gradient-to-r from-[#9945ff] to-[#14f195] bg-clip-text text-transparent">
            US Solana ETF Dashboard
          </span>
        </h1>
        <p className="text-muted text-sm mt-1">
          All live US-listed Solana spot ETFs &amp; ETPs — sorted by AUM
        </p>
      </div>

      {/* Stats bar */}
      <div className="grid grid-cols-2 sm:grid-cols-4 gap-4 mb-6">
        <div className="bg-card border border-card-border rounded-lg p-4">
          <p className="text-xs text-muted uppercase tracking-wide">Total ETFs</p>
          <p className="text-2xl font-bold mt-1">{etfCount}</p>
        </div>
        <div className="bg-card border border-card-border rounded-lg p-4">
          <p className="text-xs text-muted uppercase tracking-wide">Total AUM</p>
          <p className="text-2xl font-bold mt-1 text-[#c490ff]">{formatUsd(totalAum)}</p>
        </div>
        <div className="bg-card border border-card-border rounded-lg p-4">
          <p className="text-xs text-muted uppercase tracking-wide">Staking-Enabled</p>
          <p className="text-2xl font-bold mt-1 text-accent-green">
            {stakingEnabled} / {etfCount}
          </p>
        </div>
        <div className="bg-card border border-card-border rounded-lg p-4">
          <p className="text-xs text-muted uppercase tracking-wide">Pending Filings</p>
          <p className="text-2xl font-bold mt-1">{filings?.length ?? 0}</p>
        </div>
      </div>

      {/* Legend */}
      <div className="flex flex-wrap gap-5 text-xs text-muted mb-4 px-1">
        <span className="flex items-center gap-1.5">
          <span className="w-2.5 h-2.5 rounded-sm bg-[rgba(153,69,255,0.5)]" />
          Staking commission active
        </span>
        <span className="flex items-center gap-1.5">
          <span className="w-2.5 h-2.5 rounded-sm bg-[rgba(63,185,80,0.3)]" />
          Staking fee waived (limited period)
        </span>
        <span className="flex items-center gap-1.5">
          <span className="w-2.5 h-2.5 rounded-sm bg-accent-green" />
          Live from Yahoo Finance
        </span>
        <span className="flex items-center gap-1.5">
          <span className="w-2.5 h-2.5 rounded-sm bg-[#d29922]" />
          Static / fallback data
        </span>
      </div>

      {/* Main ETF table */}
      <div className="bg-card border border-card-border rounded-lg overflow-x-auto mb-10">
        <table className="w-full text-sm min-w-[1100px]">
          <thead>
            <tr className="border-b border-card-border text-left text-muted text-xs uppercase tracking-wide">
              <th className="px-3 py-3">#</th>
              <th className="px-3 py-3">Ticker</th>
              <th className="px-3 py-3">Issuer</th>
              <th className="px-3 py-3">Exchange</th>
              <th className="px-3 py-3 text-right">AUM</th>
              <th className="px-3 py-3 text-right">Price</th>
              <th className="px-3 py-3">Exp. Ratio</th>
              <th className="px-3 py-3">Staking</th>
              <th className="px-3 py-3">Commission</th>
              <th className="px-3 py-3 text-right">% Staked</th>
              <th className="px-3 py-3 text-right">Gross Yield</th>
              <th className="px-3 py-3 text-right">Net Yield</th>
            </tr>
          </thead>
          <tbody>
            {etfs?.map((etf, i) => {
              const isLive = etf.price_source === "live";
              const rowBg = etf.fee_waived
                ? ""
                : "bg-[rgba(153,69,255,0.07)]";

              return (
                <tr
                  key={etf.id}
                  className={`border-b border-card-border/50 hover:bg-card-border/20 ${rowBg}`}
                  title={etf.description ?? ""}
                >
                  <td className="px-3 py-3 text-muted text-xs">{i + 1}</td>
                  <td className="px-3 py-3">
                    <span className="font-mono font-bold text-[#58a6ff]">
                      {etf.ticker}
                    </span>
                  </td>
                  <td className="px-3 py-3 font-medium">{etf.issuer}</td>
                  <td className="px-3 py-3 text-muted">{etf.exchange}</td>
                  <td className="px-3 py-3 text-right">
                    <span className={`font-semibold ${isLive ? "text-accent-green" : "text-[#d29922]"}`}>
                      {formatUsd(etf.aum_usd)}
                    </span>
                    <span className={`text-[10px] ml-1 ${isLive ? "text-accent-green" : "text-[#d29922]"}`}>
                      {isLive ? "● LIVE" : "● Static"}
                    </span>
                  </td>
                  <td className="px-3 py-3 text-right font-mono">
                    <span className={isLive ? "" : "text-[#d29922]"}>
                      {formatPrice(etf.price_usd)}
                    </span>
                  </td>
                  <td className="px-3 py-3">
                    <span className={etf.fee_waived ? "text-accent-green font-semibold" : ""}>
                      {etf.exp_ratio_current}
                    </span>
                    {etf.exp_waiver_note && (
                      <span className={`block text-[11px] mt-0.5 ${etf.fee_waived ? "text-accent-green" : "text-muted"}`}>
                        ↳ {etf.exp_waiver_note}
                      </span>
                    )}
                  </td>
                  <td className="px-3 py-3">
                    {etf.fee_waived ? (
                      <span className="inline-flex items-center gap-1 px-2 py-0.5 rounded-full text-[11px] font-semibold uppercase tracking-wide bg-[rgba(63,185,80,0.18)] text-accent-green border border-[rgba(63,185,80,0.35)]">
                        ✓ Waived
                      </span>
                    ) : (
                      <span className="inline-flex items-center gap-1 px-2 py-0.5 rounded-full text-[11px] font-semibold uppercase tracking-wide bg-[rgba(153,69,255,0.22)] text-[#c490ff] border border-[rgba(153,69,255,0.38)]">
                        ✓ Active
                      </span>
                    )}
                  </td>
                  <td className="px-3 py-3">
                    <span className={etf.fee_waived ? "text-accent-green font-semibold" : ""}>
                      {etf.commission_current ?? "N/A"}
                    </span>
                    {etf.commission_note && (
                      <span className={`block text-[11px] mt-0.5 ${etf.fee_waived ? "text-accent-green" : "text-muted"}`}>
                        ↳ {etf.commission_note}
                      </span>
                    )}
                  </td>
                  <td className="px-3 py-3 text-right">
                    {etf.pct_staked === "N/A" ? (
                      <span className="text-muted" title="Not publicly disclosed by issuer">
                        N/A <span className="cursor-help">ⓘ</span>
                      </span>
                    ) : (
                      <span className="text-accent-green font-semibold">{etf.pct_staked}</span>
                    )}
                  </td>
                  <td className="px-3 py-3 text-right font-semibold text-accent-green">
                    {etf.gross_yield ?? "—"}
                  </td>
                  <td className="px-3 py-3 text-right font-semibold text-accent-green">
                    {etf.net_yield ?? "—"}
                  </td>
                </tr>
              );
            })}
          </tbody>
        </table>
      </div>

      {/* Upcoming Filings */}
      <h2 className="text-xl font-bold mb-4">Upcoming Filings</h2>
      <p className="text-muted text-sm mb-4">
        Pending SEC filings for Solana spot ETFs not yet trading
      </p>

      {filings && filings.length > 0 ? (
        <div className="bg-card border border-card-border rounded-lg overflow-x-auto">
          <table className="w-full text-sm min-w-[800px]">
            <thead>
              <tr className="border-b border-card-border text-left text-muted text-xs uppercase tracking-wide">
                <th className="px-4 py-3">Issuer</th>
                <th className="px-4 py-3">ETF Name</th>
                <th className="px-4 py-3">Proposed Ticker</th>
                <th className="px-4 py-3">Filing Type</th>
                <th className="px-4 py-3">Status</th>
                <th className="px-4 py-3">Filing Date</th>
                <th className="px-4 py-3">Deadline</th>
                <th className="px-4 py-3">Staking</th>
                <th className="px-4 py-3">Notes</th>
              </tr>
            </thead>
            <tbody>
              {filings.map((f) => (
                <tr key={f.id} className="border-b border-card-border/50 hover:bg-card-border/20">
                  <td className="px-4 py-3 font-medium">{f.issuer}</td>
                  <td className="px-4 py-3">{f.etf_name}</td>
                  <td className="px-4 py-3 font-mono text-[#58a6ff]">
                    {f.ticker_proposed ?? "TBD"}
                  </td>
                  <td className="px-4 py-3">
                    <span className="bg-card-border/50 px-2 py-0.5 rounded text-xs font-medium">
                      {f.filing_type}
                    </span>
                  </td>
                  <td className="px-4 py-3">
                    <FilingStatusBadge status={f.status} />
                  </td>
                  <td className="px-4 py-3 font-mono text-xs">
                    {f.filing_date ?? "—"}
                  </td>
                  <td className="px-4 py-3 font-mono text-xs">
                    {f.decision_deadline ?? "—"}
                  </td>
                  <td className="px-4 py-3">
                    {f.staking_included === true ? (
                      <span className="text-accent-green text-xs font-semibold">Yes</span>
                    ) : f.staking_included === false ? (
                      <span className="text-accent-red text-xs">No</span>
                    ) : (
                      <span className="text-muted text-xs">TBD</span>
                    )}
                  </td>
                  <td className="px-4 py-3 text-muted text-xs max-w-[250px] truncate" title={f.notes ?? ""}>
                    {f.notes ?? "—"}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      ) : (
        <p className="text-muted text-sm">No pending filings.</p>
      )}

      {/* Footer note */}
      <div className="mt-8 text-xs text-muted leading-relaxed border-t border-card-border pt-4">
        <strong className="text-foreground">Data sources:</strong> AUM &amp; price from Yahoo Finance API.
        Staking data sourced from issuer websites (Bitwise, Grayscale, 21Shares, VanEck, Fidelity, Canary Capital).
        Refreshed twice daily (8 AM &amp; 5 PM ET).
        Filing data from SEC EDGAR.
      </div>
    </div>
  );
}

function FilingStatusBadge({ status }: { status: string }) {
  const styles: Record<string, string> = {
    filed: "bg-[rgba(88,166,255,0.15)] text-[#58a6ff] border-[rgba(88,166,255,0.3)]",
    acknowledged: "bg-[rgba(210,153,34,0.15)] text-[#d29922] border-[rgba(210,153,34,0.3)]",
    comment_period: "bg-[rgba(210,153,34,0.15)] text-[#d29922] border-[rgba(210,153,34,0.3)]",
    effective: "bg-[rgba(63,185,80,0.15)] text-accent-green border-[rgba(63,185,80,0.3)]",
    approved: "bg-[rgba(63,185,80,0.15)] text-accent-green border-[rgba(63,185,80,0.3)]",
    withdrawn: "bg-[rgba(248,81,73,0.15)] text-accent-red border-[rgba(248,81,73,0.3)]",
  };

  const style = styles[status] ?? styles.filed;
  const label = status.replace(/_/g, " ");

  return (
    <span className={`inline-flex px-2 py-0.5 rounded-full text-[11px] font-semibold uppercase tracking-wide border ${style}`}>
      {label}
    </span>
  );
}
