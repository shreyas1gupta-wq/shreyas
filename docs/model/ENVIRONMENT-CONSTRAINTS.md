# Environment constraints (verified 2026-08-28)

Findings from directly probing this remote session's network. These are facts about
where the system can be *built and run*, not design choices.

## Outbound network is allowlisted — no market data can be fetched from this session

Every external data host tested returns `403` at the egress proxy's CONNECT stage
(an organisation egress policy denial, not a transient failure or a TLS problem):

| Host | Result |
|---|---|
| `nsearchives.nseindia.com` | 403 CONNECT denied |
| `www.nseindia.com` | 403 CONNECT denied |
| `www.bseindia.com` | 403 CONNECT denied |
| `fred.stlouisfed.org` | 403 CONNECT denied |
| `api.worldbank.org` | 403 CONNECT denied |
| `data.rbi.org.in` | 403 CONNECT denied |
| `query1.finance.yahoo.com` | 403 CONNECT denied |
| `stooq.com` | 403 CONNECT denied |
| `huggingface.co` | 403 CONNECT denied |
| `www.kaggle.com` | 403 CONNECT denied |
| `data.bis.org` | 403 CONNECT denied |
| `ourworldindata.org` | 403 CONNECT denied |

Reachable from here: PyPI, npm, crates.io, GitHub, and the Anthropic APIs. Web *search*
works (it runs Anthropic-side, not through this egress path), so facts can be verified
and documentation read — but **bulk data cannot be downloaded here**.

### Consequence for the build

The data ingestion layer must run on the owner's own machine, not in a Claude Code
remote session. That splits the project cleanly, and the split is a reasonable one:

- **In this repo / this session:** all code, config, the cycle and signal registries,
  the backtester, the signal library, the optimizer, the risk engine, and the tests.
  Everything is developed against fixtures and synthetic or committed sample data.
- **On the owner's machine:** the scrapers and downloaders run, populating a local
  bitemporal store. The store is not committed (see `.gitignore`).

This makes one design requirement non-negotiable rather than merely good practice:
**every module must be testable without live data.** Signals are computed from a
`DataSource` interface, and the test suite runs against committed fixture files. If a
module can only be exercised by hitting NSE, it cannot be developed here at all.

It also means the ingestion code is written here but **first executed by the owner**, so
it needs to be unusually defensive: explicit rate limiting, resumable downloads,
integrity checks on every file, and clear failure messages. A scraper that is debugged
interactively is cheap; one that must be debugged over a chat round-trip is not.

## Verified data-availability facts

- NSE daily bhavcopy archives are freely downloadable and, per existing open-source
  projects that assemble them, go back to **January 1994** for NSE and **January 2007**
  for BSE. That is a longer usable price history than assumed, and it is enough to cover
  roughly 2-3 credit cycles.
  Sources: [bhav-copy](https://github.com/riyaz-ali/bhav-copy),
  [NSE all-reports](https://www.nseindia.com/all-reports),
  [nser R package](https://cran.r-project.org/web/packages/nser/nser.pdf)
- NSE's bhavcopy format changed to the "udiff" CSV layout in 2024; any ingester must
  handle both the legacy and current layouts, and the changeover date needs pinning.
- Note that price history being available is *not* the same as a survivorship-free
  universe: delisted names appear in old bhavcopies and simply stop appearing, so the
  universe has to be reconstructed as a union across all dates rather than taken from
  any current listing.

## Practical note on scraping NSE

NSE rejects requests without browser-like headers and an established cookie, which is
why naive scripts get blocked. The ingester needs a session-priming step (fetch the
homepage, keep cookies, send a real user-agent) and polite rate limiting. This is well
covered by existing open-source projects, so the ingester should follow their approach
rather than rediscover it.
