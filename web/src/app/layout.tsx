import type { Metadata } from "next";
import Link from "next/link";
import "./globals.css";

export const metadata: Metadata = {
  title: "Stablecoin Monitor",
  description: "Real-time stablecoin market data, rankings, and chain breakdowns",
};

const navLinks = [
  { href: "/", label: "Overview" },
  { href: "/rankings", label: "Rankings" },
  { href: "/by-type", label: "By Type" },
  { href: "/solana-etfs", label: "Solana ETFs" },
];

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html
      lang="en"
      className="h-full antialiased"
    >
      <body className="min-h-full flex flex-col">
        <header className="border-b border-card-border bg-card/80 backdrop-blur-sm sticky top-0 z-50">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 flex items-center justify-between h-14">
            <Link href="/" className="text-lg font-bold text-accent">
              Stablecoin Monitor
            </Link>
            <nav className="flex gap-6">
              {navLinks.map((link) => (
                <Link
                  key={link.href}
                  href={link.href}
                  className="text-sm text-muted hover:text-foreground transition-colors"
                >
                  {link.label}
                </Link>
              ))}
            </nav>
          </div>
        </header>
        <main className="flex-1 max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 w-full">
          {children}
        </main>
        <footer className="border-t border-card-border py-4 text-center text-xs text-muted">
          Stablecoin data from CoinGecko &amp; DeFiLlama. ETF data from Yahoo Finance &amp; issuer sites.
        </footer>
      </body>
    </html>
  );
}
