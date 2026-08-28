# Roadmap: The Multi-Cycle Basket Model

**Universe:** NIFTY 750 + Gold + a debt sleeve · **Capital:** proprietary
**Books:** aggressive ₹100 cr (high churn) and moderate ₹1,000 cr (low churn)
**Constraint set:** frozen in `docs/model/DECISIONS.md`
**Theory:** `docs/theory/01-CYCLE-THEORY.md` · **Methods:** `docs/theory/02-ECONOMETRIC-METHODS.md`
**References:** `docs/theory/03-BIBLIOGRAPHY.md`

---

## 0. What this is

A portfolio construction system that reads the position of many economic and market cycles
— from the multi-century currency/debt arc down to the one-month reversal — and turns that
reading into a target basket across Indian equities, gold and debt, with an options overlay
and bounded leverage.

The distinguishing idea is not that cycles matter. It is **horizon-aware authority**: slow
cycles set the strategic centre of gravity with wide bands and rare changes, fast cycles move
a bounded tactical deviation around it, and each cycle's allowed influence is capped by how
much evidence actually exists for it. A 250-year debt cycle and a 3-month momentum signal
both appear in the model. They do not get the same power.

---

## 1. The honest arithmetic, first

You asked for honesty over reassurance, so this goes at the top rather than in an appendix.

### 1.1 The return target

| Step | Aggressive book |
|---|---|
| Your target, net of costs, pre-tax | 35–60% |
| Less Nifty 500 TRI long-run beta (~13–14% CAGR over 20–25y) | leaves **~22–46 pp of alpha** |
| Turnover cost at 500%/yr (5 round trips × ~0.5–0.8% all-in in Indian mid/small caps) | **~2.5–4.0% pa drag** |
| So gross alpha required, before costs | **~25–50 pp per year, sustained** |

Grinold's fundamental law says alpha = IR × tracking error. At a 15% tracking error, 30 pp of
alpha requires an information ratio of **2.0**. Sustained IRs above 1.0 are rare; above 1.5
over a decade is a handful of firms globally; 2.0 in a long-biased equity book is not
something anyone has done at any size for a decade.

Two things genuinely work in your favour, and they are not trivial:

- **₹100 cr is small.** Capacity constraints are what destroy most published alpha. In the
  Indian mid/small tail, at ₹100 cr, real inefficiency is reachable that a ₹5,000 cr fund
  cannot touch.
- **India is a less efficient market** than the US, with a shorter history of systematic
  participation and a retail-dominated tail.

So the honest range is wider here than it would be for a US large-cap book. But 35–60%
*sustained* is not a target, it is an outcome that a good year produces.

### 1.2 The drawdown target, and why it binds harder

You set: max drawdown below the Nifty 50's, ceiling 30–35%. The Nifty 50 fell roughly 38% in
March 2020 and roughly 60% in 2008. The **30–35% absolute ceiling is the binding constraint**,
not the relative one.

This collides directly with two other frozen parameters:

- **1.5x gross leverage.** A 1.25x-levered Indian mid/small book in 2008 would have drawn down
  well past 70%. Leverage has to be *state-contingent* — available in low-volatility,
  favourable-cycle states and unavailable otherwise — not a standing 1.25x average.
- **Momentum at 500% turnover.** Daniel & Moskowitz (2016) document that momentum's
  catastrophic losses occur precisely at market rebounds off bottoms. A levered momentum book
  is the single most likely path to breaching your drawdown ceiling.

**Resolution, which shapes the whole build:** the cash-call engine and the volatility-scaled
momentum construction are not features to be added later. They are load-bearing, and they are
built in Phase 2 and Phase 3 respectively — before any of the return-seeking cleverness.

### 1.3 What the model is built to target

| Book | Return (net of cost, pre-tax) | Max drawdown | Stretch case |
|---|---|---|---|
| **Aggressive, ₹100 cr** | **22–28% CAGR** | **25–30%** | 35%+ when nominal growth is high, the value spread is wide, and the credit cycle is early |
| **Moderate, ₹1,000 cr** | **15–19% CAGR** | **20–25%** | 22%+ in the same conditions |

These are the numbers the model is *engineered* to. Your 35–60% remains the aspiration, and
the stretch column names the conditions under which it becomes reachable. Building to the
aspiration rather than the engineering target is how a fund takes the risk that breaches the
drawdown ceiling — which is the constraint you said matters.

**If you want me to build to 35–60% as the design target instead, say so and I will** — but
the leverage policy, the momentum sizing and the cash-call thresholds all change, and the
drawdown ceiling becomes unreachable. That is the trade, stated plainly.

---

## 2. Architecture

Your three-stage pipeline, with the layer stack inside each stage.

```
┌─────────────────────────────────────────────────────────────────────┐
│  STAGE 1 — CYCLES + QUANT            must produce a COMPLETE        │
│                                       portfolio on its own          │
│                                                                     │
│   TOP-DOWN (what to own, in aggregate)                              │
│     L02  Long wave: currency, debt, reserve      50–250y   tier C   │
│     L03  Credit / capex / property               7–25y     tier B   │
│     L04  Macro regime: growth, inflation, rates  1–10y     tier A/B │
│     L05  Valuation + expected returns            3–15y     tier B   │
│     L06  External: INR, crude, commodities       2–25y     tier B   │
│     L07  Flows, supply, sentiment                1m–5y     tier B   │
│              │                                                      │
│              ├──> cash-call level, equity/gold/debt split           │
│              │                                                      │
│   CROSS-SECTIONAL (what to own, name by name)                       │
│     L08  Momentum + trend                        1m–2y     tier A   │
│     L09  Factor library: value/quality/lowvol    1–5y      tier A   │
│     L10  Sector model                            3m–5y     tier B   │
│     L11  Bottom-up fundamental scoring           1–5y      tier B   │
│     L12  Special situations + recent IPOs        1w–2y     tier B   │
│              │                                                      │
│              └──> per-name scores + expected returns                │
├─────────────────────────────────────────────────────────────────────┤
│  STAGE 2 — AI AGENTS + HUMAN            SWITCHABLE OFF              │
│     L18  Forward-looking views, red-teaming, sanity checks          │
│          Enters as Black-Litterman views. Hard-capped deviation.    │
├─────────────────────────────────────────────────────────────────────┤
│  STAGE 3 — OPTIMIZER                                                │
│     L14  Constrained optimisation -> target weights                 │
│     L15  Execution scheduler -> tranches and dates                  │
│     L16  Options overlay -> hedge ratio (swept parameter)           │
│     L17  Risk engine + cash-call + de-gearing ladder                │
└─────────────────────────────────────────────────────────────────────┘
   Cross-cutting: L19 free-data pipeline · L20 backtest + validation
```

The load-bearing rule from your Q5 answer: **Stage 1 alone must emit a complete portfolio.**
Stage 2 is an overlay. That makes quant-only vs. quant-plus-overlay a measurable comparison,
which is the only honest way to know whether the AI/human layer adds anything.

---

## 3. The cycle ladder

The full ladder, with the authority each level gets. Tiers and influence caps come from
`01-CYCLE-THEORY.md §5`; data feasibility assumes free sources only.

| Horizon | Cycle | Mechanism | Tier | Obs. in India | Free data? | Max influence (agg / mod) |
|---|---|---|---|---|---|---|
| 150–250y | Reserve-currency / hegemonic debt arc | Debt accumulation → devaluation → monetary reorder | C | <1 | Partial (IMF COFER, WGC, BIS) | 3 pp / 2 pp |
| 50–80y | Kondratiev long wave | Technology diffusion, long price waves | C | <1 | Yes (JST, Shiller) | 2 pp / 1 pp |
| 30–50y | Sovereign debt / fiscal cycle | Debt-to-GDP accumulation and repression | C | ~0.5 | Yes (IMF, RBI) | 3 pp / 2 pp |
| 16–25y | **Financial cycle (credit + property)** | Minsky; leverage build and deleveraging | **B** | ~1.5 | **Yes (BIS gap, RBI HPI)** | **8 pp / 6 pp** |
| 15–25y | Commodity supercycle | Capex underinvestment → shortage → glut | B | ~1 | Yes (World Bank Pink Sheet) | 4 pp / 3 pp |
| 15–20y | Demographic / financialisation arc | Savings migration, physical → financial | B | ~1 | Yes (RBI, MOSPI) | 3 pp / 3 pp |
| 7–11y | **Credit cycle** | Juglar + Minsky; the anchor signal | **B/A** | ~3 | **Yes (RBI, BIS)** | **10 pp / 8 pp** |
| 7–11y | Capex / investment cycle | Capacity added in lumps, then digested | B | ~3 | Yes (OBICUS, GFCF) | 6 pp / 5 pp |
| 5–10y | Dollar / DXY cycle | Global liquidity and EM transmission | B | ~2.5 | Yes (FRED) | 5 pp / 4 pp |
| 3–7y | **Macro regime (growth × inflation)** | Policy and demand cycle | **A** | ~6 | **Yes (MOSPI, RBI)** | **12 pp / 9 pp** |
| 3–7y | Valuation mean reversion | Multiple compression / expansion | B | ~4 | Yes (NSE, MOSPI) | 10 pp / 8 pp |
| 3–5y | Kitchin / inventory | Order–delivery lag overshooting | B | ~7 | Yes (IIP, filings) | 4 pp / 3 pp |
| 2–5y | Earnings / margin cycle | Margin mean reversion | B | ~5 | Yes (filings) | 6 pp / 5 pp |
| 1–3y | Flows and supply | FII/DII/SIP, IPO supply | B | ~8 | Yes (NSDL, AMFI, SEBI) | 8 pp / 5 pp |
| 1–3y | Small-vs-large cap cycle | Risk appetite, liquidity | B | ~8 | Yes (NSE indices) | 8 pp / 5 pp |
| 6m–2y | Sector rotation | Cycle-conditional sector leadership | B | ~12 | Yes (NSE sector indices) | 10 pp / 8 pp |
| 3–12m | **Cross-sectional momentum** | Underreaction, flows | **A** | ~25 | **Yes (bhavcopy)** | **15 pp / 8 pp** |
| 3–12m | Time-series trend | Trend persistence | A | ~25 | Yes (bhavcopy) | 10 pp / 6 pp |
| 1–3m | Earnings drift (PEAD) | Underreaction to results | A | ~100 | Yes (filings) | 6 pp / 3 pp |
| 1–4w | Short-term reversal | Liquidity provision | A | ~300 | Yes (bhavcopy) | 4 pp / 1 pp |
| event | Special situations / IPO base | Corporate action, supply dynamics | B | varies | Yes (exchange filings) | 8 pp / 4 pp |

Read the pattern down the "obs." column. **Authority tracks evidence.** The 3-month momentum
signal gets more allocation power than the 200-year debt cycle, not because it matters more in
the world, but because we can actually know where we are in it.

### 3.1 The influence budget must add up

If every signal screamed maximum in the same direction simultaneously, the sum of the
aggressive column above is ~145 pp — far beyond any sane allocation. Three mechanisms bound it:

1. **Family compositing.** Correlated cycles are grouped into families (credit family: credit
   cycle + capex + financial cycle + earnings; each family emits ONE composite). This collapses
   ~22 signals into ~8 independent inputs.
2. **Orthogonalisation by horizon.** Slowest first; each faster signal is residualised against
   the slower composites already in the stack, so a fast signal only earns influence for the
   part of it that is genuinely new information.
3. **A hard projection step.** After aggregation, the proposed weights are projected onto the
   feasible set defined by the frozen caps (equity, gold ≤50%, debt ≤70%, gross ≤1.5x, sector
   ≤25%, name ≤6% entry / 10% drift). The projection is the last word.

The arithmetic must be demonstrated, not asserted — a property test in the suite asserts that
for any signal vector in [−1, +1]^n, the output satisfies every frozen constraint. That test is
written in Phase 6 and is a gate.

---

## 4. Build sequence — and why it is not "largest cycles first"

You said to start from the largest cycles and work down. I want to push back on the *build*
order while agreeing with the *design* order, and then explain the resolution.

**Where you are right:** the architecture must be designed top-down, largest first. If the
long-cycle layers are bolted on later, the aggregation scheme will have been built around
fast signals and will have no room for slow ones. That is a real failure mode and it is why
the cycle ladder and the influence budget are specified before any code.

**Where building largest-first goes wrong:**

1. The long-cycle layers are the **least validatable** — under two observations. Building them
   first means spending the first month on the part of the system you can never prove works.
2. They are the **least actionable** — capped at 2–3 pp of influence each. Even fully built,
   they barely move the portfolio.
3. They are **not on the critical path** to your binding constraint. The drawdown ceiling is
   met by the cash-call engine, which runs off the macro regime and credit cycle — the *middle*
   of the ladder.
4. Nothing works end to end until the data pipeline and backtester exist, and those are
   horizon-agnostic.

**The resolution — design top-down, build middle-out:**

```
  design order:   250y ──────────────────────────────> 1m   (Phase A, on paper)
  build order:         credit/macro ──> selection ──> long wave ──> fast overlay
                       (the anchor)     (the alpha)   (the prior)   (the polish)
```

Build the middle first because that is where evidence, actionability and the drawdown
constraint all coincide. Add the long wave once the machinery exists to hold it properly —
it is a small, slow, capped overlay and it can be added in an afternoon once the framework
is there. Add the fastest signals last because they are the highest-turnover, highest-cost,
and most sensitive to the execution machinery being right.

---

## 5. The phases

Calendar assumes you plus AI, part-time. **Total: 24 weeks to a validated system.** Weeks are
sequential; entries in *italic* are gates that must pass before the next phase begins.

### Phase A — Design freeze (weeks 1–2)

No code. The artefacts that everything else is built against.

| Deliverable | Detail |
|---|---|
| `config/cycles.yaml` | The full cycle registry: every cycle with horizon, tier, indicators, free source, band widths, hysteresis, min dwell, max influence, slide triggers |
| `config/signals.yaml` | Every signal, deduplicated across layers, with exact formula, inputs, source, feasibility, scoring, influence cap |
| Interface contracts | `Signal`, `CycleModel`, `RegimeClassifier`, `Allocator`, `CostModel`, `ExecutionScheduler`, `RiskModel`, `Backtester`, `DataSource` — as real typed Python ABCs |
| Influence budget arithmetic | The demonstration that maximum simultaneous influence lands inside the frozen caps |
| Trial register | `research/register/` initialised. Nothing gets backtested before it is registered |

*Gate: the constraint arithmetic is demonstrated on paper and the interfaces compile.*

### Phase B — Skeleton (weeks 3–5)

Get one crude thing running end to end before adding any cleverness. **This phase's output
is deliberately bad** — a trivial signal, a small universe — and that is the point: it proves
the pipeline, not the idea.

| Week | Work |
|---|---|
| 3 | Bhavcopy ingester (NSE 1994→, both legacy and udiff formats), resumable, rate-limited, integrity-checked. **Runs on your machine** — see `ENVIRONMENT-CONSTRAINTS.md` |
| 3 | Symbol mastering: ISIN-anchored permanent IDs, symbol-change history. Skipping this quietly ruins every later backtest |
| 4 | Bitemporal store (DuckDB + Parquet): prices, corporate actions, index membership, with event date and knowledge date |
| 4 | Corporate action adjustment: bonus, split, rights, dividend, demerger — with a golden-file test per type |
| 5 | Backtester with the **real India cost model** (STT, stamp, exchange, GST, spread, square-root impact by market-cap decile) |
| 5 | One trivial signal (12-1 momentum), one trivial allocator (equal weight, top 30), full report |

*Gate: a survivorship-free universe reconstructed as a union across all dates; a look-ahead
detection test that deliberately tries to leak the future and fails; end-to-end run produces
a return series and a cost breakdown.*

### Phase C — The honest baseline (week 6)

You cannot know if the model is good without knowing what it must beat.

- Nifty 50 TRI, Nifty 500 TRI, Nifty Total Market TRI reconstructed
- Static 60/20/20 equity/gold/debt with quarterly rebalance
- Equal-weight Nifty 500, and a naive 12-1 momentum portfolio
- Full stats: CAGR, vol, Sharpe, max DD and recovery time, rolling 1/3/5y worst cases
- **The relative-drawdown test** made a first-class metric, since it is your binding constraint

*Gate: baselines reproduce published index returns within tolerance. If we cannot reproduce
the Nifty 500 TRI, the data is wrong and nothing downstream is trustworthy.*

### Phase D — Macro regime and the credit cycle (weeks 7–10)

The anchor. Best evidence, computable from free macro data, and the input to the cash call.

| Week | Work |
|---|---|
| 7 | Macro data ingestion: RBI DBIE, MOSPI, BIS credit-to-GDP gap, FRED, World Bank. Vintage-aware where available; conservative publication lag where not |
| 7 | Hamilton (2018) regression filter as the standard cycle extractor. **No HP filter** — endpoint instability disqualifies it (`02-ECONOMETRIC-METHODS.md §1`) |
| 8 | Macro regime classifier over growth × inflation × liquidity. Probability-weighted, not hard-switching; minimum dwell; confirmation lag |
| 8 | Nominal-growth nowcast via Kalman filter over GST collections, IIP, PMI, credit growth — handles ragged publication lags natively |
| 9 | Credit-cycle phase scorecard. **Rule-based, not fitted** — India has ~3 transitions, far below the 10-transition bar for a Markov-switching model. Thresholds from the Jordà–Schularick–Taylor panel, applied to India out-of-sample |
| 10 | Cross-country validation on the JST panel with country fixed effects and year-clustered errors |

*Gate: the classifier, run historically, identifies India's known turning points (2008, 2013,
2018, 2020) without being fitted to them. If it cannot find 2008, it is not a cycle model.*

### Phase E — Valuation, expected returns, and the cash-call engine (weeks 11–13)

| Week | Work |
|---|---|
| 11 | Aggregate valuation: market-cap/GDP, earnings yield vs. GSec spread, India percentile bands. Expanding-window z-scores only — full-sample normalisation leaks |
| 11 | Grinold–Kroner expected returns for equity and gold; debt at your frozen 10% **with risk attached** (4% vol, 6% worst DD, equity correlation flipping −0.2 → +0.4 across inflation regimes) |
| 12 | **The debt free-lunch fix, demonstrated.** A 10% return with no risk makes any optimiser corner-solution to the 70% cap. Worked arithmetic proving the formulation does not degenerate |
| 12 | Flows / supply / euphoria composite, calibrated against Jan-2008, Mar-2020, Oct-2021, and the 2024-25 small-cap episode |
| 13 | **The cash-call engine.** Target cash from euphoria + valuation percentile + credit phase + trend state + realised drawdown. With hysteresis, minimum dwell, and — critically — an explicit **re-entry rule**. De-risking systems that never re-risk lock in losses; that is the standard failure mode |

*Gate: a working top-down allocator producing equity/gold/debt/cash weights. Backtested
drawdown vs. Nifty 50 across 2008, 2013, 2018, 2020. **The measured CAGR cost of the cash-call
policy is reported** — market timing usually costs return, and you deserve that number.*

### Phase F — Cross-sectional selection (weeks 14–17)

| Week | Work |
|---|---|
| 14 | Fundamentals ingestion from exchange XBRL. Expect this to be the ugliest work in the project. **Forward-archiving starts here** — snapshot everything with our own knowledge timestamps from day one, so that in two years we have genuine point-in-time data |
| 15 | Factor library: value, quality (gross profitability, accruals, asset growth), low-vol, size×quality. Benchmarked against the **IIM-A Indian factor library** — the best free India-specific validation available |
| 15 | India forensic screens: promoter pledge, auditor changes, related-party intensity, receivable-days, CFO/PAT divergence, ASM/GSM lists |
| 16 | Momentum: 12-1, residual (Blitz-Huij-Martens), **volatility-scaled (Barroso–Santa-Clara)**, 52-week high. Vol-scaling is not optional — it is what stops Daniel–Moskowitz momentum crashes breaching your drawdown ceiling |
| 16 | Nominal-growth gate on momentum sleeve weight — your hypothesis, implemented and *tested*, with an honest report of whether the evidence supports it |
| 17 | Sector model: sector momentum, sector PE vs. own history, sector growth from free high-frequency proxies (auto sales, cement despatches, credit growth, steel output) |

*Gate: factor returns broadly reconcile with the IIM-A library. Momentum sleeve survives a
simulated March-2020 rebound without breaching the drawdown ladder.*

### Phase G — Bottom-up, gold, special situations (weeks 18–19)

| Week | Work |
|---|---|
| 18 | Bottom-up quant scorecard: incremental ROIC on reinvested capital, cash conversion, balance-sheet resilience, promoter/governance metrics. Reverse-DCF to a comparable expected return per name. Explicitly orthogonalised against the quality factor so the two do not double-count |
| 18 | Gold sizing function: real rates, debasement score, external vulnerability, trend, valuation vs. CPI/M2, and current portfolio hedge need → 0–50%. With momentum-exhaustion guardrails so it cannot max out at a gold top |
| 19 | Special situations: index rebalance flow, demergers, holdco discount, open offers, lockup expiries |
| 19 | **Recently-listed IPO sub-model** — its own scoring path, since 12-1 momentum, fundamental history and factor percentiles are all undefined for a 3-month-old listing. Base formation defined computably: consolidation range, volatility contraction, volume dry-up, breakout confirmation. Plus anchor-lockup calendar and float/overhang dynamics |

### Phase H — Optimiser and execution (weeks 20–21)

| Week | Work |
|---|---|
| 20 | Constrained optimiser. Horizon-aware blending: slow signals move the centre via heavy exponential smoothing, fast signals move a bounded deviation. Turnover penalty calibrated to produce 500%+ and <100% from **one engine** |
| 20 | **Property tests**: for any signal vector, output satisfies entry cap, drift cap, min names, sector cap, gold cap, debt cap, gross leverage, in-progress budget. This is the constraint arithmetic made executable |
| 21 | Execution scheduler: target weight + ADV + AUM + urgency → tranche sizes and dates. Implements your ~1% tranches over several weeks for thin names, and the 20% in-progress budget with a queue and a rule for signals that decay while queued |
| 21 | Days-to-build and days-to-exit tables by market-cap decile at ₹100 cr and ₹1,000 cr. **This is what actually determines each book's investable universe** |

*Gate: property tests pass. The ₹1,000 cr universe is derived rather than assumed.*

### Phase I — Options overlay (week 22)

- Hedge-ratio sweep as a **config parameter**: 0 / 25 / 50 / 75 / 100 / 125%, per your Q15
- Exposure accounting: delta-adjusted for directional, separate notional limit for tail hedges
  (a far-OTM tail put has huge notional and tiny delta; counting it at full notional would
  crowd out the equity book for no risk reason)
- Index futures for fast beta adjustment — likely the main tool for the cash call, and usually
  superior to options for simple de-risking
- **Honest limitation:** free long-dated Indian option history barely exists. Most of this is
  validated by simulation over a modelled volatility surface, not by backtest. Labelled as such
- The sweep is 6 configurations and **counts against the trial register**

### Phase J — Validation (weeks 23–24)

- Walk-forward with expanding windows as the primary reported result
- Purged and embargoed CV; combinatorial purged CV for a distribution of outcomes
- Deflated Sharpe and probability of backtest overfitting, with the trial count from the register
- **The price-only variant** — the strategy using only price/volume, which has genuine
  point-in-time integrity. The gap between it and the fundamental version is an upper bound on
  how much apparent alpha could be a restatement artefact
- Attribution: per-layer and per-signal contribution to return and risk
- Regime-conditional performance; the relative-drawdown test in every stress window

*Gate: honest out-of-sample numbers, with haircuts applied, against the Phase C baselines.*

### Stage 2 — deferred to after week 24

The AI/human forward-looking layer is built **last**, deliberately. Stage 1 must work alone
first, because the whole accountability mechanism is the comparison between them. Building the
overlay before the baseline exists means never knowing whether it helped.

---

## 6. What we are deliberately not building

| Not building | Why |
|---|---|
| Elliott Wave, Gann, harmonic and planetary cycles | Unfalsifiable; wave counts revised after the fact |
| Fixed-period calendar cycles (decennial, "seven-year") | 10–15 non-independent observations; fails any multiple-testing correction |
| Neural nets / gradient boosting for return prediction | 25 years of lag-approximated data. Their capacity to fit noise exceeds our ability to detect it. *Permitted for* text extraction, entity resolution, data-quality anomaly detection |
| A managed bond sleeve | You froze it at a flat 10%. No credit model, no duration overlay |
| PMS / AIF structuring | Proprietary capital. Out of scope |
| Markov-switching on the credit cycle | ~3 observed transitions, below the 10-transition identifiability bar |
| Analyst-estimate revision signals | Not available free. Proxied by realised surprise vs. a seasonal random walk |
| Threshold optimisation against backtest Sharpe | The moment a threshold is tuned to the outcome it becomes a fitted parameter and must be counted |

---

## 7. The risk contract

| Control | Aggressive | Moderate |
|---|---|---|
| Gross leverage | ≤1.5x, **state-contingent**, not a standing 1.25x | ≤1.5x, state-contingent |
| De-gear ladder | −10% DD → gross to 1.0x; −15% → cut equity beta 25%; −20% → defensive posture; −25% → halt and review | Same, tighter by 5 pp at each rung |
| Re-gear rule | Explicit and pre-committed. Trend state + volatility normalisation + minimum dwell | Same |
| Momentum crash guard | Volatility-scaled momentum + bear-state gate + drawdown-conditional de-gearing | Same |
| Liquidity | Days-to-liquidate ≤ N days at stated participation; caps derived per decile | Stricter — the bottom 250 names are largely excluded |
| Single name | 5–6% entry, 10% drift | Same |
| Sector | 25% | 20% |
| Gold / debt | ≤50% / ≤70% | Same |
| Options | ≤50% directional notional, ≤75% tail | Same |
| Kill switch | Data-quality circuit breaker, signal-staleness monitor, model-failure detection | Same |

---

## 8. How success is measured

Primary tests, in priority order:

1. **Relative drawdown** — max DD below the Nifty 50's in every stress window (2008, 2013,
   2018, 2020, 2024-25), and below the 30–35% absolute ceiling. *This is the binding test.*
2. **Net-of-cost CAGR** vs. Nifty 500 TRI and vs. the static 60/20/20 baseline.
3. **Deflated Sharpe** with the true trial count, not the flattering one.
4. **Out-of-sample R²** against the historical-mean benchmark for every timing signal.
5. **Attribution coherence** — the system can say which layer caused a loss. If it cannot, the
   model cannot be improved and the number of layers should be cut.
6. **The price-only gap** — how much of the alpha survives when fundamental data (with its
   restatement bias) is removed.

Failure criteria, pre-committed: three consecutive years below benchmark net; or a drawdown
ceiling breach; or a PBO above 0.5 on the final configuration.

---

## 9. Immediate next steps

1. **You:** confirm the target pair in §1.3, or tell me to build to 35–60% and accept the
   drawdown consequence.
2. **You:** confirm the build order in §4 (middle-out) or hold to largest-first.
3. **Me:** Phase A — write `cycles.yaml`, `signals.yaml`, and the interface contracts.
4. **Me:** Phase B code, written here against fixtures; the ingester runs on your machine.

Neither of your confirmations blocks Phase A. I will start on the registries and interfaces
now, since those are needed under either answer.
