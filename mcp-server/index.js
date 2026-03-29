import "dotenv/config";
import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { StreamableHTTPServerTransport } from "@modelcontextprotocol/sdk/server/streamableHttp.js";
import { createClient } from "@supabase/supabase-js";
import express from "express";
import { randomUUID } from "node:crypto";
import { z } from "zod";

// Config
const PORT = process.env.PORT || 3000;
const API_KEY = process.env.API_KEY || "stablecoin-monitor-key";
const SUPABASE_URL = process.env.SUPABASE_URL;
const SUPABASE_KEY = process.env.SUPABASE_SERVICE_ROLE_KEY;

if (!SUPABASE_URL || !SUPABASE_KEY) {
  console.error("Missing SUPABASE_URL or SUPABASE_SERVICE_ROLE_KEY");
  process.exit(1);
}

const supabase = createClient(SUPABASE_URL, SUPABASE_KEY);

// ── Helper ──────────────────────────────────────────────────────────
function fmt(num) {
  if (num == null) return "N/A";
  if (num >= 1e9) return `$${(num / 1e9).toFixed(1)}B`;
  if (num >= 1e6) return `$${(num / 1e6).toFixed(1)}M`;
  return `$${num.toLocaleString()}`;
}

// ── MCP Server ──────────────────────────────────────────────────────
function createMcpServer() {
  const server = new McpServer({
    name: "stablecoin-monitor",
    version: "1.0.0",
  });

  // ─── Tool: get_market_overview ───────────────────────────────────
  server.tool(
    "get_market_overview",
    "Get a high-level overview of the stablecoin market: total market cap, number of coins/issuers, and top 5 by market cap.",
    {},
    async () => {
      const { data: coins } = await supabase
        .from("stablecoins")
        .select("ticker, name, market_cap_usd, type, issuer_id")
        .order("market_cap_usd", { ascending: false });

      const { data: issuers } = await supabase
        .from("issuers")
        .select("id");

      const totalMcap = coins.reduce((s, c) => s + (c.market_cap_usd || 0), 0);
      const top5 = coins.slice(0, 5);

      const overview = {
        total_market_cap_usd: totalMcap,
        total_market_cap_formatted: fmt(totalMcap),
        num_stablecoins: coins.length,
        num_issuers: issuers.length,
        top_5: top5.map((c, i) => ({
          rank: i + 1,
          ticker: c.ticker,
          name: c.name,
          market_cap_usd: c.market_cap_usd,
          market_cap_formatted: fmt(c.market_cap_usd),
          market_share_pct: totalMcap > 0
            ? ((c.market_cap_usd / totalMcap) * 100).toFixed(1) + "%"
            : "N/A",
        })),
      };

      return {
        content: [{ type: "text", text: JSON.stringify(overview, null, 2) }],
      };
    }
  );

  // ─── Tool: query_stablecoins ─────────────────────────────────────
  server.tool(
    "query_stablecoins",
    "Search and filter stablecoins by type, issuer, peg currency, chain, or market cap range. Returns matching coins with current market data.",
    {
      type: z.string().optional().describe("Filter by type: fiat-backed, crypto-backed, synthetic, etc."),
      issuer: z.string().optional().describe("Filter by issuer name (partial match)"),
      peg: z.string().optional().describe("Filter by peg currency: USD, EUR, etc."),
      chain: z.string().optional().describe("Filter by blockchain name: Ethereum, Solana, etc."),
      min_mcap: z.number().optional().describe("Minimum market cap in USD"),
      max_mcap: z.number().optional().describe("Maximum market cap in USD"),
    },
    async (args) => {
      let query = supabase
        .from("stablecoins")
        .select("*, issuers(name)")
        .order("market_cap_usd", { ascending: false });

      if (args.type) query = query.ilike("type", `%${args.type}%`);
      if (args.peg) query = query.ilike("peg_currency", `%${args.peg}%`);
      if (args.min_mcap) query = query.gte("market_cap_usd", args.min_mcap);
      if (args.max_mcap) query = query.lte("market_cap_usd", args.max_mcap);

      let { data: coins } = await query;

      // Filter by issuer name if provided
      if (args.issuer) {
        const issuerLower = args.issuer.toLowerCase();
        coins = coins.filter(
          (c) => c.issuers?.name?.toLowerCase().includes(issuerLower)
        );
      }

      // Filter by chain if provided
      if (args.chain) {
        const { data: chainRow } = await supabase
          .from("chains")
          .select("id")
          .ilike("name", `%${args.chain}%`)
          .single();

        if (chainRow) {
          const { data: links } = await supabase
            .from("stablecoin_chains")
            .select("stablecoin_id")
            .eq("chain_id", chainRow.id);

          const ids = new Set(links.map((l) => l.stablecoin_id));
          coins = coins.filter((c) => ids.has(c.id));
        }
      }

      const results = coins.map((c) => ({
        ticker: c.ticker,
        name: c.name,
        type: c.type,
        peg: c.peg_currency,
        issuer: c.issuers?.name,
        market_cap: fmt(c.market_cap_usd),
        market_cap_usd: c.market_cap_usd,
      }));

      return {
        content: [
          {
            type: "text",
            text: `Found ${results.length} stablecoin(s):\n${JSON.stringify(results, null, 2)}`,
          },
        ],
      };
    }
  );

  // ─── Tool: get_stablecoin_detail ─────────────────────────────────
  server.tool(
    "get_stablecoin_detail",
    "Get full details for a specific stablecoin by ticker, including issuer info, chain deployments, reserves, custodians, and regulatory status.",
    {
      ticker: z.string().describe("Stablecoin ticker, e.g. USDT, USDC, PYUSD"),
    },
    async ({ ticker }) => {
      const { data: coin } = await supabase
        .from("stablecoins")
        .select("*, issuers(*)")
        .ilike("ticker", ticker)
        .single();

      if (!coin) {
        return {
          content: [{ type: "text", text: `Stablecoin "${ticker}" not found.` }],
        };
      }

      // Get chains
      const { data: chainLinks } = await supabase
        .from("stablecoin_chains")
        .select("chains(name, slug)")
        .eq("stablecoin_id", coin.id);

      const chains = chainLinks?.map((l) => l.chains.name) || [];

      // Get recent snapshots
      const { data: snapshots } = await supabase
        .from("market_snapshots")
        .select("*")
        .eq("stablecoin_id", coin.id)
        .order("date", { ascending: false })
        .limit(7);

      const detail = {
        ticker: coin.ticker,
        name: coin.name,
        type: coin.type,
        peg_currency: coin.peg_currency,
        market_cap: fmt(coin.market_cap_usd),
        market_cap_usd: coin.market_cap_usd,
        circulating_supply: coin.circulating_supply,
        reserve_assets: coin.reserve_assets,
        reserve_manager: coin.reserve_manager,
        custodians: coin.custodians,
        attestation_audit: coin.attestation_audit,
        regulator_charter: coin.regulator_charter,
        third_party_issuance: coin.third_party_issuance,
        sponsor: coin.sponsor,
        description: coin.description,
        issuer: coin.issuers
          ? { name: coin.issuers.name, website: coin.issuers.website }
          : null,
        chains,
        recent_snapshots: snapshots || [],
      };

      return {
        content: [{ type: "text", text: JSON.stringify(detail, null, 2) }],
      };
    }
  );

  // ─── Tool: compare_stablecoins ───────────────────────────────────
  server.tool(
    "compare_stablecoins",
    "Compare 2-5 stablecoins side by side on market cap, type, chains, reserves, custodians, and regulatory status.",
    {
      tickers: z
        .array(z.string())
        .min(2)
        .max(5)
        .describe("Array of tickers to compare, e.g. ['USDT', 'USDC']"),
    },
    async ({ tickers }) => {
      const comparisons = [];

      for (const ticker of tickers) {
        const { data: coin } = await supabase
          .from("stablecoins")
          .select("*, issuers(name)")
          .ilike("ticker", ticker)
          .single();

        if (!coin) {
          comparisons.push({ ticker, error: "Not found" });
          continue;
        }

        const { data: chainLinks } = await supabase
          .from("stablecoin_chains")
          .select("chains(name)")
          .eq("stablecoin_id", coin.id);

        comparisons.push({
          ticker: coin.ticker,
          name: coin.name,
          issuer: coin.issuers?.name,
          type: coin.type,
          peg: coin.peg_currency,
          market_cap: fmt(coin.market_cap_usd),
          market_cap_usd: coin.market_cap_usd,
          chains: chainLinks?.map((l) => l.chains.name) || [],
          num_chains: chainLinks?.length || 0,
          reserve_assets: coin.reserve_assets,
          custodians: coin.custodians,
          regulator: coin.regulator_charter,
          attestation: coin.attestation_audit,
        });
      }

      return {
        content: [
          {
            type: "text",
            text: JSON.stringify(comparisons, null, 2),
          },
        ],
      };
    }
  );

  // ─── Tool: get_chain_breakdown ───────────────────────────────────
  server.tool(
    "get_chain_breakdown",
    "Get which blockchains a stablecoin is deployed on. If no ticker given, shows all chain-stablecoin mappings.",
    {
      ticker: z.string().optional().describe("Stablecoin ticker. If omitted, returns all."),
    },
    async ({ ticker }) => {
      if (ticker) {
        const { data: coin } = await supabase
          .from("stablecoins")
          .select("id, ticker, name")
          .ilike("ticker", ticker)
          .single();

        if (!coin) {
          return {
            content: [{ type: "text", text: `Stablecoin "${ticker}" not found.` }],
          };
        }

        const { data: links } = await supabase
          .from("stablecoin_chains")
          .select("chains(name), supply_on_chain")
          .eq("stablecoin_id", coin.id);

        return {
          content: [
            {
              type: "text",
              text: JSON.stringify(
                {
                  ticker: coin.ticker,
                  name: coin.name,
                  chains: links.map((l) => ({
                    chain: l.chains.name,
                    supply_on_chain: l.supply_on_chain,
                  })),
                },
                null,
                2
              ),
            },
          ],
        };
      }

      // All chains summary
      const { data: chains } = await supabase.from("chains").select("id, name");
      const { data: links } = await supabase
        .from("stablecoin_chains")
        .select("chain_id, stablecoins(ticker)");

      const chainMap = {};
      for (const ch of chains) chainMap[ch.id] = { name: ch.name, coins: [] };
      for (const l of links) {
        if (chainMap[l.chain_id]) chainMap[l.chain_id].coins.push(l.stablecoins.ticker);
      }

      const result = Object.values(chainMap)
        .map((ch) => ({ chain: ch.name, stablecoins: ch.coins, count: ch.coins.length }))
        .sort((a, b) => b.count - a.count);

      return {
        content: [{ type: "text", text: JSON.stringify(result, null, 2) }],
      };
    }
  );

  // ─── Tool: get_market_trends ─────────────────────────────────────
  server.tool(
    "get_market_trends",
    "Get historical market data and trends for a stablecoin over a given period. Requires market_snapshots data (populated by the ingestion pipeline).",
    {
      ticker: z.string().describe("Stablecoin ticker"),
      period: z.enum(["7d", "30d", "90d"]).describe("Time period to look back"),
    },
    async ({ ticker, period }) => {
      const { data: coin } = await supabase
        .from("stablecoins")
        .select("id, ticker, name, market_cap_usd")
        .ilike("ticker", ticker)
        .single();

      if (!coin) {
        return {
          content: [{ type: "text", text: `Stablecoin "${ticker}" not found.` }],
        };
      }

      const days = { "7d": 7, "30d": 30, "90d": 90 }[period];
      const since = new Date();
      since.setDate(since.getDate() - days);

      const { data: snapshots } = await supabase
        .from("market_snapshots")
        .select("*")
        .eq("stablecoin_id", coin.id)
        .gte("date", since.toISOString().split("T")[0])
        .order("date", { ascending: true });

      if (!snapshots || snapshots.length === 0) {
        return {
          content: [
            {
              type: "text",
              text: `No historical data yet for ${ticker}. The ingestion pipeline needs to run to accumulate market_snapshots. Current market cap: ${fmt(coin.market_cap_usd)}.`,
            },
          ],
        };
      }

      const first = snapshots[0];
      const last = snapshots[snapshots.length - 1];
      const mcapChange = last.market_cap_usd - first.market_cap_usd;
      const mcapChangePct =
        first.market_cap_usd > 0
          ? ((mcapChange / first.market_cap_usd) * 100).toFixed(2)
          : null;

      return {
        content: [
          {
            type: "text",
            text: JSON.stringify(
              {
                ticker: coin.ticker,
                period,
                data_points: snapshots.length,
                start_date: first.date,
                end_date: last.date,
                start_mcap: fmt(first.market_cap_usd),
                end_mcap: fmt(last.market_cap_usd),
                change_usd: fmt(mcapChange),
                change_pct: mcapChangePct ? `${mcapChangePct}%` : "N/A",
                trend: mcapChange > 0 ? "growing" : mcapChange < 0 ? "declining" : "flat",
                snapshots,
              },
              null,
              2
            ),
          },
        ],
      };
    }
  );

  // ─── Tool: get_top_movers ────────────────────────────────────────
  server.tool(
    "get_top_movers",
    "Get stablecoins ranked by market cap. Since real-time 24h change requires the ingestion pipeline, this currently ranks by absolute market cap.",
    {
      limit: z.number().optional().default(10).describe("Number of results (default 10)"),
      direction: z.enum(["top", "bottom"]).optional().default("top").describe("'top' for largest, 'bottom' for smallest"),
    },
    async ({ limit, direction }) => {
      const { data: coins } = await supabase
        .from("stablecoins")
        .select("ticker, name, market_cap_usd, type")
        .order("market_cap_usd", { ascending: direction === "bottom" })
        .limit(limit);

      return {
        content: [
          {
            type: "text",
            text: JSON.stringify(
              coins.map((c, i) => ({
                rank: i + 1,
                ticker: c.ticker,
                name: c.name,
                market_cap: fmt(c.market_cap_usd),
                type: c.type,
              })),
              null,
              2
            ),
          },
        ],
      };
    }
  );

  // ─── Tool: list_alerts ───────────────────────────────────────────
  server.tool(
    "list_alerts",
    "List all active monitoring alerts.",
    {},
    async () => {
      const { data: alerts } = await supabase
        .from("alerts")
        .select("*, stablecoins(ticker, name)")
        .eq("is_active", true)
        .order("created_at", { ascending: false });

      if (!alerts || alerts.length === 0) {
        return {
          content: [{ type: "text", text: "No active alerts." }],
        };
      }

      return {
        content: [
          {
            type: "text",
            text: JSON.stringify(
              alerts.map((a) => ({
                id: a.id,
                stablecoin: a.stablecoins?.ticker,
                condition: a.condition_type,
                threshold: a.threshold_value,
                created_at: a.created_at,
                last_triggered: a.last_triggered_at,
              })),
              null,
              2
            ),
          },
        ],
      };
    }
  );

  // ─── Tool: create_alert ──────────────────────────────────────────
  server.tool(
    "create_alert",
    "Create a monitoring alert for a stablecoin. Conditions: mcap_below, mcap_above, share_change, depeg.",
    {
      ticker: z.string().describe("Stablecoin ticker"),
      condition_type: z
        .enum(["mcap_below", "mcap_above", "share_change", "depeg"])
        .describe("Alert condition type"),
      threshold_value: z
        .number()
        .describe("Threshold value (e.g. 40000000000 for $40B market cap)"),
    },
    async ({ ticker, condition_type, threshold_value }) => {
      const { data: coin } = await supabase
        .from("stablecoins")
        .select("id, ticker")
        .ilike("ticker", ticker)
        .single();

      if (!coin) {
        return {
          content: [{ type: "text", text: `Stablecoin "${ticker}" not found.` }],
        };
      }

      const { data: alert, error } = await supabase
        .from("alerts")
        .insert({
          stablecoin_id: coin.id,
          condition_type,
          threshold_value,
        })
        .select()
        .single();

      if (error) {
        return {
          content: [{ type: "text", text: `Error creating alert: ${error.message}` }],
        };
      }

      return {
        content: [
          {
            type: "text",
            text: `Alert created (ID: ${alert.id}): ${condition_type} ${fmt(threshold_value)} for ${coin.ticker}.`,
          },
        ],
      };
    }
  );

  // ─── Tool: delete_alert ──────────────────────────────────────────
  server.tool(
    "delete_alert",
    "Delete a monitoring alert by ID.",
    {
      alert_id: z.number().describe("The alert ID to delete"),
    },
    async ({ alert_id }) => {
      const { error } = await supabase
        .from("alerts")
        .delete()
        .eq("id", alert_id);

      if (error) {
        return {
          content: [{ type: "text", text: `Error deleting alert: ${error.message}` }],
        };
      }

      return {
        content: [{ type: "text", text: `Alert ${alert_id} deleted.` }],
      };
    }
  );

  // ─── Tool: get_news ──────────────────────────────────────────────
  server.tool(
    "get_news",
    "Get recent news items, optionally filtered by stablecoin ticker.",
    {
      ticker: z.string().optional().describe("Filter news by stablecoin ticker"),
      limit: z.number().optional().default(10).describe("Number of news items (default 10)"),
    },
    async ({ ticker, limit }) => {
      let query = supabase
        .from("news_items")
        .select("*")
        .order("published_at", { ascending: false })
        .limit(limit);

      const { data: news } = await query;

      if (!news || news.length === 0) {
        return {
          content: [
            {
              type: "text",
              text: "No news items yet. News ingestion will be set up in a future phase.",
            },
          ],
        };
      }

      // Filter by ticker if provided
      let filtered = news;
      if (ticker) {
        const { data: coin } = await supabase
          .from("stablecoins")
          .select("id")
          .ilike("ticker", ticker)
          .single();

        if (coin) {
          filtered = news.filter(
            (n) => n.stablecoin_ids && n.stablecoin_ids.includes(coin.id)
          );
        }
      }

      return {
        content: [
          {
            type: "text",
            text: JSON.stringify(
              filtered.map((n) => ({
                title: n.title,
                source: n.source,
                url: n.url,
                published: n.published_at,
              })),
              null,
              2
            ),
          },
        ],
      };
    }
  );

  return server;
}

// ── Express HTTP Server ─────────────────────────────────────────────
const app = express();

// API key auth middleware
app.use("/mcp", (req, res, next) => {
  const key = req.headers["x-api-key"] || req.query.api_key;
  if (key !== API_KEY) {
    return res.status(401).json({ error: "Invalid API key" });
  }
  next();
});

// Health check
app.get("/health", (req, res) => {
  res.json({ status: "ok", service: "stablecoin-monitor-mcp" });
});

// Store transports by session
const transports = new Map();

app.all("/mcp", async (req, res) => {
  const sessionId = req.headers["mcp-session-id"];

  if (sessionId && transports.has(sessionId)) {
    // Existing session
    const { transport } = transports.get(sessionId);
    await transport.handleRequest(req, res, req.body);
  } else if (!sessionId) {
    // New session (initialize request has no session ID)
    const mcpServer = createMcpServer();
    const transport = new StreamableHTTPServerTransport({
      sessionIdGenerator: () => randomUUID(),
    });

    transport.onclose = () => {
      if (transport.sessionId) {
        transports.delete(transport.sessionId);
      }
    };

    await mcpServer.connect(transport);
    await transport.handleRequest(req, res, req.body);

    // After handling, the transport now has a session ID
    if (transport.sessionId) {
      transports.set(transport.sessionId, { transport, server: mcpServer });
    }
  } else {
    res.status(404).json({ error: "Session not found. Send an initialize request first." });
  }
});

app.listen(PORT, "0.0.0.0", () => {
  console.log(`Stablecoin Monitor MCP server running on port ${PORT}`);
  console.log(`Health: http://localhost:${PORT}/health`);
  console.log(`MCP endpoint: http://localhost:${PORT}/mcp`);
});
