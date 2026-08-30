# Cold-start prompt

Paste everything below the line into a fresh Claude Code session in an empty repo.

Its purpose is not to describe the model — it is to **front-load the conclusions that cost
a full session to discover**, so the new session starts from the current frontier instead of
rediscovering the same walls. Roughly two-thirds of it is findings, not requirements.

---

## THE MANDATE

Build a multi-horizon "cycle stack" portfolio construction model for Indian markets.
Universe: NIFTY 750 equities, gold, and a debt sleeve. Proprietary capital, so leverage and
options are permitted. Two books, which are **different products, not one dialled down**:

- **Aggressive** — ₹100 cr, turnover up to 500%/yr, reaches the NIFTY 750 mid/small tail.
- **Moderate** — ₹1,000 cr, turnover under 100%/yr, confined to roughly ranks 1–500.

Read many cycles at once — from the multi-century currency/debt arc down to the one-month
reversal — and turn that reading into a target basket. Combine top-down and bottom-up.
Include forward-looking judgement that cannot be backtested. Build step by step.

**Architecture (fixed):**
```
Stage 1  Cycles + Quant   -> must emit a COMPLETE portfolio on its own
Stage 2  AI + human       -> forward views and checks; SWITCHABLE OFF
Stage 3  Optimizer        -> final construction
```
Stage 1's self-sufficiency is load-bearing: quant-only vs quant-plus-overlay is the only
honest way to measure whether Stage 2 adds anything.

## FROZEN CONSTRAINTS

Returns net of costs, pre-tax. **Drawdown is the binding constraint:** below the Nifty 50's
over the same window, absolute ceiling 30–35%.

Debt ≤70%, gold ≤50%, gross leverage ≤1.5x. Name entry 5–6%, drift cap 10%, minimum 10 names
when equity <50%, in-progress positions ≤20% aggregate. Options notional ≤50% directional,
≤75% tail hedge, with the hedge ratio a swept config parameter (0/25/50/75/100/125%).
Sector: fully active. Debt sleeve is a flat 10% assumption — no credit model, no duration
overlay. Gold via ETF and futures only. Rebalance: weekly permitted, bi-weekly to monthly
preferred. Special situations in scope, including recently listed IPOs.

**Data: free sources only.** NSE/BSE bhavcopy, RBI DBIE, MOSPI, CCIL, BIS, IMF, FRED, World
Bank, AMFI, NSDL, World Gold Council, exchange filings, Kaggle/HuggingFace. Scraping allowed.
No paid feeds of any kind.

**Team and time:** the owner plus you, 3–6 months. Scope must be cut to fit; be ruthless.

## WHAT IS ALREADY KNOWN — do not rediscover these

**1. Cycles have persistence, not periodicity.** Of 32 candidate cycles, only five survive a
"clock test" of four or more observed periods, and three of those are calendar-anchored.
Everything else is a *state variable*. Order the ladder by `tau_half` — the autocorrelation
half-life in months — which is estimable from overlapping windows even with zero complete
cycles. Do not order by claimed period; that model does not survive the record.

**2. Authority must track evidence, not importance.** Tier cycles by independent observations
*of the effect*: A (≥30, may be fitted with purged CV), B (4–30, or n<4 with ≥10 cross-country
analogues; parameters frozen in git at inception), C (<4, narrative). **Tier-C cycles may only
REDUCE risk**, and all of them combined are capped at 150 bps of NAV. Consequence: the
200-year debt cycle moves the book by at most 1.5pp, and the long-wave view therefore lives in
a structural gold floor and a tail-hedge policy rather than in cycle influence at all.

**3. The cycle stack is the risk system; name selection is the return system.** Cycle-driven
allocation contributes only 100–300 bps/yr. If the aggressive book is to compound in the
twenties, essentially all of it comes from the cross-section. The cycles buy permission to run
concentrated and levered without breaching the drawdown ceiling.

**4. A standing 1.25x leverage is incompatible with a 30–35% drawdown ceiling.** At 1.25x with
no de-risking, 2008 is −58% and March 2020 is −36%. Leverage must be a state-contingent
permission, not an average; the compatible average is ~1.10–1.15x aggressive, ~1.05x moderate.

**5. A flat 10% debt return breaks every optimizer.** Fed 10% return / 4% vol, naive
mean-variance puts 70% in debt at *every* risk aversion, risk parity independently lands at
67%, and the corner even beats a balanced portfolio on modelled drawdown. So do not optimise
the asset mix — **compose it** from a policy portfolio (equity 60 / gold 12 / debt 28) set by
construction, and optimise only the equity cross-section. State the implied override
explicitly: that policy point prices debt roughly 400 bps/yr below its stated return.

**6. Turnover costs 3.91% of NAV/yr at 500% turnover** (0.60% at 100%), which makes the
incremental hurdle for the high-churn book ~3.3pp/yr of extra gross alpha.

**7. The measurement error is the same size as the thing measured.** Free Indian fundamentals
are restated with no knowledge date, biasing fundamental backtests upward by 150–450 bps/yr
after reconstruction engineering, plus survivorship effects. Against a 3.3pp hurdle, that is
not a footnote — it means **a price-only factor book (genuinely point-in-time, buildable in
about four days from bhavcopy alone) is the only instrument that can answer the central
question.** Build it in week one and put the gap between it and the fundamental book on the
cover page of every backtest.

**8. Fast crashes cannot be met by cycles.** The stack handles slow bear markets but not a
five-week 38% fall with no signal in the preceding quarter. Fast volatility and funding
triggers plus options cut March 2020 to roughly −20% at portfolio level, with 8–12% of
drawdown that nothing removes. Do not claim otherwise.

**9. Honest targets: roughly 22–28% CAGR with 25–30% drawdown (aggressive) and 15–19% with
20–25% (moderate).** Three independent routes converge there. Higher aspirations are a stretch
case conditional on high nominal growth, a wide value spread and an early credit cycle — not a
design target, because building to an impossible target forces exactly the risk-taking the
drawdown constraint exists to prevent.

**10. The moderate book's engine is the factor book, not momentum.** Value and quality run
about five times momentum's half-life, so they cost roughly a fifth as much turnover per unit
of authority.

**11. Claude Code's remote environment has no network access to any market data source** —
NSE, RBI, FRED, Kaggle all return 403 at the egress proxy. Web *search* works. So: ingestion
code is written here but first run on the owner's machine, every indicator resolves against a
committed fixture, and **every module must be testable with zero live data.** This is an
architectural requirement, not a convenience.

## METHOD

**Make the design executable, not tabular.** Put every cycle, threshold, band and influence
cap in `config/cycle_registry.yaml` and write a validator that enforces the rules in CI —
evidence tiers, the tier-C cap, per-bucket budget containment, 3σ aggregation inside the
mandate caps, turnover, and DAG acyclicity. A registry that violates its own budget must fail
to load. Doing this surfaced four real defects that reading the tables had missed; it is the
single highest-leverage hour in the project.

**Estimation standards.** No HP filter anywhere — its endpoint estimate revises every month,
which makes honest backtesting impossible; use Hamilton's (2018) regression filter. No
regime-switching model without ≥10 observed transitions. Pool on the Jordà–Schularick–Taylor
panel to make mid-cycle layers estimable at all, since India alone offers ~1.5 credit cycles.
Correct for Stambaugh bias on persistent predictors. Report out-of-sample R² against the
historical mean, never in-sample. Purged and embargoed cross-validation. Pre-register every
hypothesis in a trial register before running it, and never re-test a rejected idea with
tweaked parameters. Deflated Sharpe with the true trial count.

**Build order: design top-down from the largest cycles, but BUILD middle-out.** The long-cycle
layers are least validatable and least actionable; the credit and macro layers are where
evidence, actionability and the drawdown constraint coincide. Every phase must end with
something that runs and can be evaluated.

## TRAPS

Do not: optimise the asset mix; tune thresholds against backtest Sharpe; use neural nets for
return prediction on 25 years of lag-approximated data; include Elliott Wave, Gann, or
fixed-period calendar cycles; treat the 500% turnover budget as a target; let a signal with no
free data source into the design; or report a fundamental backtest without its price-only
counterpart.

## HOW TO WORK WITH ME

Ask me the questions that genuinely change the build, in batches of ten, each with two to four
options and **your recommended default** so I can say "defaults for the rest" and unblock you.
Where my stated constraints are internally inconsistent — and several are — say so with the
arithmetic rather than quietly picking a side.

Use subagents on Sonnet, no more than three at a time; Opus burns the session limit in two
batches. When you fan out to write specifications, give each agent the frozen contract and
tell it to read the existing specs from disk rather than guess.

## FIRST DELIVERABLE

Before writing any model code: the cycle registry, its CI validator with the influence budget
passing as a test, and the core interface contracts (`Signal`, `CycleModel`,
`RegimeClassifier`, `Allocator`, `CostModel`, `ExecutionScheduler`, `RiskModel`, `Backtester`,
`DataSource`) as real typed Python. Then Phase 0: free bhavcopy ingestion for a limited
universe, a survivorship-free price store, ISIN-anchored symbol mastering, one trivial signal,
and a backtester carrying the real India cost model — end to end and crude, before any
cleverness. Include a look-ahead detection test that deliberately tries to leak the future and
must fail.
