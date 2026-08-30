# Layer 19 — Free-Data Acquisition and the Point-in-Time Pipeline

**Abstract.** Under free-sources-only this layer is the project's largest engineering workstream and the one everything else waits on: no backtest above a toy panel runs without it, and every honesty claim in layers 01–17 (`pit=true`/`pit=lag_approx`/`pit=reconstructed`) is a promise this layer keeps. The hardest problem is not acquisition but **point-in-time integrity on data published with no knowledge date** — free Indian fundamentals arrive current and restated. The fix is bitemporal from day one: every fact carries `event_date` and `knowledge_date`; forward-archiving with our own timestamps starts today, free and compounding; history before today gets a fixed, conservative, per-statement-type lag, and every backtest built on it is labelled `pit=lag_approx`, never true PIT. The second-hardest problem is survivorship: delisted and suspended names are assembled as a union across every historical bhavcopy, never a current listing, proved survivorship-free by a concrete test, not asserted. Prices, corporate actions and index membership are D1/D4 and solvable free; fundamentals are D2 and carry an estimated **+100–150bps/yr restatement bias on top of the measured 150–300bps/yr survivorship bias** — a combined ~250–450bps/yr inflation risk on any fundamentals-heavy backtest. Parquet + DuckDB is the storage answer at this scale (≈5.6M price rows, single-machine-sized), with an ASOF-join query layer making look-ahead structurally hard, not merely discouraged. Every registry indicator resolves against a committed fixture so the layer runs with zero live data, per `ENVIRONMENT-CONSTRAINTS.md`. MVP effort: **~50 person-days**; full inventory including Stage-2 text sources: **~68**. Owns raw ingestion, the bitemporal store, corporate-action adjustment, symbol mastering, index-membership reconstruction; does **not** own factor construction (L09), execution cost or liquidity-derived investable universes (L15), or the risk/cash-call model (L17) — those are being written concurrently and consume this layer's interface only.

---

## 1. Scope and the interface boundary

**Owns.** Raw acquisition from every named free source; the bitemporal store; corporate-action adjustment arithmetic; ISIN-anchored symbol mastering; survivorship-free universe reconstruction; index-membership reconstruction; forward-archiving; the backward lag policy; ingestion orchestration/validation/quarantine; the fixture set every other layer's tests depend on.

| Belongs elsewhere | Not duplicated here |
|---|---|
| **L09 factor library** | Turning raw XBRL/price facts into value/quality/lowvol scores, sector-pool compositing, forensic thresholds. I hand L09 `pit_store` and forward-archived filings; L09 does the accounting. |
| **L15 execution & cost** | `investable_universe(book, asof)` (liquidity-filtered, per-book) and `EXEC_COST.c_j`. I supply raw ADV/price/volume; L15 derives capacity. My `universe(asof)` is the full survivorship-free listed set — a different, larger object. |
| **L17 risk engine** | `LIQUIDITY(asof)` (ADV-based days-to-liquidate), the covariance model, the cash-call engine — consumes my `adj_prices`/`macro_series` directly. |
| **L01 cycle registry** | Cycle construction, tiering, budgets. L01 consumes `macro_series`/`pit_store`; I compute no cycle signal. |
| **L16 options overlay (future)** | Option-chain interpretation, IV surfaces, hedge sizing. I supply EOD F&O bhavcopy facts only. |

No NAV moves here — every object below is a fact, not a signal.

---

## 2. The complete data inventory

### 2.1 Prices, volumes, adjusted series

| Segment | Free source | Method | History | PIT | Effort (d) |
|---|---|---|---|---|---|
| NSE equity bhavcopy, legacy CSV | `nsearchives.nseindia.com`; mirrored by the `bhav-copy` OSS project | Bulk daily download, legacy `cm<DDMMYYYY>bhav.csv` parser | 1994–2024-07 **[verify cutover]** | True, same-day | 3.0 |
| NSE equity bhavcopy, UDiFF CSV | Same host, new unified layout | New parser, same semantic fields (OHLC, qty, value, ISIN) | 2024-07– **[verify]** | True | 1.5 |
| BSE equity bhavcopy | `bseindia.com` "EQ_ISINCODE" daily zips | Bulk download, `SC_CODE` schema, joined via ISIN | 2007– | True | 2.0 |
| F&O bhavcopy (futures/options, EOD) + India VIX | NSE F&O archive, same file family | Per-contract OHLC/OI/settlement | Futures ~2000–, options ~2001–, VIX 2008– **[verify]** | True | 3.0 |
| Participant-category OI (FII/DII/Pro/Client) | NSE daily reports | Bulk download | ~2013– **[verify]** | True | 1.0 |

**Assembly rule.** NSE is primary; a `(ISIN, trade_date)` row from BSE is inserted only when NSE has no row for that ISIN that day — captures BSE-exclusive small-caps without double-booking dual-listed names, why ISIN not exchange symbol is the join key (§5). Delisted names need no separate source: they are simply a property of the union (§4).

### 2.2 Corporate actions — the adjustment arithmetic

| Type | Free source | Adjustment (applied to all prices strictly before ex-date) |
|---|---|---|
| **Bonus** `a:b` | NSE corporate-action bulletin | `factor = b/(a+b)`; `price×=factor`; `volume/=factor` |
| **Split** `F_old→F_new` | Same | `factor = F_new/F_old`, same multiplicative rule |
| **Rights** `n:m` at `P_rights`, cum-price `P_cum` | Same, cross-checked vs the letter of offer | `factor = (m·P_cum + n·P_rights) / ((m+n)·P_cum)` |
| **Dividend** (total-return series only) | Same bulletin | `factor = (P_cum − D)/P_cum`, chained backward — CRSP-style |
| **Demerger** | **Primary:** the company's own s.49(2C)/(2D) cost-of-acquisition tax circular — an authoritative, free, company-published allocation, better than inferring one from price. **Fallback:** market-cap-weighted ratio from day-1 closes of parent and spinoff | Split ratio applied as an ex-date add-back so a continuously-held position compounds invariantly through the restructuring |

All five write to `corporate_actions` (DDL §3) with `source ∈ {NSE_circular, company_tax_circular, price_ratio_estimate}` — demerger fallbacks are flagged and revisited if an official circular later surfaces. **Golden-file test per type**: a 4–6 row fixture with a known-by-construction adjusted series; CI asserts exact reproduction.

### 2.3 Index membership — Nifty Total Market reconstruction

**Source.** NSE index-reconstitution circulars (semi-annual, additions/deletions with an effective date). NSE's own **Nifty Total Market Index** (≈750 names, launched **2017 [verify]**) is close to a direct NIFTY 750 proxy going forward; pre-2017, the union of **Nifty 500 + Smallcap 250 + Microcap 250** approximates it.

**Method.** Parse every circular into `(index_code, isin, add|delete, effective_date)`, build a piecewise-constant per-index membership timeline (§3 DDL). Structured archiving is reliable from **~2005**; before that, circulars are scanned PDFs of inconsistent format.

**Accuracy.** From 2005: high — each reconstitution is discrete, dated, ~30–60 names, locally correctable. Pre-2005: validated by **replication** — reconstruct a value-weighted return from recovered membership/weights, compare to the published TRI; rolling-12m divergence **>20pp** flags the window for repair (same tolerance L09 uses for its IIM-A reconciliation). Effort: **4.0d**.

### 2.4 Fundamentals, shareholding, governance

| Object | Free route | History | PIT | Effort (d) |
|---|---|---|---|---|
| Quarterly/annual P&L, standalone+consol. | NSE/BSE XBRL (Reg 33/34) | XBRL ~2017–; PDF to ~2001, degraded | Restated — **imposed lag, §3c** | 4.0 |
| Balance sheet + cash flow | Half-yearly (Reg 33) + annual audited | 2001– annual; half-yearly **~2019– [verify]** | Restated | (above) |
| Bulk fundamentals, secondary | Kaggle/HuggingFace scrapes | 10–15y, ~4,000–4,500 names | **Unverified**, survivorship/PIT-contaminated; gap-filler only | 1.5 |
| Free-float market cap | Shareholding pattern (Reg 31) × price | 2001– | Deadline 21d; **imposed = quarter_end+30d** | — |
| Promoter pledge | Reg 31 | 2009– | Same | 2.0 |
| Insider trading / auditor events | Reg 29/30 disclosures | 2016– | **True PIT, ~24h** — cleanest data here | 1.5 |
| Sector classification | niftyindices factsheets | Current only; history D4 | Current-as-of-today | (§2.3) |

XBRL tags are **not standardised before ~2019**, so a tag-mapping layer (not a fixed dictionary) is required — the single most engineering-heavy item here.

### 2.5 Annual reports and concall transcripts (Stage-2 feed)

| Object | Free route | History | Effort (d) |
|---|---|---|---|
| Annual reports (PDF) | BSE/NSE filings archive; company IR pages fallback | ~2001–, patchy pre-2010 | 2.5 |
| Concall transcripts | Company IR pages — ~750 heterogeneous sites, no common schema | Post-2015 for most large/mid caps | 2.5 |

Highest-variance item in the inventory (no single template fits 750 companies); **explicitly deferred to Stage 2** (post week 24) — feeds no Stage-1 signal.

### 2.6 Macro, gold, G-Sec curve

| Object | Free source | History | PIT |
|---|---|---|---|
| Policy rate, LAF, USDINR, savings | RBI DBIE | 1996–2004 typical start | True (D1) / lag_approx |
| GDP/GVA, IIP, CPI, WPI | MOSPI | GDP 1996, IIP 1994, CPI 2011, WPI 1994 | lag_approx, 12–60d |
| GST collections | GST portal | 2017– | True, ~1–3d |
| Credit-to-GDP gap (published vintage) | BIS | India 1951– | True, ~120–150d **[registry inconsistency, §12]** |
| WEO/IFS/COFER | IMF | 1980s– | lag_approx/true |
| Commodities (Pink Sheet), WDI | World Bank | 1960– | lag_approx |
| US rates/inflation, vintaged | FRED **ALFRED** | 1960s– | **True vintage** |
| Long-run cross-country panel | Jordà–Schularick–Taylor, `macrohistory.net` | 18 countries, 1870– | True (static) |
| US equity CAPE/rates | Shiller (own site) | 1871– | True |
| Historical GDP/FX/inflation | MeasuringWorth | Multi-century | True |
| Long-run global series | Our World in Data | Mostly Maddison-sourced | True |
| Gold, USD | FRED (LBMA fixing) | 1968– | True |
| Gold, INR futures | MCX bhavcopy | ~2003– | True |
| Gold demand/CB purchases | World Gold Council Goldhub | ~2000– | True, quarterly |
| G-Sec yield curve | CCIL, published ZCYC — use as-is, don't refit | ~1999–2005 by tenor **[verify]** | True |

**MVP macro batch (§9): 3.0d** for the subset the 14 MVP cycles cite (repo rate, BIS credit gap, IIP/GDP/CPI, GST, CCIL term spread, India VIX). **Full batch beyond that: 4.0d.** Gold (FRED+MCX+WGC): **2.0d**, done early since gold sits in the neutral portfolio from day one.

---

## 3. The point-in-time problem

### 3a. Bitemporal store design

Every fact carries `event_date` (what it's about) and `knowledge_date` (when it became knowable). Prices are trivial (`knowledge_date = event_date`). Fundamentals are the hard case — multiple vintages of the "same" fact coexist.

```sql
CREATE TABLE fact_bitemporal (
  entity_id VARCHAR NOT NULL,           -- ISIN-anchored id (§5) or macro series_code
  field_code VARCHAR NOT NULL,          -- 'PAT_CONSOL', 'IIP_YOY', 'BIS_CREDIT_GAP_IND', ...
  period_end DATE NOT NULL, value DOUBLE, value_text VARCHAR,   -- non-numeric: auditor name, pledge flag
  knowledge_date DATE NOT NULL,         -- when this value became publicly known
  knowledge_date_basis VARCHAR NOT NULL CHECK (knowledge_date_basis IN ('observed','imposed_lag')),
  source VARCHAR NOT NULL, filing_id VARCHAR,        -- null if imposed
  restated_from VARCHAR,                -- filing_id this vintage supersedes, or null
  ingested_at TIMESTAMP NOT NULL,       -- forward-archive audit trail
  PRIMARY KEY (entity_id, field_code, period_end, knowledge_date)
);

CREATE TABLE prices_daily (
  entity_id VARCHAR NOT NULL, exchange VARCHAR NOT NULL CHECK (exchange IN ('NSE','BSE')),
  trade_date DATE NOT NULL, open DOUBLE, high DOUBLE, low DOUBLE, close DOUBLE,
  volume BIGINT, delivery_volume BIGINT,
  adj_factor_cum DOUBLE NOT NULL DEFAULT 1.0,        -- cumulative corp-action factor
  isin VARCHAR NOT NULL, source_file VARCHAR NOT NULL, ingested_at TIMESTAMP NOT NULL,
  PRIMARY KEY (entity_id, exchange, trade_date)
);

CREATE TABLE corporate_actions (
  entity_id VARCHAR NOT NULL,
  action_type VARCHAR NOT NULL CHECK (action_type IN ('bonus','split','rights','dividend','demerger')),
  ex_date DATE NOT NULL, record_date DATE,
  ratio_num DOUBLE, ratio_den DOUBLE, cash_amount DOUBLE,
  adjustment_factor DOUBLE NOT NULL, demerger_split_ratio DOUBLE,
  source VARCHAR NOT NULL CHECK (source IN ('NSE_circular','company_tax_circular','price_ratio_estimate')),
  knowledge_date DATE NOT NULL, ingested_at TIMESTAMP NOT NULL,
  PRIMARY KEY (entity_id, action_type, ex_date)
);

CREATE TABLE index_membership (
  index_code VARCHAR NOT NULL, entity_id VARCHAR NOT NULL,
  effective_from DATE NOT NULL, effective_to DATE,   -- NULL = still a member
  weight_pct DOUBLE, source_circular VARCHAR NOT NULL, knowledge_date DATE NOT NULL,
  PRIMARY KEY (index_code, entity_id, effective_from)
);
```

### 3b. Forward-archiving — starts today, compounds free

From 2026-08-30 forward, every filing, macro release and index circular is snapshotted with `knowledge_date_basis='observed'`, `restated_from` chaining each vintage to what it superseded. This costs nothing beyond ingestion already required, and is the only route to genuinely PIT Indian fundamentals for free. By 2028 this is a real, if short, panel; L09 §3's `restatement_delta` metric is defined to consume it. Mechanics: on every re-ingest, diff against the last-seen value per `(entity_id, field_code, period_end)`; a change inserts a new row. **Must start day one** — a month not archived cannot be recovered.

### 3c. Backward approximation — the fixed lag table

History before today gets `knowledge_date_basis='imposed_lag'` with a fixed, conservative lag. Consumed identically by L09 (§6.3) and by every macro-citing cycle in `config/cycle_registry.yaml`:

| Statement type | LODR deadline | **Imposed lag** |
|---|---|---|
| Q1–Q3 results | 45 days | `period_end + 60` days |
| Q4 / annual audited | 60 days | `period_end + 90` days |
| Half-yearly BS + cash flow | with H1/annual | `+75` / `+105` days |
| Shareholding pattern, pledge | 21 days | `quarter_end + 30` days |
| Annual report (RPT, contingent, subsidiaries) | AGM ≤6mo | `FY_end + 210` days |
| Auditor resignation, qualification | 24h | `+1` day — true PIT |
| ASM/GSM, surveillance | daily | file date — true PIT |
| Macro releases | statutory calendar | 12–150 days, per source (§2.6) |

Every `imposed_lag` row propagates a `pit=lag_approx` tag to every consumer, per the standing rule in `docs/theory/02-ECONOMETRIC-METHODS.md` §5.4 — enforced at the source, not left to each consumer to remember.

### 3d. Quantified bias, and its direction

Two mechanisms, additive, not the same number.

**Timing bias — safe on average, one sharp exception.** The imposed lag uses the *maximum* legal filing window, so the backtest never sees a fact earlier than the market could have, on average. Exception: a chronic late filer beyond even the extended deadline is disproportionately a stressed small-cap — exactly what L09's forensic screens target. Safest where the book is calmest, weakest where the risk is highest.

**Restatement bias — dominant, upward.** We read today's restated value of a historical fact, not what was first reported; restatements systematically excise bad news rather than adding symmetric noise (Banz & Breen 1986; Kothari, Sabino & Zach 2005 [verify]). First-order own-estimate, pending the 2028 replay:

```
bias_bps/yr ≈ 10,000 × p_restate × mag_restate × overweight
  p_restate ≈ 0.03   (share of name-periods later materially restated)
  mag_restate ≈ 0.20 (avg |restated PAT change| among restated periods)
  overweight ≈ 1.75  (value/quality tilt over-samples distress, mirroring L09's ~2x survivorship overweight)
  ⇒ ≈ 105 bps/yr, range 50–150, ADDITIVE to L09's separately measured 150–300bps/yr
    survivorship bias — different mechanism: survivorship drops a failed name entirely;
    restatement keeps the name but overwrites its story.
```

**Combined: ~250–450bps/yr of upward inflation risk on any fundamentals-heavy backtest**, concentrated in the value/quality composite — why L09 reports a price-only book (PO-FL) alongside the fundamental book (FUND-FL) as the honest bracket, and why the forward archive (§3b) is the only way to replace this estimate with a measurement.

---

## 4. The survivorship problem

**Rule S1.** The universe at date *t* is the **union**, across every historical bhavcopy up to *t*, of every ISIN traded in the trailing 10 sessions — never a name list from a current index or listing. A delisted name stops appearing; it is not retroactively removed from earlier universes.

**Test, CI-enforced against a committed fixture:**

1. **Presence.** Hand-verified delisted names (Satyam Computer Services pre-2009, Kingfisher Airlines, Unitech, others) must appear in `universe(t)` for every `t` between listing and delisting, and be **absent** from `universe(today)`.
2. **Monotonicity.** Cumulative distinct-ISIN count of `universe(t)` is non-decreasing in *t* (union only grows); a violation is a reconstruction bug, not a shrinking market.
3. **Economic sign.** A naive "current-constituents-only" backtest of a value/small-cap strategy must beat the reconstructed-union version by a plausible, bounded amount (**~150–300bps/yr**, per L09 §3); a gap of the wrong sign, or >10x that band, fails CI.

A synthetic 30-name fixture with a known delisting subset backs all three with zero live data. Effort: **2.0d**.

---

## 5. Symbol mastering

Symbols change on renames, mergers, demergers; ISIN is more stable but not immune — a merger typically retires the absorbed entity's ISIN. Three concerns, kept separate: resolving a *raw symbol at an exchange* to a permanent entity; tracking *symbol changes on an unchanged ISIN*; tracking *entity lineage across an ISIN change*.

```sql
CREATE TABLE symbol_master (
  entity_id VARCHAR PRIMARY KEY,             -- canonical = the ISIN currently in force
  company_name_current VARCHAR, first_seen_date DATE, last_seen_date DATE,
  status VARCHAR CHECK (status IN ('active','delisted','merged','suspended'))
);

CREATE TABLE symbol_change_history (
  entity_id VARCHAR NOT NULL REFERENCES symbol_master(entity_id),
  exchange VARCHAR NOT NULL, trading_symbol VARCHAR NOT NULL,
  effective_from DATE NOT NULL, effective_to DATE,
  change_reason VARCHAR CHECK (change_reason IN ('name_change','symbol_change','initial_listing','relisting')),
  source VARCHAR NOT NULL, PRIMARY KEY (entity_id, exchange, effective_from)
);

CREATE TABLE entity_lineage (
  predecessor_entity_id VARCHAR NOT NULL, successor_entity_id VARCHAR NOT NULL,
  event_type VARCHAR CHECK (event_type IN ('merger','demerger','amalgamation','isin_reissue')),
  event_date DATE NOT NULL, value_allocation_ratio DOUBLE,   -- ties to §2.2's demerger split
  source VARCHAR NOT NULL,
  PRIMARY KEY (predecessor_entity_id, successor_entity_id, event_date)
);
```

**Resolution algorithm.**

```
resolve(raw_symbol, exchange, asof_date) -> entity_id:
  1. lookup (exchange, raw_symbol) in symbol_change_history
       WHERE effective_from <= asof_date AND (effective_to IS NULL OR effective_to > asof_date)
  2. if not found: every bhavcopy row carries an ISIN -> entity_id := ISIN
  3. if entity_lineage later maps entity_id to a successor, a RETURN-SERIES builder (not the
     universe) follows the lineage and splices the successor's series, scaled by
     value_allocation_ratio; the entity's identity for universe/membership is never rewritten.
  4. no match -> raise SymbolResolutionError. Never silently guess.
```

Effort: **3.0d** — the highest-leverage 3 days in the layer; skipping it is how a backtest silently splices two unrelated companies' histories under one symbol.

---

## 6. The ingestion pipeline

Written with no network access here, **first run on the owner's machine** (`ENVIRONMENT-CONSTRAINTS.md`) — every failure must be diagnosable without a chat round-trip.

**Session priming (NSE).** NSE rejects a bare `GET`. The ingester primes cookies via the homepage first, sends a realistic `User-Agent`/`Accept`/`Referer` on every request, reuses one `Session()`, and re-primes on a mid-run 403 rather than failing the batch — following existing OSS scrapers (`bhav-copy`, `nser`) rather than reinventing the approach.

**Rate limiting.** 2–3s minimum between requests per host; exponential backoff with jitter on 403/429/5xx (base 5s, cap 300s, 6 retries); a logged daily request budget per host.

**Retry, idempotency, resumability.** An `ingestion_log` keyed by `(source, logical_date, segment)` with `{status, attempts, last_error, file_hash}`. Re-running a `success` date is a no-op unless `--force`; a crashed run resumes from `status != success`.

**Validation and anomaly detection**, before any row reaches the analytic tables:

| Check | Rule | On failure |
|---|---|---|
| Price spike | `\|return\| > 20%` with no matching `corporate_actions` row | Quarantine |
| Missing day | Calendar gap not explained by a holiday | Flag, re-download |
| Volume/value cross-check | Bhavcopy total vs NSE's published daily summary, tol. 0.1% | Re-download |
| Impossible financials | Negative revenue, current ratio outside `[0,50]`, YoY `>1000%` | Quarantine, never imputed |
| Format drift | Column mismatch vs expected parser schema | Hard fail, explicit message |

**Quarantine.** Suspect rows go to a parallel `_quarantine` table (same schema + `flag_reason`); never enter the analytic tables until a human, or a later automated pass, promotes or discards them.

**Orchestration.** A single-process, topologically-sorted Python runner, not a distributed scheduler — at this volume (§7) a cluster is pure overhead, and the pipeline must be debuggable interactively by one person. Each step is independently idempotent; a `Makefile`/`cron` entry suffices for daily runs.

**Defensive requirements** (debugged over a chat transcript, not interactively, on first run): print HTTP status + body snippet on any non-2xx response; support `--dry-run`; fail loudly rather than write partial output; a runbook comment atop each scraper naming likely failures and fixes (expired cookie → re-prime; 403 → check headers; format changed → bump parser version).

Effort: rate limiting/priming **1.5d**; orchestration/state/retry/quarantine **3.0d**; validation/anomaly detection **2.5d**.

---

## 7. Storage and access

**The case for Parquet + DuckDB.** NIFTY 750 at daily granularity over ~30 years is **≈5.6M price rows** (750×~30×~250); fundamentals, actions, membership and macro are each well under 1M rows — single-laptop scale, and per `ENVIRONMENT-CONSTRAINTS.md` it must run on the owner's own machine with no guaranteed server. A distributed engine is pure overhead for one operator; SQLite lacks a native `ASOF JOIN` and columnar scan performance; raw CSV has no query engine, precisely how look-ahead bugs get written into ad hoc joins with no enforced temporal semantics. DuckDB is embeddable, free, and its **`ASOF JOIN`** is purpose-built for this layer's core query — "the most recent fact known no later than *t*" (Raasveldt & Mühleisen 2019).

**Layout.** Hive-partitioned Parquet under `warehouse/`: `warehouse/prices/exchange=NSE/year=2019/*.parquet`, `warehouse/fact_bitemporal/field_code=.../*.parquet`. DuckDB views over these; partition pruning keeps a backtest query from scanning full history.

**Rule P1 — look-ahead-proof queries.** Researchers never get direct access to raw tables. All reads go through an `_asof(asof_date)` macro:

```sql
CREATE MACRO fact_asof(asof_date) AS TABLE
  SELECT * EXCLUDE (rn) FROM (
    SELECT *, ROW_NUMBER() OVER (
      PARTITION BY entity_id, field_code, period_end ORDER BY knowledge_date DESC) AS rn
    FROM fact_bitemporal WHERE knowledge_date <= asof_date
  ) WHERE rn = 1;
```

— equivalently, a backtest date series `ASOF JOIN`ed to the fact store `ON b.asof_date >= f.knowledge_date`. No "current" table is exposed; a raw `SELECT *` returns every vintage, useless without an `asof_date`, by design. The Python `DataSource` wrapper (§11) refuses to construct without an explicit `asof`; a CI grep bans raw-table references outside the macro/wrapper. This is the "final-vintage reads raise" contract L01, L09 and L17 cite.

Effort: schema + ASOF views **3.0d**; look-ahead-proof wrapper + CI lint **2.0d**.

---

## 8. The fixture strategy

Every registry indicator (`config/cycle_registry.yaml`, and any future `config/signals.yaml`) resolves against a **committed fixture** — this session's egress is blocked to every host tested, and the pipeline must run with zero live data.

**Format.** Small, curated files under `tests/fixtures/l19/`: `bhavcopy_nse_legacy_sample.csv`, `bhavcopy_nse_udiff_sample.csv`, `bhavcopy_bse_sample.csv`, `corporate_actions_sample.csv` (one row per action type incl. both demerger sourcing paths), `index_circular_sample.csv`, `xbrl_sample.xml`, `macro_series_sample.csv` (20–30 points per MVP indicator), `gsec_curve_sample.csv`, `gold_sample.csv`.

**Generation.** Real files are hand-trimmed slices of an actual bhavcopy/filing (a handful of names/dates, one corporate action, one delisting), never fabricated where a real free file is reachable; fabricated only where no sample is obtainable here (macro series, XBRL skeleton).

**Size limits.** No fixture file exceeds **200KB**; the whole directory caps at **~5MB** — a testing artefact, not a data mirror. Real archives live only on the owner's machine, `.gitignore`d.

**CI rule (F1).** A test iterates every `indicators[].source_name`/`source_url` in the registry, resolves it via `fixtures/manifest.yaml` (`indicator_code -> file`), asserts the file exists, parses correctly, and yields non-null rows. A fixture that fails to parse fails CI — the same discipline `src/cyclestack/registry.py` applies to R1/R3/R4/R6. Effort: fixture generation **3.0d**; manifest + CI wiring **1.5d**.

---

## 9. The minimum viable dataset, in order

This ordering **is** the critical path, sequenced to `ROADMAP.md`'s own week numbers rather than a competing schedule:

| Order | Deliverable | Why here, not later |
|---|---|---|
| 1 | NSE bhavcopy, legacy+UDiFF, resumable, rate-limited | Nothing exists without a price tape |
| 2 | ISIN-anchored symbol mastering | Every later join depends on identity; retrofitting after backtests exist means redoing them |
| 3 | BSE bhavcopy (2007–), ISIN-merged | Completes the tape for BSE-only small-caps before universe work |
| 4 | Bitemporal schema + Parquet/DuckDB + ASOF views | The look-ahead defence must exist before any backtest query is written |
| 5 | Corporate actions + adjustment, golden-file tested | Required before any return series is trustworthy |
| 6 | Survivorship-free universe + 3-part test | Gates Phase B: a look-ahead test that tries to leak the future and fails |
| 7 | Index membership (Nifty 50/500/Total Market) | Needed for Phase C's Nifty 500 TRI reproduction — if we can't reproduce it, nothing downstream is trustworthy |
| 8 | Macro MVP subset | Feeds Phase D's macro-regime/credit-cycle classifiers |
| 9 | Gold (FRED, MCX, WGC) | In the neutral portfolio from day one; cheap, done early |
| 10 | Shareholding pattern / pledge | L09's MVP forensic screens need it; D1/D2-clean, cheap vs. XBRL |
| 11 | Forward-archiving, minimal | Must start day one even as a stub — a month unarchived can't be recovered |
| 12 | Fundamentals XBRL | Not in the first six weeks — L09 doesn't need it until its own week 14; starting before the price/universe spine is solid risks rework |

**Deferred beyond MVP:** full macro batch; Kaggle/HuggingFace secondary fundamentals; insider-trading beyond auditor events; full option-chain OI/IV and participant positioning (beyond VIX and the futures basis L17's fast triggers need); annual reports and concall transcripts (Stage 2, post week 24).

---

## 10. Effort estimate

| Item | Days | MVP |
|---|---|---|
| NSE bhavcopy, legacy parser | 3.0 | ✅ |
| NSE bhavcopy, UDiFF parser | 1.5 | ✅ |
| BSE bhavcopy | 2.0 | ✅ |
| Symbol mastering (master + history + lineage + resolver) | 3.0 | ✅ |
| Corporate-action ingestion | 2.0 | ✅ |
| Corporate-action adjustment arithmetic + golden files | 3.0 | ✅ |
| Survivorship-free universe + 3-part test | 2.0 | ✅ |
| Index membership reconstruction | 4.0 | ✅ |
| Bitemporal schema + Parquet/DuckDB + ASOF views | 3.0 | ✅ |
| Look-ahead-proof query wrapper + CI lint | 2.0 | ✅ |
| Ingestion orchestration (state, retry, quarantine) | 3.0 | ✅ |
| Session priming / rate limiting | 1.5 | ✅ |
| Validation & anomaly detection | 2.5 | ✅ |
| Macro — MVP subset | 3.0 | ✅ |
| Gold ingestion | 2.0 | ✅ |
| Shareholding pattern / promoter pledge | 2.0 | ✅ |
| Forward-archiving daemon (minimal) | 2.0 | ✅ |
| Backward lag-policy implementation | 1.0 | ✅ |
| F&O bhavcopy (VIX + futures-basis subset) | 1.5 | ✅ |
| Fixture generation | 3.0 | ✅ |
| Fixture manifest + CI wiring | 1.5 | ✅ |
| Owner-facing runbook | 1.5 | ✅ |
| **MVP subtotal** | **~50** | |
| Macro — full batch beyond MVP | 4.0 | ⬜ |
| XBRL fundamentals, full ingestion + tag mapping | 4.0 | ⬜ |
| Kaggle/HuggingFace secondary fundamentals | 1.5 | ⬜ |
| Insider trading beyond auditor events | 1.5 | ⬜ |
| Annual reports + concall transcripts | 5.0 | ⬜ |
| Full option chain OI/IV + participant positioning | 1.5 | ⬜ |
| **Full-inventory total** | **~68** | |

Person-days of effort, not calendar weeks — most items after #4 in §9 parallelize across the owner+AI pairing and interleave with other layers' build weeks, which is why `ROADMAP.md`'s own calendar (bhavcopy/mastering week 3, bitemporal store week 4, XBRL from week 14) compresses to fewer elapsed weeks than a naive sum of this table.

---

## 11. Interfaces

**Exposes**

```python
DATA_STORE                                    # DuckDB catalogue + warehouse/ Parquet tree
SYMBOL_MASTER                                 # entity_id <-> (exchange, symbol, ISIN)

pit_store(entity_id, field_code, asof)        -> {value, knowledge_date, source, vintage_id}
adj_prices(entities, start, end)              -> OHLCV panel, corp-action adjusted, true PIT
universe(asof)                                -> set[entity_id]              # survivorship-free
membership(index_code, asof)                  -> set[entity_id]
macro_series(series_code, asof)               -> pd.Series                   # vintage-aware where source allows
symbol_resolve(raw_symbol, exchange, asof)    -> entity_id
forward_archive(entity_id, field_code)        -> [{knowledge_date, value, restated_from}]
```

Every function requires an explicit `asof`; a final-vintage read raises `LookaheadError` (Rule P1) — the exact contract L01 §11, L09 §1/§11 and L17 §11 cite verbatim.

**Consumed by**

| Layer | Object(s) | Contract |
|---|---|---|
| L01 | `macro_series`, `pit_store` | Feeds cycle z-scores; L01 computes no data itself |
| L09 | `pit_store`, `universe`, `membership`, `forward_archive` | Fundamentals adapter builds legs from these |
| L14 | `membership`, `adj_prices` (implicit) | Sector/constituent weights, covariance panel |
| L15 | `adj_prices` (raw ADV/volume) | Derives `investable_universe(book, asof)` — not built here |
| L17 | `pit_store`, `adj_prices`, `universe`, `membership`, CCIL/RBI series | Risk and liquidity model inputs |
| L20 | Forward-archive vintages | `restatement_delta`, the 2028 bias-isolation metric |

---

## 12. Risks and open items

1. **Registry lag inconsistency.** `bis_credit_gap_ind`/`india_credit_gdp` carry `lag_days: 120`, but L01 §10's worked example for the same BIS indicator uses `150`. This layer's lag policy (§2.6, §3c) must pick one — flagged for the registry owner, not silently resolved here.
2. **Several `[verify]` dates** (UDiFF cutover, Total Market launch year, half-yearly BS/CFS mandate, participant-OI start) are training-era recollections needing confirmation before the ingester is built — a wrong cutover mis-parses a year of files with the wrong schema.
3. **The demerger price-ratio fallback** is a real error source exactly where L12's special-situations model cares most; every fallback ratio must carry its `source` flag downstream so a demerger-heavy window can be re-run once an official circular surfaces.
4. **Kaggle/HuggingFace cannot be quality-checked from this session** (403 at egress); contamination is asserted from the general character of community scrapes, not a specific dataset — re-assess once the owner's machine can reach them.
5. **The restatement-bias estimate (§3d) is a model, not a measurement** — the honest placeholder until the 2028 replay; not to be quoted elsewhere as empirical.
6. **Pre-2019 XBRL non-standardisation** is the largest unbudgeted-risk item here; if tag mapping exceeds 4.0 days, L09's fundamental book (FUND-FL) slips, not the price-only book — an acceptable, pre-declared degradation.

---

## 13. References

1. Shumway, T. (1997). "The Delisting Bias in CRSP Data." *Journal of Finance* 52(1), 327–340. — §4's union-across-bhavcopy design is the free-data analogue of this.
2. Shumway, T. & Warther, V. A. (1999). "The Delisting Bias in CRSP's Nasdaq Data and Its Implications for the Size Effect." *Journal of Finance* 54(6), 2361–2379.
3. Banz, R. W. & Breen, W. J. (1986). "Sample-Dependent Results Using Accounting and Market Data: Some Evidence." *Journal of Finance* 41(4), 779–793. — the E/P look-ahead result behind §3d's bias direction.
4. Kothari, S. P., Sabino, J. S. & Zach, T. (2005). "Implications of data restrictions on performance of accounting-based value strategies." [verify exact journal/year].
5. Snodgrass, R. T. (1999). *Developing Time-Oriented Database Applications in SQL*. Morgan Kaufmann. — the event-time/knowledge-time model this layer's DDL implements.
6. Jensen, C. S. & Snodgrass, R. T. (1999). "Temporal Data Management." *IEEE TKDE* 11(1), 36–44.
7. Melnik, S. et al. (2010). "Dremel: Interactive Analysis of Web-Scale Datasets." *VLDB* 3(1), 330–339. — columnar rationale for §7.
8. Raasveldt, M. & Mühleisen, H. (2019). "DuckDB: an Embeddable Analytical Database." *ACM SIGMOD* (demo). — source of the `ASOF JOIN` Rule P1 relies on.
9. López de Prado, M. (2018). *Advances in Financial Machine Learning*. Wiley. — purged/embargoed CV depends on this layer's PIT labelling being honest.
10. Jordà, Ò., Schularick, M. & Taylor, A. — Macrohistory Database, 18 countries, 1870–. `https://www.macrohistory.net/database/`.
11. Free-source index (`[verify]` = unconfirmed history-start/cutover): NSE bhavcopy `https://www.nseindia.com/all-reports` (legacy+UDiFF, F&O, VIX, participant OI) · BSE bhavcopy `https://www.bseindia.com` · RBI DBIE `https://dbie.rbi.org.in` · MOSPI `https://mospi.gov.in` · GST Council portal · BIS `https://data.bis.org` · IMF WEO/IFS/COFER · World Bank Pink Sheet/WDI · FRED/ALFRED `https://alfred.stlouisfed.org` · Shiller (Yale) · MeasuringWorth `https://measuringworth.com` · Our World in Data `https://ourworldindata.org` · CCIL `https://www.ccilindia.com` · World Gold Council `https://www.gold.org/goldhub` · MCX `https://www.mcxindia.com` · niftyindices `https://www.niftyindices.com` · AMFI · NSDL FPI `https://www.fpi.nsdl.co.in` · Kaggle/HuggingFace (secondary fundamentals only, unverified from this session) · OSS references: `bhav-copy` (GitHub), `nser` (CRAN).

*Items marked [verify] require confirmation against the primary source, ideally from the owner's machine where these hosts are reachable, before the ingester is built against the assumed date or format.*
